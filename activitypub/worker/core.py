from __future__ import annotations

import base64
import hashlib
import hmac
import ipaddress
import json
import re
from collections.abc import Iterable
from dataclasses import dataclass
from datetime import UTC
from datetime import datetime
from datetime import timedelta
from email.utils import format_datetime
from email.utils import parsedate_to_datetime
from http import HTTPStatus
from typing import Protocol
from urllib.parse import urlsplit

from pydantic import ValidationError

try:
    from .models import INBOUND_ACTIVITY_ADAPTER
    from .models import AnnounceActivity
    from .models import CreateReplyActivity
    from .models import FollowActivity
    from .models import InboundActivity
    from .models import LikeActivity
    from .models import OutboundActivity
    from .models import PublishedNote
    from .models import QuoteInstrument
    from .models import QuoteRequestActivity
    from .models import UndoActivity
except ImportError:  # pragma: no cover - modules are top-level in a Worker bundle
    from models import INBOUND_ACTIVITY_ADAPTER
    from models import AnnounceActivity
    from models import CreateReplyActivity
    from models import FollowActivity
    from models import InboundActivity
    from models import LikeActivity
    from models import OutboundActivity
    from models import PublishedNote
    from models import QuoteInstrument
    from models import QuoteRequestActivity
    from models import UndoActivity

ACTIVITYSTREAMS_CONTEXT = "https://www.w3.org/ns/activitystreams"
PUBLIC = "https://www.w3.org/ns/activitystreams#Public"
QUOTE_REQUEST = "https://w3id.org/fep/044f#QuoteRequest"
QUOTE_AUTHORIZATION = "https://w3id.org/fep/044f#QuoteAuthorization"
MAX_BODY_BYTES = 256 * 1024
MAX_REMOTE_BYTES = 512 * 1024
REMOTE_FETCH_TIMEOUT_MS = 10_000
MAX_DATE_SKEW = timedelta(minutes=5)
GRACE_PERIOD = timedelta(minutes=15)
MAX_ATTEMPTS = 8
SIGNATURE_HEADERS = ("(request-target)", "host", "date", "digest")
SOURCE_ID_RE = re.compile(r"^\d{14}-[a-z0-9][a-z0-9-]*$")


class _StreamReadResult(Protocol):
    @property
    def done(self) -> bool: ...

    @property
    def value(self) -> Iterable[int] | None: ...


class _StreamReader(Protocol):
    async def read(self) -> _StreamReadResult: ...

    async def cancel(self) -> object: ...

    def releaseLock(self) -> None: ...


class _ResponseBody(Protocol):
    def getReader(self) -> _StreamReader: ...


class StreamingResponse(Protocol):
    @property
    def body(self) -> _ResponseBody | None: ...


class ProtocolError(ValueError):
    """An HTTP-facing ActivityPub protocol failure."""

    def __init__(
        self, message: str, status: HTTPStatus = HTTPStatus.BAD_REQUEST
    ) -> None:
        super().__init__(message)
        self.status = status


@dataclass(frozen=True)
class Signature:
    """Parsed fields from a legacy HTTP Signature header."""

    key_id: str
    algorithm: str
    headers: tuple[str, ...]
    value: bytes


@dataclass(frozen=True)
class InboxEvent:
    """Normalized action produced from a validated inbox activity."""

    kind: str
    activity_id: str
    actor: str
    object_id: str
    source_id: str | None = None


def canonical_json(value: object) -> str:
    """Serialize a value deterministically for hashing and delivery."""

    return json.dumps(value, ensure_ascii=False, separators=(",", ":"), sort_keys=True)


def utc_now() -> datetime:
    return datetime.now(UTC)


def isoformat(value: datetime) -> str:
    """Format a datetime as a UTC ActivityStreams timestamp."""

    return value.astimezone(UTC).isoformat(timespec="seconds").replace("+00:00", "Z")


