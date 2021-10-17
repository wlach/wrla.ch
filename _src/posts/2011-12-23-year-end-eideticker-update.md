    Title: Year end Eideticker update
    Date: 2011-12-23T00:00:00
    Tags: Data Visualization, Mozilla

Just before I leave for some Christmas vacation, it's time for another update on the state of [Eideticker][1]. Since I last blogged about the software, I've been working on the following three areas:

1. Coming up with better algorithm (green screen / red screen) for both determining the area of the capture as well as the start/end of the capture. The harness was already flood filling the area with these colours at the beginning/end of the capture, but now we're actually using this information. The code's a little hacky, but it seems to work well enough for the test cases I've been using so far.
2. As a demonstration, I wrote up a quick test that demonstrates checkerboarding on mobile Fennec, and wrote up a quick bit of analysis code to detect this pattern and give an overall measure of how much this test "checkerboards" (i.e. has regions that are not fully painted when the user scrolls). As I understand this is an area that our mobile team is currently working on this problem quite a bit, it will be interesting to watch the numbers given by this test and see if things improve.
3. It's a minor thing, but you can now view a complete webm movie of the captured movie right from the web interface.

Here's a quick demonstration video that shows all the above in action. As before, you might want to watch this full screen:

<video src="/files/eideticker/eideticker-2011-12-21.webm" width="600px" controls></video>

Happy holidays!

[1]: http://wrla.ch/blog/2011/11/measuring-what-the-user-sees/
