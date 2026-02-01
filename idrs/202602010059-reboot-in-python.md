# 2026-02-01: Reboot in Python

Owner: Will Lachance <wlach@protonmail.com>

## Overview

### Problem Statement

Create a new version of wrla.ch reflective of my new goals for 2026.

### Context (as needed)

At some point in the last 10 years, I moved from wordpress to using [frog], a static
site generator written in Racket.
It's a pretty reasonable static site generator, but in practice I've found it a pain to configure and maintain: this is the only time I've used Racket and realized the mechanics of this system are
simple enough that I'd prefer to just maintain something simple in my own language of choice (Python).
Incidentally, this is basically what Frog's creator recommends now:

> Eventually I felt even that was too complicated, and my own blog should simply be a Makefile driving a few pieces of code inherited from Frog. In other words, I no longer use Frog for my own blog.

### Goals

- Recreate core frog functionality (new blog entry, preview blog, publish blog as static site)
- Preserve exact file generation semantics so that people don't need to update their RSS feeds
- Preserve look and feel for site (no major changes)
- Use a language (Python) that I'm familiar with
- Keep things as simple as possible

### Non-Goals

- Create a "blog framework" of any kind, the tooling need only work for this site
- Port existing content over (as a seperate effort, we'll fork the old version and publish it as https://archive-pre-2026.wrla.ch, with redirects for any existing pages)
- Create / update continuous integration
- Handle particulars of hosting (e.g. generating a 404.html page for Cloudflare)

### Proposed Solution

Create a standard python project using uv. Add a command-line tool using [typer] which can:

- Create a new blog entry (in the style of existing entries) as a markdown file
- Preview the entire site via a static host (use Python's built-in `http.server`)
- Publish the site

As before, keep all content and templates in a source directory. But we'll rename it from `_src` to `src` (which also helps us distinguish it from the old content)

The format of entries should be _nearly_ the same as before, except we'll use standard markdown frontmatter.
So a typical entry might be:

```md
---
tags: Music
---

# Rethinking music listening

On this day in 2026, I canceled my Spotify subscription.
This was a long time coming, but what finally pushed me over the edge was listening to this podcast on streaming services a couple weeks ago:

...
```

Note there is no title entry in the frontmatter. It should be inferred from the content. All entries _must_ have a title block like `# <title>`. Additionally all headers should increment successively: exit with a parse error if this isn't the case. Tags are optional and are not case sensitive (i.e. `Music` becomes `music`)

There is no date. Posts live in directories and are created as: `src/posts/YYYYMMDDHHMMSS-title-slug/index.md` (note this is slightly different from the previous format)

Another contrast with the previous approach is that we should no longer check the generated files into Git. Generated content will go to a `_build` directory for deployment to a service like Cloudflare Pages.

For parsing and generating HTML from the markdown files, use [markdown-it-py]. For templating needs, use [jinja](https://jinja.palletsprojects.com/en/stable/).
For now we will continue to use tailwind to generate the
site CSS. We will check in its output, so no need to make it part of the build process.

Frog allows browsing a view of all entries, or by tag using pagination (configurable limit per page, let's go with 10).

In addition to the blog, we want to have one static page "about" linked from the header. This will just be a markdown page rendered at `/about.html` using the same
template as the rest of the site. The header will be static for now, but keep the mechanism for generating static pages general in case we want to create more in the future.

All template content should go into `src` as well,
under the appropriate directory (e.g. `src/css`).

Static files are stored in `files/`, indexed by date as is done previously.

Generate a sitemap.txt in `_build` based on generated content. Should have the same format as the old one:

```
https://wrla.ch/blog/2012/03/eideticker-dashboard-update/
https://wrla.ch/blog/2014/06/managing-test-manifests-manifestdestiny-manifestparser/
```

**Important**: Where there is ambiguity in requirements, use the existing site (files in `blog/`, `feeds/`, `css/`, etc.) as the source of truth for behavior and formatting.

## Future plans (as needed)

- Extract out Python blog and necessary files into a _new_ site
- Actually deploy new site (planning Cloudflare pages)
- Create an archive-pre-2026 site, create redirects.

## Other reading (as needed)

- [frog]

[frog]: https://github.com/greghendershott/frog
[typer]: https://typer.tiangolo.com/
[markdown-it-py]: https://github.com/executablebooks/markdown-it-py

## Implementation (ephemeral)

**When implementation details are not specified below, reference existing site files to match structure and behavior.**

### File Structure and Naming

New blog entries created as: `src/posts/YYYYMMDDHHMMSS-title-slug/index.md`

Date is always from the filename. Generated output follows existing pattern:

- Blog post: `/blog/YYYY/MM/title-slug/index.html`
- Feeds: `/feeds/*.atom.xml` and `/feeds/*.rss.xml`
- Sitemap: `/sitemap.txt`

Note: this is _incompatible_ with the previous markdown format and file structure, which is fine.
Create a simple test post in `src/posts` to test the new generation system.

### Templates

Create in `src/templates/`:

- `post.html` - individual post page
- `index.html` - homepage/pagination pages
- `tag.html` - tag listing page

Use Jinja2 with variables like `{{ title }}`, `{{ content }}`, `{{ date }}`, `{{ tags }}`, etc.

### Command Line Interface

```bash
uv run site new-post "My Post Title"     # creates src/posts/YYYYMMDDHHMMSS-my-post-title/index.md
uv run site preview                      # builds to _build/, serves on localhost:5000
uv run site build                        # just builds to _build/
```

### RSS Feeds

Generate both `.atom.xml` and `.rss.xml` for:

- `all` (all posts, most recent based on configurable value)
- Each tag that exists (most recent N per tag based on config)

Sort by date descending. Use existing feed URLs to maintain compatibility.

### Static Assets

Copy as-is from `src` to `_build/`:

- `css/`
- `js/`
- `img/`
- `fonts/`
- `files/`

### Pagination

Generate `index.html`, `index-2.html`, etc. with 10 posts per page.

### Markdown Processing

Use markdown-it-py with:

- Syntax highlighting via `mdit-py-plugins` with pygments plugin (compatible with existing `css/pygments.css`)
- Standard extensions (tables, strikethrough, etc.)

Parse frontmatter for tags (optional). Title is always first `# ` line (required). Exit with error if no title or headers don't increment properly (h1 → h2 → h3, not h1 → h3).

### Site Configuration

Add to `pyproject.toml`:

```toml
[tool.blog]
title = "William Lachance's Log"
author = "William Lachance"
base_url = "https://wrla.ch"
posts_per_page = 10
posts_in_rss = 20
```

### Content Handling

New system only processes files in `src/`. Existing content in `blog/`, `feeds/`, etc. is for reference only and should be ignored during build.

### Publishing

`uv run site build` command generates complete site in `_build/`. Manual deployment to hosting service (Cloudflare Pages or similar).
