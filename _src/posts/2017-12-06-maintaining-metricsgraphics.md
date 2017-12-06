    Title: Maintaining metricsgraphics
    Date: 2017-12-06T17:16:23
    Tags: Mozilla, Mission Control

Just a quick announcement that I've taken it upon myself to assume some maintership
duties of the popular [MetricsGraphics](https://github.com/mozilla/metrics-graphics)
library and have released a [new version](https://www.npmjs.com/package/metrics-graphics)
with some bug fixes (2.12.0). We use this package pretty extensively at Mozilla for
visualizing telemetry and other time series data, but its original authors (Hamilton
Ulmer and Ali Almossawi) have mostly moved on to other things so there was a bit of a
gap in getting fixes and improvements in that I hope to fill.

I don't yet claim to be an expert in this library (which is quite rich and complex),
but I'm sure I'll learn more as I go along. At least initially, I expect that the changes
I make will be small and primarily targetted to filling the needs of the
[Mission Control](https://github.com/mozilla/missioncontrol) project.

Note that this emphatically does *not* mean I am promising to respond to every
issue/question/pull request made against the project. Like my work with mozregression
and perfherder, my maintenance work is being done on a best-effort basis to support
Mozilla and the larger open source community. I'll help people out where I can, but
there are only so many working hours in a day and I need to spend most of those
pushing my team's immediate projects and deliverables forward! In particular, when it
comes to getting pull requests merged, small, self-contained and logical changes with
good commit messages will take priority.
