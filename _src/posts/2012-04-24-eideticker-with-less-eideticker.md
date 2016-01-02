    Title: Eideticker with less eideticker
    Date: 2012-04-24T00:00:00
    Tags: Eideticker, Mozilla


*[ For more information on the Eideticker software I&#8217;m referring to, see [this entry][1] ]*

tl;dr: You can now run the standard eideticker benchmarks easily on any Android phone without any kind of specialized hardware.

So Eideticker is pretty great at comparing relative performance between different browsers and generally measuring things in an absolutely neutral way. Unfortunately it&#8217;s a bit of a pain to use it at the moment to catch regressions: the software still has a few bugs and encoding/decoding/analyzing the capture still takes a great deal of time. Not to mention the fact that it currently requires specialized hardware (though that will soon be less of a concern at least inside MoCo, where we have a bunch of Eideticker boxes on order for the Toronto and Mountain View offices).

A few months ago, Chris Lord wrote up some great code to internally measure the amount of checkerboarding going on in Fennec. I&#8217;ve thought for a while that it would be a neat idea to hook this up to the Eideticker harness, and today I finally did so. After installing Eideticker, you can now run the benchmark on any machine against an arbitrary fennec build just by typing this from the eideticker root directory:

```
adb shell setprop log.tag.GeckoLayerRendererProf DEBUG
./bin/get-metric-for-build.py --no-capture --get-internal-checkerboard-stats --num-runs 3 nightly.apk src/tests/scrolling/taskjs.org/index.html
```

In return, you&#8217;ll get some nice clean results like this:

```
=== Internal Checkerboard Stats (sum of percents, not percentage) ===
[167.34348, 171.871015, 175.3420296]
```

Just to be sure that the results were comparable, I did a quick set of runs on the Eideticker machine in Mountain View with both internal checkerboard statistics gathering and HDMI capturing enabled.

<table>
  <tr>
    <td>
      Stats file
    </td>
    
    <td>
      HDMI capturing
    </td>
  </tr>
  
  <tr>
    <td>
      167.34348
    </td>
    
    <td>
      177.022
    </td>
  </tr>
  
  <tr>
    <td>
      171.87
    </td>
    
    <td>
      184.46
    </td>
  </tr>
  
  <tr>
    <td>
      175.34
    </td>
    
    <td>
      184.44
    </td>
  </tr>
</table>

While the results aren&#8217;t identical (we measure number of frames differently inside Fennec than we do with Eideticker, for one thing), they do seem roughly correlated. So go forth, benchmark and tweak! 😉

P.S. If you&#8217;ve been following mobile automation, you might be asking why I don&#8217;t just suggest running Talos and Robocop on your workstation. Can&#8217;t they do the same sorts of things? The short answer is that yes, they can, but unfortunately they&#8217;re much more involved to set up and use at the moment. Arguably they shouldn&#8217;t be, and this is something we ([Mozilla tools & automation][2]) need to work on. We&#8217;ll get there eventually (and help would be welcome!). For now, hacks like this should help with getting out the first release of Fennec by providing a fast, easy to use tool for bisection and analysis.

 [1]: http://wrla.ch/blog/2011/11/measuring-what-the-user-sees/
 [2]: https://wiki.mozilla.org/Auto-tools/