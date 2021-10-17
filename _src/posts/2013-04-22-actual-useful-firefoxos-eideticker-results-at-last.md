    Title: Actual useful FirefoxOS Eideticker results at last
    Date: 2013-04-22T00:00:00
    Tags: Eideticker, FirefoxOS, Mozilla

Another update on getting [Eideticker working with FirefoxOS][1]. Once again this is sort of high-level, looking forward to writing something more in-depth soon now that we have the basics working.

I finally got the last kinks out of the rig I was using to capture live video from FirefoxOS phones using the Point Grey devices last week. In order to make things reasonable I had to write some custom code to isolate the actual device screen from the rest of capture and a few other things. The setup looks interesting (reminds me a bit of something out of the War of the Worlds):

[<img src="/files/2013/04/eideticker-pointgrey-mounted.jpg" alt="eideticker-pointgrey-mounted" width="512" height="683" class="alignnone size-full wp-image-894" srcset="/files/2013/04/eideticker-pointgrey-mounted-224x300.jpg 224w, /files/2013/04/eideticker-pointgrey-mounted.jpg 512w" sizes="(max-width: 512px) 100vw, 512px" />][2]

Here's some example video of a test I wrote up to measure the performance of contacts scrolling performance (measured at a very respectable 44 frames per second, in case you wondering):

<video src="/files/eideticker/contacts-scrolling-pointgrey.webm" controls></video>

Surprisingly enough, I didn't wind up having to write up any code to compensate for a noisy image. Of course there's a certain amount of variance in every frame depending on how much light is hitting the camera sensor at any particular moment, but apparently not enough to interfere with getting useful results in the tests I've been running.

Likely next step: Create some kind of chassis for mounting both the camera and device on a permanent basis (instead of an adhoc one on my desk) so we can start running these sorts of tests on a daily basis, much like we currently do with Android on the [Eideticker Dashboard][3].

As an aside, I've been really impressed with both the [Marionette][4] framework and the gaiatests python module that was written up for FirefoxOS. Writing the above test took just 5 minutes &#8212; and [the code][5] is quite straightforward. Quite the pleasant change from my various efforts in Android automation.

[1]: http://wrla.ch/blog/2013/02/eideticker-for-firefoxos/
[2]: /files/2013/04/eideticker-pointgrey-mounted.jpg
[3]: http://eideticker.wrla.ch
[4]: https://wiki.mozilla.org/Auto-tools/Projects/Marionette
[5]: https://github.com/mozilla/eideticker/blob/master/src/tests/b2g/appscrolling/scroll.py
