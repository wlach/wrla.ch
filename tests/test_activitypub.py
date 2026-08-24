from __future__ import annotations

import json
import shutil
from datetime import UTC
from datetime import datetime
from pathlib import Path

import pytest

from sitegen.activitypub import build_excerpt_html
from sitegen.activitypub import first_image
from sitegen.activitypub import load_redactions
from sitegen.config import BlogConfig
from sitegen.site import build_site


def test_preserves_links_and_adds_ellipsis_for_later_content() -> None:
    html = build_excerpt_html(
        "Read [the documentation](/docs) first.\n\nThen do the thing.",
        canonical_url="https://example.com/post/",
        title="A post",
    )
    assert '<a href="https://example.com/docs">the documentation</a>' in html
    assert "first. …</p>" in html
    assert "Read the full post" in html


def test_truncates_at_word_boundary() -> None:
    html = build_excerpt_html(
        "word " * 100,
        canonical_url="https://example.com/post/",
        title="A post",
    )
    excerpt = html.split("<p>")[2].split("</p>")[0]
    assert len(excerpt.removesuffix(" …")) <= 300
    assert excerpt.endswith(" …")


def test_uses_character_boundary_without_whitespace() -> None:
    html = build_excerpt_html(
        "字" * 400,
        canonical_url="https://example.com/post/",
        title="A post",
    )
    excerpt = html.split("<p>")[2].split("</p>")[0]
    assert len(excerpt.removesuffix(" …")) == 300


def test_does_not_cut_link_text() -> None:
    html = build_excerpt_html(
        "a " * 145 + "[complete link text](https://example.net) after",
        canonical_url="https://example.com/post/",
        title="A post",
    )
    assert "complete link" not in html
    assert "example.net" not in html


def test_omits_ellipsis_only_when_paragraph_is_whole_post() -> None:
    html = build_excerpt_html(
        "The whole post.",
        canonical_url="https://example.com/post/",
        title="A post",
    )
    assert "The whole post.</p>" in html
    assert "The whole post. …" not in html


def test_code_block_after_first_paragraph_adds_ellipsis() -> None:
    html = build_excerpt_html(
        "Introduction.\n\n```python\nprint('later')\n```",
        canonical_url="https://example.com/post/",
        title="A post",
    )
    assert "Introduction. …</p>" in html


def test_finds_first_image_with_alt_text() -> None:
    image = first_image(
        "![](ignored.png)\n\n![Useful description](photo.jpg)",
        "https://example.com/log/post/",
    )
    assert image == {
        "type": "Image",
        "url": "https://example.com/log/post/photo.jpg",
        "name": "Useful description",
    }


def test_redaction_config_rejects_unknown_fields(tmp_path: Path) -> None:
    path = tmp_path / "redactions.json"
    path.write_text(
        json.dumps(
            [
                {
                    "source_id": "20260101000000-secret",
                    "deleted": "2026-01-02T00:00:00Z",
                    "typo": True,
                }
            ]
        )
    )
    with pytest.raises(ValueError):
        load_redactions(path)


def test_explicit_redaction_generates_tombstone(tmp_path: Path) -> None:
    root = tmp_path
    repo_root = Path(__file__).resolve().parents[1]
    shutil.copytree(repo_root / "src/templates", root / "src/templates")
    (root / "src/posts/20260101000000-secret").mkdir(parents=True)
    (root / "src/posts/20260101000000-secret/index.md").write_text(
        "# Secret\n\nSomething to remove.\n", encoding="utf-8"
    )
    (root / "activitypub").mkdir()
    shutil.copy2(
        repo_root / "activitypub/public-key.pem",
        root / "activitypub/public-key.pem",
    )
    (root / "activitypub/redactions.json").write_text(
        json.dumps(
            [
                {
                    "source_id": "20260101000000-secret",
                    "deleted": "2026-01-02T00:00:00Z",
                }
            ]
        )
    )
    config = BlogConfig(
        title="Test",
        author="Test",
        base_url="https://example.com",
        posts_per_page=10,
        posts_in_rss=10,
        repo_url="https://example.com/repo",
    )
    build_site(root, config)
    tombstone = json.loads(
        (root / "_build/activitypub/posts/20260101000000-secret/index.html").read_text()
    )
    assert tombstone["type"] == "Tombstone"
    outbox = json.loads(
        (root / "_build/activitypub/wrlach/outbox/index.html").read_text()
    )
    assert outbox["totalItems"] == 0
    manifest = json.loads((root / "_build/activitypub/manifest.json").read_text())
    assert manifest["posts"][0]["redacted"]
    assert manifest["posts"][0]["deleted"] == datetime(
        2026, 1, 2, tzinfo=UTC
    ).isoformat().replace("+00:00", "Z")
