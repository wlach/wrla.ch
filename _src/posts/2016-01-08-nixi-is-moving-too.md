    Title: NIXI is moving too
    Date: 2016-01-08T23:21:13
    Tags: BIXI, Nixi

As my blog goes to github pages, so do my other side projects. I just
moved nixi, my bikestation finder project, to github pages. Its new location:

[http://wlach.github.io/nixi](http://wlach.github.io/nixi)

I opted not to move over the domain: it would have cost extra money, time and
hassle and I couldn't justify it for the very, very small number of people that
still use this site (yes, there are a few, including myself!). For now, nixi.ca
will redirect to the github pages site until I decommision my linode server,
probably at the end of January (end of Feburary at the latest).

This transition brings some other changes with it:

* Now using the [citybik.es](https://citybik.es) API directly,
  instead of proxing through an intermediary server. This was necessitated
  by the switch to github pages, but I suspect this will be more reliable
  than what we were doing before. Thanks citybik.es!
* Removed all analytics and facebook integration. As with the domain, it didn't
  seem worth bringing over. Also, it's nice to give people at least marginally
  more privacy than they had before where possible.

I still think nixi is worlds more usable than most bikesharing maps, even if it's
not an actively maintained project of mine any more. Here's hoping it lasts
many more years in its new incarnation.
