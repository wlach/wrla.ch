    Title: mozregression for MacOS
    Date: 2020-04-24T10:59:04
    Tags: Mozilla, mozregression

Just a quick note that, as a side-effect of the work I mentioned a while ago to [add telemetry to mozregression](/blog/2020/02/this-week-in-glean-special-guest-post-mozregression-telemetry-part-1/), mozregression now has a graphical Mac client! It's a bit of a pain to install (since it's unsigned),
but likely worlds easier for the average person to get going than the command-line version. Please feel
free to [point people to it](https://mozilla.github.io/mozregression/install.html) if you're looking to get a regression range for a MacOS-specific problem with Firefox.

<center><img style="width:600px" src="/files/2020/04/mozregression-gui-mac.png"/></center>

More details: The [Glean Python SDK](https://mozilla.github.io/glean/book/dev/python/index.html), which [mozregression now uses for telemetry](https://mozilla.github.io/mozregression/documentation/telemetry.html), requires Python 3. This provided the impetus to port the GUI itself to Python 3 and PySide2 (the modern incarnation of PyQt), which brought with it a much easier installation/development experience for the GUI on platforms like Mac and Linux.

I haven't gotten around to producing GUI binaries for the Linux yet, but it should not be much work.

Speaking of Glean, mozregression, and Telemetry, stay tuned for more updates on that soon. It's been an adventure!
