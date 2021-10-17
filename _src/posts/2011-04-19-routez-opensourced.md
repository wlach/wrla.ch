    Title: Routez opensourced
    Date: 2011-04-19T00:00:00
    Tags: Free Software, hbus, Open Data, Transit to Go

Just a quick note to say that I just opensourced the software behind [hbus.ca][1], nicknamed "Routez" under the [Affero GPL][2]. You can get the code on [github][3].

<a href="http://wrla.ch/blog/2011/04/routez-opensourced/hbus_shot_apr_2011/" rel="attachment wp-att-238"><img src="/files/2011/04/hbus_shot_apr_2011.png" alt="" title="hbus_shot_apr_2011" width="300" height="225" class="aligncenter size-full wp-image-238" /></a>

For those new to the project, hbus.ca is a generic trip planning / transit information site for Halifax, Nova Scotia written using the [Django][4] web framework. It currently has two main features:

- A trip planning front-end much like Google Transit (built from the ground up using the [libroutez][5] library).
- A "nearby" routes feature which gives you all the bus departures near a particular location.

On the backend, both of these features are accessible via JSON APIs, for use in transit apps, etc. [Transit to Go][6] uses these to great effect.

There is nothing particularly Halifax-specific to the underlying Routez software, aside from various references in the web front end to Halifax and hbus.ca. In fact, we use Routez to provide information for Transit to Go Edmonton right now, with no modification.

Originally my plan was to release something that was completely generic out of the box so that anyone could trivially make up a version of this site for their favourite city. I've made some headway towards that goal over the last week or so, but there's still some ways to go. There's basically two major issues:

1. The geocoder depends on information gleaned from the geobase road network dataset. The intent behind this is noble (provide an end-to-end solution that doesn't depend on third parties) but in practice this limits the software's usefulness. It would be better to optionally allow a Routez-based site to use Google's geocoder on the front-end. Unfortunately, to comply with Google's terms of service, we'd also need to use their Maps API for the base map as well. Perhaps the best option here would be to use something like [Mapstraction][7] to allow users to select their preferred mapping provider.
2. The trip planning software used in the backend, libroutez, is getting a bit long in the tooth and is quite finicky about what kind of data it will accept. I think the long-term solution to this is to switch to [Graphserver][8] (which is more mature and better supported), but some features would have to be added to it to support the kind of things that Routez needs (like a list of upcoming departures at a particular transit stop).

Even with these problems, I figured it would be better to open up what I have for people to check out and play with. Have a look and let me know what you think!

[1]: http://hbus.ca
[2]: http://www.affero.org/oagpl.html
[3]: http://github.com/wlach/routez
[4]: http://www.django-project.com
[5]: http://github.com/wlach/libroutez
[6]: http://transittogo.mindsea.ca
[7]: http://mapstraction.com
[8]: http://graphserver.github.com/graphserver/
