from __future__ import annotations

import asyncio
import base64
import hashlib
import sqlite3
from dataclasses import dataclass
from datetime import UTC
from datetime import datetime
from datetime import timedelta
from pathlib import Path

import pytest
from pydantic import ValidationError

from activitypub.worker.core import GRACE_PERIOD
from activitypub.worker.core import PUBLIC
from activitypub.worker.core import ProtocolError
from activitypub.worker.core import accept_quote_request
from activitypub.worker.core import digest_header
from activitypub.worker.core import eligible
from activitypub.worker.core import ensure_remote_url
from activitypub.worker.core import parse_inbound_activity
from activitypub.worker.core import parse_signature
from activitypub.worker.core import quote_authorization
from activitypub.worker.core import read_limited_body
from activitypub.worker.core import retry_at
from activitypub.worker.core import signature_input
from activitypub.worker.core import validate_digest
from activitypub.worker.core import validate_inbox_activity
from activitypub.worker.models import DeliveryRow
from activitypub.worker.models import Manifest
from activitypub.worker.models import PostRow
from activitypub.worker.models import QuoteRequestActivity
from activitypub.worker.models import RemoteActor

BASE_URL = "https://wrla.ch"
REMOTE_ACTOR = "https://remote.example/users/me"
POST_URL = f"{BASE_URL}/activitypub/posts/20260101000000-post"


def test_digest_round_trip() -> None:
    body = b'{"type":"Follow"}'
    value = digest_header(body)
    assert (
        value == "SHA-256=" + base64.b64encode(hashlib.sha256(body).digest()).decode()
    )
    validate_digest(value, body)
    with pytest.raises(ProtocolError):
        validate_digest(value, body + b" ")


def test_signature_canonicalization_includes_query() -> None:
    signed = signature_input(
        method="POST",
        url="https://remote.example/inbox?one=two",
        headers={"date": "date", "digest": "digest"},
        covered=("(request-target)", "host", "date", "digest"),
    )
    assert signed.decode() == (
        "(request-target): post /inbox?one=two\n"
        "host: remote.example\n"
        "date: date\n"
        "digest: digest"
    )


def test_signature_requires_covered_headers() -> None:
    value = 'keyId="https://remote.example/key",headers="date",signature="YWJj"'
    with pytest.raises(ProtocolError):
        parse_signature(value)


def test_like_and_undo() -> None:
    like = {
        "id": "https://remote.example/activities/1",
        "type": "Like",
        "actor": REMOTE_ACTOR,
        "object": POST_URL,
    }
    event = validate_inbox_activity(like, actor_url=REMOTE_ACTOR, base_url=BASE_URL)
    assert event.kind == "Like"
    assert event.source_id == "20260101000000-post"

    undo = {
        "id": "https://remote.example/activities/2",
        "type": "Undo",
        "actor": REMOTE_ACTOR,
        "object": like,
    }
    event = validate_inbox_activity(undo, actor_url=REMOTE_ACTOR, base_url=BASE_URL)
    assert event.kind == "UndoLike"
    assert event.activity_id == like["id"]


def test_pydantic_retains_federation_extensions() -> None:
    activity = parse_inbound_activity(
        {
            "id": "https://remote.example/likes/1",
            "type": "Like",
            "actor": REMOTE_ACTOR,
            "object": POST_URL,
            "toot:identityProof": {"type": "IdentityProof"},
        }
    )
    assert activity.type == "Like"
    assert "toot:identityProof" in activity.model_extra


def test_pydantic_rejects_coercion_and_malformed_undo() -> None:
    with pytest.raises(ProtocolError):
        parse_inbound_activity(
            {
                "id": 123,
                "type": "Like",
                "actor": REMOTE_ACTOR,
                "object": POST_URL,
            }
        )
    with pytest.raises(ProtocolError):
        parse_inbound_activity(
            {
                "id": "https://remote.example/undo/1",
                "type": "Undo",
                "actor": REMOTE_ACTOR,
                "object": {
                    "id": "https://remote.example/follow/1",
                    "type": "Create",
                    "actor": REMOTE_ACTOR,
                    "object": POST_URL,
                },
            }
        )


def test_public_reply() -> None:
    activity = {
        "id": "https://remote.example/activities/3",
        "type": "Create",
        "actor": REMOTE_ACTOR,
        "object": {
            "id": "https://remote.example/notes/3",
            "type": "Note",
            "attributedTo": REMOTE_ACTOR,
            "inReplyTo": POST_URL,
            "to": [PUBLIC],
        },
    }
    event = validate_inbox_activity(activity, actor_url=REMOTE_ACTOR, base_url=BASE_URL)
    assert event.kind == "Reply"


