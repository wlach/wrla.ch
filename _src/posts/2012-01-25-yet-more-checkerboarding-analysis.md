    Title: Yet more checkerboarding analysis
    Date: 2012-01-25T00:00:00
    Tags: Eideticker, Mozilla

I've been spending a bit more time on refining the checkerboarding tests in Eideticker that I talked about last time. Most of my work has been focused on making the results as representative of a real world scenario as possible, to that effect I've been working on:

- Changed the test case from a web site of my own concoction to a more realistic example (the [taskjs.org][1] site)
- Use actual Android native events (via [MonkeyRunner][2]) to synthesize touch-based scrolling instead of simulating the event in JavaScript (which exercises a completely different codepath).
- Fixing various synchronization issues to make results more repeatable. Before captures were of wildly variable lengths, which made the numbers extremely suspect. There's probably still a few issues, but much less than before.

The end result of this is a framework that gives much more meaningful results. The bad news is that the results that I'm measuring don't show a very positive picture for where we're at with the native re-write of Firefox. Even relative to the version of mobile Firefox which is currently on the Android Market, we still have some catching up to do. Here's some video of the "old" firefox in action:

<video src="/files/eideticker/taskjs_xul.webm" width="600px" controls></video>

And here's the Native fennec (what we're currently offering in nightly, with some minor modifications by me to change the way the "checkerboard" is drawn for analysis purposes):

<video src="/files/eideticker/taskjs_native.webm" width="600px" controls></video>

The numbers behind this comparison:

<table>
  <tr>
    <td>
      Platform
    </td>
    
    <td>
      Percent checkerboarding over run of test
    </td>
  </tr>
  
  <tr>
    <td>
      Old Fennec
    </td>
    
    <td>
      2%
    </td>
  </tr>
  
  <tr>
    <td>
      Native Fennec
    </td>
    
    <td>
      57%
    </td>
  </tr>
</table>

(by the way, this performance regression is filed as [bug 719447][3])

I know there's lots of great effort going into improving this situation, so I have hope that we'll be doing much better on this metric in the coming days/weeks. The process for creating these videos/analyses is mostly automated at this point, so my plan is to create a small dashboard (ala [arewefastyet.com][4]) to measure these numbers over time on the latest nightlies. Stay tuned!

[1]: http://taskjs.org
[2]: http://developer.android.com/guide/developing/tools/monkeyrunner_concepts.html
[3]: https://bugzilla.mozilla.org/show_bug.cgi?id=719447
[4]: http://arewefastyet.com
