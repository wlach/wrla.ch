    Title: Glean Dictionary updates
    Date: 2021-06-02T12:01:52
    Tags: Mozilla, Glean

([this is a cross-post from the data blog](https://blog.mozilla.org/data/2021/06/02/this-week-in-glean-glean-dictionary-updates/))

Lots of progress on the Glean Dictionary since I made the initial release announcement a couple of months ago. For those coming in late, the Glean Dictionary is intended to be a [data dictionary](https://en.wikipedia.org/wiki/Data_dictionary) for applications built using the [Glean SDK](https://mozilla.github.io/glean) and [Glean.js](https://github.com/mozilla/glean.js/). This currently includes Firefox for Android and Firefox iOS, as well as newer initiatives like [Rally](https://rally.mozilla.org). Desktop Firefox _will_ use Glean in the future, see [Firefox on Glean (FoG)](https://firefox-source-docs.mozilla.org/toolkit/components/glean/index.html).

## Production URL

We're in production! You can now access the Glean Dictionary at [dictionary.telemetry.mozilla.org](https://dictionary.telemetry.mozilla.org). The old protosaur-based URL will redirect.

## Glean Dictionary + Looker = ❤️

At the end of last year, Mozilla chose [Looker](https://looker.com) as our internal business intelligence tool. Frank Bertsch, Daniel Thorn, Anthony Miyaguchi and others have been building out first class support for Glean applications inside this platform, and we're starting to see these efforts bear fruit. Looker's explores are far easier to use for basic data questions, opening up data based inquiry to a much larger cross section of Mozilla.

I recorded a quick example of this integration here:

<iframe width="560" height="315" src="https://www.youtube.com/embed/B635wgZy7Iw" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>

Note that Looker access is restricted to Mozilla employees and NDA'd volunteers. Stay tuned for [more public data](https://docs.telemetry.mozilla.org/cookbooks/public_data.html) to be indexed inside the Glean Dictionary in the future.

## Glean annotations!

I did up the first cut of a GitHub-based system for adding annotations to metrics -- acting as a knowledge base for things data scientists and others have discovered about Glean Telemetry in the field. This can be _invaluable_ when doing new analysis. A good example of this is the annotation added for the [opened as default browser](https://dictionary.telemetry.mozilla.org/apps/firefox_ios/metrics/app_opened_as_default_browser) metric for Firefox for iOS, which has several gotchas:

![](/files/2021/06/annotations-example.png)

Many thanks to Krupa Raj and Leif Oines for producing the requirements which led up to this implementation, as well as their evangelism of this work more generally inside Mozilla. Last month, Leif and I did a presentation about this at Data Club, which has been syndicated onto YouTube:

<iframe width="560" height="315" src="https://www.youtube.com/embed/aGjrXhXNRq8" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>

Since then, we've had a very successful working session with some people Data Science and have started to fill out an initial set of annotations. You can see the progress in the [glean-annotations](https://github.com/mozilla/glean-annotations) repository.

## Other Improvements

Lots more miscellaneous improvements and fixes have gone into the Glean Dictionary in the last several months: see our [releases](https://github.com/mozilla/glean-dictionary/releases) for a full list. One thing that irrationally pleases me are the [new labels Linh Nguyen added last week](https://github.com/mozilla/glean-dictionary/pull/626): colorful and lively, they make it easy to see when a Glean Metric is coming from a library:

![](/files/2021/06/labels-example.png)

## Future work

The Glean Dictionary is just getting started! In the next couple of weeks, we're hoping to:

- Expand the Looker integration outlined above, as our deploy takes more shape.
- Work on adding "feature" classification to the Glean Dictionary, to make it easier for product managers and other non-engineering types to quickly find the metrics and other information they need without needing to fully understand what's in the source tree.
- Continue to refine the user interface of the Glean Dictionary as we get more feedback from people using it across Mozilla.

If you're interested in getting involved, join us! The Glean Dictionary is developed in the open using cutting edge front-end technologies like [Svelte](https://svelte.dev). Our conviction is that being transparent about the data Mozilla collects helps us build trust with our users and the community. We're a friendly group and hang out on the [#glean-dictionary channel](https://chat.mozilla.org/#/room/#glean-dictionary:mozilla.org) on Matrix.
