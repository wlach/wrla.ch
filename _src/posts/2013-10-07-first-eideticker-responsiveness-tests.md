    Title: First Eideticker Responsiveness Tests
    Date: 2013-10-07T00:00:00
    Tags: Eideticker, Mozilla, Responsiveness


*[ For more information on the Eideticker software I&#8217;m referring to, see [this entry][1] ]*

Time for another update on Eideticker. In the last quarter, I&#8217;ve been working on two main items:

  1. Responsiveness tests (Android / FirefoxOS)
  2. Eideticker for FirefoxOS

The focus of this post is the responsiveness work. I&#8217;ll talk about Eideticker for FirefoxOS soon. 

So what do I mean by responsiveness? At a high-level, I mean how quickly one sees a response after performing an action on the device. For example, if I perform a swipe gesture to scroll the content down while browsing CNN.com, how long does it take after  
I start the gesture for the content to *visibly* scroll down? If you break it down, there&#8217;s a multi-step process that happens behind the scenes after a user action like this:

[<img src="/files/2013/10/input-events.png" alt="input-events" width="880" height="752" class="alignnone size-full wp-image-957" srcset="/files/2013/10/input-events-300x256.png 300w, /files/2013/10/input-events.png 880w" sizes="(max-width: 880px) 100vw, 880px" />][2]

If anywhere in the steps above, there is a significant delay, the user experience is likely to be bad. Usability research  
suggests that any lag that is consistently above 100 milliseconds will lead the user to [perceive things as being laggy][3]. To keep our users happy, we need to do our bit to make sure that we respond quickly at all levels that we control (just the application layer on Android, but pretty much everything on FirefoxOS). Even if we can&#8217;t complete the work required on our end to completely respond to the user&#8217;s desire, we should at least display something to acknowledge that things have changed.

But you can&#8217;t improve what you can&#8217;t measure. Fortunately, we have the means to do calculate of the time delta between *most* of the steps above. I learned from [Taras Glek][4] this weekend that it should be [possible to simulate][5] the actual capacitative touch event on a modern touch screen. We can recognize when the hardware event is available to be consumed by userspace by monitoring the \`/dev/input\` subsystem. And once the event reaches the application (the Android or FirefoxOS application) there&#8217;s no reason we can&#8217;t add instrumentation in all sorts of places to track the processing of both the event and the rendering of the response.

My working hypothesis is that it&#8217;s application-level latency (i.e. the time between the application receiving the event and being able to act on it) that dominates, so that&#8217;s what I decided to measure. This is purely based on intuition and by no means proven, so we should test this (it would certainly be an interesting exercise!). However, even if it turns out that there are significant problems here, we still care about the other bits of the stack &#8212; there&#8217;s lots of potentially-latency-introducing churn there and the risk of regression in our own code is probably higher than it is elsewhere since it changes so much.

Last year, I wrote up a tool called [Orangutan][6] that can directly inject input events into an input device on Android or FirefoxOS. It seemed like a fairly straightforward extension of the tool to output timestamps when these events were registered. It was. Then, by [synchronizing the time][7] between the device and the machine doing the capturing, we can then correlate the input timestamps to events. To help visualize what&#8217;s going on, I generated this view:

[<img src="/files/2013/10/taskjs-framediff-view.png" alt="taskjs-framediff-view" width="583" height="418" class="alignnone size-full wp-image-962" srcset="/files/2013/10/taskjs-framediff-view-300x215.png 300w, /files/2013/10/taskjs-framediff-view.png 583w" sizes="(max-width: 583px) 100vw, 583px" />][8]

[[Link to original]][9]

The X axis in that graph represents time. The Y-axis represents the difference between the frame at that time with the previous one in number of pixels. The &#8220;red&#8221; represents periods in capture when events are ongoing (we use different colours only to  
distinguish distinct events). <sup>[1]</sup>

For a first pass at measuring responsiveness, I decided to measure the time between the first event being initiated and there being a significant frame difference (i.e. an observable response to the action). You can see some preliminary results on the eideticker dashboard:

[<img src="/files/2013/10/taskjs-responsiveness.png" alt="taskjs-responsiveness" width="637" height="540" class="alignnone size-full wp-image-956" srcset="/files/2013/10/taskjs-responsiveness-300x254.png 300w, /files/2013/10/taskjs-responsiveness.png 637w" sizes="(max-width: 637px) 100vw, 637px" />][10]

[[Link to original]][11]

The results seem pretty highly variable at first because I was synchronizing time between the device and an external ntp server, rather than the host machine. I believe this is now fixed, hopefully giving us results that will indicate when regressions occur. As time goes by, we may want to craft some special eideticker tests for responsiveness specifically (e.g. a site where there is heavy javascript background processing).

<sup>[1]</sup> *Incidentally, these &#8220;frame difference&#8221; graphs are also quite useful for understanding where and how application startup has regressed in Fennec &#8212; try opening these two startup views side-by-side (before/after a large regression) and spot the difference: [[1]][12] and [[2]][13])*

 [1]: http://wrla.ch/blog/2012/06/mobile-firefox-measuring-how-a-browser-feels/
 [2]: /files/2013/10/input-events.png
 [3]: http://stackoverflow.com/questions/536300/what-is-the-shortest-perceivable-application-response-delay
 [4]: http://taras.glek.net/
 [5]: http://hackaday.com/2012/05/04/reaching-out-to-a-touch-screen-with-a-microcontroller/
 [6]: http://wrla.ch/blog/2012/07/the-evolution-of-simulating-events-in-eideticker-from-monkeys-to-orangutns/?utm_source=rss&#038;utm_medium=rss&#038;utm_campaign=the-evolution-of-simulating-events-in-eideticker-from-monkeys-to-orangutns
 [7]: http://wrla.ch/blog/2013/07/simple-command-line-ntp-client-for-android-and-firefoxos/
 [8]: /files/2013/10/taskjs-framediff-view.png
 [9]: http://eideticker.wrla.ch/framediff-view.html?title=Frame%20Difference%20Scrolling%20on%20taskjs.org%20%282013-10-06%29&#038;video=videos/video-1381129971.63.webm&#038;framediff=framediffs/framediff-1381129990.79.json&#038;actionlog=actionlogs/action-log-1381129990.79.json
 [10]: /files/2013/10/taskjs-responsiveness.png
 [11]: http://eideticker.mozilla.org/#/samsung-gn/taskjs/timetoresponse
 [12]: http://eideticker.wrla.ch/framediff-view.html?title=Frame%20Difference%20Startup%20to%20about:home%20%28dirty%20profile%29%20%282013-08-20%29&#038;video=videos/video-1377070981.95.webm&#038;framediff=framediffs/framediff-1377070991.95.json
 [13]: http://eideticker.wrla.ch/framediff-view.html?title=Frame%20Difference%20Startup%20to%20about:home%20%28dirty%20profile%29%20%282013-08-23%29&#038;video=videos/video-1377330042.28.webm&#038;framediff=framediffs/framediff-1377330051.67.json