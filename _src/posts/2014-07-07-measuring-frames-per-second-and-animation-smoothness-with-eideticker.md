    Title: Measuring frames per second and animation smoothness with Eideticker
    Date: 2014-07-07T00:00:00
    Tags: Eideticker, FirefoxOS, Mozilla

_[ For more information on the Eideticker software I'm referring to, see [this entry][1] ]_

Just wanted to write up a few notes on using Eideticker to measure animation smoothness, since this is a topic that comes up pretty often and I wind up explaining these things repeatedly. 😉

When rendering web content, we want the screen to update something like 60 times per second (typical refresh rate of an LCD screen) when an animation or other change is occurring. When this isn't happening, there is often a user perception of jank (a.k.a. things not working as they should). Generally we express how well we measure up to this ideal by counting the number of "frames per second" that we're producing. If you're reading this, you're probably already familiar with the concept in outline. If you want to know more, you can check out the [wikipedia article][2] which goes into more detail.

At an internal level, this concept matches up conceptually with what Gecko is doing. The graphics pipeline produces frames inside graphics memory, which is then sent to the LCD display (whether it be connected to a laptop or a mobile phone) to be viewed. By instrumenting the code, we can see how often this is happening, and whether it is occurring at the right frequency to reach 60 fps. My understanding is that we have at least some code which does exactly this, though I'm not 100% up to date on how accurate it is.

But even assuming the best internal system monitoring, Eideticker might still be useful because:

- It is more "objective". This is valuable not only for our internal purposes to validate other automation (sometimes internal instrumentation can be off due to a bug or whatever), but also to "prove" to partners that our software has the performance characteristics that we claim.
- The visual artifacts it leaves behind can be valuable for inspection and debugging. i.e. [you can correlate videos with profiling information][3].

Unfortunately, deriving this sort of information from a video capture is more complicated than you'd expect.

**What does frames per second even mean?**

Given a set of N frames captured from the device, the immediate solution when it comes to "frames per second" is to just compare frames against each other (e.g. by comparing the value of individual pixels) and then counting the ones that are different as "unique frames". Divide the total number of unique frames by the length of the  
capture and... voila? Frames per second? Not quite.

First off, there's the inherent problem that sometimes the expected behaviour of a test is for the screen to be unchanging for a period of time. For example, at the very beginning of a capture (when we are waiting for the input event to be acknowledged) and at the end (when we are waiting for things to settle). Second, it's also easy to imagine the display remaining static for a period of time in the middle of a capture (say in between gestures in a multi-part capture). In these cases, there will likely be no observable change on the screen and thus the number of frames counted will be artificially low, skewing the frames per second number down.

**Measurement problems**

Ok, so you might not consider that class of problem that big a deal. Maybe we could just not consider the frames at the beginning or end of the capture. And for pauses in the middle, as long as we get an absolute number at the end, we're fine right? That's at least enough to let us know that we're getting better or worse, assuming that whatever we're testing is behaving the same way between runs and we're just trying to measure how many frames hit the screen.

I might agree with you there, but there's a further problems that are specific to measuring on-screen performance using a high-speed camera as we are currently with FirefoxOS.

An LCD updates gradually, and not all at once. Remnants of previous frames will remain on screen long past their interval. Take for example these five frames (sampled at 120fps) from a capture of a pan down in the FirefoxOS Contacts application ([movie][4]):

[<img src="/files/2014/07/sidebyside-1024x263.png" alt="sidebyside" width="474" height="121" class="alignnone size-large wp-image-1074" srcset="/files/2014/07/sidebyside-300x77.png 300w, /files/2014/07/sidebyside-1024x263.png 1024w" sizes="(max-width: 474px) 100vw, 474px" />][5]

Note how if you look closely these 5 frames are actually the intersection of \*three\* seperate frames. One with "Adam Card" at the top, another with "Barbara Bloomquist" at the top, then another with "Barbara Bloomquist" even further up. Between each frame, artifacts of the previous one are clearly visible.

Plausible sounding solutions:

- Try to resolve the original images by distinguishing "new" content from ghosting artifacts. Sounds possible, but probably hard? I've tried a number of simplistic techniques (i.e. trying to find times when change is "peaking"), but nothing has really worked out very well.
- Somehow reverse engineering the interface between the graphics chipset and the LCD panel, and writing some kind of custom hardware to "capture" the framebuffer as it is being sent from one to the other. Also sounds difficult.
- Just forget about this problem altogether and only try to capture periods of time in the capture where the image has stayed static for a sustained period of time (i.e. for say 4-5 frames and up) and we're pretty sure it's jank.

Personally the last solution appeals to me the most, although it has the obvious disadvantage of being a "homebrew" metric that no one has ever heard of before, which might make it difficult to use to prove that performance is adequate &#8212; the numbers come with a long-winded explanation instead of being something that people immediately understand.

[1]: http://wrla.ch/blog/2012/06/mobile-firefox-measuring-how-a-browser-feels/
[2]: http://en.wikipedia.org/wiki/Frame_rate
[3]: http://wrla.ch/blog/2012/09/more-eideticker-happenings-profiling-and-startup-testing/
[4]: /files/2014/07/movie.webm
[5]: /files/2014/07/sidebyside.png
