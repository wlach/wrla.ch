    Title: Follow up on "Finding a Camera for Eideticker"
    Date: 2013-03-08T00:00:00
    Tags: Eideticker, Mozilla

Quick update on my [last post][1] about finding some kind of camera suitable for use in automated performance testing of fennec and b2g with eideticker. Shortly after I wrote that, I found out about a company called [Point Grey Research][2] which manufactures custom web cameras intended for exactly the sorts of things we're doing. Initial results with the [Flea3 camera][3] I ordered from them are quite promising:

<video width="400px" src="/files/eideticker/pointgrey-taskjs.webm" controls></video>

(the actual capture is even higher quality than that would suggest some detail is lost in the conversion to webm)

There seems to be some sort of issue with the white balance in that capture which is causing a flashing effect (I suspect this just involves flipping some kind of software setting: still trying to grok their SDK), and we'll need to create some sort of enclosure for the setup so ambient light doesn't interfere with the capture but overall I'm pretty optimistic about this baby. 60 frames per second, very high resolution (1280x960), no issues with HDMI (since it's just a USB camera), relatively inexpensive.

[1]: http://wrla.ch/blog/2013/02/finding-a-camera-for-eideticker/
[2]: http://ptgrey.com
[3]: http://ww2.ptgrey.com/USB3/Flea3
