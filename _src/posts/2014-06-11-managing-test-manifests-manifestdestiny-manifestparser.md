    Title: Managing test manifests: ManifestDestiny -> manifestparser
    Date: 2014-06-11T00:00:00
    Tags: ateam, Mozilla

Just wanted to make a quick announcement that [ManifestDestiny][1], the python package we use internally here at Mozilla for declaratively managing lists of tests in [Mochitest][2] and other places, has been renamed to [manifestparser][3]. We kept the versioning the same (0.6), so the only thing you should need to change in your python package dependencies is a quick substitution of "ManifestDestiny" with "manifestparser". We will keep ManifestDestiny around indefinitely on pypi, but only to make sure old stuff doesn't break. New versions of the software will only be released under the name "manifestparser".

Quick history lesson: "Manifest destiny" refers to a philosophy of exceptionalism and expansionism that was widely held by American settlers in the 19th century. The concept is considered offensive by some, as it was used to justify displacing and dispossessing Native Americans. Wikipedia's [article][4] on the subject has a good summary if you want to learn more.

Here at [Mozilla Tools &#038; Automation][5], we're most interested in creating software that everyone can feel good about depending on, so we agreed to rename it. When I raised this with my peers, there were no objections. I know these things are often the source of much drama in the free software world, but there's really none to see here.

Happy manifest parsing!

[1]: https://pypi.python.org/pypi/ManifestDestiny
[2]: https://developer.mozilla.org/en/docs/Mochitest
[3]: https://pypi.python.org/pypi/manifestparser
[4]: http://en.wikipedia.org/wiki/Manifest_destiny
[5]: https://wiki.mozilla.org/Auto-tools
