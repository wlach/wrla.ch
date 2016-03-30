    Title: Are We Fast Yet and Perfherder
    Date: 2016-03-30T11:42:39
    Tags: Mozilla, Perfherder

Historically at Mozilla, we've had a bunch of different systems
running to benchmark Firefox's performance. The two most
broadly-scoped are [Talos](https://wiki.mozilla.org/Buildbot/Talos) (which runs as part of our build process,
and emphasizes common real-world use cases, like page loading) and
[Are We Fast Yet](https://arewefastyet.com/) (which runs seperately, and emphasizes JavaScript
performance and benchmarks).

As many of you know, most of my focus over the last year-and-a-bit
has been developing a system called Perfherder, which aims to make
monitoring and acting on performance data easier. A great introduction
to Perfherder is my [project of the month post](/blog/2016/03/platform-engineering-project-of-the-month-perfherder/).

The initial focus of Perfherder has been Talos, which is deeply
integrated into our automation and also maintained by Engineering
Productivity (my group). However, the intention was always to allow anyone in the Mozilla community to
submit performance data for Firefox and sheriff it, much like
Treeherder has supported the submission of test result data from
third parties (e.g. autophone, Firefox UI tests). There are more
commonalities than differences in how we do performance sheriffing
with Are We Fast Yet (which currently has its own web interface) and
Perfherder, so it made sense to see if we could pool resources.

So, over the last couple of months, [Joel Maher](https://elvis314.wordpress.com/) and I have been in discussions with
Hannes Verschore, current maintainer of Are We Fast Yet (AWFY) to see what could be done.
It looks like it is possible for Perfherder to provide most of what AWFY needs,
though there are a few exceptions. I thought for the benefit of others,
it might be useful to outline what's done, what's coming next, and what
might not be implemented (at least not any time soon).

### What's done

* Get AWFY submitting data to Perfherder and allow it to be sheriffed
  seperately from Talos. This is working on treeherder stage, and you
  can already examine the [alert data](https://treeherder.allizom.org/perf.html#/alerts?status=0&framework=5).

### What's in progress (or in the near-term pipeline)

* Allow custom alerting behaviour ([bug 1254595](https://bugzilla.mozilla.org/show_bug.cgi?id=1254595)). For example, we want
  to alert on subtests for AWFY while still summarizing the results.
  This is something we don't currently support.
* Allow creating an alert manually ([bug 1260791](https://bugzilla.mozilla.org/show_bug.cgi?id=1260791)). Sadly, our regression detection
  algorithm is not perfect. AWFY already supports this, we should too. This is something we also want for Talos.
* Make regression-filing templates non-talos-specific ([bug 1260805](https://bugzilla.mozilla.org/show_bug.cgi?id=1260805)). Currently we have a convenience template for filing bugs for performance
  regressions, but this is currently specific to various things about Talos (job running instructions, links to documentation, etc.). We should
  make it configurable so other projects like AWFY can take advantage of this functionality.

### Under consideration

* Some kind of support for bisecting a push to figure out which patch
  caused a regression. AWFY currently supports this, but it's a fairly
  difficult thing to add to Perfherder (much of which is built upon
  Treeherder's per-push result model). Maybe this is something we should
  do, but it would be a significant amount of effort.
* Proprietary benchmarks: AWFY runs one benchmark the results for
  which we can't make public. Adding "private" jobs or results to
  Treeherder is likely a big can of worms, but it might be something
  we want to do eventually.

### Probably won't fix

* Supporting comparative measurements between Firefox and other
  browsers. This is an important task, but doesn't really fit into the
  model of Perfherder, which is intimately tied to the revision data
  associated with Firefox. To do this would require detailed tracking
  of Chrome on the same basis, and I don't think that's really a place
  where we want to go. We should definitely monitor for general
  trends, but I think that is best done with a seperate system.
