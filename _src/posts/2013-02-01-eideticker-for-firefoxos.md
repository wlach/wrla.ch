    Title: Eideticker for FirefoxOS
    Date: 2013-02-01T00:00:00
    Tags: Eideticker, FirefoxOS, Mozilla


*[ For more information on the Eideticker software I&#8217;m referring to, see [this entry][1] ]*

Here&#8217;s a long overdue update on where we&#8217;re at with Eideticker for FirefoxOS. While we&#8217;ve had a good amount of success getting [useful, actionable data][2] out of Eideticker for Android, so far we haven&#8217;t been able to replicate that success for FirefoxOS. This is not for lack of trying: first, [Malini Das][3] and then me have been working at it since summer 2012.

When it comes right down to it, instrumenting Eideticker for B2G is just a whole lot more complex. On Android, we could take the operating system (including support for all the things we needed, like HDMI capture) as a given. The only tricky part was instrumenting the capture so the right things happened at the right moment. With FirefoxOS, we need to run these tests on entire builds of a whole operating system which was constantly changing. Not nearly as simple. That said, I&#8217;m starting to see light at the end of the tunnel.

**Platforms**

We initially selected the [pandaboard][4] as the main device to use for eideticker testing, for two reasons. First, it&#8217;s the same hardware platform we&#8217;re targeting for other b2g testing in tbpl (mochitest, reftest, etc.), and is the platform we&#8217;re using for running Gaia UI tests. Second, unlike every other device that we&#8217;re prototyping FirefoxOS on (to my knowledge), it has HDMI-out capability, so we can directly interface it with the Eideticker video capture setup.

However, the panda also has some serious shortcomings. First, it&#8217;s obviously not a platform we&#8217;re shipping, so the performance we&#8217;re seeing from it is subject to different factors that we might not see with a phone actually shipped to users. For the same reason, we&#8217;ve had many problems getting B2G running reliably on it, as it&#8217;s not something most developers have been hacking on a day to day basis. Thanks to the heroic efforts of Thomas Zimmerman, we&#8217;ve mostly got things working ok now, but it was a fairly long road to get here (several months last fall).

More recently, we became aware of something called an [Elmo][5] which might let us combine  
the best of both worlds. An elmo is really just a tiny mounted video camera with a bunch of outputs, and is I understand most commonly used to project documents in a classroom/presentation setting. However, it seems to do a great job of capturing mobile phones in action as well. 

<video width="400px" src="/files/eideticker/startup-test-elmo.webm" controls></video>

The nice thing about using an external camera for the video capture part of eideticker is that we are no longer limited to devices with HDMI out &#8212; we can run the standard set of automated tests on ANYTHING. We&#8217;ve already used this to some success in getting some videos of FirefoxOS startup times versus Android on the Unagi (a development phone that we&#8217;re using internally) for manual analysis. Automating this process may be trickier because of the fact that the video capture is no longer &#8220;perfect&#8221;, but we may be able to work around that (more discussion about this later).

**FirefoxOS web page tests**

These are the same tests we run on Android. They should give us an idea of roughly where our performance when browsing / panning web sites like CNN. So far, I&#8217;ve only run these tests on the Pandaboard and they are INCREDIBLY slow (like 1-3 frames per second when scrolling). So much so that I have to think there is something broken about our hardware acceleration on this platform.

**FirefoxOS application tests**

These are some new tests written in a framework that allows you to script arbitrary interactions in FirefoxOS, like launching applications or opening the task switcher.

I&#8217;m pretty happy with this. It seems to work well. The only problems I&#8217;m seeing with this is with the platform we&#8217;re running these tests on. With the pandaboard, applications look weird (since the screen resolution doesn&#8217;t remotely resemble the 320&#215;480 resolution on our current devices) and performance is abysmal. Take, for example, this capture of application switching performance, which operates only at roughly 3-4 fps:

<video width="400px" src="/files/eideticker/b2g-appswitching-video.webm" controls></video>

**So what now?**

I&#8217;m not 100% sure yet (partly it will depend on what others say as well as my own investigation), but I have a feeling that capturing video of real devices running FirefoxOS using the Elmo is the way forward. First, the hardware and driver situation will be much more representative of what we&#8217;ll actually be shipping to users. Second, we can flash new builds of FirefoxOS onto them automatically, unlike the pandaboards where you currently either need to manually flash and reset (a time consuming and error prone process) or set up an instance of [mozpool][6] (which I understand is quite complicated).

The main use case I see with eideticker-on-panda would be where we wanted to run a suite of tests on checkin (in tbpl-like fashion) and we&#8217;d need to scale to many devices. While cool, this sounds like an expensive project (both in terms of time and hardware) and I think we&#8217;d do better with getting something slightly smaller-scale running first.

So, the real question is whether or not the capture produced by the Elmo is amenable to the same analysis that we do on the raw HDMI output. At the very least, some of eideticker&#8217;s image analysis code will have to be adapted to handle a much &#8220;noisier&#8221; capture. As opposed to capturing the raw HDMI signal, we now have to deal with the real world and its irritating fluctuations in ambient light levels and all that the rest. I have no doubt it is \*possible\* to compensate for this (after all this is what the human eye/brain does all the time), but the question is how much work it will be. Can&#8217;t speak for anyone else at Mozilla, but I&#8217;m not sure if I really have the time to start a Ph.D-level research project in computational vision. 😉 I&#8217;m optimistic that won&#8217;t be necessary, but we&#8217;ll just have to wait and see.

 [1]: http://wrla.ch/blog/2012/06/mobile-firefox-measuring-how-a-browser-feels/
 [2]: http://eideticker.wrla.ch
 [3]: http://nakubu.com/
 [4]: http://pandaboard.org
 [5]: http://www.elmousa.com/
 [6]: https://github.com/djmitche/mozpool