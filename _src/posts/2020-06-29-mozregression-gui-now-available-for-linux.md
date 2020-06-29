    Title: mozregression GUI: now available for Linux
    Date: 2020-06-29T16:39:06
    Tags: Mozilla, mozregression

Thanks to [@AnAverageHuman](https://github.com/AnAverageHuman), [mozregression](https://mozilla.github.io/mozregression) once again has an easy to use and install GUI version for Linux! This used to work a few years ago, but got broken with some changes in the mozregression-python2 era and didn't get resolved until now:

![](/files/2020/06/mozregression-on-linux.png)

This is an area where using telemetry in mozregression can help us measure the impact of a change like this: although Windows still dominates in terms of marketshare, Linux is very widely used by contributors -- of the usage of mozregression in the past 2 months, fully 30% of the sessions were on Linux (and it is possible we were undercounting that due to [bug 1646402](https://bugzilla.mozilla.org/show_bug.cgi?id=1646402)):

![](/files/2020/06/mozregression-usage-share-by-os.png)
[link to query](https://sql.telemetry.mozilla.org/queries/72363/source) (internal-only)

It will be interesting to watch the usage numbers for Linux evolve over the next few months. In particular, I'm curious to see what percentage of users on that platform prefer a GUI.

## Appendix: reducing mozregression-GUI's massive size

One thing that's bothered me a bunch lately is that the mozregression GUI's size is _massive_ and this is even more apparent on Linux, where the initial distribution of the GUI came in at over 120 megabytes! Why so big? There were a few reasons:

1. [PySide2](https://pypi.org/project/PySide2/) (the GUI library we use) is very large (10s of megabytes), and [PyInstaller](https://www.pyinstaller.org/) packages _all of it_ by default into your application distribution.
2. The binary/rust portions of the [Glean Python SDK](https://pypi.org/project/glean-sdk/) were been built with debugging information included (basically as a carry-over when it was a pre-alpha product), which made it 38 megabytes big (!) on Linux.
3. On Linux at least, a large number of other system libraries are packaged into the distribution.

A few aspects of this were under our control: Ian Moody (:Kwan) and myself crafted a script to manually remove unneeded PySide2 libraries as part of the packaging process. The Glean team was awesome-as-always and quickly rebuilt Glean without debugging information (this was basically an oversight). Finally, I managed to shave off a few more megabytes by reverting the Linux build to an earlier version of Ubuntu (Xenial), which is something I had been meaning to do anyway.

Even after doing all of these things, the end result is still a little underwhelming: the mozregression GUI distribution on Linux is still 79.5 megabytes big. There are probably other things we could do, but we're definitely entering the land of diminishing returns.

Honestly, my main takeaway is just not to build an application like this in Python unless you absolutely have to (e.g. you're building an application which needs system-level access). The web is a pretty wonderful medium for creating graphical applications these days, and by using it you sidestep these type of installation issues.
