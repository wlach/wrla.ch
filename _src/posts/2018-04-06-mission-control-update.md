    Title: Mission Control update
    Date: 2018-04-06T14:46:43
    Tags: Mozilla, Mission Control

Yep, still working on this project. We've shifted gears somewhat from trying to
identify problems in a time series of error aggregates to tracking somewhat longer
term trends release over release, to fill the needs of the release management team
at Mozilla. It's been a good change, I think. A bit of a tighter focus.

The main motivator for this work is that the ADI (active daily install)
numbers that crash stats used to provide as input to a similar service,
[AreWeStableYet](https://arewestableyet.com) (link requires Mozilla
credentials), are going away and we need some kind of replacement. I've been
learning about this older system worked (this [blog
post](https://home.kairo.at/blog/2014-04/how_effective_is_the_stability_program)
from KaiRo was helpful) and trying to develop a replacement which reproduces
some of its useful characteristics while also taking advantage of some of the
new features that are provided by the
[error_aggregates](https://docs.telemetry.mozilla.org/datasets/streaming/error_aggregates/reference.html)
dataset and the mission control user interface.

Some preliminary screenshots of what I've been able to come up with:

<center>
  <img style="width:400px" srcset="/files/2018/04/missioncontrol-main-view.png 2x"/>
  <img style="width:400px" srcset="/files/2018/04/missioncontrol-windows-release.png 2x"/>
</center>

One of the key things to keep in mind with this dashboard is that by default
it shows an *adjusted* set of rates (defined as total number of events divided by total usage khours), which
means we compare the latest release to the previous one within the same time interval.

So if, say, the latest release is "59" and it's been out for two weeks, we will
compare it against the previous release ("58") in its first two weeks. As I've said
here before, things are [always crashier when they first go out](/blog/2017/10/better-or-worse-by-what-measure), and comparing
a new release to one that has been out in the field for some time is not a fair
comparison at all.

This adjusted view of things is still not apples-to-apples: the causality
of crashes and errors is so complex that there will always be differences between
releases which are beyond our control or even understanding. Many crash reports,
for example, have nothing to do with our product but with third party software and
web sites beyond our control. That said, I feel like this adjusted rate is still good
enough to tell us (broadly speaking) (1) whether our latest release / beta / nightly
is ok (i.e. there is no major showstopper issue) and (2) whether our overall error
rate is going up or down over several versions (if there is a continual increase
in our crash rate, it might point to a problem in our release/qa process).

Interestingly, the first things that we've found with this system are not real problems
with the product but data collection issues:

* [we don't seem to be collecting counts of gmplugin crashes on Windows anymore via telemetry](https://bugzilla.mozilla.org/show_bug.cgi?id=1447161)
* [the number of content_shutdown_crashes is greater than the number of content_crashes, even though the former is a superset of the latter](https://bugzilla.mozilla.org/show_bug.cgi?id=1413172#c8)

Data issues aside, the indications are that there's been a steady increase
in the quality of Firefox over the last few releases based on the main user facing
error metric we've cared about in the past (main crashes), so that's good. :)

If you want to play with the system yourself, the [development instance](https://data-missioncontrol.dev.mozaws.net/) is still up. We will probably look at making this thing
"official" next quarter.
