from __future__ import annotations

import shutil
from dataclasses import dataclass
from datetime import UTC, datetime
from math import ceil
from pathlib import Path
from typing import Any

import frontmatter
from jinja2 import Environment, FileSystemLoader, select_autoescape
from markupsafe import Markup
from slugify import slugify
from pygments.formatters import HtmlFormatter  # type: ignore[unresolved-import]

from .config import BlogConfig
from .markdown import (
    extract_title,
    format_atom_date,
    format_pretty_date,
    format_rss_date,
    markdown_renderer,
    normalize_tags,
    strip_html,
    truncate_text,
    validate_heading_sequence,
)


@dataclass(frozen=True)
class Tag:
    name: str
    slug: str

    @property
    def url(self) -> str:
        return f"/tags/{self.slug}.html"

    @property
    def atom_feed_url(self) -> str:
        return f"/feeds/{self.slug}.atom.xml"

    @property
    def rss_feed_url(self) -> str:
        return f"/feeds/{self.slug}.rss.xml"


@dataclass(frozen=True)
class Post:
    title: str
    slug: str
    date: datetime
    content_html: str
    content_text: str
    tags: tuple[Tag, ...]

    @property
    def url(self) -> str:
        return f"/blog/{self.date.year:04d}/{self.date.month:02d}/{self.slug}/"

    @property
    def date_pretty(self) -> str:
        return format_pretty_date(self.date)


def _make_urn(base_url: str, path: str) -> str:
    base = base_url.replace("https://", "https-").replace("http://", "http-")
    base = base.replace(".", "-")
    normalized = path.rstrip("/").replace("/", "-").replace(".", "-")
    return f"urn:{base}:{normalized}"


def _load_posts(posts_dir: Path) -> list[Post]:
    md = markdown_renderer()
    posts: list[Post] = []
    for path in sorted(posts_dir.glob("*/index.md")):
        directory = path.parent
        stem = directory.name
        if len(stem) < 16 or stem[14] != "-":
            raise ValueError(f"Invalid post directory: {directory.name}")  # noqa: TRY003
        timestamp = stem[:14]
        slug = stem[15:]
        try:
            date = datetime.strptime(timestamp, "%Y%m%d%H%M%S").replace(tzinfo=UTC)
        except ValueError as exc:
            raise ValueError(f"Invalid timestamp in {directory.name}") from exc  # noqa: TRY003
        raw = path.read_text(encoding="utf-8")
        parsed = frontmatter.loads(raw)
        title, body_without_title = extract_title(parsed.content)
        validate_heading_sequence(parsed.content, md)
        tags = tuple(
            Tag(name=tag, slug=slugify(tag))
            for tag in normalize_tags(parsed.metadata.get("tags"))
        )
        content_html = md.render(body_without_title)
        content_text = strip_html(content_html)
        posts.append(
            Post(
                title=title,
                slug=slug,
                date=date,
                content_html=content_html,
                content_text=content_text,
                tags=tags,
            )
        )
    posts.sort(key=lambda post: post.date, reverse=True)
    return posts


def _load_pages(pages_dir: Path) -> list[dict[str, Any]]:
    md = markdown_renderer()
    pages: list[dict[str, Any]] = []
    for path in sorted(pages_dir.glob("*.md")):
        raw = path.read_text(encoding="utf-8")
        parsed = frontmatter.loads(raw)
        title = parsed.metadata.get("title") or path.stem.replace("-", " ").title()
        content_html = md.render(parsed.content)
        content_text = strip_html(content_html)
        pages.append(
            {
                "title": title,
                "slug": path.stem,
                "content_html": content_html,
                "content_text": content_text,
            }
        )
    return pages


def _copy_static_assets(root: Path, build_dir: Path) -> None:
    src_dir = root / "src"
    for folder in ("css", "js", "img", "fonts", "files"):
        source = src_dir / folder
        if not source.exists():
            continue
        target = build_dir / folder
        if target.exists():
            shutil.rmtree(target)
        shutil.copytree(source, target)


def _write_pygments_css(build_dir: Path) -> None:
    css_dir = build_dir / "css"
    css_dir.mkdir(parents=True, exist_ok=True)
    formatter = HtmlFormatter(cssclass="colorful")
    css = formatter.get_style_defs(".colorful")
    (css_dir / "pygments.css").write_text(css.strip() + "\n", encoding="utf-8")


def _render_template(env: Environment, template_name: str, context: dict[str, Any]) -> str:
    template = env.get_template(template_name)
    return template.render(**context)


