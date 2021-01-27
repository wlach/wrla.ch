    Title: The Glean Dictionary
    Date: 2021-01-27T08:53:44
    Tags: Mozilla, Glean

_(“This Week in Glean” is a series of blog posts that the Glean Team at Mozilla is using to try to communicate better about our work. They could be release notes, documentation, hopes, dreams, or whatever: so long as it is inspired by Glean. You can find [an index of all TWiG posts online.](https://mozilla.github.io/glean/book/appendix/twig.html))_

On behalf of Mozilla's Data group, I'm happy to announce the availability of the first milestone of the Glean Dictionary, a project to provide a comprehensive "data dictionary" of the data Mozilla collects inside its products and how it makes use of it. You can access it via this development URL:

[https://dictionary.protosaur.dev/](https://dictionary.protosaur.dev/)

![](/files/2021/01/glean-dictionary.png)

The goal of this first milestone was to provide an equivalent to the [popular "probe" dictionary](https://probes.telemetry.mozilla.org) for newer applications which use the Glean SDK, such as Firefox for Android. As Firefox on Glean (FoG) comes together, this will also serve as an index of what data is available for Firefox and how to access it.

Part of the vision of this project is to act as a showcase for Mozilla's practices around [lean data](https://www.mozilla.org/en-US/about/policy/lean-data/) and [data governance](https://wiki.mozilla.org/Firefox/Data_Collection): you'll note that every metric and ping in the Glean Dictionary has a data review associated with it -- giving the general public a window into what we're collecting and why.

In addition to displaying a browsable inventory of the low-level metrics which these applications collect, the Glean Dictionary also provides:

- Code search functionality (via [Searchfox](https://searchfox.org)) to see where any given data collection is defined and used.
- Information on how this information is represented inside Mozilla's BigQuery data store.
- Where available, links to browse / view this information using the [Glean Aggregated Metrics Dashboard](https://glam.telemetry.mozilla.org) (GLAM).

Over the next few months, we'll be expanding the Glean Dictionary to include derived datasets and dashboards / reports built using this data, as well as allow users to add their own annotations on metric behaviour via a GitHub-based documentation system. For more information, see the [project proposal](https://docs.google.com/document/d/1OkTWA3rsSJ0m5g9GDnxXVUMkJP-xJMQk_bDgDq-Z9xM/edit#).

The Glean Dictionary is the result of the efforts of many contributors, both inside and outside Mozilla Data. Special shout-out to [Linh Nguyen](https://www.linh-nguyen.com/outreachy), who has been moving mountains inside the codebase as part of an Outreachy internship with us. We welcome your feedback and involvement! For more information, see our [project repository](https://github.com/mozilla/glean-dictionary) and Matrix channel ([#glean-dictionary on chat.mozilla.org](https://chat.mozilla.org/#/room/#glean-dictionary:mozilla.org)).
