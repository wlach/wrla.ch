    Title: mozregression 0.24
    Date: 2014-09-15T00:00:00
    Tags: Mozilla, mozregression

I just released [mozregression][1] 0.24. This would be a good time to note some of the user-visible fixes / additions that have gone in recently:

1. Thanks to Sam Garrett, you can now specify a different branch other than inbound to get finer grained regression ranges from. E.g. if you're pretty sure a regression occurred on fx-team, you can do something like:
   `mozregression --inbound-branch fx-team -g 2014-09-13 -b 2014-09-14`

2. Fixed a bug where we could get an incorrect regression range ([bug 1059856][2]). Unfortunately the root cause of the bug is still open (it's a bit tricky to match mozilla-central commits to that of other branches) but I think this most recent fix should make things work in 99.9% of cases. Let me know if I'm wrong.
3. Thanks to Julien Pagès, we now download the inbound build metadata in parallel, which speeds up inbound bisection quite significantly

If you know a bit of python, contributing to mozregression is a great way to have a high impact on Mozilla. Many platform developers use this project in their day-to-day work, but there's still [lots of room for improvement][3].

[1]: http://mozilla.github.io/mozregression/
[2]: https://bugzilla.mozilla.org/show_bug.cgi?id=1059856
[3]: https://bugzilla.mozilla.org/buglist.cgi?component=mozregression&product=Testing
