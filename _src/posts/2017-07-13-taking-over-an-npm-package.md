    Title: Taking over an npm package: sanity prevails
    Date: 2017-07-13T11:08:40
    Tags: Mozilla

Sometimes problems are easier to solve than expected.

For the last few months I've been working on the front end of a new project
called [Mission Control](https://github.com/mozilla/missioncontrol), which
aims to chart lots of interesting live information in something approximating
realtime. Since this is a greenfield project, I thought it would make sense
to use the currently-invogue framework at Mozilla (react) along with our
standard visualization library, [metricsgraphics](http://metricsgraphicsjs.org/).

Metricsgraphics is great, but its jquery-esque api is somewhat at odds with
the react way. The obvious solution to this problem is to wrap its
functionality in a react component, and a quick google search determined
that several people have tried to do exactly that, the most popular one
being one called (obviously) react-metrics-graphics. Unfortunately, it hadn't
been updated in quite some time and some pull requests (including ones
implementing features I needed for my project) weren't being responded to.

I expected this to be pretty difficult to resolve: I had no interaction
with the author (Carter Feldman) before but based on my past experiences in
free software, I was expecting stonewalling, leaving me no choice
but to fork the package and give it a new name, a rather unsatisfying end
result.

But, hey, let's keep an open mind on this. What does google say about
unmaintained npm packages? Oh what's this? They actually have a [policy](https://docs.npmjs.com/misc/disputes)?

tl;dr: You email the maintainer (politely) and CC support@npmjs.org about
your interest in helping maintain the software. If you're unable to come up
with a resolution on your own, they will intervene.

So I tried that. It turns out that Carter was really happy to hear that
Mozilla was interested in taking over maintenance of this project, and
not only gave me permission to start publishing newer versions to npm,
but even transferred his repository over to Mozilla (so we could preserve
issue and PR history). The project's new location is here:

[https://github.com/mozilla/react-metrics-graphics](https://github.com/mozilla/react-metrics-graphics)

In hindsight, this is obviously the most reasonable outcome and I'm
not sure why I was expecting anything else. Is the node community just
friendlier than other areas I've worked in? Have community standards
improved generally? In any case, thank you Carter for a great piece of
software, hopefully it will thrive in its new home. :P
