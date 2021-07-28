    Title: Irydium @ Recurse Updates
    Date: 2021-07-28T15:16:42
    Tags: Irydium, Recurse

Some quick updates on where [Irydium] is at, roughly a week-and-a-half before my mini-sabbatical at the [Recurse Centre] ends.

## JupyterBook and MyST

I'd been admiring [JupyterBook] from afar for some time: their project philosophy appealed to me greatly.
In particular, the [MyST extensions] to markdown seemed like a natural fit for this project and a natural point of collaboration and cross-pollination.
A couple of weeks ago, I finally got in touch with some people working on that project, which prompted a few small efforts:

- [Adding Svelte support to VSCode's MyST Plugin](https://github.com/executablebooks/myst-vs-code/pull/32), which in turn prompted me to figure out [why the VSCode plugin for Svelte doesn't render inline content correctly](https://github.com/sveltejs/language-tools/issues/1094) (tl;dr: probably a bug in VSCode?)
- [Adding support for a couple of MyST's built-in directives](https://irydium.dev/examples#myst-directives) ("warning" and "note").

[![](https://i.imgur.com/A24e302.png)](https://irydium.dev/examples#myst-directives)

I've become convinced that building on top of MyST is right for both Irydium and the larger community. Increasing Irydium's support for MyST is tracked in [irydium/irydium#123].

## Using Irydium to build Irydium

I've been spending a fair bit of time thinking of how to ma ke it easier for people to build Irydium documents through _composition_ of existing documents.
Landed the first pieces of this.
The first is the ability to "import" a code chunk from another irydium document. There's a few examples of this in the new [components section](https://irydium.dev/components) of irydium.dev:

![](https://i.imgur.com/y4qNTj6.png)

In a sense this allows you to define a reusable piece of code along with both documentation and usage examples.
I think this concept will be particularly useful for supporting language plugins (which I will write about in an upcoming post).

## It's a real project now

I spent a bit of time last week doing some community gardening.
I still consider Irydium an "experiment" but I'd like to at least open up the possibility of it being something larger.
To help make that happen, I started working on some basic project governance pieces, namely:

- We have a [code of conduct](https://github.com/irydium/irydium/blob/main/CODE_OF_CONDUCT.md) and [contributing guidelines](https://github.com/irydium/irydium/blob/main/CONTRIBUTING.md). I opted to go for the Contributor Covenant, which seems to be a good minimal viable social contract. I considered something proposing something more comprehensive (like the [Rust Code of Conduct]), but I felt that's something for a _group_ of people to discuss and debate, should the time come where Irydium is more than a one-person show. For now, I'll do my best to make sure that everyone in Irydium's orbit has a good experience.
- There's a proper issues list, including some "good first bugs" for people to look at (shout out to [@m-clare](https://github.com/m-clare/) for submitting the first PR to Irydium!)
- We have a [channel on gitter](https://gitter.im/irydium/community), also accessible [via Matrix](https://matrix.to/#/#irydium_community:gitter.im). Come say hi!

## Next steps

There's not a ton of time left at RC, so some of these things may have to be done in my spare time after the batch ends.
That said, here's my near-term roadmap:

- Add support for code chunks to output content directly to the DOM (currently the only way to output to an Irydium document is through a Svelte component). This will be particularly important for Python support, where people expect the output of a cell running [altair](https://github.com/altair-viz) or [matplotlib](https://github.com/matplotlib/matplotlib/) to display directly in the document (as they do in Jupyter). Tracked in [irydium/irydium#122].
- Integrate [ellx.io]'s next-generation JavaScript bundler, [tokamak]. This should make building irydium documents much more robust and error proof and paves the way to further improvements. Special shout-out to the ellx developers for being so friendly and open to collaboration: ellx is a novel approach to application development and definitely worth checking out if you haven't already. Tracked in [irydium/irydium#125].
- Finish and document support for language plugins (and make another blog post especially about them, they're cool!). Tracked in [irydium/irydium#144].

[irydium]: https://irydium.dev
[recurse centre]: https://recurse.com
[jupyterbook]: https://jupyterbook.org
[myst extensions]: https://myst-parser.readthedocs.io/
[rust code of conduct]: https://www.rust-lang.org/policies/code-of-conduct
[irydium/irydium#122]: https://github.com/irydium/irydium/issues/122
[irydium/irydium#123]: https://github.com/irydium/irydium/issues/123
[irydium/irydium#125]: https://github.com/irydium/irydium/issues/125
[irydium/irydium#144]: https://github.com/irydium/irydium/issues/144
[ellx.io]: https://ellx.io/
[tokamak]: https://github.com/dmaevsky/tokamak
