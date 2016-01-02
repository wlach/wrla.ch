    Title: Eideticker: Limitations in cross-browser performance testing
    Date: 2013-03-20T00:00:00
    Tags: Android, Eideticker, Mozilla


Last summer I [wrote a bit][1] about using [Eideticker][2] to measure the relative performance of Firefox for Android versus other browsers (Chrome, stock, etc.). At the time I was pretty optimistic about Eideticker&#8217;s usefulness as a truly &#8220;objective&#8221; measure of user experience that would give us a more accurate view of how we compared against the competition than traditional benchmarking suites (which more often than not, measure things that a user will never see normally when browsing the web). Since then, there&#8217;s been some things that I&#8217;ve discovered, as well as some developments in terms of the &#8220;state of the art&#8221; in mobile browsing that have caused me to reconsider that view &#8212; while I haven&#8217;t given up entirely on this concept (and I&#8217;m still very much convinced of eideticker&#8217;s utility as an internal benchmarking tool), there&#8217;s definitely some limitations in terms of what we can do that I&#8217;m not sure how to overcome. 

Essentially, there are currently three different types of Eideticker performance tests:

  * Animation tests: Measure the smoothness of an animation by comparing frames and seeing how many are different. Currently the only example of this is the [canvas &#8220;clock&#8221; test][3], but many others are possible.
  * Startup tests: Measure the amount of time it takes from when the application is launched to when the browser is fully running/available. There are currently two variants of this test in the dashboard, both measure the amount of time taken to fully render Firefox&#8217;s home screen (the only difference between the two is whether the browser profile is fully initialized). The [dirty profile][4] benchmark probably most closely resembles what a user would usually experience.
  * Scrolling tests: Measure the amount of undrawn areas when the user is panning a website. Most of the current eideticker tests are of this kind. A good example of this is the [taskjs benchmark][5].

In this blog post, I&#8217;m going to focus on startup and scrolling tests. Animation tests are interesting, but they are also generally the sorts of tests that are easiest to measure in synthetic ways (e.g. by putting a frame counter in your javascript code) and have thus far not been a huge focus for Eideticker development.

As it turns out, it&#8217;s unfortunately been rather difficult to create truly objective tests which measure the difference between browsers in these two categories. I&#8217;ll go over them in order.

**Startup tests**

There are essentially two types of startup tests: one where you measure the amount of time to get to the browser&#8217;s home screen when you explicitly launch the app (e.g. by pressing the Firefox icon in the app chooser), another where you load a web page in a browser from another app (e.g. by clicking on a link in the Twitter application).

The first is actually fairly easy to test across browsers, although we are not currently. There&#8217;s not really a good reason for that, it was just an oversight, so I filed [bug 852744][6] to add something like this.

The second case (startup to the browser&#8217;s homescreen) is a bit more difficult. The problem here is that, in a nutshell, an apples to apples comparison is very difficult if not impossible simply because different browsers do different things when the user presses the application icon. Here&#8217;s what we see with Firefox:

<img src="/files/eideticker/firefox-startup.png" style="width:25%;" />

And here&#8217;s what we see with Chrome:

<img src="/files/eideticker/chrome-startup.png" style="width:25%;" />

And here&#8217;s what we see with the stock browser:

<img src="/files/eideticker/stock-startup.png" style="width:25%;" />

As you can see Chrome and the stock browser are totally different: they try to &#8220;restore&#8221; the browser back to its state from the last time (in Chrome&#8217;s case, I was last visiting taskjs.org, in Stock&#8217;s case, I was just on the homepage).

Personally I prefer Firefox&#8217;s behaviour (generally I want to browse somewhere new when I press the icon on my phone), but that&#8217;s really beside the point. It&#8217;s possible to hack around what chrome is doing by restoring the profile between sessions to some sort of clean &#8220;new tab&#8221; state, but at that point you&#8217;re not really reproducing a realistic user scenario. Sure, we can draw a comparison, but how valid is it really? It seems to me that the comparison is mostly only useful in a very broad &#8220;how quickly does the user see something useful&#8221; sense.

**Panning tests**

I had quite a bit of hope for these initially. They seemed like a place where Eideticker could do something that conventional benchmarking suites couldn&#8217;t, as things like panning a web page are not presently possible to do in JavaScript. The main measure I tried to compare against was something called &#8220;checkerboarding&#8221;, which essentially represents the amount of time that the user waits for the page to redraw when panning around.

At the time that I wrote these tests, most browsers displayed regions that were not yet drawn while panning using the page background. We figured that it would thus be possible to detect regions of the page which were not yet drawn by looking for the background color while initiating a panning action. I thus hacked up existing web pages to have a magenta background, then wrote some image analysis code to detect regions that were that color (under the assumption that magenta is only rarely seen in webpages). It worked pretty well.

The world&#8217;s moved on a bit since I wrote that: modern browsers like Chrome and Firefox use something like progressive drawing to display a lower resolution &#8220;tile&#8221; where possible in this case, so the user at least sees something resembling the actual page while panning on a slower device. To see what I mean, try visiting a slow-to-render site like taskjs.org and try panning down quickly. You should see something like this (click to expand):

[<img src="/files/eideticker/firefox-partialy-drawn.png" style="width:50%;" />][7]

Unfortunately, while this is certainly a better user experience, it is not so easy to detect and measure.  For Firefox, we&#8217;ve disabled this behaviour so that we see the old checkerboard pattern. This is useful for our internal measurements (we can see both if our drawing code as well as our heuristics about when to draw are getting better or worse over time) but it only works for us.

If anyone has any suggestions on what to do here, let me know as I&#8217;m a bit stuck. There are other metrics we could still compare against (i.e. how smooth is the panning animation aka frames per second?) but these aren&#8217;t nearly as interesting.

 [1]: http://wrla.ch/blog/2012/06/mobile-firefox-measuring-how-a-browser-feels/
 [2]: https://wiki.mozilla.org/Project_Eideticker
 [3]: http://eideticker.wrla.ch/#/samsung-gn/clock/fps
 [4]: http://eideticker.wrla.ch/#/samsung-gn/startup-abouthome-dirty/timetostableframe
 [5]: http://eideticker.wrla.ch/#/samsung-gn/taskjs/fps
 [6]: https://bugzilla.mozilla.org/show_bug.cgi?id=852744
 [7]: /files/eideticker/firefox-partialy-drawn.png