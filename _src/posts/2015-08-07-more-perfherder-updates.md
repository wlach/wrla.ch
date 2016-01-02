    Title: More Perfherder  updates
    Date: 2015-08-07T00:00:00
    Tags: Data Visualization, Mozilla, Perfherder


Since my last update, we&#8217;ve been trucking along with improvements to [Perfherder][1], the project for making Firefox performance sheriffing and analysis easier.

**Compare visualization improvements**

I&#8217;ve been spending quite a bit of time trying to fix up the display of information in the compare view, to address feedback from developers and hopefully generally streamline things. [Vladan][2] (from the perf team) referred me to [Blake Winton][3], who provided tons of awesome suggestions on how to present things more concisely. 

Here&#8217;s an old versus new picture:

<table>
  <tr>
    <td>
      <a href="/files/2015/07/Screen-Shot-2015-07-14-at-3.53.20-PM.png"><img src="/files/2015/07/Screen-Shot-2015-07-14-at-3.53.20-PM-300x206.png" alt="Screen Shot 2015-07-14 at 3.53.20 PM" width="300" height="206" class="alignnone size-medium wp-image-1218" srcset="/files/2015/07/Screen-Shot-2015-07-14-at-3.53.20-PM-300x206.png 300w, /files/2015/07/Screen-Shot-2015-07-14-at-3.53.20-PM.png 980w" sizes="(max-width: 300px) 100vw, 300px" /></a>
    </td>
    
    <td>
      <a href="/files/2015/08/Screen-Shot-2015-08-07-at-1.57.39-PM.png"><img src="/files/2015/08/Screen-Shot-2015-08-07-at-1.57.39-PM-300x178.png" alt="Screen Shot 2015-08-07 at 1.57.39 PM" width="300" height="178" class="alignnone size-medium wp-image-1229" srcset="/files/2015/08/Screen-Shot-2015-08-07-at-1.57.39-PM-300x178.png 300w, /files/2015/08/Screen-Shot-2015-08-07-at-1.57.39-PM.png 1003w" sizes="(max-width: 300px) 100vw, 300px" /></a>
    </td>
  </tr>
</table>

