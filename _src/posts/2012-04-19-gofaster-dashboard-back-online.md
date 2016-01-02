    Title: GoFaster dashboard back online
    Date: 2012-04-19T00:00:00
    Tags: GoFaster, Mozilla, Release Engineering


Build times for mozilla-central are a major factor in developer productivity. Faster build times mean more people using try (reducing breakage) and more fine-grained regression ranges (reducing the impact of breakages). As a side benefit, it allows us to avoid buying and maintaining more hardware (or put new hardware to better use). About a half-year ago, we set up a project called BuildFaster to try to bring these times down, setting the ambitious goal of getting build times (from checkin to tests done) down to 2 hours. We didn&#8217;t quite succeed, though we did make some major strides. As part of this project, we also developed a dashboard to track our progress and narrow down the major bottlenecks which were keeping up our build times.

Unfortunately, this dashboard went down earlier this year with the rest of Brasstacks and we hadn&#8217;t had the chance to bring it back up. I&#8217;m pleased to announce that thanks to Jonathan Griffin, it&#8217;s finally [back online][1]. 

While no one is actively working on build performance at the moment (at least to my knowledge), it&#8217;s still useful to keep track of build times to make sure that we don&#8217;t regress. Anecdotally, it has seemed to me that the time needed to get results from try has been pretty stable over the last while, and this is borne out by the results:

<a href="http://wrla.ch/blog/2012/04/gofaster-dashboard-back-online/gofaster-dashboard-update-2012/" rel="attachment wp-att-529"><img src="/files/2012/04/gofaster-dashboard-update-2012.png" alt="" title="gofaster-dashboard-update-2012" width="628" height="508" class="alignnone size-full wp-image-529" srcset="/files/2012/04/gofaster-dashboard-update-2012-300x242.png 300w, /files/2012/04/gofaster-dashboard-update-2012.png 628w" sizes="(max-width: 628px) 100vw, 628px" /></a>

As the cliche goes: no news is good news.

 [1]: http://brasstacks.mozilla.com/gofaster/#/