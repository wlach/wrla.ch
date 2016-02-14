    Title: Talos suites now visible from trychooser
    Date: 2016-02-13T14:28:47
    Tags: Mozilla, Talos

It's a small thing, but I submitted a patch to [trychooser](http://trychooser.pub.build.mozilla.org/)
last week which adds a tooltip indicating the actual Talos tests that are run
as part of the various jobs that you can schedule as part of a try push. It's in production
as of now:

<video src="/files/2016/02/talos-trychooser.webm" controls autoplay/>

Previously, the only way to do this was to dig into the actual buildbot
code, which was more than a little annoying.

If you think your patch might have a good chance of regressing performance, please
do run the [Talos tests](https://wiki.mozilla.org/Buildbot/Talos/Tests) before you
check in. It's much less work for all of us when these things are caught before integration
and back outs are no fun for anyone. We really need better documentation for this stuff, but
meanwhile if you need help with this, please ask in the #perf channel on irc.mozilla.org