def parse_time(value: str) -> datetime:
    """Parse a timezone-aware timestamp and normalize it to UTC."""

    parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    if parsed.tzinfo is None:
        raise ProtocolError("Timestamp has no timezone")
    return parsed.astimezone(UTC)


def http_date(value: datetime) -> str:
    return format_datetime(value.astimezone(UTC), usegmt=True)


def validate_date(value: str | None, now: datetime) -> None:
    """Require an HTTP Date within the allowed clock skew."""

    if not value:
        raise ProtocolError("Missing Date header")
    try:
        parsed = parsedate_to_datetime(value).astimezone(UTC)
    except (TypeError, ValueError) as exc:
        raise ProtocolError("Invalid Date header") from exc
    if abs(now - parsed) > MAX_DATE_SKEW:
        raise ProtocolError("Stale Date header", HTTPStatus.UNAUTHORIZED)


def digest_header(body: bytes) -> str:
    """Build the SHA-256 Digest header for an HTTP body."""

    digest = base64.b64encode(hashlib.sha256(body).digest()).decode("ascii")
    return f"SHA-256={digest}"


def validate_digest(value: str | None, body: bytes) -> None:
    """Verify that a Digest header matches an HTTP body."""

    if not value:
        raise ProtocolError("Missing Digest header")
    expected = digest_header(body)
    if not hmac.compare_digest(value, expected):
        raise ProtocolError("Invalid Digest header", HTTPStatus.UNAUTHORIZED)


def parse_signature(value: str | None) -> Signature:
    """Parse and validate the supported legacy HTTP Signature fields."""

    if not value:
        raise ProtocolError("Missing Signature header", HTTPStatus.UNAUTHORIZED)
    fields: dict[str, str] = {}
    for match in re.finditer(r'(\w+)="([^"]*)"(?:,\s*|$)', value):
        fields[match.group(1)] = match.group(2)
    required = {"keyId", "headers", "signature"}
    if not required <= fields.keys():
        raise ProtocolError("Malformed Signature header", HTTPStatus.UNAUTHORIZED)
    headers = tuple(fields["headers"].lower().split())
    if not set(SIGNATURE_HEADERS) <= set(headers):
        raise ProtocolError(
            "Signature does not cover required headers", HTTPStatus.UNAUTHORIZED
        )
    try:
        signature = base64.b64decode(fields["signature"], validate=True)
    except ValueError as exc:
        raise ProtocolError(
            "Invalid signature encoding", HTTPStatus.UNAUTHORIZED
        ) from exc
    algorithm = fields.get("algorithm", "rsa-sha256").lower()
    if algorithm not in {"rsa-sha256", "hs2019"}:
        raise ProtocolError("Unsupported signature algorithm", HTTPStatus.UNAUTHORIZED)
    return Signature(fields["keyId"], algorithm, headers, signature)


def signature_input(
    *, method: str, url: str, headers: dict[str, str], covered: tuple[str, ...]
) -> bytes:
    """Build the canonical bytes covered by an HTTP signature."""

    parsed = urlsplit(url)
    target = parsed.path or "/"
    if parsed.query:
        target = f"{target}?{parsed.query}"
    lowered = {key.lower(): value.strip() for key, value in headers.items()}
    lines: list[str] = []
    for name in covered:
        if name == "(request-target)":
            value = f"{method.lower()} {target}"
        elif name == "host":
            value = parsed.netloc
        elif name in lowered:
            value = lowered[name]
        else:
            raise ProtocolError(
                f"Signed header is missing: {name}", HTTPStatus.UNAUTHORIZED
            )
        lines.append(f"{name}: {value}")
    return "\n".join(lines).encode()


def signature_header(key_id: str, signature: bytes) -> str:
    """Format an RSA signature as a legacy Signature header."""

    encoded = base64.b64encode(signature).decode("ascii")
    headers = " ".join(SIGNATURE_HEADERS)
    return (
        f'keyId="{key_id}",algorithm="rsa-sha256",'
        f'headers="{headers}",signature="{encoded}"'
    )


