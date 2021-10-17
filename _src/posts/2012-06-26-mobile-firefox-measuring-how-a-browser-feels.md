    Title: Mobile Firefox: Measuring How a Browser Feels
    Date: 2012-06-26T00:00:00
    Tags: Eideticker, Mozilla

> A while back, I began work on a new test framework for mobile browsers called Eideticker, which aims to benchmark browsers by capturing them on HMDI video, then running image analysis on the result. I wrote about this in a blog post entitled, “[Measuring what the user sees][1].” Some seven months later, we are about to release a new version of Firefox for Android and Eideticker has played a major role in qualifying its performance and identifying areas for improvement along the way.

I thought it would be worth publicizing some of the results that we have seen so far and explain why Eideticker has been useful. This post aims to explain the ideas behind Eideticker and hopes to inspire ideas on how to further improve objective cross-browser benchmarks.

**Idea 1: Put cross-browser performance tests on a more rigorous footing**

One of the problems with existing benchmarks is that the graphical performance that they measure is entirely synthetic. So when something like Microsoft's fishbowl demo claims 50 frames per second, that is based entirely on an internal measurement. There is no guarantee that is what the user is actually seeing. For all we know, it could be throwing half those frames away. To say nothing of the fact that measuring the results could interfere with the results themselves!

With Eideticker, we only analyze what the user sees (under the assumption that what the user sees is what comes out of the device's HDMI out). To measure frame rate, Eideticker painstakingly analyzes a video capture to see the difference between each frame. Only if one frame is qualitatively different than the one before it will it consider it to be a step forward in the animation progression. There is no room for a browser to "cheat" by, for example, throwing a frame away. Here are two example frames from an Eideticker capture of an animated clock, along with a visual representation of the difference it measured between them:

<table style="border:none;">
  <tr>
    <td>
      <image width="150px" src="/files/2012/06/clock1.png">
    </td>
    
    <td>
      <image width="150px" src="/files/2012/06/clock2.png">
    </td>
    
    <td>
      <image width="150px" src="/files/2012/06/clockdiff.png">
    </td>
  </tr>
</table>

&nbsp;

</table>

_Note: The red area of the graphic on the right indicates a region that Eideticker has detected as having changed between the two images. The black area of the graphic indicates a region that is unchanged._

Seeing visual evidence like this increases our confidence that things are truly better than they were before. For example, Eideticker very clearly, and accurately, measured the improvement when [Off Main Thread Compositing][2] landed. We saw a big performance jump in the afore-mentioned clock benchmark:  
<image src="/files/2012/06/canvas-clock-jump-highlighted.png">  
&nbsp;

&nbsp;  
_Note: Nightly = the new Firefox for Android as of that date (an incremental step towards what was just released), XUL = Previous Firefox for Android, Stock = Default browser that comes with Android 2.2._

**Idea 2: Measure subjective performance based on actual user interaction patterns**

Measuring real browser output is useful, but the problem is that these benchmarks do not actually measure how a user experiences the Web. Does an animated image of a clock or a [fishtank][3] actually represent a normal user experience? Thanks to the development of mobile gaming, this is slowly changing, but I was still say “no.”  The majority of users time spent mobile browsing is spent on news websites, Wikipedia, Facebook and I Can Haz Cheezburger. [][4] For these sites, I would submit that there are two things users care about:

1. When I swipe to move the content (e.g. to scroll down to see more content on [CNN.com][5]), does it respond instantaneously and in a pleasing manner? Do I see a nice smooth animation or a jerky mess?

2. When the content moves, do I see new content right away? Or do I have to wait a few moments while the view updates (this slow load is also called checkerboarding)?

&nbsp;  
I think the key here is to measure what the user sees. Internal measurements for anything other than what the user experiences are misleading and inconsistent across browsers.

For the first item, I believe the best indication of perceived responsiveness and smoothness is found by measuring the number of frames that are displayed in response to user interaction. As with all measurements, it is not perfect, but one can safely say that if there are only a few frames changed in response to a swipe, the experience is going to be jerky.

Compare these two videos of panning on [CNN.com][5]. The first is the previous Firefox for Android, clocking in at about 12.3 frames per second (fps). The second is the recent Firefox for Android , clocking in at 23 fps using Eideticker's internal measurements:

&nbsp;

<table style="border: none;">
  <tr>
    <td>
      <video width="200px" height="240" src="/files/2012/06/xul-fennec-cnn.webm" controls="controls"> </video>
    </td>
    
    <td>
      <video width="200px" height="240" src="/files/2012/06/native-fennec-cnn.webm" controls="controls"> </video>
    </td>
  </tr>
</table>

For the second, we can easily measure how quickly a user sees content by setting the background color of the page to an obvious color (in Eideticker we use magenta), overlaying an image on top, then measuring the amount of the page that is magenta while panning around. Since all modern browsers just use the background color of the page when something is to be redrawn (or at least can be configured that way), it's easy to compare across browsers. You can see in the videos above that the new Native Firefox does much better than the old one in this regard, at least on this benchmark. Here's an image of Eideticker detecting checkerboarding on a capture (red indicates checkerboarded areas):

<table style="border:none;">
  <tr>
    <td>
      <image width="200px" src="/files/2012/06/checkerboard-page.png">
    </td>
    
    <td>
      <image width="200px" src="/files/2012/06/checkerboard-analysis.png">
    </td>
  </tr>
</table>

</table>

<table style="border: none;">
  <tr>
    <td>
    </td>
    
    <td>
    </td>
  </tr>
</table>

_Note: The red area of the graphic on the right indicates a region that Eideticker has detected as checkerboarded (i.e. undrawn). The black area of the graphic indicates a region that is fully drawn._

The important thing in both cases is that these captures represent **a real user experience**. The swipe gestures are synthesized such that they are interpreted by Android as an actual touch event. This is important: using tricks like [javascript scrollTo][6] inside your Web page to pan would not actually engage the renderer in quite the same way. On Firefox for Android (and probably other browsers as well, though I haven't checked), the response to a touch event is always handled inside the browser internal rendering engine to give the expected "physical feel." Manually moving the viewport would give completely different results since so much of the fancy code we use to reduce the redraw delay would not be engaged.

**Conclusion**

Overall, I am very happy with how Eideticker has allowed us to track and measure improvements in Firefox for Android. In developing Eideticker, we aimed to create a benchmark that measured how users actually interact with a browser – not how abstract measurements claim how great a browser is.  As we move ahead with new projects to improve Firefox for Android, Eideticker will continue to be useful in making sure that using our browser is the best experience that it can be, especially combined with other tools like Benoit Girard's [sampling profiler][7].

For more information on Eideticker, feel free to visit [its homepage][8] on [wiki.mozilla.org][9].

&nbsp;

[1]: http://wrla.ch/blog/2011/11/measuring-what-the-user-sees/
[2]: http://benoitgirard.wordpress.com/2012/05/15/off-main-thread-compositing-omtc-and-why-it-matters/
[3]: http://ie.microsoft.com/testdrive/Performance/FishIETank/
[4]: #_msocom_1
[5]: http://CNN.com/
[6]: https://developer.mozilla.org/en/DOM/window.scrollTo
[7]: http://benoitgirard.wordpress.com/2012/03/30/writing-a-profiler/
[8]: https://wiki.mozilla.org/Project_Eideticker
[9]: http://wiki.mozilla.org/
