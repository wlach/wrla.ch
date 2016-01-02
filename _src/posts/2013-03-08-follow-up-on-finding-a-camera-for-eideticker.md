    Title: Follow up on &#8220;Finding a Camera for Eideticker&#8221;
    Date: 2013-03-08T00:00:00
    Tags: Eideticker, Mozilla


Quick update on my [last post][1] about finding some kind of camera suitable for use in automated performance testing of fennec and b2g with eideticker. Shortly after I wrote that, I found out about a company called [Point Grey Research][2] which manufactures custom web cameras intended for exactly the sorts of things we&#8217;re doing. Initial results with the [Flea3 camera][3] I ordered from them are quite promising:

<video width="400px" src="/files/eideticker/pointgrey-taskjs.webm" controls></video>

(the actual capture is even higher quality than that would suggest&#8230; some detail is lost in the conversion to webm)

There seems to be some sort of issue with the white balance in that capture which is causing a flashing effect (I suspect this just involves flipping some kind of software setting&#8230; still trying to grok their SDK), and we&#8217;ll need to create some sort of enclosure for the setup so ambient light doesn&#8217;t interfere with the capture&#8230; but overall I&#8217;m pretty optimistic about this baby. 60 frames per second, very high resolution (1280&#215;960), no issues with HDMI (since it&#8217;s just a USB camera), relatively inexpensive.

 [1]: http://wrla.ch/blog/2013/02/finding-a-camera-for-eideticker/
 [2]: http://ptgrey.com
 [3]: http://ww2.ptgrey.com/USB3/Flea3