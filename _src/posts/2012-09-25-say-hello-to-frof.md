    Title: Say hello to frof
    Date: 2012-09-25T00:00:00
    Tags: Android, Mozilla, Profiling


Inspired by the work I&#8217;d been doing with Benoit Girard to [integrate the Firefox Profiler with Eideticker][1], I decided to create an easy-to-use python script to help with gathering profiles on Fennec, which I call [frof][2]. 

Frof pretty considerably reduces the amount of busywork you need to do to gather a profile. Instead of a rather complicated multi-step process to initialize fennec with the right parameters for profiling, downloading profiles, etc., you can just run the frof script like so:  
`<br />
frof org.mozilla.fennec http://wrla.ch mywonderfulprofile.zip<br />
`  
Assuming that frof was bootstrapped correctly (and your phone is connected to your computer in debugging mode), this should start up fennec automatically with that URL loaded. Now, just perform whatever action you want to profile on your phone, then press enter in the terminal when you&#8217;re done. Voila, instant profile trace which you can examine, post to bugs, etc. All the other details are automated.

Backstory: the inspiration for frof came from a personal itch of mine, the fact that leaflet.js maps seem to be causing out-of-memory errors on Fennec when zooming is enabled ([bug 784580][3]). I wanted to be able to capture some profiles to see what was going on, but the [current instructions][4] on MDN seem a bit unwieldly. I figured I&#8217;d get lots of mileage out of a tool to make this easier (especially if I was going to get into a profile, edit, debug cycle), so I spent a few hours dilligently copying the logic we put into eideticker to gather profiles into a standalone script.

<a href="http://wrla.ch/blog/2012/09/say-hello-to-frof/frof-profile-leaflet/" rel="attachment wp-att-760"><img src="/files/2012/09/frof-profile-leaflet.png" alt="A profile I generated of a leaflet map with frof" title="frof profile leaflet" width="703" height="365" class="alignnone size-full wp-image-760" srcset="/files/2012/09/frof-profile-leaflet-300x155.png 300w, /files/2012/09/frof-profile-leaflet.png 703w" sizes="(max-width: 703px) 100vw, 703px" /></a>

Unfortunately in my case, the gecko profile didn&#8217;t tell me much, aside from the fact that Gecko didn&#8217;t seem to be the culprit (remember that on Android we also have lots of Java-based frontend code to contend with, which the profiler doesn&#8217;t measure). I&#8217;m going to stare more at the Java code and dig into the various high-level tools that Android provides for profiling performance and memory usage. My current hypothesis is that the problem is the screenshot code and the CSS transitions that leaflet generates when zooming. In the mean time, the only thing I have to show for my foray away from writing tools for Mozilla is &#8230; yet another tool. 

Oh well, it could be worse. My fervent hope is that frof will be helpful for both Fennec developers and QA. Let me know if you wind up using it!

 [1]: http://wrla.ch/blog/2012/09/more-eideticker-happenings-profiling-and-startup-testing/
 [2]: https://github.com/wlach/frof
 [3]: https://bugzilla.mozilla.org/show_bug.cgi?id=784580
 [4]: https://developer.mozilla.org/en-US/docs/Performance/Profiling_with_the_Built-in_Profiler#Profiling_Firefox_mobile