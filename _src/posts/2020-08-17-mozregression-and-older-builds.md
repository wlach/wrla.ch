    Title: mozregression and older builds
    Date: 2020-08-17T15:01:57
    Tags: Mozilla, mozregression, telemetry

Periodically the discussion comes up about pruning away old stored Firefox build artifacts in S3. Each build is tens of megabytes, multiply that by the number of platforms we support and the set of revisions we churn through on a daily basis, and pretty soon you're talking about real money.

This came up recently in a discussion about [removing the legacy taskcluster deployment](https://groups.google.com/g/mozilla.dev.platform/c/0OV_M3b-cMM/m/kkknfFdECgAJ) -- what do we actually lose by cutting back our archive of integration builds? The main reason to keep them around is to facilitate bisection testing with [mozregression](https://mozilla.github.io/mozregression/), to find out when a bug was introduced. Up to now, discussions about this have been a bit hand-wavey: we do keep logs about who's accessing old builds, but it's never been clear whether it was mozregression accessing them or something else.

Happily, now that [mozregression has some telemetry](/blog/2020/05/this-week-in-glean-mozregression-telemetry-part-2/), it's a little easier to get some answers on what people are actually doing. This query gets the distribution of build ages (launched or bisected) over the past 6 months, at a month long granularity.[^1] Ages are relative to the date mozregression was launched: for example, if someone asked for a build from May 2019 in June 2020, the number would be "13".

[^1]: I only added the telemetry to capture this information [relatively recently](https://bugzilla.mozilla.org/show_bug.cgi?id=1651401), so we're actually only looking at about a month of data in this post. We'll have more complete results later this year.

```sql
SELECT metrics.string.usage_app AS app,
       metrics.string.usage_build_type AS build_type,
       DATE_DIFF(DATE(submission_timestamp), IF(LENGTH(metrics.datetime.usage_bad_date) > 0, PARSE_DATE('%Y-%m-%d', substr(metrics.datetime.usage_bad_date, 1, 10)), PARSE_DATE('%Y-%m-%d', substr(metrics.datetime.usage_launch_date, 1, 10))), MONTH) + 1 AS build_age
FROM `moz-fx-data-shared-prod`.org_mozilla_mozregression.usage
WHERE DATE(submission_timestamp) >= DATE_SUB(CURRENT_DATE(), INTERVAL 6 MONTH)
  AND client_info.app_display_version NOT LIKE '%dev%'
  AND LENGTH(metrics.string.usage_build_type) > 0
  AND (LENGTH(metrics.datetime.usage_bad_date) > 0
       OR LENGTH(metrics.datetime.usage_launch_date) > 0)
```

I ran this query on sql.telemetry.mozilla.org and generated a box plot, broken down by product and build type:

![](/files/2020/08/mozregression-build-age-box-plot.png)
[link](https://sql.telemetry.mozilla.org/queries/73968#184980) (requires Mozilla LDAP)

Unsurprisingly, Firefox shippable builds are the number one thing people try to bisect. Let's take a little bit of a closer look at what's going on there:

![](/files/2020/08/mozregression-build-age-box-plot-detail.png)

The median value is 1, which indicates that most people are bisecting builds within one month of the day in which mozregression was run. And the [upper fence](https://www.statisticshowto.com/upper-and-lower-fences/) result is 6, suggesting that most of the time people are looking at a regression range that is within a 6 month range. However, looking more closely at the data points themselves (the little points in the chart above), there are a considerable number of outliers where a range greater than 20 months was asked for.

... which brings up to the question that we want to answer. Given that getting old builds isn't that common (which we sort of knew already, based on the access patterns in the S3 logs), what is the impact of the times that we do? And it's here where I have to throw up my hands and say "I don't know" and suggest that we go back to empirical observation and user research. 

You can go back to the thread I linked above, and see that core Firefox/Gecko developers find the ability to get a precise regression range for older revisions valuable. One thing that's worth mentioning is that mozregression isn't run that often, compared to a product that we ship: on the order of 50 to 100 times per a day. But when it comes to internal tooling, a small amount of use might have a big impact: if a mozregression invocation a developer a few hours (or more), that's a real benefit to Firefox and Mozilla. The same argument might apply here, where a small number of bisections on older builds might have a disproportionate impact on the quality of the product.