    Title: Faster, but not quite there yet&#8230;
    Date: 2011-10-25T00:00:00
    Tags: Data Visualization, Mozilla


So as others have been posting about, we&#8217;ve been making [some headway][1] on our progress on the GoFaster project. Unfortunately it seems like we&#8217;re still some distance away from reaching our magic number of a 2 hour turnaround for each revision pushed.

<a href="http://wrla.ch/blog/2011/10/faster-but-not-quite-there-yet/gofaster-e2e-graph-oct25/" rel="attachment wp-att-312"><img src="/files/2011/10/gofaster-e2e-graph-oct25.png" alt="" title="gofaster-e2e-graph-oct25" width="632" height="511" class="alignnone size-full wp-image-312" srcset="/files/2011/10/gofaster-e2e-graph-oct25-300x242.png 300w, /files/2011/10/gofaster-e2e-graph-oct25.png 632w" sizes="(max-width: 632px) 100vw, 632px" /></a>

It&#8217;s a bit hard to see the exact number on the graph ([someone should fix that][2]), but we seem to teetering around an average of 3 hours at this point. Looking at our [build charts][3], it seems like the critical path has shifted in many cases from Windows to MacOS X. Is there something we can do to close the gap there? Or is there a more general fix which would lead to substantial savings? If you have any thoughts, or would like to help out, we&#8217;re scheduled to have a [short meeting tomorrow][4]. 

Anyone is welcome to join, but note that we&#8217;re practical, results-oriented people. Crazy ideas are fun, but we&#8217;re most interested in proposals that have measurable data behind them and can be implemented in reasonable amounts of time. 

 [1]: http://atlee.ca/blog/2011/10/17/going-faster/
 [2]: https://bugzilla.mozilla.org/show_bug.cgi?id=697277
 [3]: http://brasstacks.mozilla.com/gofaster/#/buildcharts
 [4]: https://wiki.mozilla.org/ReleaseEngineering/BuildFaster/Meetings/2011-10-26