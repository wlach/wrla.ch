    Title: Perfherder update
    Date: 2015-07-14T00:00:00
    Tags: FirefoxOS, Mozilla, Perfherder


Haven&#8217;t been doing enough blogging about [Perfherder][1] (our project to make Talos and other per-checkin performance data more useful) recently. Let&#8217;s fix that. We&#8217;ve been making some good progress, helped in part by a group of new contributors that joined us through an experimental &#8220;[summer of contribution][2]&#8221; program.

**Comparison mode**

Inspired by Compare Talos, we&#8217;ve designed something similar which hooks into the perfherder backend. This has already gotten some interest: see this post on [dev.tree-management][3] and this one on [dev.platform][4]. We&#8217;re working towards building something that will be really useful both for (1) illustrating that the performance regressions we detect are real and (2) helping developers figure out the impact of their changes before they land them.

<table>
  <tr>
    <td>
      <a href="/files/2015/07/Screen-Shot-2015-07-14-at-3.54.57-PM.png"><img src="/files/2015/07/Screen-Shot-2015-07-14-at-3.54.57-PM-300x207.png" alt="Screen Shot 2015-07-14 at 3.54.57 PM" width="300" height="207" class="alignnone size-medium wp-image-1219" srcset="/files/2015/07/Screen-Shot-2015-07-14-at-3.54.57-PM-300x207.png 300w, /files/2015/07/Screen-Shot-2015-07-14-at-3.54.57-PM.png 980w" sizes="(max-width: 300px) 100vw, 300px" /></a>
    </td>
    
    <td>
      <a href="/files/2015/07/Screen-Shot-2015-07-14-at-3.53.20-PM.png"><img src="/files/2015/07/Screen-Shot-2015-07-14-at-3.53.20-PM-300x206.png" alt="Screen Shot 2015-07-14 at 3.53.20 PM" width="300" height="206" class="alignnone size-medium wp-image-1218" srcset="/files/2015/07/Screen-Shot-2015-07-14-at-3.53.20-PM-300x206.png 300w, /files/2015/07/Screen-Shot-2015-07-14-at-3.53.20-PM.png 980w" sizes="(max-width: 300px) 100vw, 300px" /></a>
    </td>
  </tr>
</table>

Most of the initial work was done by [Joel Maher][5] with lots of review for aesthetics and correctness by me. Avi Halmachi from the Performance Team also helped out with the [t-test][6] model for detecting the confidence that we have that a difference in performance was real. Lately myself and [Mike Ling][7] (one of our summer of contribution members) have been working on further improving the interface for usability &#8212; I&#8217;m hopeful that we&#8217;ll soon have something implemented that&#8217;s broadly usable and comprehensible to the Mozilla Firefox and Platform developer community.

**Graphs improvements**

Although it&#8217;s received slightly less attention lately than the comparison view above, we&#8217;ve been making steady progress on the graphs view of performance series. Aside from demonstrations and presentations, the primary use case for this is being able to detect visually sustained changes in the result distribution for talos tests, which is often necessary to be able to confirm regressions. Notable recent changes include a much easier way of selecting tests to add to the graph from Mike Ling and more readable/parseable urls from [Akhilesh Pillai][8] (another summer of contribution participant). 

[<img src="/files/2015/07/Screen-Shot-2015-07-14-at-4.09.45-PM-300x174.png" alt="Screen Shot 2015-07-14 at 4.09.45 PM" width="300" height="174" class="alignnone size-medium wp-image-1221" srcset="/files/2015/07/Screen-Shot-2015-07-14-at-4.09.45-PM-300x174.png 300w, /files/2015/07/Screen-Shot-2015-07-14-at-4.09.45-PM-1024x595.png 1024w, /files/2015/07/Screen-Shot-2015-07-14-at-4.09.45-PM.png 1130w" sizes="(max-width: 300px) 100vw, 300px" />][9]

**Performance alerts**

I&#8217;ve also been steadily working on making Perfherder generate alerts when there is a significant discontinuity in the performance numbers, similar to what [GraphServer][10] does now. Currently we have an option to generate a static CSV file of these alerts, but the eventual plan is to insert these things into a peristent database. After that&#8217;s done, we can actually work on creating a UI inside Perfherder to replace [alertmanager][11] (which currently uses GraphServer data) and start using this thing to sheriff performance regressions &#8212; putting the herder into perfherder.

As part of this, I&#8217;ve converted the graphserver alert generation code into a standalone python library, which has already proven useful as a component in the [Raptor project for FirefoxOS][12]. Yay modularity and reusability.

**Python API**

I&#8217;ve also been working on creating and improving a [python API][13] to access Treeherder data, which includes Perfherder. This lets you do interesting things, like dynamically run various types of statistical analysis on the data stored in the production instance of Perfherder (no need to ask me for a database dump or other credentials). I&#8217;ve been using this to perform validation of the data we&#8217;re storing and debug various tricky problems. For example, [I found out last week that we were storing up to duplicate 200 entries in each performance series due to double data ingestion][14] &#8212; oops. 

You can also use this API to dynamically create interesting graphs and visualizations using [ipython notebook][15], here&#8217;s a simple example of me plotting the last 7 days of youtube.com pageload data inline in a notebook:

[<img src="/files/2015/07/Screen-Shot-2015-07-14-at-4.43.55-PM-300x224.png" alt="Screen Shot 2015-07-14 at 4.43.55 PM" width="300" height="224" class="alignnone size-medium wp-image-1224" srcset="/files/2015/07/Screen-Shot-2015-07-14-at-4.43.55-PM-300x224.png 300w, /files/2015/07/Screen-Shot-2015-07-14-at-4.43.55-PM.png 842w" sizes="(max-width: 300px) 100vw, 300px" />][16]

[[original][17]]

 [1]: https://wiki.mozilla.org/Auto-tools/Projects/Perfherder
 [2]: https://elvis314.wordpress.com/2015/06/09/please-welcome-the-dashboard-hacker-team/
 [3]: https://groups.google.com/d/msg/mozilla.dev.tree-management/IUmMuY8b52A/Asne1cW0I8EJ
 [4]: https://groups.google.com/d/msg/mozilla.dev.platform/PaJFBtvc3Vg/BvX-pFlsAkoJ
 [5]: https://elvis314.wordpress.com/
 [6]: https://en.wikipedia.org/wiki/Student's_t-test
 [7]: https://github.com/MikeLing
 [8]: https://github.com/akhileshpillai
 [9]: /files/2015/07/Screen-Shot-2015-07-14-at-4.09.45-PM.png
 [10]: http://graphs.mozilla.org
 [11]: http://alertmanager.allizom.org:8080/alerts.html#
 [12]: https://hacks.mozilla.org/2015/06/performance-testing-firefox-os-with-raptor/
 [13]: http://treeherder.readthedocs.org/retrieving_data.html#python-client
 [14]: https://bugzilla.mozilla.org/show_bug.cgi?id=1182282
 [15]: http://wrla.ch/blog/2014/04/pycon-2014-impressions-ipython-notebook-is-the-future-more/
 [16]: /files/2015/07/Screen-Shot-2015-07-14-at-4.43.55-PM.png
 [17]: http://nbviewer.ipython.org/url/wrla.ch/blog/wp-content/uploads/2015/07/perfherder-api.ipynb