def test_public_quote_request_builds_stable_accept_and_authorization() -> None:
    value = {
        "@context": [
            "https://www.w3.org/ns/activitystreams",
            {
                "QuoteRequest": "https://w3id.org/fep/044f#QuoteRequest",
                "quote": {
                    "@id": "https://w3id.org/fep/044f#quote",
                    "@type": "@id",
                },
            },
        ],
        "id": f"{REMOTE_ACTOR}/quote-requests/1",
        "type": "QuoteRequest",
        "actor": REMOTE_ACTOR,
        "object": POST_URL,
        "instrument": {
            "id": f"{REMOTE_ACTOR}/posts/quoted",
            "type": "Note",
            "attributedTo": REMOTE_ACTOR,
            "quote": POST_URL,
            "to": [PUBLIC],
        },
    }
    activity = parse_inbound_activity(value)
    assert isinstance(activity, QuoteRequestActivity)
    event = validate_inbox_activity(activity, actor_url=REMOTE_ACTOR, base_url=BASE_URL)
    assert event.kind == "QuoteRequest"
    assert event.object_id == f"{REMOTE_ACTOR}/posts/quoted"

    authorization = quote_authorization(f"{BASE_URL}/activitypub/wrlach", activity)
    accept = accept_quote_request(
        f"{BASE_URL}/activitypub/wrlach", activity, authorization
    )
    assert authorization["type"] == "QuoteAuthorization"
    assert authorization["interactingObject"] == event.object_id
    assert authorization["interactionTarget"] == POST_URL
    assert accept["result"] == authorization["id"]
    assert accept["object"]["instrument"] == event.object_id
    assert (
        quote_authorization(f"{BASE_URL}/activitypub/wrlach", activity) == authorization
    )


@pytest.mark.parametrize(
    ("change", "message"),
    [
        ({"attributedTo": "https://attacker.example/users/me"}, "author"),
        (
            {"quote": "https://wrla.ch/activitypub/posts/20260101000000-other"},
            "targets",
        ),
        ({"to": ["https://remote.example/users/me/followers"]}, "public"),
        ({"id": "https://attacker.example/posts/quoted"}, "belong"),
    ],
)
def test_rejects_invalid_quote_requests(
    change: dict[str, object], message: str
) -> None:
    instrument = {
        "id": f"{REMOTE_ACTOR}/posts/quoted",
        "type": "Note",
        "attributedTo": REMOTE_ACTOR,
        "quote": POST_URL,
        "to": [PUBLIC],
        **change,
    }
    activity = {
        "id": f"{REMOTE_ACTOR}/quote-requests/1",
        "type": "QuoteRequest",
        "actor": REMOTE_ACTOR,
        "object": POST_URL,
        "instrument": instrument,
    }
    with pytest.raises(ProtocolError, match=message):
        validate_inbox_activity(activity, actor_url=REMOTE_ACTOR, base_url=BASE_URL)


def test_rejects_private_and_foreign_replies() -> None:
    activity = {
        "id": "https://remote.example/activities/3",
        "type": "Create",
        "actor": REMOTE_ACTOR,
        "object": {
            "id": "https://remote.example/notes/3",
            "type": "Note",
            "attributedTo": REMOTE_ACTOR,
            "inReplyTo": "https://elsewhere.example/post",
        },
    }
    with pytest.raises(ProtocolError):
        validate_inbox_activity(activity, actor_url=REMOTE_ACTOR, base_url=BASE_URL)


@pytest.mark.parametrize(
    "unsafe",
    [
        "http://social.example/inbox",
        "https://localhost/inbox",
        "https://127.0.0.1/inbox",
        "https://169.254.1.1/inbox",
    ],
)
def test_remote_url_policy(unsafe: str) -> None:
    assert ensure_remote_url("https://social.example/inbox") == (
        "https://social.example/inbox"
    )
    with pytest.raises(ProtocolError):
        ensure_remote_url(unsafe)


