from __future__ import annotations

import re
from datetime import datetime
from typing import Annotated
from typing import Literal
from typing import NotRequired
from typing import TypedDict

from pydantic import BaseModel
from pydantic import ConfigDict
from pydantic import Field
from pydantic import StringConstraints
from pydantic import TypeAdapter
from pydantic import field_validator
from pydantic import model_validator

NonEmptyString = Annotated[str, StringConstraints(strip_whitespace=True, min_length=1)]
Addressing = NonEmptyString | list[NonEmptyString]
PostState = Literal["historical", "pending", "delivered", "cancelled", "redacted"]
DeliveryKind = Literal["Create", "Delete", "Accept"]

_ActivityContext = TypedDict("_ActivityContext", {"@context": str})


class OutboundActivity(_ActivityContext):
    id: str
    type: DeliveryKind
    actor: str
    object: object
    to: NotRequired[list[str]]
    cc: NotRequired[list[str]]


class SqlRow(BaseModel):
    """Fields consumed from a repository-owned SQL result."""

    model_config = ConfigDict(extra="ignore", strict=True)


class PostRow(SqlRow):
    source_id: str
    object_url: str
    first_seen: str
    state: PostState


class DeliveryRow(SqlRow):
    id: int
    source_id: str
    destination: str
    kind: DeliveryKind
    body: str
    attempts: int


POST_STATE_ADAPTER = TypeAdapter(PostState)


class ActivityPubModel(BaseModel):
    """Required protocol fields are strict; federation extensions are retained."""

    model_config = ConfigDict(extra="allow", strict=True, populate_by_name=True)


class FollowActivity(ActivityPubModel):
    id: NonEmptyString
    type: Literal["Follow"]
    actor: NonEmptyString
    object: NonEmptyString


class LikeActivity(ActivityPubModel):
    id: NonEmptyString
    type: Literal["Like"]
    actor: NonEmptyString
    object: NonEmptyString


class AnnounceActivity(ActivityPubModel):
    id: NonEmptyString
    type: Literal["Announce"]
    actor: NonEmptyString
    object: NonEmptyString


UndoableActivity = Annotated[
    FollowActivity | LikeActivity | AnnounceActivity,
    Field(discriminator="type"),
]


class UndoActivity(ActivityPubModel):
    id: NonEmptyString
    type: Literal["Undo"]
    actor: NonEmptyString
    object: UndoableActivity


class ReplyNote(ActivityPubModel):
    id: NonEmptyString
    type: Literal["Note"]
    attributed_to: NonEmptyString = Field(alias="attributedTo")
    in_reply_to: NonEmptyString = Field(alias="inReplyTo")
    to: Addressing | None = None
    cc: Addressing | None = None
    audience: Addressing | None = None


class CreateReplyActivity(ActivityPubModel):
    id: NonEmptyString
    type: Literal["Create"]
    actor: NonEmptyString
    object: ReplyNote
    to: Addressing | None = None
    cc: Addressing | None = None
    audience: Addressing | None = None


InboundActivity = Annotated[
    FollowActivity
    | LikeActivity
    | AnnounceActivity
    | UndoActivity
    | CreateReplyActivity,
    Field(discriminator="type"),
]
INBOUND_ACTIVITY_ADAPTER = TypeAdapter(InboundActivity)


class ActorEndpoints(ActivityPubModel):
    shared_inbox: NonEmptyString | None = Field(default=None, alias="sharedInbox")


class RemotePublicKey(ActivityPubModel):
    id: NonEmptyString
    owner: NonEmptyString
    public_key_pem: NonEmptyString = Field(alias="publicKeyPem")


class RemoteActor(ActivityPubModel):
    id: NonEmptyString
    inbox: NonEmptyString
    endpoints: ActorEndpoints = Field(default_factory=ActorEndpoints)
    public_key: RemotePublicKey | list[RemotePublicKey] = Field(alias="publicKey")

    @property
    def public_keys(self) -> list[RemotePublicKey]:
        return self.public_key if isinstance(self.public_key, list) else [self.public_key]


class PublishedNote(ActivityPubModel):
    id: NonEmptyString
    type: Literal["Note"]
    attributed_to: NonEmptyString = Field(alias="attributedTo")
    published: NonEmptyString
    to: list[NonEmptyString]
    cc: list[NonEmptyString]

    @field_validator("published")
    @classmethod
    def published_has_timezone(cls, value: str) -> str:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
        if parsed.tzinfo is None:
            raise ValueError("published must include a timezone")
        return value


class ManifestPost(BaseModel):
    model_config = ConfigDict(extra="forbid", strict=True, populate_by_name=True)

    source_id: NonEmptyString
    published: NonEmptyString
    object_url: NonEmptyString = Field(alias="object")
    activity: NonEmptyString | None = None
    content_hash: NonEmptyString
    redacted: bool
    deleted: NonEmptyString | None = None

    @field_validator("published", "deleted")
    @classmethod
    def timestamps_have_timezones(cls, value: str | None) -> str | None:
        if value is None:
            return None
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
        if parsed.tzinfo is None:
            raise ValueError("manifest timestamps must include a timezone")
        return value

    @field_validator("source_id")
    @classmethod
    def source_id_has_expected_shape(cls, value: str) -> str:
        if not re.fullmatch(r"\d{14}-[a-z0-9][a-z0-9-]*", value):
            raise ValueError("invalid source_id")
        return value

    @field_validator("content_hash")
    @classmethod
    def content_hash_is_sha256(cls, value: str) -> str:
        if not re.fullmatch(r"[0-9a-f]{64}", value):
            raise ValueError("content_hash must be a lowercase SHA-256 digest")
        return value

    @model_validator(mode="after")
    def redaction_fields_are_consistent(self) -> ManifestPost:
        if self.redacted and self.deleted is None:
            raise ValueError("redacted posts require deleted")
        if not self.redacted and self.activity is None:
            raise ValueError("active posts require activity")
        return self


class Manifest(BaseModel):
    model_config = ConfigDict(extra="forbid", strict=True)

    version: Literal[1]
    actor: NonEmptyString
    posts: list[ManifestPost]