def ensure_remote_url(url: str, *, allow_insecure: bool = False) -> str:
    """Reject unsafe remote URLs before outbound requests."""

    parsed = urlsplit(url)
    allowed_schemes = {"https"}
    if allow_insecure:
        allowed_schemes.add("http")
    if parsed.scheme not in allowed_schemes or not parsed.hostname or parsed.username:
        raise ProtocolError("Unsafe remote URL")
    hostname = parsed.hostname.lower().rstrip(".")
    if hostname == "localhost" or hostname.endswith(".localhost"):
        if not allow_insecure:
            raise ProtocolError("Unsafe remote host")
        return url
    try:
        address = ipaddress.ip_address(hostname)
    except ValueError:
        return url
    if not address.is_global and not allow_insecure:
        raise ProtocolError("Remote URL uses a non-public address")
    return url


async def read_limited_body(
    response: StreamingResponse, limit: int = MAX_REMOTE_BYTES
) -> bytes:
    """Read a streaming response without buffering more than the allowed size."""

    if response.body is None:
        return b""
    reader = response.body.getReader()
    body = bytearray()
    try:
        while True:
            result = await reader.read()
            if result.done:
                return bytes(body)
            value = result.value
            if value is None:
                raise ProtocolError("Remote response stream returned no data")
            converter = getattr(value, "to_py", None)
            chunk = converter() if converter else value
            body.extend(chunk)
            if len(body) > limit:
                try:
                    await reader.cancel()
                except Exception:
                    pass
                raise ProtocolError(
                    "Remote response is too large",
                    HTTPStatus.REQUEST_ENTITY_TOO_LARGE,
                )
    finally:
        reader.releaseLock()


def source_id_from_object(object_id: str, base_url: str) -> str | None:
    """Extract a local source ID from a canonical post object URL."""

    prefix = f"{base_url.rstrip('/')}/activitypub/posts/"
    if not object_id.startswith(prefix):
        return None
    source_id = object_id.removeprefix(prefix).rstrip("/")
    return source_id if SOURCE_ID_RE.fullmatch(source_id) else None


def parse_inbound_activity(activity: object | str | bytes) -> InboundActivity:
    """Deserialize an inbound activity into its typed protocol model."""

    try:
        if isinstance(activity, (str, bytes)):
            return INBOUND_ACTIVITY_ADAPTER.validate_json(activity)
        return INBOUND_ACTIVITY_ADAPTER.validate_python(activity)
    except ValidationError as exc:
        error_types = ", ".join(
            sorted({str(error["type"]) for error in exc.errors(include_input=False)})
        )
        raise ProtocolError(f"Invalid ActivityPub activity ({error_types})") from exc


