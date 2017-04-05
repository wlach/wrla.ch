    Title: Easier reproduction of intermittent test failures in automation
    Date: 2017-04-05T16:14:35
    Tags: Mozilla, Treeherder, Taskcluster

As part of the [Stockwell
project](https://wiki.mozilla.org/Auto-tools/Projects/Stockwell),
I've been hacking on ways to make it easier for developers to
diagnose failure of our tests in automation. It's often very difficult
to reproduce an intermittent failure we see in Treeherder locally since the
environment is so different, but historically it has been a big hassle
to get access to the machines we use in automation for various reasons.

One option that rolled out last year was the so-called one-click loaner,
which enabled developers to sign out an virtual machine instance identical to the
ones used to run unit tests (at least if the tests are running on
Taskcluster, which is increasingly often the case), then execute
their particular case with whatever extra debugging options they
would find useful. This is a big step forward, but it's still quite
a bit of hassle, since it requires a bunch of manual work on the part
of the developer to interact with the instance.

What if we could *just* re-run the particular test an arbitrary
number of times with whatever options we wanted, simply by clicking
on a few buttons on Treeherder? I've been exploring this for the
first few months of 2017 and I've come up with a prototype which
I think is ready for people to start playing with.

The user interface to this is pretty straightforward. Just find a job you
want to retrigger in Treeherder:

<img src="/files/2017/04/treeherder-selected-mochitest.png"/>

Then select the '...' option in the panel below and press "Custom Action...":

<img src="/files/2017/04/treeherder-taskcluster-options.png"/>

You should get a small piece of JSON to edit, which corresponds to
the configuration for the retriggered job:

<img src="/files/2017/04/treeherder-custom-action.png"/>

The main field to edit is "path". You should set this to the name of
the test you want to try retriggering. For example
`dom/animation/test/css-transitions/test_animation-ready.html`. You
can also set custom Firefox preferences and environment variables,
to turn on different types of debugging.

Unfortunately as usual with a new feature at Mozilla, there are a bunch of
limitations and caveats:

* This depends on functionality that's only in Taskcluster, so
  buildbot jobs are exempt.
* No support for Android yet. In combination with the above
  limitation, this implies that this functionality only works
  on Linux (at least until other platforms are moved to Taskcluster,
  which hopefully isn't that far off).
* Browser chrome tests failing in mysterious ways if run repeatedly
  ([bug 1347654](https://bugzilla.mozilla.org/show_bug.cgi?id=1347654))
* Only reftest and mochitest are currently supported. XPCShell
  support is blocked by the lack of support in its harness for
  running a job repeatedly ([bug 1347696](https://bugzilla.mozilla.org/show_bug.cgi?id=1347696)).
  Web Platform Tests need the requisite support in mozharness for
  just setting up the tests without running them -- the same issue
  that prevents us from debugging such tests with a one-click loaner
  ([bug 1348833](https://bugzilla.mozilla.org/show_bug.cgi?id=1348833)).

Aside from fixing the above limitations, the following features
would also be really nifty to have:

* Ability to trigger a custom job as part of a try push (i.e.
  not needing to retrigger off an existing job)
* Run these jobs under rr, and provide a way to login and
  interactively debug when the problem is actually reproduced.

I am actually in the process of moving to another team @ Mozilla (more
on that in another post), so I probably won't have a ton of time to
work on the above -- but I'd be happy to help anyone who's interested
in developing this idea further.

A special shout out to the [Taskcluster](https://wiki.mozilla.org/TaskCluster) team for
helping me with the development of this feature: in particular the action task
implementation from [Jonas Finnemann Jensen](https://jonasfj.dk/) that
made it possible to develop this feature in the first place.