def build_site(root: Path, config: BlogConfig) -> None:
    build_dir = root / "_build"
    if build_dir.exists():
        shutil.rmtree(build_dir)
    build_dir.mkdir(parents=True)

    posts_dir = root / "src" / "posts"
    pages_dir = root / "src" / "pages"
    templates_dir = root / "src" / "templates"

    posts = _load_posts(posts_dir)
    pages = _load_pages(pages_dir) if pages_dir.exists() else []

    env = Environment(
        loader=FileSystemLoader(templates_dir),
        autoescape=select_autoescape(["html", "xml"]),
    )

    _copy_static_assets(root, build_dir)
    _write_pygments_css(build_dir)

    keywords_all = ", ".join(sorted({tag.name for post in posts for tag in post.tags}))
    atom_all = "/feeds/all.atom.xml"
    rss_all = "/feeds/all.rss.xml"

    for index, post in enumerate(posts):
        rel_next = posts[index + 1].url if index + 1 < len(posts) else None
        rel_prev = posts[index - 1].url if index > 0 else None
        description = truncate_text(post.content_text, 255)
        context = {
            "page_title": post.title,
            "description": description,
            "author": config.author,
            "keywords": ", ".join(tag.name for tag in post.tags),
            "canonical_url": f"{config.base_url}{post.url}",
            "atom_feed_url": atom_all,
            "rss_feed_url": rss_all,
            "rel_next": rel_next,
            "rel_prev": rel_prev,
            "active_nav": None,
            "title": post.title,
            "date": post.date_pretty,
            "tags": [{"name": tag.name, "url": tag.url} for tag in post.tags],
            "content": Markup(post.content_html),
            "tag": None,
        }
        html = _render_template(env, "post.html", context)
        target_dir = build_dir / "blog" / f"{post.date.year:04d}" / f"{post.date.month:02d}" / post.slug
        target_dir.mkdir(parents=True, exist_ok=True)
        (target_dir / "index.html").write_text(html, encoding="utf-8")

    posts_per_page = config.posts_per_page
    total_pages = max(1, ceil(len(posts) / posts_per_page))
    page_urls = {
        page: "/index.html" if page == 1 else f"/index-{page}.html"
        for page in range(1, total_pages + 1)
    }
    for page in range(1, total_pages + 1):
        start = (page - 1) * posts_per_page
        end = start + posts_per_page
        page_posts = posts[start:end]
        pagination = {
            "pages": [
                {
                    "number": number,
                    "url": page_urls[number],
                    "is_current": number == page,
                }
                for number in range(1, total_pages + 1)
            ],
            "prev_url": page_urls.get(page - 1),
            "next_url": page_urls.get(page + 1),
        }
        context = {
            "page_title": config.title,
            "description": config.title,
            "author": config.author,
            "keywords": keywords_all,
            "canonical_url": f"{config.base_url}{page_urls[page]}",
            "atom_feed_url": atom_all,
            "rss_feed_url": rss_all,
            "rel_next": None,
            "rel_prev": None,
            "active_nav": None,
            "posts": [
                {
                    "title": post.title,
                    "url": post.url,
                    "date": post.date_pretty,
                    "tags": [{"name": tag.name, "url": tag.url} for tag in post.tags],
                    "content": Markup(post.content_html),
                }
                for post in page_posts
            ],
            "pagination": pagination if total_pages > 1 else None,
            "tag": None,
        }
        html = _render_template(env, "index.html", context)
        target = build_dir / page_urls[page].lstrip("/")
        target.write_text(html, encoding="utf-8")

    tag_map: dict[str, list[Post]] = {}
    tag_defs: dict[str, Tag] = {}
    for post in posts:
        for tag in post.tags:
            tag_map.setdefault(tag.slug, []).append(post)
            tag_defs[tag.slug] = tag

    tags_dir = build_dir / "tags"
    tags_dir.mkdir(parents=True, exist_ok=True)
    for tag_slug, tag_posts in sorted(tag_map.items()):
        tag = tag_defs[tag_slug]
        tag_posts.sort(key=lambda post: post.date, reverse=True)
        context = {
            "page_title": f"Posts tagged '{tag.name}'",
            "description": f"Posts tagged '{tag.name}'",
            "author": config.author,
            "keywords": tag.name,
            "canonical_url": f"{config.base_url}{tag.url}",
            "atom_feed_url": tag.atom_feed_url,
            "rss_feed_url": tag.rss_feed_url,
            "rel_next": None,
            "rel_prev": None,
            "active_nav": None,
            "posts": [
                {
                    "title": post.title,
                    "url": post.url,
                    "date": post.date_pretty,
                    "tags": [{"name": t.name, "url": t.url} for t in post.tags],
                    "content": Markup(post.content_html),
                }
                for post in tag_posts
            ],
            "tag": tag.name,
        }
        html = _render_template(env, "tag.html", context)
        (tags_dir / f"{tag.slug}.html").write_text(html, encoding="utf-8")

    for page in pages:
        description = truncate_text(page["content_text"], 255)
        context = {
            "page_title": page["title"],
            "description": description,
            "author": config.author,
            "keywords": "",
            "canonical_url": f"{config.base_url}/{page['slug']}.html",
            "atom_feed_url": atom_all,
            "rss_feed_url": rss_all,
            "rel_next": None,
            "rel_prev": None,
            "active_nav": "about" if page["slug"] == "about" else None,
            "content": Markup(page["content_html"]),
            "tag": None,
        }
        html = _render_template(env, "page.html", context)
        (build_dir / f"{page['slug']}.html").write_text(html, encoding="utf-8")

    _build_feeds(build_dir, config, posts, tag_defs, tag_map, env)
    _build_sitemap(build_dir, config, posts, pages)