def validate_inbox_activity(
    activity: InboundActivity | object,
    *,
    actor_url: str,
    base_url: str,
    allow_insecure: bool = False,
) -> InboxEvent:
    """Validate an inbound activity and normalize it for persistence."""

    if not isinstance(
        activity,
        (
            FollowActivity,
            LikeActivity,
            AnnounceActivity,
            UndoActivity,
            CreateReplyActivity,
            QuoteRequestActivity,
        ),
    ):
        activity = parse_inbound_activity(activity)
    kind = activity.type
    activity_id = activity.id
    actor = activity.actor
    if actor != actor_url:
        raise ProtocolError(
            "Activity actor does not match signing actor", HTTPStatus.UNAUTHORIZED
        )

    obj = activity.object
    if kind == "Follow":
        if obj != f"{base_url}/activitypub/wrlach":
            raise ProtocolError("Follow targets another actor")
        return InboxEvent(kind, activity_id, actor, obj)

    if kind == "Undo":
        original_kind = obj.type
        original_id = obj.id
        if obj.actor != actor:
            raise ProtocolError(
                "Undo actor does not own the activity", HTTPStatus.UNAUTHORIZED
            )
        target = obj.object
        source_id = source_id_from_object(target, base_url)
        if original_kind == "Follow" and target != f"{base_url}/activitypub/wrlach":
            raise ProtocolError("Undo targets another actor")
        return InboxEvent(f"Undo{original_kind}", original_id, actor, target, source_id)

    if kind in {"Like", "Announce"}:
        source_id = source_id_from_object(obj, base_url)
        if not source_id:
            raise ProtocolError(f"{kind} targets an unknown object")
        return InboxEvent(kind, activity_id, actor, obj, source_id)

    if isinstance(activity, QuoteRequestActivity):
        instrument = activity.instrument
        if not isinstance(instrument, QuoteInstrument):
            raise ProtocolError("Quote instrument has not been resolved")
        ensure_remote_url(activity.id, allow_insecure=allow_insecure)
        ensure_remote_url(instrument.id, allow_insecure=allow_insecure)
        if not _same_origin(activity.id, actor) or not _same_origin(
            instrument.id, actor
        ):
            raise ProtocolError(
                "Quote request does not belong to actor", HTTPStatus.UNAUTHORIZED
            )
        if instrument.attributed_to != actor:
            raise ProtocolError(
                "Quote author does not match actor", HTTPStatus.UNAUTHORIZED
            )
        if instrument.quote != obj:
            raise ProtocolError("Quote instrument targets another object")
        if PUBLIC not in _addressing(instrument):
            raise ProtocolError("Only public quotes are automatically approved")
        source_id = source_id_from_object(obj, base_url)
        if not source_id:
            raise ProtocolError("Quote targets an unknown object")
        return InboxEvent("QuoteRequest", activity_id, actor, instrument.id, source_id)

    if obj.attributed_to != actor:
        raise ProtocolError(
            "Reply author does not match actor", HTTPStatus.UNAUTHORIZED
        )
    object_id = obj.id
    parent = obj.in_reply_to
    if PUBLIC not in _addressing(obj) and PUBLIC not in _addressing(activity):
        raise ProtocolError("Only public replies are accepted")
    source_id = source_id_from_object(parent, base_url)
    if not source_id:
        raise ProtocolError("Reply targets an unknown object")
    return InboxEvent("Reply", activity_id, actor, object_id, source_id)


def _addressing(value: CreateReplyActivity | object) -> set[str]:
    result: set[str] = set()
    for key in ("to", "cc", "audience"):
        addressed = getattr(value, key, None)
        if isinstance(addressed, str):
            result.add(addressed)
        elif isinstance(addressed, list):
            result.update(addressed)
    return result


def _same_origin(left: str, right: str) -> bool:
    """Compare origins after URL parsing and case normalization."""

    left_url = urlsplit(left)
    right_url = urlsplit(right)
    return (
        left_url.scheme.casefold(),
        left_url.netloc.casefold(),
    ) == (
        right_url.scheme.casefold(),
        right_url.netloc.casefold(),
    )


def accept_activity(
    local_actor: str, follow: FollowActivity | dict[str, object]
) -> OutboundActivity:
    """Build a stable Accept activity for an inbound Follow."""

    if not isinstance(follow, FollowActivity):
        follow = FollowActivity.model_validate(follow)
    follow_value = follow.model_dump(by_alias=True, exclude_none=True)
    digest = hashlib.sha256(canonical_json(follow_value).encode()).hexdigest()[:24]
    return {
        "@context": ACTIVITYSTREAMS_CONTEXT,
        "id": f"{local_actor}/accepts/{digest}",
        "type": "Accept",
        "actor": local_actor,
        "object": follow_value,
        "to": [follow.actor],
    }


