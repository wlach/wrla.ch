    Title: mozregression updates
    Date: 2015-01-27T00:00:00
    Tags: Mozilla, mozregression

Lots of movement in [mozregression][1] (a tool for automatically determining when a regression was introduced in Firefox by bisecting builds on ftp.mozilla.org) in the last few months. Here's some highlights:

- Support for win64 nightly and inbound builds (Kapil Singh, Vaibhav Agarwal)
- Support for using an http cache to reduce time spent downloading builds (Sam Garrett)
- Way better logging and printing of remaining time to finish bisection (Julien Pagès)
- Much improved performance when bisecting inbound (Julien)
- Support for automatic determination on whether a build is good/bad via a custom script (Julien)
- Tons of bug fixes and other robustness improvements (me, Sam, Julien, others)

Also thanks to Julien, we have a [spiffy new website][2] which documents many of these features. If it's been a while, be sure to [update your copy of mozregression to the latest version][3] and check out the site for documentation on how to use the new features described above!

Thanks to everyone involved (especially Julien) for all the hard work. Hopefully the payoff will be a tool that's just that much more useful to Firefox contributors everywhere.

[1]: http://mozilla.github.io/mozregression
[2]: http://mozilla.github.io/mozregression/
[3]: http://mozilla.github.io/mozregression/install.html
