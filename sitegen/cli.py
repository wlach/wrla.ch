from __future__ import annotations

import http.server
import os
import socketserver
from datetime import datetime
from pathlib import Path

import typer
from slugify import slugify

from .config import find_project_root
from .config import load_config
from .site import build_site

app = typer.Typer(add_completion=False)


@app.command("new-post")
def new_post(title: str) -> None:
    """Create a new post in src/posts."""
    root = find_project_root(Path.cwd())
    posts_dir = root / "src" / "posts"
    posts_dir.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    slug = slugify(title)
    dir_path = posts_dir / f"{timestamp}-{slug}"
    path = dir_path / "index.md"
    if dir_path.exists():
        raise typer.Exit(code=1)
    dir_path.mkdir(parents=True)
    template = f"""---
tags: []
---

# {title}

"""
    path.write_text(template, encoding="utf-8")
    typer.echo(f"Created {path}")


@app.command()
def build() -> None:
    """Build the site into _build/."""
    root = find_project_root(Path.cwd())
    config = load_config(root)
    build_site(root, config)
    typer.echo("Build complete: _build/")


@app.command()
def preview(port: int = 5000) -> None:
    """Build and serve the site from _build/."""
    root = find_project_root(Path.cwd())
    config = load_config(root)
    build_site(root, config)
    build_dir = root / "_build"
    os.chdir(build_dir)
    handler = http.server.SimpleHTTPRequestHandler
    class ReusableTCPServer(socketserver.TCPServer):
        allow_reuse_address = True

    with ReusableTCPServer(("", port), handler) as httpd:
        typer.echo(f"Serving on http://localhost:{port}")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            typer.echo("Stopping server.")
