    Title: Making contribution work for Firefox tooling and data projects
    Date: 2018-11-26T11:13:46
    Tags: Mozilla, Community

One of my favorite parts about Mozilla is mentoring and working alongside
third party contributors. Somewhat surprisingly since I work on internal
tools, I've had a fair amount of luck finding people to help work on projects
within my purview: [mozregression](https://mozilla.github.io/mozregression),
[perfherder](https://wiki.mozilla.org/EngineeringProductivity/Projects/Perfherder),
[metrics graphics](https://metricsgraphics.org), and others have all benefited
from the contributions of people outside of Mozilla.

In most cases (a notable exception being metrics graphics), these have been
internal-tooling projects used by others to debug, develop, or otherwise
understand the behaviour of Firefox. On the face of it, none of the things I
work on are exactly "high profile cutting edge stuff" in the way, say, Firefox
or the Rust Programming Language are. So why do they bother? The exact formula
varies depending on contributor, but I think it usually comes down to some
combination of these two things:

1. A desire to learn and demonstrate competence with industry standard
   tooling (the python programming language, frontend web development, backend
   databases, "big data" technologies like Parquet, ...).
2. A desire to work with and gain recognition inside of a community of
   like-minded people.

Pretty basic, obvious stuff -- there is an appeal here to basic human desires
like the need for security and a sense of belonging. Once someone's "in the
loop", so to speak, generally things take care of themselves. The real
challenge, I've found, is getting people from the "I am potentially interested
in doing something with Mozilla internal tools" to the stage that they are
confident and competent enough to work in a reasonably self-directed way. When
I was on the A-Team, we classified this transition in terms of a [commitment
curve](https://ateam-bootcamp.readthedocs.io/en/latest/guide/curve.html):

<img srcset="/files/2018/11/commitment-curve-visualization.png 2x"/>

[prototype commitment curve graphic by Steven Brown](https://bugzilla.mozilla.org/show_bug.cgi?id=1080119)

The hardest part, in my experience, is the initial part of that curve. At this
point, people are just dipping their toe in the water.  Some may not have a
ton of experience with software development yet.  In other cases, my projects
may just not be the right fit for them. But of course, sometimes there is a
fit, or at least one could be developed! What I've found most helpful is
"clearing a viable path" forward for the right kind of contributor. That is,
some kind of initial hypothesis of what a successful contribution experience
would look like as a new person transitions from "explorer" stage in the chart
above to "associate".

I don't exactly have a perfect template for what "clearing a path" looks like
in every case. It depends quite a bit on the nature of the contributor. But
there are some common themes that I've found effective:

First, provide good, concise documentation both on the project's purpose and
vision and how to get started easily and keep it up to date. For projects with
a front-end web component, I try to decouple the front end parts from the
backend services so that people can `yarn install && yarn start` [their way to
success](/blog/2014/09/hacking-on-the-treeherder-front-end-refreshingly-easy/).
Being able to *see* the project in action quickly (and not getting
stuck on some mundane getting started step) is key in maintaining initial
interest.

Second, provide a set of good starter issues (sometimes called "good first
bugs") for people to work on. Generally these would be non-critical-path type
issues that have straightforward instructions to resolve and fix. Again, the
idea here is to give people a sense of quick progress and resolution, a "yes I
can actually do this" sort of feeling. But be careful not to let a contributor
get stuck here! These bugs take a disproportionate amount of effort to file
and mentor compared to their actual value -- the key is to progress the
contributor to the next level once it's clear they can handle the basics
involved in solving such an issue (checking out the source code, applying a
fix, submitting a patch, etc). Otherwise you're going to feel frustrated and
wonder why you're on an endless treadmill of writing up trivial bugs.

Third, once a contributor has established themselves by fixing a few of these
simple issues, I try to get to know them a little better.  Send them an email,
learn where they're from, invite them to chat on the project channel if they
can. At the same time, this is an opportunity to craft a somewhat larger piece
of work (a sort of mini-project) that they can do, tailored to the interests.
For example, a new contributor on the Mission Control has recently been
working on adding [Jest](https://jestjs.io/) tests to the project -- I
provided some basic guidance of things to look at, but did not dictate exactly
*how* to perform the task. They figured that out for themselves.

As time goes by, you just continue this process. Depending on the contributor,
they may start coming up with their own ideas for how a project might be
improved or they might still want to follow your lead (or that of the team),
but at the least I generally see an improvement in their self-directedness and
confidence after a period of sustained contribution. In either case, the key
to success remains the same: sustained and positive communication and sharing
of goals and aspirations, making sure that both parties are getting something
positive out of the experience. Where possible, I try to include contributors
in team meetings. Where there's an especially close working relationship (e.g.
[Google Summer of Code](https://summerofcode.withgoogle.com/archive/)). I try
to set up a weekly one on one. Regardless, I make reviewing code, answering
questions, and providing suggestions on how to move forward a top priority
(i.e. not something I'll leave for a few days). It's the least I can do if
someone is willing to take time out to contribute to my project.

If this seems similar to the best practices for how members of a team should
onboard each other and work together, that's not really a coincidence.
Obviously the relationship is a little different because we're not operating
with a formal managerial structure and usually the work is unpaid: I try to bear
that mind and make double sure that contributors are really getting some
useful skills and habits that they can take with them to future jobs and other
opportunities, while also emphasizing that their code contributions are their
own, not Mozilla's. So far it seems to have worked out pretty well for all
concerned (me, Mozilla, and the contributors).
