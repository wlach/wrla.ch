---
tags: ["TIL", "uv", "Python"]
---

# `uv run` isn't always what you want

Like many others, I've joined the cult of [uv]. One superpower is that you no longer really need to think of activating a virtual environment in a project managed with this tool, `uv run path/to/script.py` will do the right thing.
You don't have to think about whether the virtual environment exists or is up to date, uv takes care of that under the hood and then runs your script inside the environment.

This is _great_ for local development but isn't generally what you want if:

1. You're running a service inside a docker container and the virtual environment is already created (you ideally shouldn't even have uv installed)
2. You've created a standalone tool with a virtualenv and just want to run it by itself (and not develop it).

For these cases, generally either set your path to include the virtual environment created by uv (`/prefix/.venv/bin`) or just run the script directly (`/prefix/.venv/bin/script.py`). `uv run` has startup overhead and inside a docker container, you also don't _want_ to dynamically download a bunch of new things: you just want to use
what you already created.

tl;dr: `uv run` is for development. Just execute the actual script in production.

[uv]: https://docs.astral.sh/uv
