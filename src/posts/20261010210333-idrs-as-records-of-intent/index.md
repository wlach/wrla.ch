---
tags: [idrs, recurse]
---

# IDRs as records of intent

![Beaver Pond](./beaver_pond.jpg)

In [](../20260816221529-writing-the-docs-2026-edition/index.md), I talked a little bit about [IDRs] (Implementation Decision Records, a pun on "Architecture Decision Records" which predate adoption of LLMs).

As a refresher, I created them to serve a couple purposes:

1. To get better output out of LLMs
2. To provide a durable record of a decision made during the implementation of a feature

I've realized that left to their own devices given a vague prompt, an LLM will often just try to fill one in with a textual description of what it planned to implement anyway.[^1]  This makes them pretty lossy as a record of intent (it's basically not much better than a diff, and arguably worse) and I'm somewhat skeptical it improves their output much (it might allow you to steer them towards a better outcome before too much code is written, in some cases).

A great example is this one, where I asked the agent to update [repo-parser] to use DuckDB for the intermediate representation:

[IDRs]: https://github.com/wlach/idr-tools
[repo-parser]: https://github.com/wlach/repo-parser

```md
# DuckDB serialization

Owner: Will Lachance <wlach@protonmail.com>

## Overview

### Problem Statement

repo-parser extracts metadata and structure from repositories into an in-memory `Resource` tree, but this ephemeral representation must be re-created for each consumer. We need a persistent, queryable serialization format that allows multiple tools to consume the extracted metadata without re-scanning the repository.

### Context

<very long winded, almost inscrutable LLM context>

...
```
[link](https://github.com/wlach/repo-parser/blob/main/idrs/202601030409-duckdb-serialization-and-interactive-ui-architecture.md)

The problem statement isn't horrible, but it's also rather vague.
I don't think it really gave the agent much of a goal aside from "use duckdb in some way" to replace some other mechanism.
I think the result was ok-ish, but I wonder a bit if the IDR had much value in that process.
It certainly doesn't help explain what the duckdb output of repo-parser is actually good for (a BM25 search index of a repository's contents, possibly TUI search tools).
And it's definitely not something I want to re-read later, I cringe looking at it now.

What I'm increasingly realizing is that for an IDR to be really effective it needs to keep returning to the **intent** and decisions taken to support it.
Without this, it's just a long-winded way of restating the diff in english.

I'm much happier with this one:

```md
# Publish to PyPI from GitHub Actions

Owner: Will Lachance <wlach@protonmail.com>

## Overview

### Problem Statement

repo-parser packages can only be published to PyPI manually, which is time consuming, error prone and less secure than doing so via GitHub actions.

### Context (as needed)

### Goals

- Make it easier to publish new releases
- Improve security

### Non-Goals

- Automate version bumping (will still entail a seperate commit to bump version)

### Proposed Solution

Use the idiomatic best practice way of doing this, using the official packaging guide:

https://packaging.python.org/en/latest/guides/publishing-package-distribution-releases-using-github-actions-ci-cd-workflows/

In general this means adding a new GitHub workflow which ties uploads to PyPI to new releases.

## Other reading (as needed)

- [Official Guide](https://packaging.python.org/en/latest/guides/publishing-package-distribution-releases-using-github-actions-ci-cd-workflows/)
- [Stamina's implementation](https://github.com/hynek/stamina/blob/b25d4bc359ff603496aafbb217ab82c5a43715a6/.github/workflows/pypi-package.yml) (likely best practice)
```

[link](https://github.com/wlach/repo-parser/blob/main/idrs/202512310404-publish-to-pypi-from-github-actions.md)

The problem statement describes the "itch" that made me want to perform the intervention.
The goals, non-goals and solution are short, punchy and explain the end result without getting into implementation details. When I go back and look at a repository later, **this** is the sort of thing I want to see. 
Bonus: when using an LLM it provides clearer guard-rails.
Every sentence does the work of steering behaviour towards the actual result I want to see, rather than being a set of instructions that it might misinterpret.
If I need more detail, I'll just look at the diff.

[^1]: They'll also do this if you ask them to create a commit message without strong guardrails
