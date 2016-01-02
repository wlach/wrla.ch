    Title: Adventures in processing with prender
    Date: 2010-03-07T00:00:00
    Tags: Data Visualization


First, I&#8217;m overdue in announcing [Transit to Go][1] a.k.a. &#8220;the iPhone transit map that&#8217;s demonstrably more useful than a paper schedule&#8221; a.k.a. &#8220;your bus departure in 15 seconds or less, no matter where you are&#8221;. I wrote up a [blog post][2] about it for [Mindsea][3]&#8216;s site, if you&#8217;re interested in finding out more.

Second, all this transit excitement has made me start thinking about better routing and geometry algorithms again. I&#8217;ve been experimenting a bit with Brandon Martin Anderson&#8217;s [prender][4] framework, used by the infamous [Graphserver][5], and have been pretty happy with the results. It basically lets you do [processing][6] visualizations in python (i.e. no Java coding required). Here&#8217;s a quick picture of it in action, rendering the Nova Scotian road network, as distributed by [geobase][7].

<img src="/files/2010/03/nova_scotia.png" alt="Nova Scotia as rendered by prender" title="Nova Scotia as rendered by prender" width="400" height="220" class="alignnone size-full wp-image-95" />

The neat thing about this framework is that you can render quickly to an arbitrary level of detail, which should prove very useful when troubleshooting the behavior of some of the code I&#8217;m working on. If anyone is interested in running the framework on MacOS X (like I was), [my fork][8] of the project has the appropriate patches.

 [1]: http://transittogo.mindsea.ca/
 [2]: http://www.mindsea.com/blog/2010/03/transit-to-go-pulling-out-all-the-stops/
 [3]: http://www.mindsea.com
 [4]: http://github.com/bmander/prender
 [5]: http://bmander.github.com/graphserver/
 [6]: http://processing.org
 [7]: http://geobase.ca
 [8]: http://github.com/wlach/prender