    Title: Eideticker update
    Date: 2011-12-08T00:00:00
    Tags: Data Visualization, Mozilla


Since I last [blogged][1] about Eideticker, I&#8217;ve made some good progress. Here&#8217;s some highlights:

  1. Eideticker has a new, [much simpler harness][2] and tests are much easier to write. Initially, I was using [Talos][3] for this task with the idea that it&#8217;s better not to have duplicate code where it&#8217;s not really required. Seemed like a fine idea in principle, but in practice Talos&#8217;s architecture (which is really oriented around running a large sequence of tests and uploading the results to a central server) was difficult to extend to do what we need to do. At heart, eideticker really only needs to do a few things right now (start up Firefox, start videocapture, load a webpage, stop videocapture) so it&#8217;s best to keep things simple.
  2. I&#8217;ve reworked the capture analysis API to use [numpy][4] behind the scenes. It&#8217;s still not quite as fast as I would like (doing a framediff analysis on a 30 second animation still takes a minute or so on my fast machine), but we&#8217;re doing an order of magnitude better than before. numpy also seem to have quite the library of routines for doing the types of matrix algebra useful in image analysis, which should be helpful as the project progresses.
  3. I added the beginnings of a fancy pants web interface for browsing captures and doing visualizations on them! I&#8217;m pretty happy with how this is turning out so far, it&#8217;s already been an incredibly useful tool for debugging Eideticker&#8217;s analysis system and I think it will be equally useful for understanding Firefox&#8217;s behaviour in general.

Here&#8217;s an example analysis session, where I examine a ~60 second capture of the fishtank demo from Microsoft, borrowed from Mark Cote&#8217;s [speedtest][5] library. You might want to view this fullscreen:

<video src="/files/eideticker/eideticker-20111207.webm" width="600px" controls></video>

A few interesting things to note about this capture:

1. Our frame comparison algorithm is still comparatively dumb, it just computes the norm of the difference in RGB values between two frames. Since there&#8217;s a (very tiny) amount of noise in the capture, we have to use a threshold to determine whether two frames are the same or not. For all that, the FPS estimate it comes with for the fishtank demo seems about right (and unfortunately at 2 fps, it&#8217;s not particularly good).  
2. I added a green screen / red screen at the start / end of every capture to eliminate race conditions with starting the capture, but haven&#8217;t yet actually taken those frames out of the analysis.  
3. If you look carefully at the animation, not all of the fish that should be displaying in the demo are. I think this has to do with the new native version of Fennec that I&#8217;m using to test (old versions don&#8217;t exhibit this property). I filed [a bug][6] for this.

What&#8217;s next? Well, as I mentioned last time, the real goal is to create a tool that developers will find useful. To that end, we have plans to set up an Eideticker machine in Mozilla Mountain View office that more people can use (either locally or remotely over the VPN). For this to be workable, I need to figure out how to get the full setup working on &#8220;demand&#8221;. Most of the setup already allows this, with one big exception: the actual Android device that we want to capture video from. The LG G2X that I&#8217;m currently using works fine when I have physical access to it, but as far as I can tell it&#8217;s not possible to get it outputting proper video of an application unless it&#8217;s in an unlocked state (which it obviously isn&#8217;t most of the time). 

My current thinking is that a [Panda Board][7] running a Vanilla version of Android might be a good candidate for a permanently-connected device. It is capable of HDMI output, doesn&#8217;t have unwanted the bells and whistles of a physical phone (e.g. a lock screen), and should be much reliable due to its physical networking. So far I haven&#8217;t [had much luck][8] getting it the video output working with the Decklink capture card, but I&#8217;ve only just started trying. Work will continue.

If I can somehow figure that out, and smooth out some of the rough edges with the web interface and capture API, I think the stage will be set for us all to do some pretty interesting stuff! Looking forward to it.

 [1]: http://wrla.ch/blog/2011/11/measuring-what-the-user-sees/
 [2]: https://github.com/mozilla/eideticker/blob/master/bin/runtest.py
 [3]: https://wiki.mozilla.org/Buildbot/Talos
 [4]: http://numpy.scipy.org
 [5]: http://brasstacks.mozilla.com/speedtests/results.html
 [6]: https://bugzilla.mozilla.org/show_bug.cgi?id=708633
 [7]: http://pandaboard.org/
 [8]: http://ask.linaro.org/questions/361/hdmi-output-on-android-build