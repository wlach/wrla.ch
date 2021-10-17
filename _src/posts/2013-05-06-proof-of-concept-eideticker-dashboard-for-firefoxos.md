    Title: Proof of concept Eideticker dashboard for FirefoxOS
    Date: 2013-05-06T00:00:00
    Tags: Eideticker, FirefoxOS, Mozilla

_[ For more information on the Eideticker software I'm referring to, see [this entry][1] ]_

I just put up a proof of concept Eideticker dashboard for FirefoxOS [here][2]. Right now it has two days worth of data, manually sampled from an Unagi device running b2g18. Right now there are two tests: one the measures the "speed" of the contacts application scrolling, another that measures the amount of time it takes for the contacts application to be fully loaded.

For those not already familiar with it, Eideticker is a benchmarking suite which captures live video data coming from a device and analyzes it to determine performance. This lets us get data which is more representative of actual user experience (as opposed to an oft artificial benchmark). For example, Eideticker measures contacts startup as taking anywhere between 3.5 seconds and 4.5 seconds, versus than the 0.5 to 1 seconds that the [existing datazilla benchmarks][3] show. What accounts for the difference? If you step through an eideticker-captured video, you can see that even though _something_ appears very quickly, not all the contacts are displayed until the 3.5 second mark. There is a gap between an app being reported as "loaded" and it being fully available for use, which we had not been measuring until now.

<video src="http://eideticker.wrla.ch/b2g/videos/video-1367875760.86.webm" controls>

At this point, I am most interested in hearing from FirefoxOS developers on new tests that would be interesting and useful to track performance of the system on an ongoing basis. I'd obviously prefer to focus on things which have been difficult to measure accurately through other means. My setup is rather fiddly right now, but hopefully soon we can get some useful numbers going on an ongoing basis, as we [do already][4] for Firefox for Android.

[1]: http://wrla.ch/blog/2012/06/mobile-firefox-measuring-how-a-browser-feels/
[2]: http://eideticker.wrla.ch/b2g
[3]: https://datazilla.mozilla.org/b2g/?branch=master&range=7&test=cold_load_time&app_list=contacts&app=contacts&gaia_rev=114bf216de0a19f7&gecko_rev=9c0de2afd22a8476
[4]: http://eideticker.wrla.ch
