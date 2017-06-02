    Title: Using Docker to run automated tests
    Date: 2017-06-02T16:04:38
    Tags: Mozilla, Docker

A couple months ago, I joined the Mozilla Data Platform team, to work on our [Telemetry](https://wiki.mozilla.org/Telemetry)
and automated data collection services. This has been an interesting transition for me,
and a natural jumping off point from my work on [Perfherder](https://wiki.mozilla.org/EngineeringProductivity/Projects/Perfherder). Now, instead
of manipulating mere 10s of gigabytes worth of fairly regular data, I'm working with 100s of terrabytes of noisy data with a much larger number of dimensions. :P It's been interesting so far.

One of the first things I decided to work on was improving our unit testing story around
a few of our primary packages for data analysis/etl: [python_moztelemetry](https://github.com/mozilla/python_moztelemetry/) (a library we
use for running custom spark jobs against Telemetry data) and [telemetry-batch-view](https://github.com/mozilla/telemetry-batch-view/) (a
set of scala jobs we run against the main telemetry data store to create a useful set of
aggregations that are easily queried with tools like [redash](https://redash.io/)).

It turns out that these tools interact with several larger / more involved pieces than I'm
used to dealing with (such as hbase and thrift). For continuous integration/automation, we
already had a set of travis scripts to install and reproduce the environment needed to test
these parts, but there was no straightforward way to do this locally. My third time through
creating an Ubuntu virtual machine environment to reproduce this environment locally (long
story), I figured it was finally time for me to investigate using something to
automate that setup procedure and make it easier for new developers to get into these
projects.

I hadn't used it much before, but [Docker](https://docker.com) seemed like a fairly obvious
choice. Small, simple, and Linuxy? Sign me up.

I'm pretty happy with how things turned out, but there were a few caveats. Docker is more
of a general purpose tool for building environments for running *things*, whether that be an
apache webserver or a jabber messaging doohickey (whereas e.g. something like travis is
basically a domain-specific language for creating and running automated tests). There were a
few tricks I needed to employ to make the whole testing process smooth in both cases, which
I'll document here for posterity:

1. You can `ADD` a set of files / directories to a docker environment inside your Dockerfile,
but if you want your set of tests to pick up any changes made since the environment was
created, you really should mount your testing directory inside the container using the `-v`
option.
2. If you need to download/install a piece of software when building the docker container,
use the `RUN` directive instead of `ADD`. This will speed up rebuilding the container
while you're iterating on it (because you can take advantage of the Docker layers cache).
3. You almost certainly want to create a script ([example](https://github.com/mozilla/python_moztelemetry/blob/d2aa84bbac09465d38eeb0b5beb20edc7ddcc21b/runtests.sh)) to streamline all the steps of running the
tests: this will make running the tests easier for anyone wanting to contribute to your
project and reduce the amount of documentation that you will have to write.

The relevant files and documentation are in the repositories linked above.
