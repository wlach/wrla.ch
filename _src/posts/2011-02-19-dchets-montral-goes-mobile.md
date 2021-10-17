    Title: D&eacute;chets Montr&eacute;al goes mobile
    Date: 2011-02-19T00:00:00
    Tags: Free Software, iphone, Montreal, Open Data, Usability

A few weekends ago, there was a [Montr&eacute;al Ouvert][1] hackfest at the [Notman House][2]. I decided to take a bit of a break from my usual transit hacking and built up a mobile friendly interface to the wonderful [D&eacute;chets Montr&eacute;al][3], which lets residents easily get information on their garbage collection schedule.

<a href="http://wrla.ch/blog/?attachment_id=210" rel="attachment wp-att-210"><img src="/files/2011/02/dechets-screenies.jpg" alt="" title="Dechets Montreal Screenshots" width="400" height="243" class="alignnone size-full wp-image-210" srcset="/files/2011/02/dechets-screenies-300x182.jpg 300w, /files/2011/02/dechets-screenies.jpg 400w" sizes="(max-width: 400px) 100vw, 400px" /></a>

The interface is intentionally quite simplistic, the idea being that if you're accessing the site using a mobile device you're probably only interested in the collection schedule for the current week and nothing else. If you want something more complicated you probably should just be using the full site.

Anyway, another fun opportunity to play with mobile web technology (a bit of break from my current [consulting gig][4], which is mostly native iPhone apps). A few things that I learned this time around:

- It's easy to give your application a nice icon when added to the iPhone home screen by using a [webpage icon][5].
- Related to the above, you can give the user a nice hint to add your webpage to their homescreen by using Google's [mobile bookmark bubble][6] library.
- The iPhone's form interface will persist after pressing "Search" unless [you change the focus using an anchor element][7].
- [jQuery][8] is the best thing since sliced bread for dynamic web applications (ok, I actually knew this already but I just can't get over how great it is).

Thanks muchly to Kent Mewhort, the brains behind D&eacute;chets Montr&eacute;al, for helping me incorporate my work into his Drupal-based site.

[1]: http://montrealouvert.net/
[2]: http://notmanhouse.com
[3]: http://dechetsmontreal.ca/
[4]: http://mindsea.com
[5]: http://developer.apple.com/library/safari/#documentation/AppleApplications/Reference/SafariWebContent/ConfiguringWebApplications/ConfiguringWebApplications.html#//apple_ref/doc/uid/TP40002051-CH3
[6]: http://code.google.com/p/mobile-bookmark-bubble/
[7]: http://www.em-motion.mobi/2010/05/01/iphone-ajax-form-submission/
[8]: http://jquery.com
