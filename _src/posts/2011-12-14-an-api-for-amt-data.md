    Title: An API for AMT data
    Date: 2011-12-14T00:00:00
    Tags: Open Data, Transit

The [AMT][1] released their [GTFS schedule information][2] to the public earlier this week, which is awesome. Not coincidentally, Montreal is going to have a [Transportation Camp][3] tomorrow, wherein people will hack on transportation software and discuss open data issues.

GTFS information is useful and standard, but in its raw form it can be a bit difficult to wrangle with. So in advance of the event, I thought it might be helpful/useful to put a simple JSON API to the data, based on my [routez][4] software. Should be useful for creating an app or two! There's two endpoints that are currently defined:

`/api/v1/stop/<stop code>/upcoming_stoptimes`

This will give a set of upcoming departures at a particular AMT stop (represented by its code). Example:

<http://amt.wrla.ch/blog/api/v1/stop/11260/upcoming_stoptimes>

`/api/v1/place/<lat,lng>/upcoming_stoptimes?distance=<distance in meters>`

This will give a set of AMT stops within range of that endpoint, along with upcoming departures. Example:

<http://amt.wrla.ch/blog/api/v1/place/45.49640,%20-73.57567/upcoming_stoptimes?distance=1000>

[1]: http://www.amt.qc.ca
[2]: http://t.co/AofpyI4E
[3]: http://transportationcamp.org/montreal/
[4]: http://github.com/wlach/routez
