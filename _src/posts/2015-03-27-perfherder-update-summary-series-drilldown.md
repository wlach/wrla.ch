    Title: Perfherder update: Summary series drilldown
    Date: 2015-03-27T00:00:00
    Tags: Data Visualization, Mozilla, Perfherder

Just wanted to give another quick Perfherder update. Since the [last time][1], I've added summary series (which is what GraphServer shows you), so we now have (in theory) the best of both worlds when it comes to Talos data: aggregate summaries of the various suites we run (tp5, tart, etc), with the ability to dig into individual results as needed. This kind of analysis wasn't possible with Graphserver and I'm hopeful this will be helpful in tracking down the root causes of Talos regressions more effectively.

Let's give an example of where this might be useful by showing how it can highlight problems. Recently we tracked a regression in the Customization Animation Tests (CART) suite from the commit in [bug 1128354][2]. Using [Mishra Vikas][3]&#8216;s new "highlight revision mode" in Perfherder (combined with the revision hash when the regression was pushed to inbound), we can quickly zero in on the location of it:

[<img src="/files/2015/03/Screen-Shot-2015-03-27-at-3.18.28-PM-1024x498.png" alt="Screen Shot 2015-03-27 at 3.18.28 PM" width="474" height="230" class="alignnone size-large wp-image-1184" srcset="/files/2015/03/Screen-Shot-2015-03-27-at-3.18.28-PM-300x146.png 300w, /files/2015/03/Screen-Shot-2015-03-27-at-3.18.28-PM-1024x498.png 1024w, /files/2015/03/Screen-Shot-2015-03-27-at-3.18.28-PM.png 1167w" sizes="(max-width: 474px) 100vw, 474px" />][4]

It does indeed look like things ticked up after this commit for the CART suite, but why? By clicking on the datapoint, you can open up a subtest summary view beneath the graph:

[<img src="/files/2015/03/Screen-Shot-2015-03-27-at-2.35.25-PM.png" alt="Screen Shot 2015-03-27 at 2.35.25 PM" width="936" height="438" class="alignnone size-full wp-image-1175" srcset="/files/2015/03/Screen-Shot-2015-03-27-at-2.35.25-PM-300x140.png 300w, /files/2015/03/Screen-Shot-2015-03-27-at-2.35.25-PM.png 936w" sizes="(max-width: 936px) 100vw, 936px" />][5]

We see here that it looks like the 3-customize-enter-css.all.TART entry ticked up a bunch. The related test 3-customize-enter-css.half.TART ticked up a bit too. The changes elsewhere look minimal. But is that a trend that holds across the data over time? We can add some of the relevant subtests to the overall graph view to get a closer look:

[<img src="/files/2015/03/Screen-Shot-2015-03-27-at-2.36.49-PM-1024x503.png" alt="Screen Shot 2015-03-27 at 2.36.49 PM" width="474" height="232" class="alignnone size-large wp-image-1176" srcset="/files/2015/03/Screen-Shot-2015-03-27-at-2.36.49-PM-300x147.png 300w, /files/2015/03/Screen-Shot-2015-03-27-at-2.36.49-PM-1024x503.png 1024w, /files/2015/03/Screen-Shot-2015-03-27-at-2.36.49-PM.png 1155w" sizes="(max-width: 474px) 100vw, 474px" />][6]

As is hopefully obvious, this confirms that the affected subtest continues to hold its higher value while another test just bounces around more or less in the range it was before.

Hope people find this useful! If you want to play with this yourself, you can access the perfherder UI at <http://treeherder.mozilla.org/perf.html>.

[1]: http://wrla.ch/blog/2015/02/measuring-e10s-vs-non-e10s-performance-with-perfherder/
[2]: https://bugzilla.mozilla.org/show_bug.cgi?id=1128354
[3]: https://mozillians.org/en-US/u/mishravikas/
[4]: /files/2015/03/Screen-Shot-2015-03-27-at-3.18.28-PM.png
[5]: /files/2015/03/Screen-Shot-2015-03-27-at-2.35.25-PM.png
[6]: /files/2015/03/Screen-Shot-2015-03-27-at-2.36.49-PM.png
