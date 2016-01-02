    Title: Maps URLs on mobile Safari
    Date: 2009-02-02T00:00:00
    Tags: 


I&#8217;ve been experimenting a little bit with maps urls on the iphone. If you&#8217;ve read Apple&#8217;s web developer guidelines, you&#8217;ll know that URLs of this form will automatically redirect to the maps application:

[Halifax, Nova Scotia][1]  
<a href=&#8221;http://maps.google.com/maps?geocode=&#038;q=Halifax,Nova Scotia&#8221;>Halifax, Nova Scotia</a>

This is fine if you just want to highlight one particular location (with no custom metadata), but what if you want to do something more interesting, like display a KML file? You can load these easily from the maps application, so why can&#8217;t you link to them from a web browser? The URL guidelines explicitly say that the KML part of a query string will be discarded, and indeed it is. What is a web developer to do? Resort to undocumented behaviour, of course! At least in version 2.2 of the iphone software, URLs which request a &#8220;maps&#8221; resource with the appropriate parameters will automatically load the appropriate KML file in the maps application:

[Map link][2]  
<a href=&#8221;maps://?geocode=&#038;q=http://code.google.com/apis/kml/documentation/KML_Samples.kml&#8221;>Map link</a>

 [1]: http://maps.google.com/maps?geocode=&#038;q=Halifax,Nova Scotia
 [2]: maps://?geocode=&#038;q=http://code.google.com/apis/kml/documentation/KML_Samples.kml