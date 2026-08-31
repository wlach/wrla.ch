from __future__ import annotations

import json
from collections.abc import Iterable
from collections.abc import Mapping
from datetime import UTC
from datetime import datetime
from http import HTTPMethod
from http import HTTPStatus
from typing import Protocol
from typing import cast
from urllib.parse import parse_qs
from urllib.parse import urljoin
from urllib.parse import urlsplit

from core import MAX_ATTEMPTS
from core import MAX_BODY_BYTES
from core import MAX_REMOTE_BYTES
from core import REMOTE_FETCH_TIMEOUT_MS
from core import SIGNATURE_HEADERS
from core import ProtocolError
from core import StreamingResponse
from core import accept_activity
from core import accept_quote_request
from core import canonical_json
from core import create_activity
from core import delete_activity
from core import digest_header
from core import eligible
from core import ensure_remote_url
from core import http_date
from core import isoformat
from core import parse_inbound_activity
from core import parse_signature
from core import quote_authorization
from core import quote_authorization_document
from core import read_limited_body
from core import retry_at
from core import signature_header
from core import signature_input
from core import source_id_from_object
from core import utc_now
from core import validate_date
from core import validate_digest
from core import validate_inbox_activity
from models import POST_STATE_ADAPTER
from models import DeliveryRow
from models import FollowActivity
from models import InboundActivity
from models import Manifest
from models import OutboundActivity
from models import PostRow
from models import PublishedNote
from models import QuoteAuthorizationRow
from models import QuoteInstrument
from models import QuoteRequestActivity
from models import RemoteActor
from pydantic import BaseModel
from pydantic import ValidationError
from pyodide.ffi import to_js as _to_js
from workers import Request
from workers import Response
from workers import WorkerEntrypoint
from workers import fetch

# These names are injected by Pyodide from the JavaScript global scope.
from js import AbortSignal  # ty: ignore[unresolved-import]
from js import Object  # ty: ignore[unresolved-import]
from js import Uint8Array  # ty: ignore[unresolved-import]
from js import crypto  # ty: ignore[unresolved-import]

ACTIVITY_JSON = "application/activity+json; charset=utf-8"
JRD_JSON = "application/jrd+json; charset=utf-8"

type _Row = dict[str, object]


class _D1Result(Protocol):
    results: object


class _D1PreparedStatement(Protocol):
    def bind(self, *bindings: object) -> _D1PreparedStatement: ...

    async def all(self) -> _D1Result: ...

    async def first(self) -> object | None: ...

    async def run(self) -> object: ...


class _D1Database(Protocol):
    def prepare(self, sql: str) -> _D1PreparedStatement: ...


class _ScheduledController(Protocol):
    scheduledTime: int | float


def _to_python(value: object) -> object | None:
    if value is None:
        return None
    converter = getattr(value, "to_py", None)
    return converter() if converter else value


async def _all(db: _D1Database, sql: str, *bindings: object) -> list[_Row]:
    statement = db.prepare(sql)
    if bindings:
        statement = statement.bind(*bindings)
    result = await statement.all()
    rows = cast(Iterable[Mapping[str, object]], _to_python(result.results))
    return [dict(row) for row in rows]


async def _first(db: _D1Database, sql: str, *bindings: object) -> _Row | None:
    statement = db.prepare(sql)
    if bindings:
        statement = statement.bind(*bindings)
    value = cast(Mapping[str, object] | None, _to_python(await statement.first()))
    return dict(value) if value is not None else None


async def _all_as[ModelT: BaseModel](
    db: _D1Database, model: type[ModelT], sql: str, *bindings: object
) -> list[ModelT]:
    return [model.model_validate(row) for row in await _all(db, sql, *bindings)]


async def _run(db: _D1Database, sql: str, *bindings: object) -> object:
    statement = db.prepare(sql)
    if bindings:
        statement = statement.bind(*bindings)
    return await statement.run()


def _integer_column(row: _Row | None, column: str) -> int:
    if row is None or not isinstance(value := row.get(column), int):
        raise RuntimeError(f"D1 did not return integer column {column!r}")
    return value


