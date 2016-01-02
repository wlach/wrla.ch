    Title: Measuring what the user sees
    Date: 2011-11-11T00:00:00
    Tags: Data Visualization, Free Software, Mozilla


I&#8217;ve been spending the last month or so at Mozilla prototyping a new project called [Eideticker][1] which aims to use video capture data and image/frame analysis for performance measurement of [Firefox Mobile][2]. It&#8217;s still in quite a rough state, but it&#8217;s now complete enough that I thought it would be worth spending a bit of time describing both its motivation and how it works.

First, a bit of an introduction. Up to now, our automated performance tools have used entirely synthetic benchmarks (how long til we get the onload event? how many ms since we last hit the main loop?) to gather performance information. As we&#8217;ve found out, there&#8217;s a lot you can measure with synthetic benchmarks. Tools like [Talos][3] have proven themselves by catching performance regressions on a very regular basis. 

Still, there&#8217;s many things that synthetic benchmarks can&#8217;t easily or reliably measure. For example, it&#8217;s nice to know that a page has triggered an &#8220;onload&#8221; event (and the sooner it does that, the better), but what does the browser look like before then? If it&#8217;s a complicated or image intensive page, it might take 10 or 15 seconds to load. In this interval, user studies have clearly shown that an application displaying *something* sooner rather than later is always desirable if it&#8217;s not possible to display everything immediately (due to network traffic, CPU constraints, whatever). It&#8217;s this area of user-perceived performance that Eideticker aims to help with. Eideticker creates a system to capture live data of what the browser is displaying, then performs image/frame analysis on the result to see how we&#8217;re actually doing on these inherently subjective metrics. The above was just one example, others might include:

  * Measuring amount of time it takes to actually see the start page from time of launch.
  * Measuring amount of time you see the checkboard pattern after panning the browser.
  * Measuring the visual artifacts while loading a complicated page (how long does it take to display something? how long until we get something close to the final expected result? how long until we get the actual final result?)

It turns out that it&#8217;s possible to put together a system that does this type of analysis using off-the-shelf components. We&#8217;re still very much in the early phase, but initial signs are promising. The initial test system has the following pieces:

  1. A Linux workstation equipped with a Decklink extreme 3D video capture card
  2. An Android phone with HDMI output (currently using the LG G2X)
  3. A version of talos modified to video capture the results of a test.
  4. A bit of python code to actually analyze the video capture data.

So far, I&#8217;ve got the system working end-to-end for two simple cases. The first is the &#8220;pageload&#8221; case. This lets you capture the results of loading any page within a talos pageset. Here&#8217;s a quick example of the movie we generate from a tsvg test:

<video src="http://people.mozilla.com/~wlachance/eideticker-map.webm" width="50%" height="50%" controls></video>

Here&#8217;s another example, a color cycle test (actually the first test case I created, as a throwaway):

<video src="http://people.mozilla.com/~wlachance/eideticker-colorcycle.webm" width="50%" height="50%" controls></video>

After the video is captured, the next step is to analyze it! As described above (and in further detail on the [Eideticker wiki page][1]), there&#8217;s lots of things we could measure but the easiest thing is probably just to count the number of unique frames and derive a frame rate for the capture based on that (the higher the better, obviously). Based on an initial prototype from Chris Jones, I&#8217;ve started work on a [python library][4] to do exactly this. Assuming you have an eideticker capture handy, you can run a tool called &#8220;analyze.py&#8221; on the command line, and it&#8217;ll give you its best guess of the # of unique frames:

`<br />
(eideticker)wlach@eideticker:~/src/eideticker$ bin/analyze.py  ./src/talos/talos/captures/capture-2011-11-11T11:23:51.627183.zip<br />
Unique frames: 121/272<br />
`

(There are currently some rough edges with this: we&#8217;re doing frame comparisons based on per-pixel changes, but the video capture data is slightly noisy so sometimes a pixel changes its value even when nothing has actually happened in the browser) 

So that&#8217;s what I&#8217;ve got working so far. What&#8217;s next? Short term, we have some [specific high-level goals][5] about where we want to be with the system by the end of the quarter. The big unfinished pieces are getting an end-to-end test involving real user interaction (typing into the URL bar, etc.) going and turning this prototype system into something that&#8217;s easy for others to duplicate and is robust enough to be easily extended. Hopefully this will come together fairly quickly now that the basics are in place.

The longer term picture really depends on feedback from the community. Unlike many of the projects we work on in [automation &#038; tools][6], Eideticker is **not** meant to be something that&#8217;s run on every checkin. Rather, it&#8217;s intended to be a useful tool that can be run on an as needed basis by developers and QA. We obviously have our own ideas on how something like this might be useful (and what a reasonable user interface might be), but I&#8217;ve found in cases like this it&#8217;s much better to go to the people who will actually be using this thing. So with that in mind, here&#8217;s a call for feedback. I have two very specific questions:

  * Is there a specific problem you&#8217;ve been working on that a framework like this might be helpful for?
  * What do you think of the current workflow model described in the [README][7]? 

My goal is to make something that people will love, so please do let me know what you think.  Nothing about this project is cast in stone and the last thing I want is to deliver a product that people don&#8217;t actually want to use. 

Equally, while Eideticker is being written primarily with the goal of making Mobile Firefox better (and in the slightly-less short term, desktop Firefox and [Boot to Gecko][8]), much of it is broadly applicable to any user-facing mobile or desktop application. If you think some component of Eideticker might be interesting to your project and want to collaborate, feel free to get in touch.

 [1]: https://wiki.mozilla.org/Project_Eideticker
 [2]: https://wiki.mozilla.org/Mobile/Fennec/Android
 [3]: https://wiki.mozilla.org/Buildbot/Talos
 [4]: https://github.com/mozilla/eideticker/blob/master/src/videocapture/videocapture/capture.py
 [5]: https://wiki.mozilla.org/Auto-tools/Goals/2011Q4#Eideticker
 [6]: https://wiki.mozilla.org/Auto-tools
 [7]: http://github.com/mozilla/eideticker/README.md
 [8]: https://github.com/andreasgal/B2G