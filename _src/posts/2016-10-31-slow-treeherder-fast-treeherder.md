    Title: Slow Treeherder, Fast Treeherder
    Date: 2016-10-31T11:40:00
    Tags: Mozilla, Treeherder, Performance

Just wanted to talk about some recent performance improvements we've made
recently to [Treeherder](https://wiki.mozilla.org/EngineeringProductivity/Projects/Treeherder):

* [Bug 1311511](https://bugzilla.mozilla.org/show_bug.cgi?id=1311511): Changed the repository endpoint so we don't do 40 redundant database
  queries (this was generally innocuous, but could delay loading by
  400ms if the database was under heavy load).
* [Bug 1310016](https://bugzilla.mozilla.org/show_bug.cgi?id=1310016): Persisted database connections across requests (this
  can save ~40-50ms per request, of which there can be 5-10
  when loading a Treeherder page).
* [Bug 1308782](https://bugzilla.mozilla.org/show_bug.cgi?id=1308782): *Don't* download job type and group information
  from the server to get a "sorting order" for the job lists. This was
  never necessary, but it's gotten exponentially more painful as
  people have added job types to Treeherder (job type information is
  now around a megabyte of JSON these days). This saves 5-10 seconds on a
  typical page load.

There's more to come, but with these changes Treeherder should be
faster for everyone to load. It should be particularly noticeable
on try pushes, where the last item was by far the largest bottleneck.
Here's a youtube video of the changes:

<iframe width="560" height="315" src="https://www.youtube.com/embed/xNJGoZhA4Vs" frameborder="0" allowfullscreen></iframe>

The original is on the left. The newer, faster Treeherder is on the right.
Pay particular attention to how much faster the job information populates.

Moral of the story? Optimization can be helpful, but it's better if you can
avoid doing the work altogether.