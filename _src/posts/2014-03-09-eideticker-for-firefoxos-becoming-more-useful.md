    Title: Eideticker for FirefoxOS: Becoming more useful
    Date: 2014-03-09T00:00:00
    Tags: Eideticker, FirefoxOS, Mozilla

_[ For more information on the Eideticker software I'm referring to, see [this entry][1] ]_

Time for a long overdue eideticker-for-firefoxos update. [Last time we were here][2] (almost 5 months ago! man time flies), I was discussing methodologies for measuring startup performance. Since then, [Dave Hunt][3] and myself have been doing lots of work to make Eideticker more robust and useful. Notably, we now have a setup in London running a suite of Eideticker tests on the latest version of FirefoxOS on the Inari on a daily basis, reporting to <http://eideticker.mozilla.org/b2g>.

[<img src="/files/2014/03/b2g-contacts-startup-dashboard.png" alt="b2g-contacts-startup-dashboard" width="840" height="601" class="alignnone size-full wp-image-1005" srcset="/files/2014/03/b2g-contacts-startup-dashboard-300x214.png 300w, /files/2014/03/b2g-contacts-startup-dashboard.png 840w" sizes="(max-width: 840px) 100vw, 840px" />][4]

There were more than a few false starts with and some of the earlier data is not to be entirely trusted but it now seems to be chugging along nicely, hopefully providing startup numbers that provide a useful counterpoint to the [datazilla startup numbers][5] we've already been collecting for some time. There still seem to be some minor problems, but in general I am becoming more and more confident in it as time goes on.

One feature that I am particularly proud of is the detail view, which enables you to see frame-by-frame what's going on. Click on any datapoint on the graph, then open up the view that gives an account of what eideticker is measuring. Hover over the graph and you can see what the video looks like at any point in the capture. This not only lets you know that something regressed, but how. For example, in the messages app, you can scan through this view to see exactly when the first message shows up, and what exact state the application is in when Eideticker says it's "done loading".

[<img src="/files/2014/03/capture-detail-view.png" alt="Capture Detail View" width="964" height="843" class="alignnone size-full wp-image-1008" srcset="/files/2014/03/capture-detail-view-300x262.png 300w, /files/2014/03/capture-detail-view.png 964w" sizes="(max-width: 964px) 100vw, 964px" />][6]  
[[link to original]][7]

(apologies for the low quality of the video &#8212; should be fixed with [this bug][8] next week)

As it turns out, this view has also proven to be particularly useful when working with the new entropy measurements in Eideticker which I've been using to measure checkerboarding (redraw delay) on FirefoxOS. More on that next week.

[1]: http://wrla.ch/blog/2012/06/mobile-firefox-measuring-how-a-browser-feels/
[2]: http://wrla.ch/blog/2013/10/automatically-measuring-startup-load-time-with-eideticker/
[3]: http://blargon7.com/
[4]: /files/2014/03/b2g-contacts-startup-dashboard.png
[5]: https://datazilla.mozilla.org/b2g
[6]: /files/2014/03/capture-detail-view.png
[7]: http://eideticker.wrla.ch/b2g/framediff.html?id=3819a484a6d611e3ab89f0def1767b24
[8]: https://bugzilla.mozilla.org/show_bug.cgi?id=980479