def _string_column(row: _Row, column: str) -> str:
    if not isinstance(value := row.get(column), str):
        raise TypeError(f"D1 did not return string column {column!r}")
    return value


def _json(
    value: object,
    *,
    status: HTTPStatus = HTTPStatus.OK,
    content_type: str = ACTIVITY_JSON,
) -> Response:
    return Response(
        json.dumps(value, ensure_ascii=False),
        status=status,
        headers={"Content-Type": content_type, "Cache-Control": "no-store"},
    )


def _pem_bytes(pem: str) -> bytes:
    lines = [line.strip() for line in pem.splitlines() if not line.startswith("---")]
    import base64

    return base64.b64decode("".join(lines))


def _js(value: object) -> object:
    return _to_js(value, dict_converter=Object.fromEntries)


async def _verify_rsa(public_pem: str, signed: bytes, signature: bytes) -> bool:
    key = await crypto.subtle.importKey(
        "spki",
        _to_js(_pem_bytes(public_pem)),
        _js({"name": "RSASSA-PKCS1-v1_5", "hash": "SHA-256"}),
        False,
        _js(["verify"]),
    )
    return bool(
        await crypto.subtle.verify(
            "RSASSA-PKCS1-v1_5",
            key,
            _to_js(signature),
            _to_js(signed),
        )
    )


async def _sign_rsa(private_pem: str, signed: bytes) -> bytes:
    key = await crypto.subtle.importKey(
        "pkcs8",
        _to_js(_pem_bytes(private_pem)),
        _js({"name": "RSASSA-PKCS1-v1_5", "hash": "SHA-256"}),
        False,
        _js(["sign"]),
    )
    result = await crypto.subtle.sign("RSASSA-PKCS1-v1_5", key, _to_js(signed))
    return bytes(Uint8Array.new(result).to_py())


async def _remote_json(url: str, *, allow_insecure: bool) -> dict:
    current = ensure_remote_url(url, allow_insecure=allow_insecure)
    for _ in range(4):
        try:
            response = await fetch(
                current,
                headers={"Accept": "application/activity+json, application/ld+json"},
                redirect="manual",
                signal=AbortSignal.timeout(REMOTE_FETCH_TIMEOUT_MS),
            )
        except Exception as exc:
            raise ProtocolError("Remote fetch failed", HTTPStatus.BAD_GATEWAY) from exc
        if response.status in {
            HTTPStatus.MOVED_PERMANENTLY,
            HTTPStatus.FOUND,
            HTTPStatus.SEE_OTHER,
            HTTPStatus.TEMPORARY_REDIRECT,
            HTTPStatus.PERMANENT_REDIRECT,
        }:
            location = response.headers.get("location")
            if not location:
                raise ProtocolError(
                    "Remote redirect has no Location", HTTPStatus.BAD_GATEWAY
                )
            current = ensure_remote_url(
                urljoin(current, location), allow_insecure=allow_insecure
            )
            continue
        if not response.ok:
            raise ProtocolError(
                f"Remote fetch failed: {response.status}", HTTPStatus.BAD_GATEWAY
            )
        length = response.headers.get("content-length")
        try:
            if length and int(length) > MAX_REMOTE_BYTES:
                raise ProtocolError(
                    "Remote response is too large",
                    HTTPStatus.REQUEST_ENTITY_TOO_LARGE,
                )
        except ValueError as exc:
            raise ProtocolError(
                "Remote response has invalid Content-Length", HTTPStatus.BAD_GATEWAY
            ) from exc
        try:
            # The Python SDK exposes this as a dynamically typed JS ReadableStream.
            body = await read_limited_body(cast(StreamingResponse, response))
        except ProtocolError:
            raise
        except Exception as exc:
            raise ProtocolError("Remote fetch failed", HTTPStatus.BAD_GATEWAY) from exc
        try:
            value = json.loads(body)
        except (UnicodeDecodeError, json.JSONDecodeError) as exc:
            raise ProtocolError(
                "Remote response is not JSON", HTTPStatus.BAD_GATEWAY
            ) from exc
        if not isinstance(value, dict):
            raise ProtocolError(
                "Remote response is not an object", HTTPStatus.BAD_GATEWAY
            )
        return value
    raise ProtocolError("Too many remote redirects", HTTPStatus.BAD_GATEWAY)


