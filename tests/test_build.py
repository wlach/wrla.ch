from __future__ import annotations

import shutil
import tempfile
import unittest
from datetime import UTC
from datetime import datetime
from datetime import timedelta
from pathlib import Path

from sitegen.config import BlogConfig
from sitegen.site import build_site


class BuildSiteTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp_dir = tempfile.TemporaryDirectory()
        self.root = Path(self.temp_dir.name)
        (self.root / "src").mkdir(parents=True, exist_ok=True)
        self._copy_templates()
        self._write_posts(count=30, tag_count=15)

    def tearDown(self) -> None:
        self.temp_dir.cleanup()

    def _copy_templates(self) -> None:
        repo_root = Path(__file__).resolve().parents[1]
        source = repo_root / "src" / "templates"
        target = self.root / "src" / "templates"
        shutil.copytree(source, target)

    def _write_posts(self, count: int, tag_count: int) -> None:
        posts_dir = self.root / "src" / "posts"
        posts_dir.mkdir(parents=True, exist_ok=True)
        base = datetime(2026, 1, 1, tzinfo=UTC)
        for idx in range(count):
            timestamp = (base + timedelta(minutes=idx)).strftime("%Y%m%d%H%M%S")
            slug = f"post-{idx:02d}"
            tag = f"tag-{idx % tag_count:02d}"
            directory = posts_dir / f"{timestamp}-{slug}"
            directory.mkdir(parents=True, exist_ok=True)
            content = "\n".join(
                [
                    "---",
                    f"tags: [{tag}]",
                    "---",
                    "",
                    f"# Post {idx}",
                    "",
                    "Body text.",
                    "",
                    "## Section",
                    "",
                    "More text.",
                ]
            )
            (directory / "index.md").write_text(content, encoding="utf-8")

    def _config(self) -> BlogConfig:
        return BlogConfig(
            title="Test Blog",
            author="Test Author",
            base_url="https://example.com",
            posts_per_page=10,
            posts_in_rss=20,
            repo_url="https://example.com/repo",
        )

    def test_generates_paginated_indexes(self) -> None:
        build_site(self.root, self._config())
        build_dir = self.root / "_build"
        self.assertTrue((build_dir / "index.html").exists())
        self.assertTrue((build_dir / "index-2.html").exists())
        self.assertTrue((build_dir / "index-3.html").exists())
        self.assertFalse((build_dir / "index-4.html").exists())

    def test_generates_tag_pages(self) -> None:
        build_site(self.root, self._config())
        tags_dir = self.root / "_build" / "tags"
        self.assertTrue(tags_dir.exists())
        tag_pages = sorted(path.name for path in tags_dir.glob("*.html"))
        self.assertEqual(len(tag_pages), 15)
        self.assertIn("tag-00.html", tag_pages)
        self.assertIn("tag-14.html", tag_pages)

    def test_generates_posts(self) -> None:
        build_site(self.root, self._config())
        post_dir = self.root / "_build" / "log" / "2026" / "01" / "post-00"
        self.assertTrue((post_dir / "index.html").exists())
        html = (post_dir / "index.html").read_text(encoding="utf-8")
        self.assertIn("Source on GitHub", html)

    def test_generates_sitemap(self) -> None:
        build_site(self.root, self._config())
        sitemap = self.root / "_build" / "sitemap.txt"
        self.assertTrue(sitemap.exists())
        content = sitemap.read_text(encoding="utf-8").strip().splitlines()
        self.assertEqual(len(content), 30)

    def test_copies_post_images_and_rewrites_feed_urls(self) -> None:
        # Create a post with an image reference
        posts_dir = self.root / "src" / "posts"
        post_dir = posts_dir / "20260201120000-img-test"
        post_dir.mkdir(parents=True, exist_ok=True)
        (post_dir / "index.md").write_text(
            "---\ntags: [test]\n---\n\n# Image Test\n\n![photo](photo.jpg)\n",
            encoding="utf-8",
        )
        # Place a fake image file
        (post_dir / "photo.jpg").write_bytes(b"\xff\xd8fake")

        build_site(self.root, self._config())

        # Image should be copied to the output directory
        output_img = self.root / "_build" / "log" / "2026" / "02" / "img-test" / "photo.jpg"
        self.assertTrue(output_img.exists())
        self.assertEqual(output_img.read_bytes(), b"\xff\xd8fake")

        # Post HTML should use relative image src (unchanged)
        post_html = (self.root / "_build" / "log" / "2026" / "02" / "img-test" / "index.html").read_text(encoding="utf-8")
        self.assertIn('src="photo.jpg"', post_html)

        # Feed should use absolute post URL for the image (HTML-escaped in Atom)
        atom = (self.root / "_build" / "feeds" / "all.atom.xml").read_text(encoding="utf-8")
        self.assertIn("/log/2026/02/img-test/photo.jpg", atom)
        self.assertNotIn('src="photo.jpg"', atom)

        # Index page should also use absolute image paths
        index_html = (self.root / "_build" / "index.html").read_text(encoding="utf-8")
        self.assertIn('src="/log/2026/02/img-test/photo.jpg"', index_html)
        self.assertNotIn('src="photo.jpg"', index_html)

    def test_generates_page_source_link(self) -> None:
        pages_dir = self.root / "src" / "pages"
        pages_dir.mkdir(parents=True, exist_ok=True)
        (pages_dir / "about.md").write_text("# About\n\nHello.\n", encoding="utf-8")
        build_site(self.root, self._config())
        about_html = (self.root / "_build" / "about" / "index.html").read_text(encoding="utf-8")
        self.assertIn("Source on GitHub", about_html)
