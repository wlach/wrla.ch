    Title: Perfherder: Onward!
    Date: 2015-11-04T00:00:00
    Tags: Mozilla, Perfherder

In addition to the [database refactoring][1] I mentioned a few weeks ago, some cool stuff has been going into [Perfherder][2] lately.

**Tracking installer size**

Perfherder is now tracking the size of the Firefox installer for the various platforms we support ([bug 1149164][3]). I originally only intended to track Android .APK size (on request from the mobile team), but installer sizes for other platforms came along for the ride. I don't think anyone will complain.

[<img src="/files/2015/11/Screen-Shot-2015-11-03-at-5.28.48-PM-300x181.png" alt="Screen Shot 2015-11-03 at 5.28.48 PM" width="300" height="181" class="alignnone size-medium wp-image-1274" srcset="/files/2015/11/Screen-Shot-2015-11-03-at-5.28.48-PM-300x181.png 300w, /files/2015/11/Screen-Shot-2015-11-03-at-5.28.48-PM-1024x618.png 1024w" sizes="(max-width: 300px) 100vw, 300px" />][4]

[link][5]

Just as exciting to me as the feature itself is how it's implemented: I added a log parser to treeherder which just picks up a line called "PERFHERDER_DATA" in the logs with specially formatted JSON data, and then automatically stores whatever metrics are in there in the database (platform, options, etc. are automatically determined). For example, on Linux:

```
PERFHERDER_DATA: {"framework": {"name": "build_metrics"}, "suites": [{"subtests": [{"name": "libxul.so", "value": 99030741}], "name": "installer size", "value": 55555785}]}
```

This should make it super easy for people to add their own metrics to Perfherder for build and test jobs. We'll have to be somewhat careful about how we do this (we don't want to add thousands of new series with irrelevant / inconsistent data) but I think there's lots of potential here to be able to track things we care about on a per-commit basis. Maybe build times (?).

**More compare view improvements**

I added filtering to the Perfherder compare view and added back links to the graphs view. Filtering should make it easier to highlight particular problematic tests in bug reports, etc. The graphs links shouldn't really be necessary, but unfortunately are due to the unreliability of our data &#8212; sometimes you can only see if a particular difference between two revisions is worth paying attention to in the context of the numbers over the last several weeks.

[<img src="/files/2015/11/Screen-Shot-2015-11-03-at-5.37.02-PM-300x157.png" alt="Screen Shot 2015-11-03 at 5.37.02 PM" width="300" height="157" class="alignnone size-medium wp-image-1275" srcset="/files/2015/11/Screen-Shot-2015-11-03-at-5.37.02-PM-300x157.png 300w, /files/2015/11/Screen-Shot-2015-11-03-at-5.37.02-PM-1024x536.png 1024w" sizes="(max-width: 300px) 100vw, 300px" />][6]

**Miscellaneous**

Even after the [summer of contribution][7] has ended, Mike Ling continues to do great work. Looking at the commit log over the past few weeks, he's been responsible for the following fixes and improvements:

- [Bug 1218825][8]: Can zoom in on perfherder graphs by selecting the main view
- [Bug 1207309][9]: Disable &#8216;<' button in test chooser if no test selected
- [Bug 1210503][10] : Include non-summary tests in main comparison view
- [Bug 1153956][11] : Persist the selected revision in the url on perfherder (based on earlier work by Akhilesh Pillai)

**Next up**

My main goal for this quarter is to create a fully functional interface for actually sheriffing performance regressions, to replace [alertmanager][12]. Work on this has been going well. More soon.

[<img src="/files/2015/11/Screen-Shot-2015-11-04-at-10.41.26-AM-300x176.png" alt="Screen Shot 2015-11-04 at 10.41.26 AM" width="300" height="176" class="alignnone size-medium wp-image-1280" srcset="/files/2015/11/Screen-Shot-2015-11-04-at-10.41.26-AM-300x176.png 300w, /files/2015/11/Screen-Shot-2015-11-04-at-10.41.26-AM-1024x600.png 1024w, /files/2015/11/Screen-Shot-2015-11-04-at-10.41.26-AM.png 1126w" sizes="(max-width: 300px) 100vw, 300px" />][13]

[1]: http://wrla.ch/blog/2015/10/the-new-old-perfherder-data-model/
[2]: https://wiki.mozilla.org/Auto-tools/Projects/Perfherder
[3]: https://bugzilla.mozilla.org/show_bug.cgi?id=1149164
[4]: /files/2015/11/Screen-Shot-2015-11-03-at-5.28.48-PM.png

[5]: https://treeherder.mozilla.org/perf.html#/graphs?series=[mozilla-inbound,4eb0cde5431ee9aeb5eb14512ddb3da6d4702cf0,1]&#038;series=[mozilla-inbound,80cac7ef44b76864458627c574af1a18a425f338,1]&#038;series=[mozilla-inbound,0060252bdfb7632df5877b7594b4d16f1b5ca4c9,1]
[6]: /files/2015/11/Screen-Shot-2015-11-03-at-5.37.02-PM.png
[7]: http://wrla.ch/blog/2015/09/perfherder-summer-of-contribution-thoughts/
[8]: https://bugzilla.mozilla.org/show_bug.cgi?id=1218825
[9]: https://bugzilla.mozilla.org/show_bug.cgi?id=1207309
[10]: https://bugzilla.mozilla.org/show_bug.cgi?id=1210503
[11]: https://bugzilla.mozilla.org/show_bug.cgi?id=1153956
[12]: http://alertmanager.allizom.org:8080/alerts.html
[13]: /files/2015/11/Screen-Shot-2015-11-04-at-10.41.26-AM.png
