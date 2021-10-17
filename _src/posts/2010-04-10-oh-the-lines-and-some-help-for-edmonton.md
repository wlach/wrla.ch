    Title: Oh, the lines! And some help for Edmonton.
    Date: 2010-04-10T00:00:00
    Tags: hbus, Transit to Go

<img src="/files/2010/04/linked_map1.jpg" alt="Map with new link nodes" title="Map with new link nodes" width="320" height="242" class="aligncenter size-full wp-image-118" />

A productive day on the transit development front. Finished up a few big features related to hbus.ca and Transit to Go:

- Sped up the graph and database generation by an order of magnitude. Not too exciting from a user perspective, but I should now be able to iterate the codebase much faster.
- Better transit stop / street graph linking: No more does libroutez simply try to find the closest street level vertice to link to when merging transit stops with street information: we now actually create \_new\_ street level vertices as needed and link to those. Upshot? Slightly better directions and prettier polylines. When I first thought up the algorithm a month ago, I thought I was totally brilliant, only to later find out that Andrew Byrd had done something almost identical a few months earlier for [graphserver][1]. Ah well, at least it's implemented.
- I [coded up a script][2] to automatically generate synthetic headsigns for GTFS feeds which don't have them. This was needed to provide a sensible view for the Edmonton version of Transit to Go. All the props in the world for opening up your data guys, but can't you do better than saying that all your buses go in the "1" direction? There's a reason why it's a required field you know. Not only would it help me, but [Google Transit][3] would give better results for your city as well.

[1]: http://github.com/andrewbyrd/graphserver
[2]: http://gist.github.com/361848
[3]: http://google.com/transit
