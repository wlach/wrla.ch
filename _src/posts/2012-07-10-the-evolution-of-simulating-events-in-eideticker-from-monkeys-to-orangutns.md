    Title: The evolution of simulating events in Eideticker: from monkeys to orangutans
    Date: 2012-07-10T00:00:00
    Tags: Eideticker, Mozilla, Orangutan

_[ For more information on the Eideticker software I'm referring to, see [this entry][1] ]_

I just merged a new approach I've been using to simulate touch events into the master branch of Eideticker called [Orangutan][2].

<a href="http://wrla.ch/blog/2012/07/the-evolution-of-simulating-events-in-eideticker-from-monkeys-to-orangutns/orangutan/" rel="attachment wp-att-696"><img src="/files/2012/07/orangutan.jpg" alt="Image of Orangutan" title="orangutan" width="415" height="600" class="alignnone size-full wp-image-696" srcset="/files/2012/07/orangutan-207x300.jpg 207w, /files/2012/07/orangutan.jpg 415w" sizes="(max-width: 415px) 100vw, 415px" /></a>

As I've mentioned before, we really need to simulate actual user gestures when doing this type of testing to measure real-world performance with Eideticker. Up to now, I've been using google's [MonkeyRunner][3] tool to do this. I was always a little skeptical about its approach (which involved using a privileged tool written in Java with special access to Android's windowing system), but up until recently I'd managed to get around its [issues][4] with a [successively][5] [more][6] [complicated][7] series of hacks.

Unfortunately, I finally came up with a problem that I couldn't figure out how to fix: monkeyrunner doesn't attach precise timing information to the events it generates, which completely throws off Google Chrome for Android when you try to simulate a pan gesture. I've tried just about every way of using the existing functionality (both the networked mode and the "script" mode), but nothing seemed to help. My conclusion is that the only way of continuing to use monkey would be to create a fix for the software itself, which implies forking and extending the entire Android Open Source Project. As noble a goal as that might be, doing that across all the major Android versions I want to support (2.2, 2.3, 4.0 and now 4.1) was more work than I felt like taking on (not to mention the question of how to deploy that work). I decided to build something entirely new which did not have this requirement.

Enter Orangutan. Unlike MonkeyRunner, Orangutan simply injects events directly into low-level the kernel device file that represents an Android device's touch screen. It's fast (written in native C), trivial to build, and seems to work seamlessly with any application I've tried using it with (including Google Chrome for Android). Most interestingly for Mozilla, this interface is also present on Firefox OS ([Boot to Gecko][8]) based devices, so we should be able to use Orangutan there to support both Eideticker and any other testing framework which needs to test real-world user input test cases. Exciting times!

[1]: http://wrla.ch/blog/2012/06/mobile-firefox-measuring-how-a-browser-feels/
[2]: http://github.com/wlach/orangutan
[3]: http://developer.android.com/tools/help/monkeyrunner_concepts.html
[4]: http://code.google.com/p/android/issues/detail?id=27955
[5]: https://github.com/mozilla/eideticker/commit/8d034212bc38c1fc80b9fe792c0b06919c74141a
[6]: https://github.com/mozilla/eideticker/commit/55d63960dc0a5090cee00fe917a851db082ee0fd
[7]: https://github.com/mozilla/eideticker/commit/686882d32fb25a700afec35c39e53a73658688e3
[8]: https://wiki.mozilla.org/B2G
