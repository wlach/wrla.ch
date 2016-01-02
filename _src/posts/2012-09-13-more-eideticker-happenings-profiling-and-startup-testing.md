    Title: More Eideticker happenings: Profiling and startup testing
    Date: 2012-09-13T00:00:00
    Tags: Eideticker, Mozilla


*[ For more information on the Eideticker software I&#8217;m referring to, see [this entry][1] ]*

Just wanted to give some updates on a few new Eideticker features which have landed in the past week.

**Profiling support**

While Eideticker is a great tool for observing the external behaviour of the mobile browser, it hasn&#8217;t been able to tell us much about what&#8217;s going on inside. If something&#8217;s slow, why is it slow? If it&#8217;s slower than it was the day before, what&#8217;s the cause? If it&#8217;s faster? What explains the deviations in test results from one run to the other?

Thanks to [Benoit Girard][2] (+ a little bit of integration work from me), we can now start providing answers to these questions. Eideticker now has a mode that allows us to capture a [sampling profile][3] of the application while the video capture is ongoing. From the dashboard, you can now get access said profile, just by clicking on a link.

<a href="http://wrla.ch/blog/2012/09/more-eideticker-happenings-profiling-and-startup-testing/dash-with-link-to-profile/" rel="attachment wp-att-737"><img src="/files/2012/09/dash-with-link-to-profile.png" alt="" title="Eideticker dashboard with link to profile" width="764" height="555" class="alignnone size-full wp-image-737" srcset="/files/2012/09/dash-with-link-to-profile-300x217.png 300w, /files/2012/09/dash-with-link-to-profile.png 764w" sizes="(max-width: 764px) 100vw, 764px" /></a>  
<a href="http://wrla.ch/blog/2012/09/more-eideticker-happenings-profiling-and-startup-testing/profiler-et-screenshot/" rel="attachment wp-att-740"><img src="/files/2012/09/profiler-et-screenshot.png" alt="" title="Profile of Eideticker Capture" width="852" height="425" class="alignnone size-full wp-image-740" srcset="/files/2012/09/profiler-et-screenshot-300x149.png 300w, /files/2012/09/profiler-et-screenshot.png 852w" sizes="(max-width: 852px) 100vw, 852px" /></a>

Note that the profile is not yet synchronized precisely to the videocapture (the profile works over the entire run of the browser), but Benoit is busily making that happen. That should hopefully land soon, in the mean time we still have some pretty useful data.

To say I&#8217;m excited about this would be an understatement. I think it has the potential to open up a whole new world of understanding of why our mobile (and desktop, someday) browser performs the way it does.

**Startup / pageload testing**

Eideticker has had support for measuring startup and page load time for a few months now, but I hadn&#8217;t yet hooked it up to the dashboard. As of today, it now is. There&#8217;s a bunch of different angles that are interesting to measure here (new vs. old profiles, whether the browser has been launched since boot, launching web applications, loading about:home or loading a web page, &#8230;) which I&#8217;ll get to in due course. For now, we at least have a baseline of how long it takes to see the Firefox homescreen on a Galaxy Nexus:

<video width="400px" src="http://wrla.ch/eideticker/dashboard/videos/video-1347572002.11.webm" controls></video>

Of course, this is hooked up to the profiling support previously mentioned. Here&#8217;s [an example profile][4].

I&#8217;ve already filed [one bug][5] based on the data gathered so far. 

 [1]: http://wrla.ch/blog/2012/06/mobile-firefox-measuring-how-a-browser-feels/
 [2]: http://benoitgirard.wordpress.com/
 [3]: https://developer.mozilla.org/en-US/docs/Performance/Profiling_with_the_Built-in_Profiler
 [4]: http://people.mozilla.com/~bgirard/cleopatra/?zippedProfile=profiles/sps-profile-1347572285.4.zip&#038;videoCapture=videos/video-1347572285.4.webm
 [5]: https://bugzilla.mozilla.org/show_bug.cgi?id=791106