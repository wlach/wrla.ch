    Title: It&#8217;s all about the entropy
    Date: 2014-03-14T00:00:00
    Tags: Data Visualization, Eideticker, FirefoxOS, Mozilla


*[ For more information on the Eideticker software I&#8217;m referring to, see [this entry][1] ]*

So recently I&#8217;ve been exploring new and different methods of measuring things that we care about on FirefoxOS &#8212; like startup time or amount of [checkerboarding][2]. With Android, where we have a mostly clean signal, these measurements were pretty straightforward. Want to measure startup times? Just capture a video of Firefox starting, then compare the frames pixel by pixel to see how much they differ. When the pixels aren&#8217;t that different anymore, we&#8217;re &#8220;done&#8221;. Likewise, to measure checkerboarding we just calculated the areas of the screen where things were not completely drawn yet, frame-by-frame.

On FirefoxOS, where we&#8217;re using a camera to measure these things, it has not been so simple. I&#8217;ve already discussed this with respect to startup time in a [previous post][3]. One of the ideas I talk about there is &#8220;entropy&#8221; (or the amount of unique information in the frame). It turns out that this is a pretty deep concept, and is useful for even more things than I thought of at the time. Since this is probably a concept that people are going to be thinking/talking about for a while, it&#8217;s worth going into a little more detail about the math behind it.

The [wikipedia article][4] on information theoretic entropy is a pretty good introduction. You should read it. It all boils down to this formula:

<img src="/files/2014/03/wikipedia-entropy-formula.png" alt="wikipedia-entropy-formula" width="401" height="37" class="alignnone size-full wp-image-1014" srcset="/files/2014/03/wikipedia-entropy-formula-300x27.png 300w, /files/2014/03/wikipedia-entropy-formula.png 401w" sizes="(max-width: 401px) 100vw, 401px" />

You can see this section of the wikipedia article (and the various articles that it links to) if you want to break down where that comes from, but the short answer is that given a set of random samples, the more different values there are, the higher the entropy will be. Look at it from a probabilistic point of view: if you take a random set of data and want to make predictions on what future data will look like. If it is highly random, it will be harder to predict what comes next. Conversely, if it is more uniform it is easier to predict what form it will take.

Another, possibly more accessible way of thinking about the entropy of a given set of data would be &#8220;how well would it compress?&#8221;. For example, a bitmap image with nothing but black in it could compress very well as there&#8217;s essentially only 1 piece of unique information in it repeated many times &#8212; the black pixel. On the other hand, a bitmap image of completely randomly generated pixels would probably compress very badly, as almost every pixel represents several dimensions of unique information. For all the statistics terminology, etc. that&#8217;s all the above formula is trying to say.

So we have a model of entropy, now what? For Eideticker, the question is &#8212; how can we break the frame data we&#8217;re gathering down into a form that&#8217;s amenable to this kind of analysis? The approach I took (on the recommendation of [this article][5]) was to create a histogram with 256 bins (representing the number of distinct possibilities in a black &#038; white capture) out of all the pixels in the frame, then run the formula over that. The exact function I wound up using looks like this:

    
    def _get_frame_entropy((i, capture, sobelized)):
        frame = capture.get_frame(i, True).astype('float')
        if sobelized:
            frame = ndimage.median_filter(frame, 3)
    
            dx = ndimage.sobel(frame, 0)  # horizontal derivative
            dy = ndimage.sobel(frame, 1)  # vertical derivative
            frame = numpy.hypot(dx, dy)  # magnitude
            frame *= 255.0 / numpy.max(frame)  # normalize (Q&D)
    
        histogram = numpy.histogram(frame, bins=256)[0]
        histogram_length = sum(histogram)
        samples_probability = [float(h) / histogram_length for h in histogram]
        entropy = -sum([p * math.log(p, 2) for p in samples_probability if p != 0])
    
        return entropy
    
    

[[Context]][6]

The &#8220;sobelized&#8221; bit allows us to optionally convolve the frame with a sobel filter before running the entropy calculation, which removes most of the data in the capture except for the edges. This is especially useful for FirefoxOS, where the signal has quite a bit of random noise from ambient lighting that artificially inflate the entropy values even in places where there is little actual &#8220;information&#8221;.

This type of transformation often reveals very interesting information about what&#8217;s going on in an eideticker test. For example, take this video of the user panning down in the contacts app: 

<div style="width: 640px; " class="wp-video">
  <video class="wp-video-shortcode" id="video-1012-2" width="640" height="917" preload="metadata" controls="controls"><source type="video/webm" src="/files/2014/03/contacts-scrolling-movie.webm?_=2" /><a href="/files/2014/03/contacts-scrolling-movie.webm">/files/2014/03/contacts-scrolling-movie.webm</a></video>
</div>

If you graph the entropies of the frame of the capture using the formula above you, you get a graph like this:

[<img src="/files/2014/03/contacts-scrolling-entropy-graph.png" alt="contacts scrolling entropy graph" width="933" height="482" class="alignnone size-full wp-image-1022" srcset="/files/2014/03/contacts-scrolling-entropy-graph-300x154.png 300w, /files/2014/03/contacts-scrolling-entropy-graph.png 933w" sizes="(max-width: 933px) 100vw, 933px" />][7]  
[[Link to original]][8]

The Y axis represents entropy, as calculated by the code above. There is no inherently &#8220;right&#8221; value for this &#8212; it all depends on the application you&#8217;re testing and what you expect to see displayed on the screen. In general though, higher values are better as it indicates more frames of the capture are &#8220;complete&#8221;. 

The region at the beginning where it is at about 5.0 represents the contacts app with a set of contacts fully displayed (at startup). The &#8220;flat&#8221; regions where the entropy is at roughly 4.25? Those are the areas where the app is &#8220;checkerboarding&#8221; (blanking out waiting for graphics or layout engine to draw contact information). Click through to the original and swipe over the graph to see what I mean. 

It&#8217;s easy to see what a hypothetical ideal end state would be for this capture: a graph with a smooth entropy of about 5.0 (similar to the start state, where all contacts are fully drawn in). We can track our progress towards this goal (or our deviation from it), by watching the eideticker b2g dashboard and seeing if the summation of the entropy values for frames over the entire test increases or decreases over time. If we see it generally increase, that probably means we&#8217;re seeing less checkerboarding in the capture. If we see it decrease, that might mean we&#8217;re now seeing checkerboarding where we weren&#8217;t before.

It&#8217;s too early to say for sure, but over the past few days the trend has been positive:

[<img src="/files/2014/03/entropy-levels-climbing.png" alt="entropy-levels-climbing" width="822" height="529" class="alignnone size-full wp-image-1025" srcset="/files/2014/03/entropy-levels-climbing-300x193.png 300w, /files/2014/03/entropy-levels-climbing.png 822w" sizes="(max-width: 822px) 100vw, 822px" />][9]  
[[Link to original]][10]

(note that there were some problems in the way the tests were being run before, so results before the 12th should not be considered valid)

So one concept, at least two relevant metrics we can measure with it (startup time and checkerboarding). Are there any more? Almost certainly, let&#8217;s find them!

 [1]: http://wrla.ch/blog/2012/06/mobile-firefox-measuring-how-a-browser-feels/
 [2]: http://www.masonchang.com/blog/2014/3/2/wow-such-checkerboard
 [3]: http://wrla.ch/blog/2013/10/automatically-measuring-startup-load-time-with-eideticker/
 [4]: http://en.wikipedia.org/wiki/Shannon_entropy
 [5]: http://brainacle.com/calculating-image-entropy-with-python-how-and-why.html
 [6]: https://github.com/mozilla/eideticker/blob/master/src/videocapture/videocapture/entropy.py#L10
 [7]: /files/2014/03/contacts-scrolling-entropy-graph.png
 [8]: http://eideticker.wrla.ch/b2g/detail.html?id=3f7b7c88a9ed11e380c5f0def1767b24#/framesobelentropies
 [9]: /files/2014/03/entropy-levels-climbing.png
 [10]: http://eideticker.wrla.ch/b2g/#/inari/b2g-contacts-scrolling/overallentropy