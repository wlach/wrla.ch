    Title: Mission Control: Ready for contributions
    Date: 2017-10-20T14:33:19
    Tags: Mozilla, Data Visualization, Mission Control

One of the great design decisions that was made for [Treeherder](https://treeherder.mozilla.org) was a strict seperation of the client and server portions of the codebase. While its
backend was moderately complicated to get up and running (especially into a state
that looked at all like what we were running in production), you could get its web frontend
running (pointed against the production data) just by starting up a simple node.js server.
This dramatically lowered the barrier to entry, for Mozilla employees and casual contributors
alike.

I knew right from the beginning that I wanted to take the same approach with
[Mission Control](https://wlach.github.io/blog/2017/10/mission-control/). While the full source of the project is available, unfortunately
it isn't presently possible to bring up the full stack with real data, as that requires
privileged access to the athena/parquet error aggregates table. But since the UI is
self-contained, it's quite easy to bring up a development environment that allows you to
freely browse the cached data which is stored server-side (essentially:
`git clone https://github.com/mozilla/missioncontrol.git && yarn install && yarn start`).

In my experience, the most interesting problems when it comes to projects like these
center around the question of how to present extremely complex data in a way that is
intuitive but not misleading. Probably 90% of that work happens in the frontend. In the
past, I've had pretty good luck finding contributors for my projects (especially [Perfherder](/tags/Perfherder.html))
by doing call-outs on this blog. So let it be known: If Mission Control sounds like an
interesting project and you know [React](https://reactjs.org/)/[Redux](http://redux.js.org/)/[D3](https://d3js.org/)/[MetricsGraphics](https://www.metricsgraphicsjs.org/) (or want to learn), let's work
together!

I've created some [good first bugs](https://github.com/mozilla/missioncontrol/issues?q=is%3Aissue+is%3Aopen+label%3A%22good+first+issue%22) to tackle in the github issue tracker. From there,
I have a galaxy of other work in mind to improve and enhance the usefulness of this
project. Please get in touch with me (wlach) on [irc.mozilla.org](https://wiki.mozilla.org/IRC)
#missioncontrol if you want to discuss further.
