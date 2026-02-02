from __future__ import annotations

import re
from datetime import UTC
from datetime import datetime
from html import escape as html_escape
from html import unescape as html_unescape
from typing import Any

from markdown_it import MarkdownIt
from pygments import highlight
from pygments.formatters import HtmlFormatter  # type: ignore[unresolved-import]
from pygments.lexers import TextLexer  # type: ignore[unresolved-import]
from pygments.lexers import get_lexer_by_name
from pygments.util import ClassNotFound

_TITLE_RE = re.compile(r"^#\s+(.+)$")


def extract_title(markdown_text: str) -> tuple[str, str]:
    for line in markdown_text.splitlines():
        if line.strip() == "":
            continue
        match = _TITLE_RE.match(line)
        if not match:
            raise ValueError("First non-empty line must be a '# ' title")  # noqa: TRY003
        title = match.group(1).strip()
        stripped = markdown_text.splitlines()
        for idx, original in enumerate(stripped):
            if original == line:
                remaining = "\n".join(stripped[idx + 1 :]).lstrip("\n")
                return title, remaining
        break
    raise ValueError("Missing title")  # noqa: TRY003


def validate_heading_sequence(markdown_text: str, md: MarkdownIt) -> None:
    tokens = md.parse(markdown_text)
    last_level = None
    for token in tokens:
        if token.type != "heading_open":
            continue
        level = int(token.tag[1:])
        if last_level is None:
            if level != 1:
                raise ValueError("First heading must be level 1")  # noqa: TRY003
            last_level = level
            continue
        if level > last_level + 1:
            raise ValueError("Heading levels must increment by one")  # noqa: TRY003
        last_level = level


def markdown_renderer() -> MarkdownIt:
    formatter = HtmlFormatter(cssclass="colorful")

    md = MarkdownIt("commonmark", {"html": True})
    md.enable("table")
    md.enable("strikethrough")

    def _fence_renderer(tokens, idx, _options, _env):
        token = tokens[idx]
        info = token.info.strip() if token.info else ""
        lang = info.split()[0] if info else ""
        try:
            lexer = get_lexer_by_name(lang) if lang else TextLexer()
        except ClassNotFound:
            lexer = TextLexer()
        highlighted = highlight(token.content, lexer, formatter)
        return f'<div class="brush: {lang}">{highlighted}</div>\n'

    md.renderer.rules["fence"] = _fence_renderer  # type: ignore[possibly-missing-attribute]
    return md


def normalize_tags(raw_tags: Any) -> list[str]:
    if raw_tags is None:
        return []
    if isinstance(raw_tags, str):
        tags = [tag.strip() for tag in raw_tags.split(",")]
    elif isinstance(raw_tags, list):
        tags = []
        for item in raw_tags:
            if item is None:
                continue
            tags.append(str(item).strip())
    else:
        tags = [str(raw_tags).strip()]
    return [tag.lower() for tag in tags if tag]


def strip_html(html: str) -> str:
    text = re.sub(r"<[^>]+>", " ", html)
    text = html_unescape(text)
    return re.sub(r"\s+", " ", text).strip()


def truncate_text(text: str, limit: int) -> str:
    if len(text) <= limit:
        return text
    return text[:limit] + "..."


def format_atom_date(dt: datetime) -> str:
    return dt.astimezone(UTC).strftime("%Y-%m-%dT%H:%M:%SZ")


def format_rss_date(dt: datetime) -> str:
    return dt.astimezone(UTC).strftime("%a, %d %b %Y %H:%M:%S UT")


def format_pretty_date(dt: datetime) -> str:
    months = [
        "January",
        "February",
        "March",
        "April",
        "May",
        "June",
        "July",
        "August",
        "September",
        "October",
        "November",
        "December",
    ]
    return f"{months[dt.month - 1]} {dt.day}, {dt.year}"


def escape_attr(text: str) -> str:
    return html_escape(text, quote=True)


def escape_xml(text: str) -> str:
    return html_escape(text, quote=False)