def test_remote_response_body_is_streamed_and_bounded() -> None:
    @dataclass
    class ReadResult:
        done: bool
        value: bytes | None

    class Reader:
        def __init__(self, chunks: list[bytes]) -> None:
            self.chunks = iter(chunks)
            self.cancelled = False
            self.released = False

        async def read(self) -> ReadResult:
            try:
                return ReadResult(done=False, value=next(self.chunks))
            except StopIteration:
                return ReadResult(done=True, value=None)

        async def cancel(self) -> None:
            self.cancelled = True

        def releaseLock(self) -> None:
            self.released = True

    class Body:
        def __init__(self, reader: Reader) -> None:
            self.reader = reader

        def getReader(self) -> Reader:
            return self.reader

    class RemoteResponse:
        def __init__(self, reader: Reader) -> None:
            self.body = Body(reader)

    reader = Reader([b"abc", b"def"])
    assert asyncio.run(read_limited_body(RemoteResponse(reader), 6)) == b"abcdef"
    assert reader.released

    oversized = Reader([b"abc", b"defg"])
    with pytest.raises(ProtocolError, match="too large"):
        asyncio.run(read_limited_body(RemoteResponse(oversized), 6))
    assert oversized.cancelled
    assert oversized.released


def test_remote_actor_deserialization() -> None:
    actor = RemoteActor.model_validate(
        {
            "id": REMOTE_ACTOR,
            "inbox": f"{REMOTE_ACTOR}/inbox",
            "endpoints": {"sharedInbox": "https://remote.example/inbox"},
            "publicKey": {
                "id": f"{REMOTE_ACTOR}#main-key",
                "owner": REMOTE_ACTOR,
                "publicKeyPem": "PUBLIC KEY",
            },
        }
    )
    assert actor.endpoints.shared_inbox == "https://remote.example/inbox"
    assert actor.public_keys[0].owner == REMOTE_ACTOR


def test_manifest_is_strict_and_checks_redactions() -> None:
    valid_post = {
        "source_id": "20260101000000-post",
        "published": "2026-01-01T00:00:00Z",
        "object": POST_URL,
        "activity": f"{POST_URL}/activity",
        "content_hash": "a" * 64,
        "redacted": False,
    }
    manifest = Manifest.model_validate(
        {"version": 1, "actor": f"{BASE_URL}/activitypub/wrlach", "posts": [valid_post]}
    )
    assert manifest.posts[0].object_url == POST_URL

    with pytest.raises(ValidationError):
        Manifest.model_validate(
            {
                "version": 1,
                "actor": f"{BASE_URL}/activitypub/wrlach",
                "posts": [{**valid_post, "unexpected": True}],
            }
        )
    with pytest.raises(ValidationError):
        Manifest.model_validate(
            {
                "version": 1,
                "actor": f"{BASE_URL}/activitypub/wrlach",
                "posts": [
                    {
                        **valid_post,
                        "activity": None,
                        "redacted": True,
                        "deleted": None,
                    }
                ],
            }
        )


def test_grace_period_and_retry_cap() -> None:
    observed = datetime(2026, 1, 1, tzinfo=UTC)
    timestamp = observed.isoformat().replace("+00:00", "Z")
    assert not eligible(timestamp, observed + GRACE_PERIOD - timedelta(seconds=1))
    assert eligible(timestamp, observed + GRACE_PERIOD)
    assert retry_at(observed, 1) == observed + timedelta(minutes=5)
    assert retry_at(observed, 20) == observed + timedelta(hours=12)


def test_d1_schema_applies_to_sqlite() -> None:
    database = sqlite3.connect(":memory:")
    migrations = Path(__file__).resolve().parents[1] / "activitypub/migrations"
    for migration in sorted(migrations.glob("*.sql")):
        database.executescript(migration.read_text())
    tables = {
        row[0]
        for row in database.execute("SELECT name FROM sqlite_master WHERE type='table'")
    }
    assert {
        "metadata",
        "followers",
        "posts",
        "replies",
        "interactions",
        "deliveries",
        "delivery_recipients",
        "quote_authorizations",
    } <= tables


def test_sql_rows_validate_consumed_fields_and_ignore_others() -> None:
    post = PostRow.model_validate(
        {
            "source_id": "20260101000000-post",
            "object_url": POST_URL,
            "first_seen": "2026-01-01T00:01:00Z",
            "state": "pending",
            "unconsumed_column": "ignored",
        }
    )
    delivery = DeliveryRow.model_validate(
        {
            "id": 1,
            "source_id": post.source_id,
            "destination": "https://remote.example/inbox",
            "kind": "Create",
            "body": "{}",
            "attempts": 0,
            "unconsumed_column": "ignored",
        }
    )
    assert post.state == "pending"
    assert delivery.kind == "Create"

    with pytest.raises(ValidationError):
        PostRow.model_validate(
            {
                "source_id": post.source_id,
                "object_url": post.object_url,
                "first_seen": post.first_seen,
                "state": "unknown",
            }
        )
