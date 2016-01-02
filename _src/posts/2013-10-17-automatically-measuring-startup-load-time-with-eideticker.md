    Title: Automatically measuring startup / load time with Eideticker
    Date: 2013-10-17T00:00:00
    Tags: Data Visualization, Eideticker, FirefoxOS, Mozilla


So we&#8217;ve been using Eideticker to automatically measure startup/pageload times for about a year now on Android, and more recently on FirefoxOS as well (albeit not automatically). This gives us nice and pretty graphs like this:

[<img src="/files/2013/10/flot-startup-times-gn.png" alt="flot-startup-times-gn" width="620" height="568" class="alignnone size-full wp-image-986" srcset="/files/2013/10/flot-startup-times-gn-300x274.png 300w, /files/2013/10/flot-startup-times-gn.png 620w" sizes="(max-width: 620px) 100vw, 620px" />][1]

Ok, so we&#8217;re generating numbers and graphing them. That&#8217;s great. But what&#8217;s really going on behind the scenes? I&#8217;m glad you asked. The story is a bit different depending on which platform you&#8217;re talking about.

**Android**

On Android we connect Eideticker to the device&#8217;s HDMI out, so we count on a nearly pixel-perfect signal. In practice, it isn&#8217;t quite, but it is within a few RGB values that we can easily filter for. This lets us come up with a pretty good mechanism for determining when a page load or app startup is finished: just compare frames, and say we&#8217;ve &#8220;stopped&#8221; when the pixel differences between frames are negligible (previously defined at 2048 pixels, now 4096 &#8212; see below). Eideticker&#8217;s new frame difference view lets us see how this works. Look at this graph of application startup:

[<img src="/files/2013/10/frame-difference-android-startup.png" alt="frame-difference-android-startup" width="803" height="514" class="alignnone size-full wp-image-973" srcset="/files/2013/10/frame-difference-android-startup-300x192.png 300w, /files/2013/10/frame-difference-android-startup.png 803w" sizes="(max-width: 803px) 100vw, 803px" />][2]  
[[Link to original]][3]

What&#8217;s going on here? Well, we see some huge jumps in the beginning. This represents the animated transitions that Android makes as we transition from the SUTAgent application (don&#8217;t ask) to the beginnings of the FirefoxOS browser chrome. You&#8217;ll notice though that there&#8217;s some more changes that come in around the 3 second mark. This is when the site bookmarks are fully loaded. If you load the original page (link above) and swipe your mouse over the graph, you can see what&#8217;s going on for yourself. 

This approach is not completely without problems. It turns out that there is sometimes some minor churn in the display even when the app is for all intents and purposes started. For example, [sometimes the scrollbar fading out of view can result in a significantish pixel value change][4], so I recently upped the threshold of pixels that are different from 2048 to 4096. We also recently encountered a [silly problem][5] with a random automation app displaying &#8220;toasts&#8221; which caused results to artificially spike. More tweaking may still be required. However, on the whole I&#8217;m pretty happy with this solution. It gives useful, undeniably objective results whose meaning is easy to understand.

**FirefoxOS**

So as mentioned previously, we use a camera on FirefoxOS to record output instead of HDMI output. Pretty unsurprisingly, this is much noisier. See this movie of the contacts app starting and note all the random lighting changes, for example:

<div style="width: 409px; " class="wp-video">
  <!--[if lt IE 9]><![endif]--><video class="wp-video-shortcode" id="video-972-1" width="409" height="580" preload="metadata" controls="controls"><source type="video/webm" src="/files/2013/10/contacts-b2g-aug30-load-taphomescreen1.webm?_=1" />
  
  <a href="/files/2013/10/contacts-b2g-aug30-load-taphomescreen1.webm">/files/2013/10/contacts-b2g-aug30-load-taphomescreen1.webm</a></video>
</div>

