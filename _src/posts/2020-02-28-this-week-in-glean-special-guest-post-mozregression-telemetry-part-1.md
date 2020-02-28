    Title: This week in Glean (special guest post): mozregression telemetry (part 1)
    Date: 2020-02-28T10:50:58
    Tags: Mozilla, Telemetry, Glean, mozregression

*(“This Week in Glean” is a series of blog posts that the Glean Team at Mozilla is using to try to communicate better about our work. They could be release notes, documentation, hopes, dreams, or whatever: so long as it is inspired by Glean. You can find [an index of all TWiG posts online.](https://mozilla.github.io/glean/book/appendix/twig.html))*

*This is a special guest post by non-Glean-team member William Lachance!*

As I [mentioned last time](/blog/2019/09/mozregression-update-python-3-edition/) I talked about [mozregression](https://mozilla.github.io/mozregression/), I have been thinking about adding some telemetry to the system to better understand the usage of this tool, to justify some part of Mozilla spending some cycles maintaining and improving it (assuming my intuition that this tool is heavily used is confirmed). 

Coincidentally, the Telemetry client team has been working on a new library for measuring these types of things in a principled way called [Glean](https://mozilla.github.io/glean/book/index.html), which even has python bindings! Using this has the potential in saving a lot of work: not only does Glean provide a framework for submitting data, our backend systems are automatically set up to process data submitted via into Glean into [BigQuery](https://cloud.google.com/bigquery) tables, which can then easily be queried using tools like [sql.telemetry.mozilla.org](https://docs.telemetry.mozilla.org/tools/stmo.html).

I thought it might be useful to go through some of what I've been exploring, in case others at Mozilla are interested in instrumenting their pet internal tools or projects. If this effort is successful, I'll distill these notes into a tutorial in the Glean documentation.

## Initial steps: defining pings and metrics

The initial step in setting up a Glean project of any type is to define explicitly the types of pings and metrics. You can look at a "ping" as being a small bucket of data submitted by a piece of software in the field. A "metric" is something we're measuring and including in a ping.

Most of the Glean documentation focuses on browser-based use-cases where we might want to sample lots of different things on an ongoing basis, but for mozregression our needs are considerably simpler: we just want to know when someone *has* used it along with a small number of non-personally identifiable characteristics of their usage, e.g. the mozregression version number and the name of the application they are bisecting.

Glean has [the concept of event pings](https://mozilla.github.io/glean/book/user/pings/events.html), but it seems like those are there more for a fine-grained view of what's going on during an application's use. So let's define a new ping just for ourselves, giving it the unimaginative name "usage". This goes in a file called `pings.yaml`:

```yaml
---
$schema: moz://mozilla.org/schemas/glean/pings/1-0-0

usage:
  description: >
    A ping to record usage of mozregression
  include_client_id: true
  notification_emails:
    - wlachance@mozilla.com
  bugs:
    - http://bugzilla.mozilla.org/123456789/
  data_reviews:
    - http://example.com/path/to/data-review
```

We also need to define a list of things we want to measure. To start with, let's just test with one piece of sample information: the app we're bisecting (e.g. "Firefox" or "Gecko View Example"). This goes in a file called `metrics.yaml`:

```yaml
---
$schema: moz://mozilla.org/schemas/glean/metrics/1-0-0

usage:
  app:
    type: string
    description: >
      The name of the app being bisected
    notification_emails: 
      - wlachance@mozilla.com
    bugs: 
      - https://bugzilla.mozilla.org/show_bug.cgi?id=1581647
    data_reviews: 
      - http://example.com/path/to/data-review
    expires: never
    send_in_pings:
      - usage
```

The `data_reviews` sections in both of the above are obviously bogus, we will need to actually get data review before landing and using this code, to make sure that we're in conformance with Mozilla's [data collection policies](https://wiki.mozilla.org/Firefox/Data_Collection).

## Testing it out

But in the mean time, we can test our setup with the [Glean debug pings viewer](https://docs.telemetry.mozilla.org/concepts/glean/debug_ping_view.html) by setting a special tag (`mozregression-test-tag`) on our output. Here's a small python script which does just that:

```py
from pathlib import Path
from glean import Glean, Configuration
from glean import (load_metrics,
                   load_pings)

mozregression_path = Path.home() / '.mozilla2' / 'mozregression'

Glean.initialize(
    application_id="mozregression",
    application_version="0.1.1",
    upload_enabled=True,
    configuration=Configuration(
      ping_tag="mozregression-test-tag"
    ),
    data_dir=mozregression_path / "data"
)
Glean.set_upload_enabled(True)

pings = load_pings("pings.yaml")
metrics = load_metrics("metrics.yaml")

metrics.usage.app.set("reality")
pings.usage.submit()
```

Running this script on my laptop, I see that a respectable JSON payload was delivered to and processed by our servers:

<img style="width:600px" src="/files/2020/02/glean-debug-ping-viewer.png"/>

As you can see, we're successfully processing both the "version" number of mozregression, some characteristics of the machine sending the information (my MacBook in this case), as well as our single measure. We also have a client id, which should tell us roughly how many distinct installations of mozregression are sending pings. This should be more than sufficient for an initial "mozregression usage dashboard".

## Next steps

There are a bunch of things I still need to work through before landing this inside mozregression itself. Notably, the Glean python bindings are python3-only, so we'll need to [port the mozregression GUI to python 3](https://bugzilla.mozilla.org/show_bug.cgi?id=1426766) before we can start measuring usage there. But I'm excited at how quickly this work is coming together: stay tuned for part 2 in a few weeks.