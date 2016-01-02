    Title: New year, new blog
    Date: 2016-01-02T13:06:55
    Tags: Meta

After thinking about doing it for longer than I'd like to admit, I finally bit the bullet
and decided to migrate away from WordPress, towards a markdown-based
blog generator ([Frog](https://github.com/greghendershott/frog) in this case).
All the content from the old blog is coming with me (thanks mostly to WordPress's
jekyll exporter plugin).

While WordPress is a pretty impressive piece of software, it isn't the ideal
platform for the sorts of things I want to
express. It's a reasonable tool for publishing straight longform essays, but my
more interesting posts tend to also include images, code and examples, and
sometimes [even math](/blog/2014/03/it-8217-s-all-about-the-entropy/). Making those look reasonable involved a
bunch of manual effort and the end result wasn't particularly great. I
was particularly disappointed in its (lack of) support for inline code snippits.

Perhaps this set of problems is resolvable by installing the right set
of plugins. Perhaps. But therein lies my second problem with
WordPress: it's big, complex piece of software written in PHP, and I'm
frankly tired of figuring out how to (barely) make it do the things I
need it to do, while half-worrying that the new fancy WPAwesome plugin
I'm installing is malware.

As I've grown older, I'm increasingly realizing the limits to what I
have the time (and energy) to accomplish. While "Making WordPress do
the things I want" is something I *could* continue working on, it would come at the expense of
other things that I find more rewarding, whether that be meditating,
[brushing up on deep learning](http://neuralnetworksanddeeplearning.com/), or even just
writing more stuff here. I don't expect this new blog to be maintenance free, but it should be an order of
magnitude simpler using Frog, which is narrowly focused on my
rather technical use case and specifically has great support for inline code, images,
and math.

Along the same lines, I'm completely tired of maintaining the Linux
server that my blog ran on. Registering domains and setting up my own
HTTP server seemed like an interesting diversion in 2009, when cheap
Linux VPSes were first starting to appear on the market. These days... well, not so
much. It's a minor, though not completely trivial, expense ($10 USD/mo.)
but more importantly it's a sink of my time to install security
patches, make sure things are to up to date, etc. It feels like I'm
solving the same (boring) set of problems over and over, with no real
payoff. Time to move on.

Thus, this blog (along with my other hosted projects, like [NIXI](http://nixi.ca) and
[meditation](meditation.wrla.ch)) will be moving to [github
pages](https://pages.github.com/). Initially I had the worry that this move would mean that I wouldn't be "in control of my
own destiny", but on reflection I don't think that's true. The fact
that my blog is basically a giant git repository should make switching
hosting providers quite easy if Github becomes unsatisfactory for
whatever reason.

Indeed, even the custom domain (wrla.ch) seems unnecessary at this
point. Although github pages does support them, I'm just not
seeing the value in keeping it around. What purpose does it *really*
serve? All a custom personal domain really says to me is that the
person had the time/money to register it. Is that something that
someone in my position really needs to communicate? And if I don't
need it, why continue with the unnecessary expense and hassle?

Perhaps the only legitimate reason to keep the domain  would be continuity for
readers (i.e. there's a link or two in their browser history), but I
don't think that's a big deal in my case. Yes, people might
occasionally be thrown off and have to use Yahoo/Google to re-find
something... but for the type of content I host, I don't think that will take too much
collective time. In the grand stream of things, I'm pretty small
potatoes. Most of my traffic just comes through planet.mozilla.org,
and that's easy to redirect automatically.

So though I'll be keeping around wrla.ch for a little bit to give people time to
migrate their links (it doesn't expire until the end of February
2016), it will also be going away. Please redirect your feed readers to
[wlach.github.io](https://wlach.github.io).

Now, onto more interesting things!