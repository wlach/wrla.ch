    Title: Functional is the future
    Date: 2017-08-28T17:02:21
    Tags: Mozilla

Just spent well over an hour tracking down a silly bug in my code. For
the [mission control](https://github.com/mozilla/missioncontrol/) project, I
wrote this very simple API method that returns a cached data structure to our front
end:

```py
def measure(request):
    channel_name = request.GET.get('channel')
    platform_name = request.GET.get('platform')
    measure_name = request.GET.get('measure')
    interval = request.GET.get('interval')
    if not all([channel_name, platform_name, measure_name]):
        return HttpResponseBadRequest("All of channel, platform, measure required")
    data = cache.get(get_measure_cache_key(platform_name, channel_name, measure_name))
    if not data:
        return HttpResponseNotFound("Data not available for this measure combination")
    if interval:
        try:
            min_time = datetime.datetime.now() - datetime.timedelta(seconds=int(interval))
        except ValueError:
            return HttpResponseBadRequest("Interval must be specified in seconds (as an integer)")

        # Return any build data in the interval
        empty_buildids = set()
        for (build_id, build_data) in data.items():
            build_data['data'] = [d for d in build_data['data'] if d[0] > min_time]
            if not build_data['data']:
                empty_buildids.add(build_id)

        # don't bother returning empty indexed data
        for empty_buildid in empty_buildids:
            del data[empty_buildid]

    return JsonResponse(data={'measure_data': data})
```

As you can see, it takes 3 required parameters (channel, platform, and measure) and
one optional one (interval), picks out the required data structure, filters it a bit,
and returns it. This is *almost* what we wanted for the frontend, unfortunately
the time zone information isn't quite what we want, since the strings that
are returned don't tell the frontend that they're in UTC format -- they need a 'Z'
appended to them for that.

After a bit of digging, I found out that Django's [json serializer](https://github.com/django/django/blob/afc06b56256f78ab832ff8066ac6f34b7443de22/django/core/serializers/json.py#L76) will only add the Z if the tzinfo structure is specified. So I figured out a simple
pattern for adding that (using the dateutil library, which we are fortunately already
using):

```py
from dateutil.tz import tzutc
datetime.datetime.fromtimestamp(mydatestamp.timestamp(), tz=tzutc())
```

I tested this quickly on the python console and it seemed to work great. But when
I added the code to my function, the unit tests mysteriously failed. Can you see
why?

```py
for (build_id, build_data) in data.items():
    # add utc timezone info to each date, so django will serialize a
    # 'Z' to the end of the string (and so javascript's date constructor
    # will know it's utc)
    build_data['data'] = [
        [datetime.datetime.fromtimestamp(d[0].timestamp(), tz=tzutc())] + d[1:] for
        d in build_data['data'] if d[0] > min_time
    ]
```

Trick question: there's actually nothing wrong with this code. But if you look at the block
in context (see the top of the post), you see that it's only executed if *interval* is
specified, which it isn't necessarily. The first case that my unit tests executed didn't
specify interval, so fail they did. It wasn't immediately obvious to me why this was happening,
so I went on a wild-goose chase of trying to figure out how the Django context might have
been responsible for the unexpected output, before realizing my basic logic error.

This was fairly easily corrected (my updated code applies the datetime-mapping
unconditionally to set of optionally-filtered results) but perfectly illustrates my
issue with idiomatic python: while the language itself has constructs like `map` and
`reduce` that support the functional programming model, the language strongly steers you
towards writing things in an imperative style that makes costly and annoying mistakes like
this much easier to make. Yes, list and dictionary comprehensions are nice and compact but they
start to break down in the more complex cases.

As an experiment, I wrote up what this function might look like in a pure functional
style with immutable data structures:

```py
def transform_and_filter_data(build_data):
    new_build_data = copy.copy(build_data)
    new_build_data['data'] = [
        [datetime.datetime.fromtimestamp(d[0].timestamp(), tz=tzutc())] + d[1:] for
        d in build_data['data'] if d[0] > min_time
    ]
    return new_build_data
transformed_build_data = {k: v for k, v in {k: transform_and_filter_data(v) for k, v in data}.items() if len(v['data']) > 0}
```

A work of art it isn't -- and definitely not "pythonic". Compare this to a
similar piece of code written in Javascript (ES6) with lodash (using a hypothetical
`tzified` function):

```js
let transformedBuildData = _.filter(_.mapValues(data, (buildData) => ({
    ...buildData,
    data: buildData.data
      .filter(datum => datum[0] > minTimestamp)
      .map(datum => [tzcified(datum[0])].concat(datum.slice(1)))
  })),
  (data, buildId) => data.data.length > 0);
```

A little bit easier to understand, but more importantly (to me anyway) it comes
across as idiomatic and natural in a way that the python version just doesn't. I've
been happily programming Python for the last 10 years, but it's increasingly
feeling time to move on to greener pastures.
