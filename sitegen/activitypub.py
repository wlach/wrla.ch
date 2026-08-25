from __future__ import annotations

import hashlib
import json
import re
from dataclasses import dataclass
from datetime import UTC
from datetime import datetime
from html import escape
from pathlib import Path
from typing import TYPE_CHECKING
from urllib.parse import urljoin

from markdown_it import MarkdownIt
from pydantic import AwareDatetime
from pydantic import BaseModel
from pydantic import ConfigDict
from pydantic import TypeAdapter
from pydantic import ValidationError
from pydantic import field_validator

from .markdown import strip_html

if TYPE_CHECKING:
    from .config import BlogConfig
    from .site import Post

ACTIVITYSTREAMS_CONTEXT = "https://www.w3.org/ns/activitystreams"
PUBLIC = "https://www.w3.org/ns/activitystreams#Public"
QUOTE_POLICY_CONTEXT: dict[str, object] = {
    "gts": "https://gotosocial.org/ns#",
    "interactionPolicy": {"@id": "gts:interactionPolicy", "@type": "@id"},
    "canQuote": {"@id": "gts:canQuote", "@type": "@id"},
    "automaticApproval": {"@id": "gts:automaticApproval", "@type": "@id"},
    "manualApproval": {"@id": "gts:manualApproval", "@type": "@id"},
}
OUTBOX_PAGE_SIZE = 20
EXCERPT_LIMIT = 300


@dataclass(frozen=True)
class InlineSegment:
    text: str
    href: str | None = None


class Redaction(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True, strict=True)

    source_id: str
    deleted: AwareDatetime

    @field_validator("source_id")
    @classmethod
    def source_id_has_expected_shape(cls, value: str) -> str:
        _source_parts(value)
        return value


REDACTIONS_ADAPTER = TypeAdapter(list[Redaction])


def _json_bytes(value: object) -> bytes:
    return (json.dumps(value, ensure_ascii=False, indent=2) + "\n").encode()


