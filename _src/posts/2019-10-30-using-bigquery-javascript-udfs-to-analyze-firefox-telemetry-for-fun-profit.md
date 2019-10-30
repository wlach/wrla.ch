    Title: Using BigQuery JavaScript UDFs to analyze Firefox telemetry for fun & profit
    Date: 2019-10-30T11:11:17
    Tags: Mozilla, Telemetry

For the last year, we've been gradually migrating our backend Telemetry
systems from AWS to GCP. I've been helping out here and there with this
effort, most recently porting a job we used to detect slow tab spinners in
Firefox nightly, which produced a small dataset that feeds a [small adhoc
dashboard](https://mikeconley.github.io/bug1310250/) which Mike Conley
Maintains. This was a relatively small task as things go, but it highlighted
some features and improvements which I think might be broadly interesting, so
I decided to write up a small blog post about it.

Essentially all this dashboard tells you is what percentage of the Firefox
nightly population saw a tab spinner over the past 6 months. And of those that
did see a tab spinner, what was the severity? Essentially we’re just trying to
make sure that there are no major regressions of user experience (and also
that efforts to improve things bore fruit):

<center><img style="width:600px" srcset="/files/2019/10/tab-spinner-dash.png"/></center>

Pretty simple stuff, but getting the data necessary to produce this kind of
dashboard used to be anything but trivial: while some common business/product
questions could be answered by a quick query to
[clients_daily](https://docs.telemetry.mozilla.org/datasets/batch_view/clients_daily/reference.html),
getting engineering-specific metrics like this usually involved trawling
through gigabytes of raw heka encoded blobs using a Spark and then extracting
the relevant information out of the telemetry probe histograms (in this case,
FX_TAB_SWITCH_SPINNER_VISIBLE_MS and FX_TAB_SWITCH_SPINNER_VISIBLE_LONG_MS)
contained therein.

The code itself was rather complicated ([take a look, if you
dare](https://github.com/mozilla/python_mozetl/blob/58dce245ce8012b338e8b102a8c2c0f00601be60/mozetl/tab_spinner/tab_spinner.py))
but even worse, running it could get *very expensive*. We had a 14 node
cluster churning through this script daily, and it took on average about an
hour and a half to run! I don't have the exact cost figures on hand (and am
not sure if I'd be authorized to share them if I did), but based on a back of
the envelope sketch, this one single script was probably costing us somewhere
on the order of $10-$40 a day.

With our move to [BigQuery](https://cloud.google.com/bigquery/), things get a
lot simpler! Thanks to the combined effort of my team and data operations[1],
we now produce "stable" ping tables on a daily basis with *all* the relevant
histogram data (stored as JSON blobs), queryable using relatively vanilla SQL.
In this case, the data we care about is in `telemetry.main` (named after the
main ping, appropriately enough). With the help of a small [JavaScript
UDF](https://cloud.google.com/bigquery/docs/reference/standard-sql/user-defined-functions)
function, all of this data can easily be extracted into a table inside a
single SQL query scheduled by
[sql.telemetry.mozilla.org](https://docs.telemetry.mozilla.org/tools/stmo.html).

```
CREATE TEMP FUNCTION
  udf_js_json_extract_highest_long_spinner (input STRING)
  RETURNS INT64
  LANGUAGE js AS """
    if (input == null) {
      return 0;
    }
    var result = JSON.parse(input);
    var valuesMap = result.values;
    var highest = 0;
    for (var key in valuesMap) {
      var range = parseInt(key);
      if (valuesMap[key]) {
        highest = range > 0 ? range : 1;
      }
    }
    return highest;
""";

SELECT build_id,
sum (case when highest >= 64000 then 1 else 0 end) as v_64000ms_or_higher,
sum (case when highest >= 27856 and highest < 64000 then 1 else 0 end) as v_27856ms_to_63999ms,
sum (case when highest >= 12124 and highest < 27856 then 1 else 0 end) as v_12124ms_to_27855ms,
sum (case when highest >= 5277 and highest < 12124 then 1 else 0 end) as v_5277ms_to_12123ms,
sum (case when highest >= 2297 and highest < 5277 then 1 else 0 end) as v_2297ms_to_5276ms,
sum (case when highest >= 1000 and highest < 2297 then 1 else 0 end) as v_1000ms_to_2296ms,
sum (case when highest > 0 and highest < 50 then 1 else 0 end) as v_0ms_to_49ms,
sum (case when highest >= 50 and highest < 100 then 1 else 0 end) as v_50ms_to_99ms,
sum (case when highest >= 100 and highest < 200 then 1 else 0 end) as v_100ms_to_199ms,
sum (case when highest >= 200 and highest < 400 then 1 else 0 end) as v_200ms_to_399ms,
sum (case when highest >= 400 and highest < 800 then 1 else 0 end) as v_400ms_to_799ms,
count(*) as count
from
(select build_id, client_id, max(greatest(highest_long, highest_short)) as highest
from
(SELECT
    SUBSTR(application.build_id, 0, 8) as build_id,
    client_id,
    udf_js_json_extract_highest_long_spinner(payload.histograms.FX_TAB_SWITCH_SPINNER_VISIBLE_LONG_MS) AS highest_long,
    udf_js_json_extract_highest_long_spinner(payload.histograms.FX_TAB_SWITCH_SPINNER_VISIBLE_MS) as highest_short
FROM telemetry.main
WHERE
    application.channel='nightly'
    AND normalized_os='Windows'
    AND application.build_id > FORMAT_DATE("%Y%m%d", DATE_SUB(CURRENT_DATE(), INTERVAL 2 QUARTER))
    AND DATE(submission_timestamp) >= DATE_SUB(CURRENT_DATE(), INTERVAL 2 QUARTER))
group by build_id, client_id) group by build_id;
```

In addition to being much simpler, this new job is also *way* cheaper. The
last run of it scanned just over 1 TB of data, meaning it cost us just over
$5. Not as cheap as I might like, but considerably less expensive than before: I've
also scheduled it to only run once every other day, since Mike tells me he
doesn't need this data any more often than that.

[1] I understand that Jeff Klukas, Frank Bertsch, Daniel Thorn, Anthony
Miyaguchi, and Wesley Dawson are the principals involved - apologies if I'm
forgetting someone.
