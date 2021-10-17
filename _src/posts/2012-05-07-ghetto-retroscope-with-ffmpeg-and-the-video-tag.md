    Title: Ghetto retroscope with ffmpeg and the &lt;video&gt; tag
    Date: 2012-05-07T00:00:00
    Tags: Mozilla, Video

So yesterday we had a small get-together at my place, which gave me the opportunity to try something I'd been meaning to do for a while: build my own retroscope.

The idea is pretty simple: have a webcam record bits and pieces of a social event, then play them back on-the-spot a few minutes/hours later. I first heard about the concept from reading Nat Friedman's [blog entry][1] from 2005 &#8212; if you read that, you see that he just hooked up a video camera to his TiVo. 7 years in the future, laptop webcams are ubiquitous and we have the awesome HTML5 <video> tag, so I figured it would be easy to knock up something interesting in short order with zero custom hardware.

Having only remembered that I wanted to do this about 30 minutes before people were scheduled to start arriving, I didn't have much time to do anything really perfect. I settled on using [this little snippet][2] from stackoverflow to generate short (5 second) movies on my laptop, then used scp to copy them over and display a montage of them in an auto-refreshing webpage on my "television" (which is a Mac-Mini connected to a large computer monitor). Despite being a total hack job, the end result generated much amusement. I think this is a bit different from what Nat originally did (it sounds from his blog like his retroscope played back longer segments), but I think the end result is actually a bit more fun.

<a href="http://wrla.ch/blog/2012/05/ghetto-retroscope-with-ffmpeg-and-the-video-tag/retroscope-screenshot/" rel="attachment wp-att-598"><img src="/files/2012/05/retroscope-screenshot-1024x694.png" alt="" title="retroscope-screenshot" width="640" height="433" class="alignnone size-large wp-image-598" srcset="/files/2012/05/retroscope-screenshot-300x203.png 300w, /files/2012/05/retroscope-screenshot-1024x694.png 1024w, /files/2012/05/retroscope-screenshot.png 1319w" sizes="(max-width: 640px) 100vw, 640px" /></a>

Perhaps unfortunately, but probably ultimately for the best, only a few snippets from the actual night got stored away. One example is this gem:

<video src="/files/2012/05/willhappy.webm" controls>

(yes, that handsome fellow with the Pernot is me)

I thought it might be fun to release the slightly-cleaned up results of this experiment as opensource for others to play with, so I created a small project for it on github. Unlike the original version, no complicated scp scheme is required &#8212; I just reused Joel Maher's most excellent mozhttpd library from [mozbase][3] to run a web server in the same process as the capture logic. All you need to do is run the server on a Linux machine with a webcam and connect to it with a web browser from any other machine on your local network.

<https://github.com/wlach/retroscope>

Enjoy!

[1]: http://nat.org/blog/2005/10/the-retroscope/
[2]: http://stackoverflow.com/questions/7500763/command-line-streaming-webcam-with-audio-from-ubuntu-server-in-webm-format
[3]: http://github.com/mozilla/mozbase