def _build_feeds(
    build_dir: Path,
    config: BlogConfig,
    posts: list[Post],
    tag_defs: dict[str, Tag],
    tag_map: dict[str, list[Post]],
    env: Environment,
) -> None:
    feeds_dir = build_dir / "feeds"
    feeds_dir.mkdir(parents=True, exist_ok=True)

    def render_feed(
        *,
        template: str,
        title: str,
        home_url: str,
        items: list[Post],
        source: str,
        medium: str,
        date_formatter,
        include_updated: bool,
        self_url: str | None = None,
    ) -> str:
        updated = (
            date_formatter(items[0].date)
            if items
            else date_formatter(datetime.now(UTC))
        )
        payload = {
            "title": title,
            "home_url": f"{config.base_url}{home_url}",
            "updated": updated,
            "items": [
                {
                    "title": post.title,
                    "link": f"{config.base_url}{post.url}?utm_source={source}&utm_medium={medium}",
                    "id": _make_urn(config.base_url, post.url),
                    "published": date_formatter(post.date),
                    "updated": date_formatter(post.date) if include_updated else "",
                    "author": config.author,
                    "content": post.content_html,
                }
                for post in items
            ],
        }
        if self_url:
            payload["self_url"] = f"{config.base_url}{self_url}"
            payload["feed_id"] = _make_urn(config.base_url, home_url)
        if template.endswith("rss.xml"):
            payload["description"] = title
        return _render_template(env, template, payload)

    feed_specs: list[dict[str, str | list[Post]]] = [
        {
            "key": "all",
            "title": f"{config.title}: {config.title}",
            "self_url": "/feeds/all.atom.xml",
            "home_url": "/index.html",
            "items": posts[: config.posts_in_rss],
            "source": "all",
        }
    ]
    for tag_slug, posts_for_tag in sorted(tag_map.items()):
        tag = tag_defs[tag_slug]
        feed_specs.append(
            {
                "key": tag.slug,
                "title": f"{config.title}: Posts tagged '{tag.name}'",
                "self_url": tag.atom_feed_url,
                "home_url": tag.url,
                "items": posts_for_tag[: config.posts_in_rss],
                "source": tag.slug,
            }
        )

    for spec in feed_specs:
        atom = render_feed(
            template="feeds/atom.xml",
            title=str(spec["title"]),
            self_url=str(spec["self_url"]),
            home_url=str(spec["home_url"]),
            items=spec["items"],  # type: ignore[arg-type]
            source=str(spec["source"]),
            medium="Atom",
            date_formatter=format_atom_date,
            include_updated=True,
        )
        rss = render_feed(
            template="feeds/rss.xml",
            title=str(spec["title"]),
            home_url=str(spec["home_url"]),
            items=spec["items"],  # type: ignore[arg-type]
            source=str(spec["source"]),
            medium="RSS",
            date_formatter=format_rss_date,
            include_updated=False,
        )
        (feeds_dir / f"{spec['key']}.atom.xml").write_text(atom, encoding="utf-8")
        (feeds_dir / f"{spec['key']}.rss.xml").write_text(rss, encoding="utf-8")


def _build_sitemap(build_dir: Path, config: BlogConfig, posts: list[Post], pages: list[dict[str, Any]]) -> None:
    urls = [f"{config.base_url}{post.url}" for post in posts]
    for page in pages:
        urls.append(f"{config.base_url}/{page['slug']}.html")
    sitemap_text = "\n".join(urls)
    (build_dir / "sitemap.txt").write_text(sitemap_text, encoding="utf-8")