def quote_authorization(
    local_actor: str, request: QuoteRequestActivity
) -> dict[str, object]:
    """Build a stable public approval stamp for a quote interaction."""

    if not isinstance(request.instrument, QuoteInstrument):
        raise ProtocolError("Quote instrument has not been resolved")
    identity = {
        "actor": request.actor,
        "interactingObject": request.instrument.id,
        "interactionTarget": request.object,
    }
    digest = hashlib.sha256(canonical_json(identity).encode()).hexdigest()[:32]
    return quote_authorization_document(
        f"{local_actor}/quote-authorizations/{digest}",
        local_actor,
        request.instrument.id,
        request.object,
    )


def quote_authorization_document(
    authorization_id: str,
    local_actor: str,
    interacting_object: str,
    interaction_target: str,
) -> dict[str, object]:
    """Serialize a stored FEP-044f quote approval stamp."""

    return {
        "@context": [
            ACTIVITYSTREAMS_CONTEXT,
            {
                "QuoteAuthorization": QUOTE_AUTHORIZATION,
                "gts": "https://gotosocial.org/ns#",
                "interactingObject": {
                    "@id": "gts:interactingObject",
                    "@type": "@id",
                },
                "interactionTarget": {
                    "@id": "gts:interactionTarget",
                    "@type": "@id",
                },
            },
        ],
        "id": authorization_id,
        "type": "QuoteAuthorization",
        "attributedTo": local_actor,
        "interactingObject": interacting_object,
        "interactionTarget": interaction_target,
    }


def accept_quote_request(
    local_actor: str,
    request: QuoteRequestActivity,
    authorization: dict[str, object],
) -> OutboundActivity:
    """Build a stable Accept carrying a FEP-044f approval stamp URL."""

    if not isinstance(request.instrument, QuoteInstrument):
        raise ProtocolError("Quote instrument has not been resolved")
    authorization_id = str(authorization["id"])
    request_value = {
        "id": request.id,
        "type": "QuoteRequest",
        "actor": request.actor,
        "object": request.object,
        "instrument": request.instrument.id,
    }
    digest = hashlib.sha256(canonical_json(request_value).encode()).hexdigest()[:24]
    return {
        "@context": [
            ACTIVITYSTREAMS_CONTEXT,
            {"QuoteRequest": QUOTE_REQUEST},
        ],
        "id": f"{local_actor}/accepts/{digest}",
        "type": "Accept",
        "actor": local_actor,
        "object": request_value,
        "result": authorization_id,
        "to": [request.actor],
    }


def delete_activity(
    local_actor: str, object_url: str, deleted: str
) -> OutboundActivity:
    """Build a Delete activity containing a tombstone."""

    return {
        "@context": ACTIVITYSTREAMS_CONTEXT,
        "id": f"{object_url}/delete",
        "type": "Delete",
        "actor": local_actor,
        "object": {"id": object_url, "type": "Tombstone", "deleted": deleted},
        "to": [PUBLIC],
        "cc": [f"{local_actor}/followers"],
    }


def create_activity(
    note: PublishedNote | dict[str, object],
) -> OutboundActivity:
    """Wrap a published Note in a stable Create activity."""

    if not isinstance(note, PublishedNote):
        note = PublishedNote.model_validate(note)
    note_value = note.model_dump(by_alias=True, exclude_none=True)
    object_url = note.id
    return {
        "@context": ACTIVITYSTREAMS_CONTEXT,
        "id": f"{object_url}/activity",
        "type": "Create",
        "actor": note.attributed_to,
        "published": note.published,
        "to": note.to,
        "cc": note.cc,
        "object": note_value,
    }


def retry_at(now: datetime, attempts: int) -> datetime:
    """Calculate the next bounded exponential delivery retry."""

    minutes = min(5 * (2 ** max(0, attempts - 1)), 12 * 60)
    return now + timedelta(minutes=minutes)


def eligible(first_seen: str, now: datetime) -> bool:
    """Return whether a post has completed its publication grace period."""

    return now >= parse_time(first_seen) + GRACE_PERIOD
