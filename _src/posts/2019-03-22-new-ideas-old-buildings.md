    Title: New ideas, old buildings
    Date: 2019-03-22T15:08:11
    Tags: Mozilla, Iodide

Last week, Brendan Colloran [announced Iodide](https://hacks.mozilla.org/2019/03/iodide-an-experimental-tool-for-scientific-communicatiodide-for-scientific-communication-exploration-on-the-web/), a
new take on scientific collaboration and reporting that I've been
really happy to contribute to over the past year-and-a-bit. I've been
describing it to people I meet as kind of "[glitch](https://glitch.com/) meets [jupyter](https://jupyter.org/)
" but that doesn't quite do it justice. I'd recommend reading
Brendan's blog post (and taking a look at our
[demonstration site](https://alpha.iodide.io)) to get the full picture.

One question that I've heard asked (including on Brendan's post) is why we
chose a rather conventional and old technology
([Django](https://www.djangoproject.com/)) for the server backend. Certainly,
Iodide has not been shy about building with relatively new or experimental
technologies for other parts (e.g. Python on WebAssembly for the notebooks,
React/Redux for the frontend). Why not complete the cycle by using a
new-fangled JavaScript web server like, I don't know,
[NestJS](https://nestjs.com/)?  And while we're at it, what's with iodide's
ridiculous [REST
API](https://en.wikipedia.org/wiki/Representational_state_transfer)? Don't you
know [GraphQL](https://graphql.org/) is the only legitimate way to expose your
backend to the world in 2019?

The great urban theorist of the twentieth century, [Jane
Jacobs](https://en.wikipedia.org/wiki/Jane_Jacobs) has a quote I love:

<i>“Old ideas can sometimes use new buildings. New ideas must use old
buildings.”</i>

Laura Thompson (an engineering director at Mozilla) has restated this
wisdom in a software development context as ["Build exciting things with boring
technologies"](https://speakerdeck.com/lauraxt/build-exciting-things-with-boring-technologies).

It so happened that the server was not an area Iodide was focusing on for
innovation (at least initially), so it made much, much more sense to use
something proven and battle-tested for the server side deployment. I'd used
Django for a number of projects at Mozilla before this one
([Treeherder/Perfherder](https://github.com/mozilla/treeherder) and [Mission
Control](https://github.com/mozilla/missioncontrol/)) and have been wildly
impressed by the project's excellent
[documentation](https://docs.djangoproject.com/), [database access
layer](https://docs.djangoproject.com/en/2.1/topics/db/), and support for
building a standardized API via the [Django REST
Framework](https://www.django-rest-framework.org/) add-on. Not to mention the
fact that so much of Mozilla's in-house ops and web development expertise is
based around this framework (I could name off probably 5 or 6 internal
business systems based around the Django stack, in addition to Treeherder), so
deploying Iodide and getting help building it would be something of a known
quantity.

Only slightly more than half a year since I began work on the iodide server,
we now have both a publicly accessible site for others to experiment with
*and* an internal one for Mozilla's business needs. It's hard to say what
would have happened had I chosen something more experimental to build Iodide's
server piece, but at the very least there would have been a substantial
learning curve involved -- in addition to engineering effort to fill in the
gaps where the new technology is not yet complete -- which would have meant
less time to innovate where it really mattered. Django's [database migration
system](https://docs.djangoproject.com/en/2.1/topics/migrations/), for
example, took years to come to fruition and I'm not aware of anything
comparable in the world of JavaScript web frameworks.

As we move ahead, we may find places where applying new backend server
technologies makes sense. Heck, maybe we'll chose to rewrite the whole
thing at some point. But to get to launch, chosing a bunch of boring, tested
software for this portion of Iodide was (in my view) absolutely
the right decision and I make no apologies for it.