Summary of significant changes in this view:

  * Removed or consolidated several types of numerical information which were overwhelming or confusing (e.g. presenting both numerical and percentage standard deviation in their own columns).
  * Added tooltips all over the place to explain what&#8217;s being displayed.
  * Highlight more strongly when it appears there aren&#8217;t enough runs to make a definitive determination on whether there was a regression or improvement.
  * Improve display of visual indicator of magnitude of regression/improvement (providing a pseudo-scale showing where the change ranges from 0% &#8211; 20%+).
  * Provide more detail on the two changesets being compared in the header and make it easier to retrigger them (thanks to Mike Ling).
  * Much better and more intuitive error handling when something goes wrong (also thanks to Mike Ling).

The point of these changes isn&#8217;t necessarily to make everything &#8220;immediately obvious&#8221; to people. We&#8217;re not building general purpose software here: Perfherder will always be a rather specialized tool which presumes significant domain knowledge on the part of the people using it. However, even for our audience, it turns out that there&#8217;s a lot of room to improve how our presentation: reducing the amount of extraneous noise helps people zero in on the things they really need to care about.

Special thanks to everyone who took time out of their schedules to provide so much good feedback, in particular [Avi Halmachi][4], [Glandium][5], and [Joel Maher][6].

Of course more suggestions are always welcome. Please [give it a try][7] and [file bugs against the perfherder component][8] if you find anything you&#8217;d like to see changed or improved.

**Getting the word out**  

```
Hammersmith:mozilla-central wlach$ hg push -f try
pushing to ssh://hg.mozilla.org/try
no revisions specified to push; using . to avoid pushing multiple heads
searching for changes
remote: waiting for lock on repository /repo/hg/mozilla/try held by 'hgssh1.dmz.scl3.mozilla.com:8270'
remote: got lock after 4 seconds
remote: adding changesets
remote: adding manifests
remote: adding file changes
remote: added 1 changesets with 1 changes to 1 files
remote: Trying to insert into pushlog.
remote: Inserted into the pushlog db successfully.
remote:
remote: View your change here:
remote:   https://hg.mozilla.org/try/rev/e0aa56fb4ace
remote:
remote: Follow the progress of your build on Treeherder:
remote:   https://treeherder.mozilla.org/#/jobs?repo=try&revision=e0aa56fb4ace
remote:
remote: It looks like this try push has talos jobs. Compare performance against a baseline revision:
remote:   https://treeherder.mozilla.org/perf.html#/comparechooser?newProject=try&newRevision=e0aa56fb4ace
```

Try pushes incorporating Talos jobs now automatically link to perfherder&#8217;s compare view, both in the output from mercurial and in the emails the system sends. One of the challenges we&#8217;ve been facing up to this point is just letting developers know that Perfherder *exists* and it can help them either avoid or resolve performance regressions. I believe this will help.

**Data quality and ingestion improvements**

Over the past couple weeks, we&#8217;ve been comparing our regression detection code when run against Graphserver data to Perfherder data. In doing so, we discovered that we&#8217;ve sometimes been using the wrong algorithm (geometric mean) to summarize some of our tests, leading to unexpected and less meaningful results. For example, the v8_7 benchmark uses a custom weighting algorithm for its score, to account for the fact that the things it tests have a particular range of expected values.

To hopefully prevent this from happening again in the future, we&#8217;ve decided to move the test summarization code out of Perfherder back into Talos ([bug 1184966][9]). This has the additional benefit of creating a stronger connection between the content of the Talos logs and what Perfherder displays in its comparison and graph views, which has thrown people off in the past.

**Continuing data challenges**

Having better tools for visualizing this stuff is great, but it also highlights some continuing problems we&#8217;ve had with data quality. It turns out that our automation setup often produces *qualitatively different* performance results for the exact same set of data, depending on when and how the tests are run.

A certain amount of random noise is always expected when running performance tests. As much as we might try to make them uniform, our testing machines and environments are just not 100% identical. That we expect and can deal with: our standard approach is just to retrigger runs, to make sure we get a representative sample of data from our population of machines.

The problem comes when there&#8217;s a *pattern* to the noise: we&#8217;ve already noticed that tests run on the weekends produce different results (see Joel&#8217;s post from a year ago, [&#8220;A case of the weekends&#8221;][10]) but it seems as if there&#8217;s other circumstances where one set of results will be different from another, depending on the time that each set of tests was run. Some tests and platforms (e.g. the a11yr suite, MacOS X 10.10) seem particularly susceptible to this issue.

We need to find better ways of dealing with this problem, as it can result in a lot of wasted time and energy, for both sheriffs and developers. See for example [bug 1190877][11], which concerned a completely spurious regression on the tresize benchmark that was initially blamed on some changes to the media code&#8211; in this case, Joel speculates that the linux64 test machines we use might have changed from under us in some way, but we really don&#8217;t know yet.

I see two approaches possible here:

  1. Figure out what&#8217;s causing the same machines to produce qualitatively different result distributions and address that. This is of course the ideal solution, but it requires coordination with other parts of the organization who are likely quite busy and might be hard.
  2. Figure out better ways of detecting and managing these sorts of case. I have noticed that the standard deviation inside the results when we have spurious regressions/improvements tends to be higher (see for example [this compare view][12] for the aforementioned &#8220;regression&#8221;). Knowing what we do, maybe there&#8217;s some statistical methods we can use to detect bad data?

For now, I&#8217;m leaning towards (2). I don&#8217;t think we&#8217;ll ever completely solve this problem and I think coming up with better approaches to understanding and managing it will pay the largest dividends. Open to other opinions of course!

 [1]: https://wiki.mozilla.org/Auto-tools/Projects/Perfherder
 [2]: https://blog.mozilla.org/vdjeric/
 [3]: https://mozillians.org/en-US/u/bwinton/
 [4]: http://avih.github.io/
 [5]: http://glandium.org/blog/
 [6]: http://elvis314.wordpress.com/
 [7]: https://treeherder.mozilla.org/perf.html#/comparechooser
 [8]: https://bugzilla.mozilla.org/enter_bug.cgi?product=Tree%20Management&#038;component=Perfherder
 [9]: https://bugzilla.mozilla.org/show_bug.cgi?id=1184966
 [10]: https://elvis314.wordpress.com/2014/10/30/a-case-of-the-weekends/
 [11]: https://bugzilla.mozilla.org/show_bug.cgi?id=1190877
 [12]: https://treeherder.mozilla.org/perf.html#/compare?originalProject=mozilla-inbound&#038;originalRevision=4d0818791d07&#038;newProject=mozilla-inbound&#038;newRevision=5e130ad70aa7