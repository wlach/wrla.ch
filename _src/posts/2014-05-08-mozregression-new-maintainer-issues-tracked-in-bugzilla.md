    Title: mozregression: New maintainer, issues tracked in bugzilla
    Date: 2014-05-08T00:00:00
    Tags: Mozilla, mozregression, Python

Just wanted to give some quick updates on [mozregression][1], your favorite regression-finding tool for Firefox:

1. I moved all issue tracking in mozregression to bugzilla from github issues. Github unfortunately doesn't really scale to handle notifications sensibly when you're part of a large organization like Mozilla, which meant many problems were flying past me unseen. [File your new bugs][2] in bugzilla, they're now much more likely to be acted upon.
2. [Sam Garrett][3] has stepped up to be co-maintainer of the project with me. He's been doing a great job whacking out a bunch of bugs and keeping things running reliably, and it was time to give him some recognition and power to keep things moving forward.
3. On that note, I just released mozregression 0.17, which now shows the revision number when running a build (a request from the graphics team, bug [1007238][4]) and handles respins of nightly builds correctly ([bug 1000422][5]). Both of these were fixed by Sam.

If you're interested in contributing to Mozilla and are somewhat familiar with python, mozregression is a great place to start. The codebase is quite approachable and the impact will be high &#8212; as I've found out over the last few months, people _all over_ the Mozilla organization (managers, developers, QA) use it in the course of their work and it saves tons of their time. A list of currently open bugs is [here][6].

[1]: http://mozilla.github.io/mozregression/
[2]: https://bugzilla.mozilla.org/enter_bug.cgi?product=Testing&component=mozregression
[3]: http://blackrhino.io/
[4]: https://bugzilla.mozilla.org/show_bug.cgi?id=1007238
[5]: https://bugzilla.mozilla.org/show_bug.cgi?id=1000422
[6]: https://bugzilla.mozilla.org/buglist.cgi?component=mozregression&product=Testing
