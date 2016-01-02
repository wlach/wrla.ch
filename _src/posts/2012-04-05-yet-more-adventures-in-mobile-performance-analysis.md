    Title: Yet more adventures in mobile performance analysis
    Date: 2012-04-05T00:00:00
    Tags: Eideticker, Mozilla


*[ For more information on the Eideticker software I&#8217;m referring to, see [this entry][1] ]*

Participated in an [interesting meeting][2] on checkerboarding in Firefox for Android yesterday. As a reminder, checkerboarding refers to the amount of time you spend waiting to see the full page after you do a swipe on your mobile device, and it&#8217;s a big issue right now &#8211; so much so that it puts our delivery goal for the new native browser at risk.

It seems like we have a number of strategies for improving performance which will likely solve the problem, but we need to be able to measure improvements to make sure that we&#8217;re making progress. This is one of the places where Eideticker could be useful (especially with regards to measuring us against the competition), though there are a few things that we need to add before it&#8217;s going to be as useful as it could be. The most urgent, as I understand, is to come up with a suite of tests which accurately represent the set of pages that we&#8217;re having issues with. The current main measure of checkerboarding that we&#8217;re using with eideticker is taskjs.org which, while an interesting test case in some ways, doesn&#8217;t accurately represent the sort of site that the user would normally go to in the wild (and thus be annoyed by). 😉

This is going to take a few days (and a lot of review: I&#8217;m definitely no expert when it comes to this stuff) to get right, but I just added two tests for the New York Times which I think are a step in the right direction of being more representative of real-world use cases. Have a look here:

<http://wrla.ch/eideticker/dashboard/#/nytimes-scrolling>  
<http://wrla.ch/eideticker/dashboard/#/nytimes-zooming>

The results here actually aren&#8217;t as bad as I would have expected/remembered. There amount of checkerboarding after a zoom out is a bit annoying (I understand this a known issue with font caching, or something) but not too terrible. Still, any improvements that show up here will probably apply across a wide variety of sites, as the design patterns on the New York Times site are very common.

(P.S. yes, I know I promised a comparison with Google Chrome for Android last time&#8230; rest assured that&#8217;s still coming soon!)

 [1]: http://wrla.ch/blog/2011/11/measuring-what-the-user-sees/
 [2]: https://wiki.mozilla.org/Fennec/NativeUI/checkerboarding