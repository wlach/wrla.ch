    Title: Measuring reduced checkerboarding in mobile Fennec
    Date: 2012-01-03T00:00:00
    Tags: Data Visualization, Eideticker, Mozilla

After my [post][1] on measuring checkerboarding in mobile Firefox, [Clint Talbert][2] (my fearless manager) suggested I run a before and after test to measure the improvement that just landed as part of [bug 709512][3]. After a bit of cleanup, I did so, measuring the delta between my build on December 20th and the latest version of Aurora. The difference is pretty remarkable: at least on the LG G2X that I've been using for testing, we've gone from checkerboarding between 10-20% of the time and not checkerboarding almost at all (in between two runs of the test with the Aurora build, there is exactly one frame that checkerboards). All credit to [Chris Lord][4] for that!

See the video evidence for yourself. Before:

<video src="/files/eideticker/lotsocheckerboarding.webm" width="600px" controls></video>

After:

<video src="/files/eideticker/almostnocheckerboarding.webm" width="600px" controls></video>

[1]: http://wrla.ch/blog/2011/12/year-end-eideticker-update/
[2]: http://cmtalbert.wordpress.com/
[3]: https://bugzilla.mozilla.org/show_bug.cgi?id=709152
[4]: http://chrislord.net/blog
