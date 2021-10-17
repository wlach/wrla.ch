    Title: Documentation for mozdevice
    Date: 2013-03-11T00:00:00
    Tags: Android, ateam, FirefoxOS, Mozilla

Just wanted to give a quick heads up that as part of the ateam's ongoing effort to improve the documentation of our automated testing infrastructure, we now have [online documentation][1] for mozdevice, the python library we use for interacting with Android- and FirefoxOS-based devices in automated testing.

Mozdevice is used in pretty much every one of our testing frameworks that has mobile support, including mochitest, reftest, [talos][2], [autophone][3], and [eideticker][4]. Additionally, mozdevice is used by release engineering to clean up, monitor, and otherwise manage <strike>our hundred-odd</strike> the 1200\*\*\* tegra and panda development boards that we use in [tbpl][5]. See [sut_tools][6] (old, buildbot-based, what we currently use) and [mozpool][7] (the new and shiny future).

- Thanks to Dustin Mitchell for the correction.

[1]: https://mozbase.readthedocs.org/en/latest/mozdevice.html
[2]: https://wiki.mozilla.org/Buildbot/Talos
[3]: https://github.com/mozilla/autophone
[4]: https://wiki.mozilla.org/Project_Eideticker
[5]: http://tbpl.mozilla.org
[6]: https://hg.mozilla.org/build/tools/file/tip/sut_tools
[7]: https://github.com/mozilla/mozpool
