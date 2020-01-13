    Title: Conda is pretty great
    Date: 2020-01-13T11:08:57
    Tags: Mozilla, Telemetry

Lately the data engineering team has been looking into productionizing (i.e.
running in Airflow) a bunch of models that the data science team has been
producing. This often involves languages and environments that are a bit
outside of our comfort zone -- for example, [the next version of Mission
Control](https://github.com/mozilla/missioncontrol-v2) relies on the
[R-stan library](https://mc-stan.org/users/interfaces/rstan) to produce a
model of expected crash behaviour as Firefox is released.

To make things as simple and deterministic as possible, we've been building
up Docker containers to run/execute this code along with their dependencies,
which makes things nice and reproducible. My initial thought was to use
just the language-native toolchains to build up my container for the above
project, but quickly found a number of problems:

1. For local testing, Docker on Mac is *slow*: when doing a large number
of statistical calculations (as above), you can count on your testing
iterations taking 3 to 4 (or more) times longer.
2. On initial setup, the default R packaging strategy is to have the
user of a package like R-stan recompile from source. This can take *forever*
if you have a long list of dependencies with C-compiled extensions (pretty
much a given if you're working in the data space): rebuilding
my initial docker environment for missioncontrol-v2 took almost an hour. This
isn't just a problem for local development: it also makes continuous
integration using a service like Circle or Travis expensive and painful.

I had been vaguely aware of [Conda](https://docs.conda.io/en/latest/) for a
few years, but didn't really understand its value proposition until I started
working on the above project: why bother with a heavyweight package manager
when you already have Docker to virtualize things? The answer is that it solves
both of the above problems: for local development, you can get something
more-or-less identical to what you're running inside Docker with no performance
penalty whatsoever. And for building the docker container itself, Conda's
package repository contains pre-compiled versions of all the dependencies
you'd want to use for something like this (even somewhat esoteric libraries
like R-stan are available on [conda-forge](https://conda-forge.org/)), which
brought my build cycle times down to less than 5 minutes.

tl;dr: If you have a bunch of R / python code you want to run in a reproducible
manner, consider Conda.
