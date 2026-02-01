from __future__ import annotations

import tomllib
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class BlogConfig:
    title: str
    author: str
    base_url: str
    posts_per_page: int
    posts_in_rss: int


def load_config(root: Path) -> BlogConfig:
    config_path = root / "pyproject.toml"
    data = tomllib.loads(config_path.read_text(encoding="utf-8"))
    tool = data.get("tool", {}).get("blog", {})
    if not tool:
        raise RuntimeError("Missing [tool.blog] configuration in pyproject.toml")  # noqa: TRY003
    return BlogConfig(
        title=tool["title"],
        author=tool["author"],
        base_url=tool["base_url"].rstrip("/"),
        posts_per_page=int(tool["posts_per_page"]),
        posts_in_rss=int(tool["posts_in_rss"]),
    )


def find_project_root(start: Path) -> Path:
    current = start.resolve()
    while True:
        if (current / "pyproject.toml").exists():
            return current
        if current.parent == current:
            raise RuntimeError("Could not find pyproject.toml in parent directories")  # noqa: TRY003
        current = current.parent
