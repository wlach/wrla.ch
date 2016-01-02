    Title: Measuring e10s vs. non-e10s performance with Perfherder
    Date: 2015-02-18T00:00:00
    Tags: Mozilla, Perfherder


For the past few months I&#8217;ve been working on a sub-project of Treeherder called Perfherder, which aims to provide a workflow that will let us more easily detect and manage performance regressions in our products (initially just those detected in [Talos][1], but there&#8217;s room to expand on that later). This is a long term project and we&#8217;re still sorting out the details of exactly how it will work, but I thought I&#8217;d quickly announce a milestone. 

As a first step, I&#8217;ve been hacking on a graphical user interface to visualize the performance data we&#8217;re now storing inside Treeherder. It&#8217;s pretty bare bones so far, but already it has two features which [graphserver][2] doesn&#8217;t: the ability to view sub-test results (i.e. the page load time for a specific page in the tp5 suite, as opposed to the geometric mean of all of them) and the ability to see results for e10s builds.

Here&#8217;s an example, comparing the tp5o 163.com page load times on windows 7 with e10s enabled (and not):

[<img src="/files/2015/02/e10s-vs-non-e10s.png" alt="e10s-vs-non-e10s" width="901" height="489" class="alignnone size-full wp-image-1157" srcset="/files/2015/02/e10s-vs-non-e10s-300x162.png 300w, /files/2015/02/e10s-vs-non-e10s.png 901w" sizes="(max-width: 901px) 100vw, 901px" />][3]  
[[link]][4]

Green is e10s, red is non-e10s (the legend picture doesn&#8217;t reflect this because we have yet to deploy a fix to [bug 1130554][5], but I promise I&#8217;m not lying). As you can see, the gap has been closing (in particular, something landed in mid-January that improved the e10s numbers quite a bit), but page load times are still measurably slower with this feature enabled.

 [1]: https://wiki.mozilla.org/Buildbot/Talos
 [2]: http://graphs.mozilla.org
 [3]: /files/2015/02/e10s-vs-non-e10s.png
 [4]: https://treeherder.mozilla.org/perf.html#/graphs?timerange=7776000&#038;seriesList=[[%22mozilla-central%22,%22a78a233646c932ee1c56cf27da58b6aaa4eda2c3%22],[%22mozilla-central%22,%228e9323fd7fadb0623ec520a8ccaec2e733f3d501%22]]
 [5]: https://bugzilla.mozilla.org/show_bug.cgi?id=1130554