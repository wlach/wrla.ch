    Title: mozregression now supports inbound builds
    Date: 2013-11-28T00:00:00
    Tags: Mozilla, mozregression

Just wanted to send out a quick note that I recently added inbound support to [mozregression][1] for desktop builds of Firefox on Windows, Mac, and Linux.

For the uninitiated, mozregression is an automated tool that lets you bisect through builds of Firefox to find out when a problem was introduced. You give it the last known good date, the last known bad date and off it will go, automatically pulling down builds to test. After each iteration, it will ask you whether this build was good or bad, update the regression range accordingly, and then the cycle repeats until there are no more intermediate builds.

Previously, it would only use nightlies which meant a one day granularity &#8212; this meant pretty wide regression ranges, made wider in the last year by the fact that so much more is now going into the tree over the course of the day. However, with inbound support (using the new inbound archive) we now have the potential to get a much tighter range, which should be super helpful for developers. Best of all, mozregression doesn't require any particularly advanced skills to use which means everyone in the Mozilla community can help out.

For anyone interested, there's quite a bit of scope to improve mozregression to make it do more things (FirefoxOS support, easier installation). Feel free to check out [the repository][2], the [issues list][3] (I just added [an easy one][4] which would make a great first bug) and ask questions on irc.mozilla.org#ateam!

[1]: http://mozilla.github.io/mozregression/
[2]: http://github.com/mozilla/mozregression
[3]: https://github.com/mozilla/mozregression/issues?state=open
[4]: https://github.com/mozilla/mozregression/issues/76
