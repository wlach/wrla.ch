    Title: mozregression update: python 3 edition
    Date: 2019-09-16T11:29:04
    Tags: Mozilla, mozregression

For those who are still wondering, yup, I am still maintaining
[mozregression](https://mozilla.github.io/mozregression/), though increasingly
reluctantly. Given how important this project is to the development of Firefox
(getting a regression window using mozregression is standard operating
procedure whenever a new bug is reported in Firefox), it feels like this
project is pretty vital, so I continue out of some sense of obligation -- but
really, someone more interested in Mozilla'a build, automation and testing
systems would be better suited to this task: over the past few years, my
interests/focus have shifted away from this area to building up Mozilla's data
storage and visualization platform.

This post will describe some of the things that have happened in the last year
and where I see the project going. My hope is to attract some new blood to add some
needed features to the project and maybe take on some of the maintainership duties.

## python 3

The most important update is that, as of today, the command-line version of
mozregression (v3.0.1) should work with python 3.5+.
[modernize](https://python-modernize.readthedocs.io/en/latest/) did most of
the work for us, though there were some unit tests that needed updating:
special thanks to [@gloomy-ghost](https://github.com/gloomy-ghost) for helping with that.

For now, we will continue to support python 2.7 in parallel, mainly because the GUI has not yet
been ported to python 3 (more on that later) and we have CI to make sure it doesn't break.

## other updates

The last year has mostly been one of maintenance. Thanks in particular to Ian
Moody (:kwan) for his work throughout the year -- including patches to adapt
mozregression support to our new updates policy and shippable
builds ([bug 1532412](https://bugzilla.mozilla.org/show_bug.cgi?id=1532412)), and Kartikaya
Gupta (:kats) for adding support for bisecting the GeckoView example app ([bug
1507225](https://bugzilla.mozilla.org/show_bug.cgi?id=1507225)).

## future work

There are a bunch of things I see us wanting to add or change with
mozregression over the next year or so. I might get to some of these if I have
some spare cycles, but probably best not to count on it:

* Port the mozregression GUI to Python 3 ([bug
  1581633](https://bugzilla.mozilla.org/show_bug.cgi?id=1581633)) As mentioned
  above, the command-line client works with python 3, but we have yet to port
  the [GUI](). We should do that. This probably also entails porting the GUI to
  use PyQT5 (which is pip-installable and thus much easier to integrate into a
  CI process), see [bug 1426766](https://bugzilla.mozilla.org/show_bug.cgi?id=1426766).
* Make self-contained GUI builds available for MacOS X ([bug
  1425105](https://bugzilla.mozilla.org/show_bug.cgi?id=1425105)) and Linux
  ([bug 1581643](https://bugzilla.mozilla.org/show_bug.cgi?id=1581643)).
* Improve our mechanism for producing a standalone version of the GUI in
  general. We've used [cx_Freeze](https://github.com/anthony-tuininga/cx_Freeze)
  which mostly works ok, but has a number of problems (e.g. it pulls in a bunch of unnecessary dependencies, which
  bloats the size of the installer). Upgrading the GUI to use python 3 may
  alleviate some of these issues, but it might be worth considering other
  options in this space, like Gregory Szorc's [pyoxidizer](https://github.com/indygreg/PyOxidizer).
* Add some kind of telemetry to mozregression to measure usage of this tool
  ([bug 1581647](https://bugzilla.mozilla.org/show_bug.cgi?id=1581647)).
  My anecdotal experience is that this tool is pretty invaluable for Firefox
  development and QA, but this is not immediately apparent to Mozilla's
  leadership and it's thus very difficult to convince people to spend their
  cycles on maintaining and improving this tool. Field data may help change
  that story.
* Supporting new Mozilla products which aren't built (entirely) out of mozilla-central,
  most especially Fenix ([bug 1556042](https://bugzilla.mozilla.org/show_bug.cgi?id=1556042))
  and Firefox Reality ([bug 1568488](https://bugzilla.mozilla.org/show_bug.cgi?id=1568488)).
  This is probably rather involved (mozregression has a big pile of assumptions about how
  the builds it pulls down are stored and organized) but that doesn't mean that
  this work isn't necessary.

If you're interested in working on any of the above, please feel free to dive
in on one of the above bugs. I can't offer formal mentorship, but am happy to
help out where I can.
