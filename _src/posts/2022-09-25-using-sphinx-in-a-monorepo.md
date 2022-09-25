    Title: Using Sphinx in a Monorepo
    Date: 2022-09-25T15:55:40
    Tags: Sphinx, Documentation, Voltus, Mozilla

Just wanted to type up a couple of notes about working with [Sphinx] (the python documentation generator) inside a monorepo,
an issue I've been struggling with (off and on) at [Voltus] since I started.
I haven't seen much written about this topic despite (I suspect) it being a reasonably frequent problem.

In general, there's a lot to like about Sphinx: it's great at handling deeply nested trees of detailed documentation with cross-references inside a version control system.
It has local search that works pretty well and some themes (like [readthedocs]) scale pretty nicely to hundreds of documents.
The directives and roles system is pretty flexible and covers most of the common things one might want to express in technical documentation.
And if the built-in set of functionality isn't enough, there's a wealth of third party extension modules.
My only major complaint is that it uses the somewhat obscure [restructuredText] file format by default, but you can get around that by using the excellent [MyST extension].

Unfortunately, it has a pretty deeply baked in assumption that all documentation for your project lives inside a _single_ subfolder.
This is fine for a small repository representing a single python module, like this:

```
<root>
README.md
setup.cfg
pyproject.toml
mymodule/
docs/
```

However, this doesn't work for a large monorepo, where you would typically see something like:

```
<root>/module-1/submodule-a
<root>/module-1/submodule-b
<root>/module-2/submodule-c
...
```

In a monorepo, you usually want to include a module's documentation inside its own directory.
This allows you to use your [code ownership constraints] for documentation, among other things.

The naive solution would be to create a sphinx site for every single one of these submodules.
This is what happened at Voltus and I don't recommend it.
For a large monorepo you'll end up with dozens, maybe hundreds of documentation "sites".
Under this scenario, discoverability becomes a huge problem: no longer can you rely on tables of contents and the built-in search to discover content: you just have to "know" where things live.
I'm more than nine months in here and I'm _still_ discovering new documentation.

It would be much better if we could somehow collect documentation from other parts of the repository into a single site.
Is this possible?
tl;dr: Yes.
There's a few solutions, each with their pros and cons.

[sphinx]: https://www.sphinx-doc.org/en/master/
[readthedocs]: https://sphinx-rtd-theme.readthedocs.io/en/stable/
[restructuredtext]: https://docutils.sourceforge.io/rst.html
[myst extension]: https://myst-parser.readthedocs.io/en/latest/
[code ownership constraints]: https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/about-code-owners
[voltus]: https://voltus.co

## The obvious solution that doesn't work

The most obvious solution here is to create a symbolic link inside your documentation directory, say the following:

```
<root>/docs/
<root>/docs/module-1/submodule-a -> <root>/module-1/submodule-a/docs
```

Unfortunately, [this doesn't work](https://stackoverflow.com/questions/10199233/can-sphinx-link-to-documents-that-are-not-located-in-directories-below-the-root). ☹️ Sphinx doesn't follow symbolic links.

## Solution 1: Just copy the files in

The most obvious solution is to just copy the files from various parts of the monorepo into place, as part of the build system.
Mozilla did this for Firefox, with the [moztreedocs](https://searchfox.org/mozilla-central/source/tools/moztreedocs/__init__.py)
system.

The [results look pretty good](https://firefox-source-docs.mozilla.org/), but this is a bespoke solution.
Aside from general ideas, there's no way I'm going to be able to apply anything in moztreedocs to Voltus's monorepo (which is based on a completely different build system).
And being honest, I'm not sure if the 40+ hour (estimated) effort to reimplement it would be a good use of time compared to other things I could be doing.

## Solution 2: Use the include directive with MyST

Later versions of MyST include support for [directly importing a markdown file from another part of the repository](https://myst-parser.readthedocs.io/en/latest/faq/index.html#include-a-file-from-outside-the-docs-folder-like-readme-md).

This is a limited form of embedding: it won't let you import an entire directory of markdown files.
But if your submodules mostly just include content in the form of a `README.md` (or similar), it might just be enough.
Just create a directory for these files to live (say `services`) and slot them in:

`<root>/docs/services/module-1/submodule-a/index.md`:

    ```{include} ../../../module-1/submodule-a/README.md
    ```

I'm currently in the process of implementing this solution inside Voltus.
I have optimism that this will be a big (if incremental) step up over what we have right now.
There are obviously limits, but you can cram a lot of useful information in a README.
As a bonus, it's a pretty nice marker for those spelunking through the source code
(much more so than a forest of tiny documentation files).

## Solution 3: Sphinx Collections

This one I just found about today: [Sphinx Collections](https://sphinx-collections.readthedocs.io) is a small python module that lets you automatically import entire _directories_ of files into your sphinx tree, under a `_collections` module. You configure it in your top-level `conf.py` like this:

```py
extensions = [
    ...
    "sphinxcontrib.collections"
]

collections = {
    "submodule-a": {
        "driver": "symlink",
        "source": "/monorepo/module-1/submodule-a/docs",
        "target": "submodule-a"
    },
    ...
}
```

After setting this up, `submodule-a` is now available under `_collections` and you can include it in your table of contents like this:

    ...

    ```{toctree}
    :caption: submodule-a

    _collections/submodule-a/index.md
    ```

    ...

At this point, `submodule-a`'s documentation should be available under `http://<my doc domain>/_collections/submodule-a/index.html`

Pretty nifty. The main downside I've found so far is that this doesn't play nicely with the [Edit on GitHub] links that the readthedocs theme automatically inserts (it thinks the files exist under `_collections`), but there's probably a way to work around that.

I plan on investigating this approach further in the coming months.

[edit on github]: https://docs.readthedocs.io/en/stable/guides/edit-source-links-sphinx.html
