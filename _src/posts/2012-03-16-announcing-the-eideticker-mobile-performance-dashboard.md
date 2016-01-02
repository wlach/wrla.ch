    Title: Announcing the Eideticker mobile performance dashboard
    Date: 2012-03-16T00:00:00
    Tags: Eideticker, Mozilla


Over the last while, Clint Talbert and I have been working on setting up automatic mobile performance tests using Eideticker (a framework to measure perceived Firefox performance by video capturing automated browser interactions: for more information, see my [earlier post][1]). 

There&#8217;s many reasons why this is interesting, but probably the most important one is that it can measure differences reliably across different types of mobile browsers. Currently I&#8217;m testing the old XUL fennec, the Android stock browser, and the latest nightlies.

I&#8217;m pleased to announce that the first iteration of the dashboard is available for public consumption, on my site.

<http://wrla.ch/eideticker/dashboard/#/canvas>

![Eideticker Results][2]

The demo is pretty cheesey (just click on any of the datapoints to see the video capture), but nonetheless does seem to illustrate some interesting differences between the three browsers. The big jump in performance for nightly comes from the landing of the Maple branch, which happened earlier this week. Hopefully this validates some of the work that the mobile/graphics team has been doing over the past while. Exciting times!

 [1]: http://wrla.ch/blog/2011/11/measuring-what-the-user-sees/
 [2]: /files/2012/03/eideticker-results.png