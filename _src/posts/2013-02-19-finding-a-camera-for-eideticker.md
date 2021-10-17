    Title: Finding a camera for Eideticker
    Date: 2013-02-19T00:00:00
    Tags: Eideticker, FirefoxOS, Mozilla

_[ For more information on the Eideticker software I'm referring to, see [this entry][1] ]_

Ok, so as I mentioned [last time][2] I've been looking into making Eideticker work for devices without native HDMI output by capturing their output with some kind of camera. So far I've tried four different DSLRs for this task, which have all been inadequate for different reasons. I was originally just going to write an email about this to a few concerned parties, but then figured I may as well structure it into a blog post. Maybe someone will find it useful (or better yet, have some ideas.)

**Elmo MO-1**

This is the device I mentioned last time. Easy to set up, plays nicely with the Decklink capture card we're using for Eideticker. It seemed almost perfect, except for that:

1. The image quality is _really_ bad (beaten even by $200 standard digital camera). Tons of noise, picture quality really bad. Not \*necessarily\* a deal breaker, but it still sucks.
2. More importantly, there seems to be no way of turning off the auto white balance adjustment. This makes automated image analysis impossible if the picture changes, as is highlighted in this video:
   <video width="400px" src="/files/eideticker/elmo-white-balance-problem.webm" controls></video>

**Canon Rebel T4i**

This is the first camera that was recommended to me at the camera shop I've been going to. It does have an HDMI output signal, but it's not "clean". This [blog post][3] explains the details better than I could. Next.

**Nikon D600**

Supposedly does native clean 720p output, but unfortunately the [output is in a "box"][4] so isn't recognized by the Decklink cards that we're using (which insist on a full 1280&#215;720 HDMI signal to work). Next.

**Nikon D800**

It is possible to configure this one to not put a box around the output, so the Decklink card does recognize it. Except that the camera shuts off the HDMI signal whenever the input parameters change on the card or the signal input is turned on, which essentially makes it useless for Eideticker (this happens every time we start the Eideticker harness). Quite a shame, as the HDMI signal is quite nice otherwise.

&#8212;

To be clear, with the exception of the Elmo all the devices above seem like fine cameras, and should more than do for manual captures of B2G or Android phones (which is something we probably want to do anyway). But for Eideticker, we need something that works in automation, and none of the above fit the bill. I guess I could explore using a "real" video camera as opposed to a DSLR acting like one, though I suspect I might run into some of the same sorts of issues depending on how the HDMI output of those devices behaves.

Part of me wonders whether a custom solution wouldn't work better. How complicated could it be to construct your own digital camera anyway? 😉 Hook up a fancy camera sensor to a [pandaboard][5], get it to output through the HDMI port, and then we're set? Or better yet, maybe just get a fancy webcam like the [Playstation Eye][6] and hook it up directly to a computer? That would eliminate the need for our expensive video capture card setup altogether.

[1]: http://wrla.ch/blog/2012/06/mobile-firefox-measuring-how-a-browser-feels/
[2]: http://wrla.ch/blog/2013/02/eideticker-for-firefoxos/
[3]: http://www.hireacamera.com/blog/index.asp?post=canon-eos-650d--hdmi-explained
[4]: http://vimeo.com/49952287
[5]: http://pandaboard.org
[6]: http://en.wikipedia.org/wiki/PlayStation_Eye