My experience has been that pixel differences can be so great between visually identical frames on an eideticker capture on these devices that it&#8217;s pretty much impossible to settle on when startup is done using the frame difference method. It&#8217;s of course possible to detect very large scale changes, but the small scale ones (like the contacts actually appearing in the example above) are very hard to distinguish from random differences in the amount of light absorbed by the camera sensor. Tricks like using median filtering (a.k.a. &#8220;blurring&#8221;) help a bit, but not much. Take a look at this graph, for example:

[<img src="/files/2013/10/plotly-contacts-load-pixeldiff.png" alt="plotly-contacts-load-pixeldiff" width="531" height="679" class="alignnone size-full wp-image-980" srcset="/files/2013/10/plotly-contacts-load-pixeldiff-234x300.png 234w, /files/2013/10/plotly-contacts-load-pixeldiff.png 531w" sizes="(max-width: 531px) 100vw, 531px" />][6]  
[[Link to original]][7]

You&#8217;ll note that the pixel differences during &#8220;static&#8221; parts of the capture are highly variable. This is because the pixel difference depends heavily on how &#8220;bright&#8221; each frame is: parts of the capture which are black (e.g. a contacts icon with a black background) have a much lower difference between them than parts that are bright (e.g. the contacts screen fully loaded).

After a day or so of experimenting and research, I settled on an approach which seems to work pretty reliably. Instead of comparing the frames directly, I measure the [entropy][8] of the [histogram][9] of colours used in each frame (essentially just an indication of brightness in this case, see [this article][10] for more on calculating it), then compare that of each frame with the average of the same measure over 5 previous frames (to account for the fact that two frames may be arbitrarily different, but that is unlikely that a sequence of frames will be). This seems to work much better than frame difference in this environment: although there are plenty of minute differences in light absorption in a capture from this camera, the overall color composition stays mostly the same. See this graph:

[<img src="/files/2013/10/plotly-contacts-load-entropy.png" alt="plotly-contacts-load-entropy" width="546" height="674" class="alignnone size-full wp-image-979" srcset="/files/2013/10/plotly-contacts-load-entropy-243x300.png 243w, /files/2013/10/plotly-contacts-load-entropy.png 546w" sizes="(max-width: 546px) 100vw, 546px" />][11]  
[[Link to original]][12]

If you look closely, you can see some minor variance in the entropy differences depending on the state of the screen, but it&#8217;s not nearly as pronounced as before. In practice, I&#8217;ve been able to get extremely consistent numbers with a reasonable &#8220;threshold&#8221; of &#8220;0.05&#8221;.

In Eideticker I&#8217;ve tried to steer away from using really complicated math or algorithms to measure things, unless all the alternatives fail. In that sense, I really liked the simplicity of &#8220;pixel differences&#8221; and am not thrilled about having to resort to this: hopefully the concepts in this case (histograms and entropy) are simple enough that most people will be able to understand my methodology, if they care to. Likely I will need to come up with something else for measuring responsiveness and animation smoothness (frames per second), as likely we can&#8217;t count on light composition changing the same way for those cases. My initial thought was to use [edge detection][13] (which, while somewhat complex to calculate, is at least easy to understand conceptually) but am open to other ideas.

 [1]: /files/2013/10/flot-startup-times-gn.png
 [2]: /files/2013/10/frame-difference-android-startup.png
 [3]: http://eideticker.wrla.ch/#/samsung-gn/startup-abouthome-dirty/timetostableframe
 [4]: https://bugzilla.mozilla.org/show_bug.cgi?id=922770
 [5]: https://bugzilla.mozilla.org/show_bug.cgi?id=926997
 [6]: /files/2013/10/plotly-contacts-load-pixeldiff.png
 [7]: https://plot.ly/~WilliamLachance/3
 [8]: http://en.wikipedia.org/wiki/Entropy
 [9]: http://en.wikipedia.org/wiki/Image_histogram
 [10]: http://brainacle.com/calculating-image-entropy-with-python-how-and-why.html
 [11]: /files/2013/10/plotly-contacts-load-entropy.png
 [12]: https://plot.ly/~WilliamLachance/5
 [13]: http://en.wikipedia.org/wiki/Edge_detection