def _write_json(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(_json_bytes(value))


def _isoformat(value: datetime) -> str:
    return value.astimezone(UTC).isoformat(timespec="seconds").replace("+00:00", "Z")


def _source_parts(source_id: str) -> tuple[datetime, str]:
    if len(source_id) < 16 or source_id[14] != "-":
        raise ValueError(f"Invalid ActivityPub source ID: {source_id}")
    try:
        published = datetime.strptime(source_id[:14], "%Y%m%d%H%M%S").replace(
            tzinfo=UTC
        )
    except ValueError as exc:
        raise ValueError(f"Invalid ActivityPub source ID: {source_id}") from exc
    return published, source_id[15:]


def load_redactions(path: Path) -> dict[str, Redaction]:
    if not path.exists():
        return {}
    try:
        raw = REDACTIONS_ADAPTER.validate_json(path.read_bytes())
    except ValidationError as exc:
        raise ValueError("Invalid activitypub/redactions.json") from exc
    redactions: dict[str, Redaction] = {}
    for item in raw:
        if item.source_id in redactions:
            raise ValueError(f"Duplicate redaction: {item.source_id}")
        redactions[item.source_id] = item
    return redactions


def _paragraph_segments(markdown_text: str) -> tuple[list[InlineSegment], bool]:
    md = MarkdownIt("commonmark", {"html": False})
    tokens = md.parse(markdown_text)
    paragraph_index = next(
        (index for index, token in enumerate(tokens) if token.type == "paragraph_open"),
        None,
    )
    if paragraph_index is None:
        return [], False
    inline = tokens[paragraph_index + 1]
    if inline.type != "inline" or not inline.children:
        return [], False

    segments: list[InlineSegment] = []
    href: str | None = None
    for token in inline.children:
        if token.type == "link_open":
            raw_href = token.attrGet("href")
            href = raw_href if isinstance(raw_href, str) else None
        elif token.type == "link_close":
            href = None
        elif token.type in {"text", "code_inline"}:
            segments.append(InlineSegment(token.content, href))
        elif token.type in {"softbreak", "hardbreak"}:
            segments.append(InlineSegment(" ", href))
        elif token.type == "image":
            alt = token.content.strip()
            if alt:
                segments.append(InlineSegment(alt, None))

    has_later_content = any(
        bool(token.content.strip()) or token.type == "hr"
        for token in tokens[paragraph_index + 3 :]
    )
    return segments, has_later_content


def _truncate_segments(
    segments: list[InlineSegment], limit: int = EXCERPT_LIMIT
) -> tuple[list[InlineSegment], bool]:
    text = "".join(segment.text for segment in segments)
    if len(text) <= limit:
        return segments, False

    candidate = text[:limit]
    whitespace = [match.start() for match in re.finditer(r"\s", candidate)]
    cutoff = whitespace[-1] if whitespace else limit
    cutoff = len(candidate[:cutoff].rstrip())

    position = 0
    for segment in segments:
        end = position + len(segment.text)
        if segment.href and position < cutoff < end:
            cutoff = position
            break
        position = end

    result: list[InlineSegment] = []
    position = 0
    for segment in segments:
        if position >= cutoff:
            break
        remaining = cutoff - position
        text_part = segment.text[:remaining]
        if text_part:
            result.append(InlineSegment(text_part, segment.href))
        position += len(segment.text)
    while result and not result[-1].text.rstrip():
        result.pop()
    if result:
        last = result[-1]
        result[-1] = InlineSegment(last.text.rstrip(), last.href)
    return result, True


def build_excerpt_html(markdown_text: str, *, canonical_url: str, title: str) -> str:
    segments, has_later_content = _paragraph_segments(markdown_text)
    segments, truncated = _truncate_segments(segments)
    rendered: list[str] = []
    for segment in segments:
        text = escape(segment.text)
        if segment.href:
            href = escape(urljoin(canonical_url, segment.href), quote=True)
            rendered.append(f'<a href="{href}">{text}</a>')
        else:
            rendered.append(text)
    ellipsis = " …" if truncated or has_later_content else ""
    safe_title = escape(title)
    safe_url = escape(canonical_url, quote=True)
    return (
        f"<p><strong>{safe_title}</strong></p>"
        f"<p>{''.join(rendered)}{ellipsis}</p>"
        f'<p><a href="{safe_url}">Read the full post</a></p>'
    )


def first_image(markdown_text: str, canonical_url: str) -> dict[str, str] | None:
    md = MarkdownIt("commonmark", {"html": False})
    for token in md.parse(markdown_text):
        if token.type != "inline" or not token.children:
            continue
        for child in token.children:
            if child.type != "image":
                continue
            alt = child.content.strip()
            src = child.attrGet("src")
            if not alt or not isinstance(src, str) or not src:
                continue
            return {
                "type": "Image",
                "url": urljoin(canonical_url, src),
                "name": alt,
            }
    return None


def _post_note(config: BlogConfig, post: Post) -> dict[str, object]:
    actor = f"{config.base_url}/activitypub/wrlach"
    object_id = f"{config.base_url}/activitypub/posts/{post.source_path}"
    canonical = f"{config.base_url}{post.url}"
    note: dict[str, object] = {
        "@context": [ACTIVITYSTREAMS_CONTEXT, QUOTE_POLICY_CONTEXT],
        "id": object_id,
        "type": "Note",
        "attributedTo": actor,
        "published": _isoformat(post.date),
        "content": build_excerpt_html(
            post.body_markdown,
            canonical_url=canonical,
            title=strip_html(post.title_html),
        ),
        "mediaType": "text/html",
        "url": canonical,
        "to": [PUBLIC],
        "cc": [f"{actor}/followers"],
        "interactionPolicy": {
            "canQuote": {
                "automaticApproval": [PUBLIC],
                "manualApproval": [],
            }
        },
        "tag": [
            {
                "type": "Hashtag",
                "name": "#" + re.sub(r"[^\w]", "", tag.name),
                "href": f"{config.base_url}{tag.url}",
            }
            for tag in post.tags
        ],
        "replies": f"{config.base_url}/activitypub/replies/{post.source_path}",
        "likes": f"{config.base_url}/activitypub/likes/{post.source_path}",
        "shares": f"{config.base_url}/activitypub/shares/{post.source_path}",
    }
    image = first_image(post.body_markdown, canonical)
    if image:
        note["attachment"] = [image]
    return note


def _create(note: dict[str, object]) -> dict[str, object]:
    object_id = str(note["id"])
    return {
        "@context": ACTIVITYSTREAMS_CONTEXT,
        "id": f"{object_id}/activity",
        "type": "Create",
        "actor": note["attributedTo"],
        "published": note["published"],
        "to": note["to"],
        "cc": note["cc"],
        "object": note,
    }


def _actor(config: BlogConfig, public_key: str) -> dict[str, object]:
    actor = f"{config.base_url}/activitypub/wrlach"
    return {
        "@context": ACTIVITYSTREAMS_CONTEXT,
        "id": actor,
        "type": "Service",
        "preferredUsername": "wrlach",
        "name": config.title,
        "summary": "New posts from wrla.ch. 🪴",
        "url": config.base_url,
        "attachment": [
            {
                "type": "PropertyValue",
                "name": "Home",
                "value": (
                    f'<a href="{escape(config.base_url, quote=True)}">'
                    f"{escape(config.base_url)}</a>"
                ),
            },
            {
                "type": "PropertyValue",
                "name": "Source",
                "value": (
                    f'<a href="{escape(config.repo_url, quote=True)}">'
                    f"{escape(config.repo_url)}</a>"
                ),
            },
        ],
        "icon": {
            "type": "Image",
            "mediaType": "image/png",
            "url": f"{config.base_url}/img/wlach_icon.png",
        },
        "inbox": f"{actor}/inbox",
        "outbox": f"{actor}/outbox",
        "followers": f"{actor}/followers",
        "publicKey": {
            "id": f"{actor}#main-key",
            "owner": actor,
            "publicKeyPem": public_key.strip() + "\n",
        },
    }


def build_activitypub(
    root: Path, build_dir: Path, config: BlogConfig, posts: list[Post]
) -> None:
    source_dir = root / "activitypub"
    public_key_path = source_dir / "public-key.pem"
    if not public_key_path.exists():
        raise RuntimeError("Missing activitypub/public-key.pem")
    public_key = public_key_path.read_text(encoding="ascii")
    redactions = load_redactions(source_dir / "redactions.json")

    post_by_id = {post.source_path: post for post in posts}
    active_posts = [post for post in posts if post.source_path not in redactions]
    unknown_redactions = set(redactions) - set(post_by_id)
    for source_id in unknown_redactions:
        _source_parts(source_id)

    actor_url = f"{config.base_url}/activitypub/wrlach"
    _write_json(
        build_dir / "activitypub" / "wrlach" / "index.html", _actor(config, public_key)
    )

    creates: list[dict[str, object]] = []
    manifest_posts: list[dict[str, object]] = []
    for post in active_posts:
        note = _post_note(config, post)
        create = _create(note)
        creates.append(create)
        body = _json_bytes(note)
        _write_json(
            build_dir / "activitypub" / "posts" / post.source_path / "index.html", note
        )
        manifest_posts.append(
            {
                "source_id": post.source_path,
                "published": _isoformat(post.date),
                "object": note["id"],
                "activity": create["id"],
                "content_hash": hashlib.sha256(body).hexdigest(),
                "redacted": False,
            }
        )

    for source_id, redaction in sorted(redactions.items()):
        object_id = f"{config.base_url}/activitypub/posts/{source_id}"
        tombstone = {
            "@context": ACTIVITYSTREAMS_CONTEXT,
            "id": object_id,
            "type": "Tombstone",
            "formerType": "Note",
            "deleted": _isoformat(redaction.deleted),
        }
        _write_json(
            build_dir / "activitypub" / "posts" / source_id / "index.html", tombstone
        )
        manifest_posts.append(
            {
                "source_id": source_id,
                "published": _isoformat(_source_parts(source_id)[0]),
                "object": object_id,
                "content_hash": hashlib.sha256(_json_bytes(tombstone)).hexdigest(),
                "redacted": True,
                "deleted": _isoformat(redaction.deleted),
            }
        )

    total_pages = max(1, (len(creates) + OUTBOX_PAGE_SIZE - 1) // OUTBOX_PAGE_SIZE)
    outbox_url = f"{actor_url}/outbox"
    outbox = {
        "@context": ACTIVITYSTREAMS_CONTEXT,
        "id": outbox_url,
        "type": "OrderedCollection",
        "totalItems": len(creates),
        "first": f"{outbox_url}/page/1",
        "last": f"{outbox_url}/page/{total_pages}",
    }
    _write_json(build_dir / "activitypub" / "wrlach" / "outbox" / "index.html", outbox)
    for page in range(1, total_pages + 1):
        start = (page - 1) * OUTBOX_PAGE_SIZE
        page_value: dict[str, object] = {
            "@context": ACTIVITYSTREAMS_CONTEXT,
            "id": f"{outbox_url}/page/{page}",
            "type": "OrderedCollectionPage",
            "partOf": outbox_url,
            "orderedItems": creates[start : start + OUTBOX_PAGE_SIZE],
        }
        if page > 1:
            page_value["prev"] = f"{outbox_url}/page/{page - 1}"
        if page < total_pages:
            page_value["next"] = f"{outbox_url}/page/{page + 1}"
        _write_json(
            build_dir
            / "activitypub"
            / "wrlach"
            / "outbox"
            / "page"
            / str(page)
            / "index.html",
            page_value,
        )

    manifest_posts.sort(key=lambda item: str(item["published"]), reverse=True)
    _write_json(
        build_dir / "activitypub" / "manifest.json",
        {"version": 1, "actor": actor_url, "posts": manifest_posts},
    )

    headers_path = build_dir / "_headers"
    existing = headers_path.read_text(encoding="utf-8") if headers_path.exists() else ""
    headers_path.write_text(
        existing
        + "\n/activitypub/*\n"
        + "  Content-Type: application/activity+json; charset=utf-8\n",
        encoding="utf-8",
    )