def _validated[ModelT: BaseModel](
    model: type[ModelT], value: object, label: str
) -> ModelT:
    try:
        return model.model_validate(value)
    except ValidationError as exc:
        error_types = ", ".join(
            sorted({str(error["type"]) for error in exc.errors(include_input=False)})
        )
        raise ProtocolError(
            f"Invalid {label} ({error_types})", HTTPStatus.BAD_GATEWAY
        ) from exc


def _actor_endpoints(actor: RemoteActor) -> tuple[str, str | None]:
    return actor.inbox, actor.endpoints.shared_inbox


class Default(WorkerEntrypoint):
    """Serve the single wrla.ch actor and run scheduled federation work."""

    @property
    def base_url(self) -> str:
        return str(self.env.BASE_URL).rstrip("/")

    @property
    def local_actor(self) -> str:
        return f"{self.base_url}/activitypub/{self.env.ACTOR_NAME}"

    @property
    def allow_insecure(self) -> bool:
        return str(self.env.ALLOW_INSECURE_TEST_URLS).lower() == "true"

    @property
    def delivery_enabled(self) -> bool:
        return str(self.env.OUTBOUND_DELIVERY_ENABLED).lower() == "true"

    async def fetch(self, request: Request) -> Response:
        """Route public ActivityPub and discovery HTTP requests."""

        try:
            url = urlsplit(str(request.url))
            path = url.path.rstrip("/") or "/"
            if request.method == "GET" and path == "/.well-known/webfinger":
                return self._webfinger(url.query)
            if request.method == "POST" and path == "/activitypub/wrlach/inbox":
                return await self._inbox(request)
            authorization_prefix = "/activitypub/wrlach/quote-authorizations/"
            if request.method == "GET" and path.startswith(authorization_prefix):
                return await self._quote_authorization(
                    path.removeprefix(authorization_prefix)
                )
            if (
                self.allow_insecure
                and request.method == "POST"
                and path == "/__test/scheduled"
            ):
                values = parse_qs(url.query)
                when = values.get("time", [""])[0]
                now = datetime.fromisoformat(when.replace("Z", "+00:00"))
                await self._sync_manifest(now)
                await self._stage_eligible_posts(now)
                await self._deliver_due(now)
                return _json({"ok": True, "time": isoformat(now)})
            if request.method == "GET" and path == "/activitypub/wrlach/followers":
                return await self._followers()
            for collection, kind in (
                ("replies", "Reply"),
                ("likes", "Like"),
                ("shares", "Announce"),
            ):
                prefix = f"/activitypub/{collection}/"
                if request.method == "GET" and path.startswith(prefix):
                    page_value = parse_qs(url.query).get("page", [None])[0]
                    try:
                        page = int(page_value) if page_value else None
                    except ValueError as exc:
                        raise ProtocolError(
                            "Invalid collection page", HTTPStatus.NOT_FOUND
                        ) from exc
                    return await self._collection(
                        path.removeprefix(prefix), kind, page=page
                    )
            return _json({"error": "Not found"}, status=HTTPStatus.NOT_FOUND)
        except ProtocolError as exc:
            return _json({"error": str(exc)}, status=exc.status)
        except Exception as exc:
            print(f"Unhandled ActivityPub request error: {exc}")
            return _json(
                {"error": "Internal server error"},
                status=HTTPStatus.INTERNAL_SERVER_ERROR,
            )

    def _webfinger(self, query: str) -> Response:
        """Return discovery metadata for the local actor handle."""

        resource = parse_qs(query).get("resource", [""])[0]
        expected = f"acct:{self.env.ACTOR_NAME}@{urlsplit(self.base_url).hostname}"
        if resource != expected:
            raise ProtocolError("Unknown WebFinger resource", HTTPStatus.NOT_FOUND)
        return _json(
            {
                "subject": expected,
                "aliases": [self.local_actor, self.base_url],
                "links": [
                    {
                        "rel": "self",
                        "type": "application/activity+json",
                        "href": self.local_actor,
                    },
                    {
                        "rel": "http://webfinger.net/rel/profile-page",
                        "href": self.base_url,
                    },
                ],
            },
            content_type=JRD_JSON,
        )

    async def _verified_actor(
        self, request: Request, body: bytes, activity: InboundActivity
    ) -> RemoteActor:
        """Resolve the signing actor and verify the request signature."""

        validate_date(request.headers.get("date"), utc_now())
        validate_digest(request.headers.get("digest"), body)
        parsed = parse_signature(request.headers.get("signature"))
        actor_url = activity.actor
        ensure_remote_url(actor_url, allow_insecure=self.allow_insecure)
        actor = _validated(
            RemoteActor,
            await _remote_json(actor_url, allow_insecure=self.allow_insecure),
            "remote actor",
        )
        if actor.id != actor_url:
            raise ProtocolError("Remote actor id mismatch", HTTPStatus.UNAUTHORIZED)
        key = next(
            (item for item in actor.public_keys if item.id == parsed.key_id),
            None,
        )
        if not key or key.owner != actor_url:
            raise ProtocolError(
                "Signing key does not belong to actor", HTTPStatus.UNAUTHORIZED
            )
        headers = {
            name: request.headers.get(name) or ""
            for name in parsed.headers
            if name != "(request-target)"
        }
        signed = signature_input(
            method=str(request.method),
            url=str(request.url),
            headers=headers,
            covered=parsed.headers,
        )
        if not await _verify_rsa(key.public_key_pem, signed, parsed.value):
            raise ProtocolError("Invalid HTTP signature", HTTPStatus.UNAUTHORIZED)
        return actor

    async def _inbox(self, request: Request) -> Response:
        """Validate and persist supported inbound activities."""

        rate_limit = await self.env.INBOX_RATE_LIMITER.limit(
            _js({"key": "activitypub-inbox"})
        )
        if not rate_limit.success:
            raise ProtocolError(
                "Inbox rate limit exceeded", HTTPStatus.TOO_MANY_REQUESTS
            )

        content_type = (request.headers.get("content-type") or "").lower()
        if not any(
            kind in content_type
            for kind in ("application/activity+json", "application/ld+json")
        ):
            raise ProtocolError(
                "Unsupported Content-Type", HTTPStatus.UNSUPPORTED_MEDIA_TYPE
            )
        length = request.headers.get("content-length")
        if length and int(length) > MAX_BODY_BYTES:
            raise ProtocolError(
                "Activity is too large", HTTPStatus.REQUEST_ENTITY_TOO_LARGE
            )
        body = (await request.text()).encode()
        if len(body) > MAX_BODY_BYTES:
            raise ProtocolError(
                "Activity is too large", HTTPStatus.REQUEST_ENTITY_TOO_LARGE
            )
        activity = parse_inbound_activity(body)
        actor = await self._verified_actor(request, body, activity)
        actor_url = actor.id
        if isinstance(activity, QuoteRequestActivity) and isinstance(
            activity.instrument, str
        ):
            instrument_url = ensure_remote_url(
                activity.instrument, allow_insecure=self.allow_insecure
            )
            instrument = _validated(
                QuoteInstrument,
                await _remote_json(instrument_url, allow_insecure=self.allow_insecure),
                "quote instrument",
            )
            if instrument.id != instrument_url:
                raise ProtocolError(
                    "Quote instrument id mismatch", HTTPStatus.UNAUTHORIZED
                )
            activity.instrument = instrument
        event = validate_inbox_activity(
            activity,
            actor_url=actor_url,
            base_url=self.base_url,
            allow_insecure=self.allow_insecure,
        )
        now = isoformat(utc_now())

        if event.kind == "Follow":
            inbox, shared = _actor_endpoints(actor)
            ensure_remote_url(inbox, allow_insecure=self.allow_insecure)
            if shared:
                ensure_remote_url(shared, allow_insecure=self.allow_insecure)
            await _run(
                self.env.DB,
                """INSERT INTO followers
                   (actor_url, inbox_url, shared_inbox_url, follow_id, active, created_at, updated_at)
                   VALUES (?, ?, ?, ?, 1, ?, ?)
                   ON CONFLICT(actor_url) DO UPDATE SET
                     inbox_url=excluded.inbox_url,
                     shared_inbox_url=excluded.shared_inbox_url,
                     follow_id=excluded.follow_id,
                     active=1,
                     updated_at=excluded.updated_at""",
                actor_url,
                inbox,
                shared,
                event.activity_id,
                now,
                now,
            )
            if not isinstance(activity, FollowActivity):
                raise ProtocolError("Follow model mismatch")
            accept = accept_activity(self.local_actor, activity)
            await self._queue_delivery(
                source_id=f"follow:{event.activity_id}",
                destination=inbox,
                activity=accept,
                now=now,
            )
            if self.delivery_enabled:
                await self._deliver_due(utc_now())
        elif event.kind == "UndoFollow":
            await _run(
                self.env.DB,
                "UPDATE followers SET active=0, updated_at=? WHERE actor_url=? AND follow_id=?",
                now,
                actor_url,
                event.activity_id,
            )
        else:
            await self._assert_known_post(event.source_id)
            if event.kind in {"Like", "Announce"}:
                await _run(
                    self.env.DB,
                    """INSERT INTO interactions
                       (activity_id, kind, actor_url, source_id, active, received_at)
                       VALUES (?, ?, ?, ?, 1, ?)
                       ON CONFLICT(kind, actor_url, source_id) DO UPDATE SET
                         activity_id=excluded.activity_id, active=1,
                         received_at=excluded.received_at""",
                    event.activity_id,
                    event.kind,
                    actor_url,
                    event.source_id,
                    now,
                )
            elif event.kind in {"UndoLike", "UndoAnnounce"}:
                await _run(
                    self.env.DB,
                    """UPDATE interactions SET active=0
                       WHERE activity_id=? AND actor_url=? AND kind=?""",
                    event.activity_id,
                    actor_url,
                    event.kind.removeprefix("Undo"),
                )
            elif event.kind == "Reply":
                await _run(
                    self.env.DB,
                    """INSERT OR IGNORE INTO replies
                       (activity_id, object_url, actor_url, source_id, received_at)
                       VALUES (?, ?, ?, ?, ?)""",
                    event.activity_id,
                    event.object_id,
                    actor_url,
                    event.source_id,
                    now,
                )
            elif event.kind == "QuoteRequest":
                if not isinstance(activity, QuoteRequestActivity):
                    raise ProtocolError("Quote request model mismatch")
                authorization = quote_authorization(self.local_actor, activity)
                await _run(
                    self.env.DB,
                    """INSERT INTO quote_authorizations
                       (authorization_id, request_id, actor_url, quote_url,
                        target_url, source_id, received_at)
                       VALUES (?, ?, ?, ?, ?, ?, ?)
                       ON CONFLICT(authorization_id) DO UPDATE SET
                         request_id=excluded.request_id,
                         received_at=excluded.received_at""",
                    authorization["id"],
                    event.activity_id,
                    actor_url,
                    event.object_id,
                    activity.object,
                    event.source_id,
                    now,
                )
                accept = accept_quote_request(self.local_actor, activity, authorization)
                await self._queue_delivery(
                    source_id=f"quote:{event.activity_id}",
                    destination=actor.inbox,
                    activity=accept,
                    now=now,
                )
                if self.delivery_enabled:
                    await self._deliver_due(utc_now())
        return Response(status=HTTPStatus.ACCEPTED)

    async def _quote_authorization(self, digest: str) -> Response:
        """Dereference a public FEP-044f approval stamp."""

        if len(digest) != 32 or any(
            character not in "0123456789abcdef" for character in digest
        ):
            raise ProtocolError("Unknown quote authorization", HTTPStatus.NOT_FOUND)
        authorization_id = f"{self.local_actor}/quote-authorizations/{digest}"
        row_value = await _first(
            self.env.DB,
            "SELECT * FROM quote_authorizations WHERE authorization_id=?",
            authorization_id,
        )
        if row_value is None:
            raise ProtocolError("Unknown quote authorization", HTTPStatus.NOT_FOUND)
        row = QuoteAuthorizationRow.model_validate(row_value)
        return _json(
            quote_authorization_document(
                row.authorization_id,
                self.local_actor,
                row.quote_url,
                row.target_url,
            )
        )

    async def _assert_known_post(self, source_id: str | None) -> None:
        """Require a known post that has not been cancelled or redacted."""

        if source_id is None:
            raise ProtocolError("Unknown local post", HTTPStatus.NOT_FOUND)
        post = await _first(
            self.env.DB,
            "SELECT state FROM posts WHERE source_id=?",
            source_id,
        )
        if not post:
            await self._sync_manifest(utc_now())
            post = await _first(
                self.env.DB,
                "SELECT state FROM posts WHERE source_id=?",
                source_id,
            )
        state = (
            POST_STATE_ADAPTER.validate_python(post["state"], strict=True)
            if post
            else None
        )
        if state in {None, "redacted", "cancelled"}:
            raise ProtocolError("Unknown local post", HTTPStatus.NOT_FOUND)

    async def _followers(self) -> Response:
        """Return the public follower collection summary."""

        row = await _first(
            self.env.DB, "SELECT COUNT(*) AS count FROM followers WHERE active=1"
        )
        return _json(
            {
                "@context": "https://www.w3.org/ns/activitystreams",
                "id": f"{self.local_actor}/followers",
                "type": "Collection",
                "totalItems": _integer_column(row, "count"),
            }
        )

    async def _collection(
        self, source_id: str, kind: str, *, page: int | None
    ) -> Response:
        """Return replies or aggregate interaction data for a post."""

        await self._assert_known_post(source_id)
        base = f"{self.base_url}/activitypub"
        if kind == "Reply":
            count_row = await _first(
                self.env.DB,
                "SELECT COUNT(*) AS count FROM replies WHERE source_id=?",
                source_id,
            )
            count = _integer_column(count_row, "count")
            collection_id = f"{base}/replies/{source_id}"
            if page is None:
                return _json(
                    {
                        "@context": "https://www.w3.org/ns/activitystreams",
                        "id": collection_id,
                        "type": "OrderedCollection",
                        "totalItems": count,
                        "first": f"{collection_id}?page=1",
                    }
                )
            if page < 1:
                raise ProtocolError("Invalid collection page", HTTPStatus.NOT_FOUND)
            page_size = 20
            offset = (page - 1) * page_size
            rows = await _all(
                self.env.DB,
                """SELECT object_url FROM replies WHERE source_id=?
                   ORDER BY received_at LIMIT ? OFFSET ?""",
                source_id,
                page_size,
                offset,
            )
            value = {
                "@context": "https://www.w3.org/ns/activitystreams",
                "id": f"{collection_id}?page={page}",
                "type": "OrderedCollectionPage",
                "partOf": collection_id,
                "orderedItems": [row["object_url"] for row in rows],
            }
            if page > 1:
                value["prev"] = f"{collection_id}?page={page - 1}"
            if offset + len(rows) < count:
                value["next"] = f"{collection_id}?page={page + 1}"
        else:
            row = await _first(
                self.env.DB,
                """SELECT COUNT(*) AS count FROM interactions
                   WHERE source_id=? AND kind=? AND active=1""",
                source_id,
                kind,
            )
            name = "likes" if kind == "Like" else "shares"
            value = {
                "@context": "https://www.w3.org/ns/activitystreams",
                "id": f"{base}/{name}/{source_id}",
                "type": "Collection",
                "totalItems": _integer_column(row, "count"),
            }
        return _json(value)

    async def scheduled(
        self, controller: _ScheduledController, _env: object, _ctx: object
    ) -> None:
        """Synchronize published posts and process due deliveries."""

        now = datetime.fromtimestamp(float(controller.scheduledTime) / 1000, UTC)
        await self._sync_manifest(now)
        if not self.delivery_enabled:
            return
        await self._stage_eligible_posts(now)
        await self._deliver_due(now)

    async def _sync_manifest(self, now: datetime) -> None:
        """Reconcile the deployed manifest with durable post state."""

        manifest = _validated(
            Manifest,
            await _remote_json(
                f"{self.base_url}/activitypub/manifest.json",
                allow_insecure=self.allow_insecure,
            ),
            "deployed manifest",
        )
        if manifest.actor != self.local_actor:
            raise ProtocolError(
                "Deployed manifest actor mismatch", HTTPStatus.BAD_GATEWAY
            )
        initialized = await _first(
            self.env.DB, "SELECT value FROM metadata WHERE key='manifest_initialized'"
        )
        existing = {
            row.source_id: row
            for row in await _all_as(
                self.env.DB,
                PostRow,
                "SELECT * FROM posts",
            )
        }
        live_ids: set[str] = set()
        now_text = isoformat(now)
        for item in manifest.posts:
            source_id = item.source_id
            object_url = item.object_url
            if source_id_from_object(object_url, self.base_url) != source_id:
                raise ProtocolError("Invalid manifest post", HTTPStatus.BAD_GATEWAY)
            live_ids.add(source_id)
            current = existing.get(source_id)
            redacted = item.redacted
            if current is None:
                state = (
                    "redacted"
                    if redacted
                    else ("pending" if initialized else "historical")
                )
                await _run(
                    self.env.DB,
                    """INSERT INTO posts
                       (source_id, object_url, activity_url, content_hash, published,
                        first_seen, state, deleted_at)
                       VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
                    source_id,
                    object_url,
                    item.activity,
                    item.content_hash,
                    item.published,
                    now_text,
                    state,
                    item.deleted,
                )
            elif redacted and current.state != "redacted":
                if current.state == "delivered":
                    await self._stage_delete(
                        source_id, object_url, str(item.deleted or now_text), now_text
                    )
                await _run(
                    self.env.DB,
                    "UPDATE posts SET state='redacted', deleted_at=?, content_hash=? WHERE source_id=?",
                    item.deleted or now_text,
                    item.content_hash,
                    source_id,
                )
            elif current.state == "pending":
                await _run(
                    self.env.DB,
                    "UPDATE posts SET content_hash=?, activity_url=? WHERE source_id=?",
                    item.content_hash,
                    item.activity,
                    source_id,
                )
        for source_id, current in existing.items():
            if source_id not in live_ids and current.state == "pending":
                await _run(
                    self.env.DB,
                    "UPDATE posts SET state='cancelled' WHERE source_id=?",
                    source_id,
                )
        if not initialized:
            await _run(
                self.env.DB,
                "INSERT INTO metadata(key, value) VALUES ('manifest_initialized', ?)",
                now_text,
            )

    async def _stage_eligible_posts(self, now: datetime) -> None:
        """Queue Create deliveries for posts beyond the grace period."""

        posts = await _all_as(
            self.env.DB,
            PostRow,
            "SELECT * FROM posts WHERE state='pending'",
        )
        destinations = await _all(
            self.env.DB,
            """SELECT DISTINCT COALESCE(shared_inbox_url, inbox_url) AS destination
               FROM followers WHERE active=1""",
        )
        now_text = isoformat(now)
        for post in posts:
            if not eligible(post.first_seen, now):
                continue
            note = _validated(
                PublishedNote,
                await _remote_json(post.object_url, allow_insecure=self.allow_insecure),
                "deployed post object",
            )
            if note.id != post.object_url or note.attributed_to != self.local_actor:
                raise ProtocolError(
                    "Deployed post object is invalid", HTTPStatus.BAD_GATEWAY
                )
            activity = create_activity(note)
            for destination in destinations:
                await self._queue_delivery(
                    source_id=post.source_id,
                    destination=_string_column(destination, "destination"),
                    activity=activity,
                    now=now_text,
                )
            await _run(
                self.env.DB,
                "UPDATE posts SET state='delivered' WHERE source_id=? AND state='pending'",
                post.source_id,
            )

    async def _stage_delete(
        self, source_id: str, object_url: str, deleted: str, now: str
    ) -> None:
        """Queue a Delete for every destination that received a post."""

        activity = delete_activity(self.local_actor, object_url, deleted)
        recipients = await _all(
            self.env.DB,
            "SELECT destination FROM delivery_recipients WHERE source_id=?",
            source_id,
        )
        for recipient in recipients:
            await self._queue_delivery(
                source_id=source_id,
                destination=_string_column(recipient, "destination"),
                activity=activity,
                now=now,
            )

    async def _queue_delivery(
        self,
        *,
        source_id: str,
        destination: str,
        activity: OutboundActivity,
        now: str,
    ) -> None:
        """Persist an idempotent outbound delivery attempt."""

        ensure_remote_url(destination, allow_insecure=self.allow_insecure)
        await _run(
            self.env.DB,
            """INSERT OR IGNORE INTO deliveries
               (source_id, destination, kind, activity_id, body, status, attempts, next_attempt)
               VALUES (?, ?, ?, ?, ?, 'pending', 0, ?)""",
            source_id,
            destination,
            activity["type"],
            activity["id"],
            canonical_json(activity),
            now,
        )

    async def _signed_post(
        self, destination: str, body: str, now: datetime
    ) -> Response:
        """POST an activity with the local actor's HTTP signature."""

        body_bytes = body.encode()
        date = http_date(now)
        digest = digest_header(body_bytes)
        headers = {"date": date, "digest": digest}
        signed = signature_input(
            method=HTTPMethod.POST,
            url=destination,
            headers=headers,
            covered=SIGNATURE_HEADERS,
        )
        signature = await _sign_rsa(str(self.env.ACTIVITYPUB_PRIVATE_KEY), signed)
        return await fetch(
            destination,
            method=HTTPMethod.POST,
            headers={
                "Content-Type": "application/activity+json",
                "Date": date,
                "Digest": digest,
                "Signature": signature_header(
                    f"{self.local_actor}#main-key", signature
                ),
                "User-Agent": "wrla.ch ActivityPub/1.0",
            },
            body=body,
            redirect="manual",
        )

    async def _deliver_due(self, now: datetime) -> None:
        """Attempt due deliveries and record success or retry state."""

        rows = await _all_as(
            self.env.DB,
            DeliveryRow,
            """SELECT * FROM deliveries
               WHERE status='pending' AND next_attempt<=?
               ORDER BY next_attempt, id LIMIT 50""",
            isoformat(now),
        )
        for row in rows:
            attempts = row.attempts + 1
            try:
                response = await self._signed_post(row.destination, row.body, now)
                if 200 <= response.status < 300:
                    await _run(
                        self.env.DB,
                        "UPDATE deliveries SET status='delivered', attempts=?, last_error=NULL WHERE id=?",
                        attempts,
                        row.id,
                    )
                    if row.kind == "Create":
                        await _run(
                            self.env.DB,
                            "INSERT OR IGNORE INTO delivery_recipients(source_id, destination) VALUES (?, ?)",
                            row.source_id,
                            row.destination,
                        )
                    continue
                retryable = response.status >= HTTPStatus.INTERNAL_SERVER_ERROR or (
                    response.status
                    in {
                        HTTPStatus.REQUEST_TIMEOUT,
                        HTTPStatus.TOO_EARLY,
                        HTTPStatus.TOO_MANY_REQUESTS,
                    }
                )
                error = f"HTTP {response.status}"
            except Exception as exc:
                retryable = True
                error = str(exc)[:500]
            terminal = not retryable or attempts >= MAX_ATTEMPTS
            await _run(
                self.env.DB,
                """UPDATE deliveries SET status=?, attempts=?, next_attempt=?, last_error=?
                   WHERE id=?""",
                "failed" if terminal else "pending",
                attempts,
                isoformat(retry_at(now, attempts)),
                error,
                row.id,
            )
