    Title: Mission Control 1.0
    Date: 2018-06-05T17:50:32
    Tags: Mozilla, Mission Control

Just a quick announcement that the first "production-ready" version of
Mission Control just went live yesterday, at this easy-to-remember URL:

[https://missioncontrol.telemetry.mozilla.org](https://missioncontrol.telemetry.mozilla.org)

For those not yet familiar with the project, Mission Control aims to track release
stability and quality across Firefox releases. It is similar in spirit to arewestableyet
and other crash dashboards, with the following new and exciting properties:

* Uses the full set of crash counts gathered via telemetry, rather than the arbitrary
  sample that users decide to submit to crash-stats
* Results are available within minutes of ingestion by telemetry (although be warned
  [initial results for a release always look bad](/blog/2017/10/better-or-worse-by-what-measure/))
* The denominator in our crash rate is usage hours, rather than the probably-incorrect
  calculation of active-daily-installs used by
  [arewestableyet](https://arewestableyet.com) (not a knock on the people who
  wrote that tool, there was nothing better available at the time)
* We have a detailed breakdown of the results by platform (rather than letting Windows
  results dominate the overall rates due to its high volume of usage)

In general, my hope is that this tool will provide a more scientific and
accurate idea of release stability and quality over time. There's lots more to
do, but I think this is a promising start. Much gratitude to
[kairo](https://home.kairo.at/blog/2014-04/how_effective_is_the_stability_program),
calixte, [chutten](https://chuttenblog.wordpress.com/) and others who helped
build my understanding of this area.

The dashboard itself an easier thing to show than talk about, so I recorded a quick
demonstration of some of the dashboard's capabilities and published it on air mozilla:

<iframe src="https://air.mozilla.org/mission-control-dashboard-intro/video/" width="896" height="524" frameborder="0" allowfullscreen></iframe>

[link](https://air.mozilla.org/mission-control-dashboard-intro/)