    Title: A better BIXI web site
    Date: 2011-06-10T00:00:00
    Tags: BIXI, Data Visualization, Montreal


There&#8217;s much to like about the BIXI bike-sharing system in Montr&eacute;al: it&#8217;s affordable ($78 for a year of biking), accessible and fun to use. There&#8217;s absolutely no doubt in my mind that it&#8217;s made cycling more of a main stream activity here in Montreal, which benefits everyone (even drivers indirectly gain from less congested streets). 

With the arrival of the first BIXI stations in NDG, I decided to subscribe to it this year even though I have a bike of my own. So far, it looks like I&#8217;m going to easily use it enough to justify the cost. I still use my regular bike for my commute from NDG to the Plateau, but on the edges there&#8217;s a ton of cases where it just makes sense to use something that I don&#8217;t have to worry about locking up and returning home. Sometimes I only want to go one way (for weather or whatever other reason). Other times I want to take public transit for one leg of my trip (or day), but need/want to take a quick jaunt elsewhere once I&#8217;m downtown.

I do have to say though, their new web site drives me *crazy*. I&#8217;ve thought prety deeply about the domain of creating user-friendly transit-focused web sites, so I think I can speak with some authority here. 

<a href="http://wrla.ch/blog/2011/06/a-better-bixi-web-site/bixi_shot/" rel="attachment wp-att-268"><img src="/files/2011/06/bixi_shot.png" alt="" title="bixi_shot" width="400" height="265" class="alignnone size-full wp-image-268" srcset="/files/2011/06/bixi_shot-300x198.png 300w, /files/2011/06/bixi_shot.png 400w" sizes="(max-width: 400px) 100vw, 400px" /></a>

Leaving aside it&#8217;s value as a promotional tool for the service itself (not my area of expertise), the experience of trying to find a nearby station is complicated by a slow, multi-layered UI that requires repeated clicking and searching to find the nearest station that has bikes available. Why bother with this step when we can just display this information outright on the map? iPhone applications like [Bixou][1] have been doing this for years. It&#8217;s time we brought the same experience to the desktop.

Thus, I present [nixi.ca][2]: a clean, useable interface to BIXI&#8217;s bike share system that presents the information you care about as effectively as possible, without all the clutter. I&#8217;ve already found it useful, and I hope you do too. Think you can do better? Fork the source on [github][3] and submit your changes back to me! Minus some glue code to fetch station info server side, it&#8217;s entirely a client-side application written in HTML/JavaScript.

<a href="http://wrla.ch/blog/2011/06/a-better-bixi-web-site/nixi_shot/" rel="attachment wp-att-269"><img src="/files/2011/06/nixi_shot.png" alt="" title="nixi_shot" width="400" height="265" class="alignnone size-full wp-image-269" srcset="/files/2011/06/nixi_shot-300x198.png 300w, /files/2011/06/nixi_shot.png 400w" sizes="(max-width: 400px) 100vw, 400px" /></a>

Note that the site uses a bunch of modern HTML5 features, so currently requires a modern browser like Firefox, Chrome, or Safari to display properly. I may or may not fix this. Other notable omissions include support for other cities with the BIXI system (Toronto, Ottawa, &#8230;) and French localization. Patches welcome!

 [1]: http://sites.google.com/site/bixouiphone/
 [2]: http://nixi.ca
 [3]: http://github.com/wlach/nixi