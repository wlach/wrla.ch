    Title: A new meditation app
    Date: 2014-08-14T00:00:00
    Tags: Buddhism, FirefoxOS, Meditation, Mozilla, zen


I had some time on my hands two weekends ago and was feeling a bit of an itch to build something, so I decided to do a project I&#8217;ve had in the back of my head for a while: a meditation timer.

If you&#8217;ve been following this log, you&#8217;d know that [meditation][1] has been a pretty major interest of mine for the past year. The foundation of my practice is a daily round of seated meditation at home, where I have been attempting to follow the breath and generally try to connect with the world for a set period every day (usually varying between 10 and 30 minutes, depending on how much of a rush I&#8217;m in).

Clock watching is rather distracting while sitting so having a tool to notify you when a certain amount of time has elapsed is quite useful. Writing a smartphone app to do this is an obvious idea, and indeed approximately a zillion of these things have been written for Android and iOS. Unfortunately, most are not very good. Really, I just want something that does this:

  1. Select a meditation length (somewhere between 10 and 40 minutes).
  2. Sound a bell after a short preparation to demarcate the beginning of meditation.
  3. While the meditation period is ongoing, do a countdown of the time remaining (not strictly required, but useful for peace of mind in case you&#8217;re wondering whether you&#8217;ve really only sat for 25 minutes).
  4. Sound a bell when the meditation ends.

Yes, meditation can get more complex than that. In Zen practice, for example, sometimes you have several periods of varying length, broken up with kinhin (walking meditation). However, that mostly happens in the context of a formal setting (e.g. [a Zendo][2]) where you leave your smartphone at the door. Trying to shoehorn all that into an app needlessly complicates what should be simple.

Even worse are the apps which &#8220;chart&#8221; your progress or have other gimmicks to connect you to a virtual &#8220;community&#8221; of meditators. I have to say I find that kind of stuff really turns me off. Meditation should be about connecting with reality in a more fundamental way, not charting gamified statistics or interacting online. We already have way too much of that going on elsewhere in our lives without adding even more to it.

So, you might ask why the alarm feature of most clock apps isn&#8217;t sufficient? Really, it is most of the time. A specialized app can make selecting the interval slightly more convenient and we can preselect an appropriate bell sound up front. It&#8217;s also nice to hear something to demarcate the start of a meditation session. But honestly I didn&#8217;t have much of a reason to write this other than the fact than I could. Outside of work, I&#8217;ve been in a bit of a creative rut lately and felt like I needed to build something, anything and put it out into the world (even if it&#8217;s tiny and only a very incremental improvement over what&#8217;s out there already). So here it is:

[<img src="/files/2014/08/meditation-timer-screen.png" alt="meditation-timer-screen" width="320" height="483" class="alignnone size-full wp-image-1089" srcset="/files/2014/08/meditation-timer-screen-198x300.png 198w, /files/2014/08/meditation-timer-screen.png 320w" sizes="(max-width: 320px) 100vw, 320px" />][3]

The app was written entirely in HTML5 so it should work fine on pretty much any reasonably modern device, desktop or mobile. I tested it on my Nexus 5 (Chrome, Firefox for Android)<sup>[1]</sup>, FirefoxOS Flame, and on my laptop (Chrome, Firefox, Safari). It lives on a [subdomain of this site][4] or you can [grab it from the Firefox Marketplace][5] if you&#8217;re using some variant of Firefox (OS). The source, such as it is, [can be found][6] on github.

I should acknowledge taking some design inspiration from the [Mind application][7] for iOS, which has a similarly minimalistic take on things. Check that out too if you have an iPhone or iPad!

Happy meditating!

<sup>[1]</sup> Note that there isn&#8217;t a way to inhibit the screen/device from going to sleep with these browsers, which means that you might miss the ending bell. On FirefoxOS, I used the [requestWakeLock][8] API to make sure that doesn&#8217;t happen. I filed [a bug][9] to get this implemented on Firefox for Android.

 [1]: http://wrla.ch/blog/category/meditation/
 [2]: http://en.wikipedia.org/wiki/Zendo
 [3]: /files/2014/08/meditation-timer-screen.png
 [4]: http://meditation.wrla.ch
 [5]: https://marketplace.firefox.com/app/meditation/
 [6]: http://github.com/wlach/meditation
 [7]: http://helloform.com/projects/mind/
 [8]: https://developer.mozilla.org/en-US/docs/Web/API/Navigator.requestWakeLock
 [9]: https://bugzilla.mozilla.org/show_bug.cgi?id=1054113