    Title: End of Q2 Eideticker update: Flame tests, future plans
    Date: 2014-06-27T00:00:00
    Tags: Android, Eideticker, FirefoxOS, Mozilla

_[ For more information on the Eideticker software I'm referring to, see [this entry][1] ]_

Just wanted to give an update on where Eideticker is at the end of Q2 2014. The big news is that we've started to run startup tests against the Flame, the results of which are starting to appear on the dashboard:

[<img src="/files/2014/06/eideticker-contacts-flame.png" alt="eideticker-contacts-flame" width="1002" height="664" class="alignnone size-full wp-image-1062" srcset="/files/2014/06/eideticker-contacts-flame-300x198.png 300w, /files/2014/06/eideticker-contacts-flame.png 1002w" sizes="(max-width: 1002px) 100vw, 1002px" />][2] [[link]][3]

It is expected that these tests will provide a useful complement to the [existing startup tests][4] we're running with b2gperf, in particular answering the "is this regression real?" question.

Pending work for Q3:

- Enable scrolling tests on the Flame. I got these working against the Hamachi [a few months ago][5] but because of some weird input issue we're seeing we can't yet enable them on the Flame. This is being tracked in [bug 1028824][6]. If anyone has background on the behaviour of the touch screen driver for this device I would appreciate some help.
- Enable tests for multiple branches on the Flame (currently we're only doing master). This is pretty much ready to go ([bug 1017834][7]), just need to land it.
- Annotate eideticker graphs with internal benchmark information. Eli Perelman of the FirefoxOS performance team has come up with a standard set of on-load events for the Gaia apps (app chrome loaded, app content loaded, ...) that each app will generate, feeding into tools like b2gperf and test-perf. We want to show this information in Eideticker's frame-by-frame analysis ([example][8]) so we can verify that the app's behaviour is consistent with what it is claimed. This is being tracked in [bug 1018334][9]
- Re-enable Eideticker for Android and run tests more frequently. Sadly we haven't been consistently generating new Eideticker results for Android for the last quarter because of networking issues in the new Mountain View office, where the test rig for those live. One way or another, we want to fix this next quarter and hopefully run tests more frequently against mozilla-inbound (instead of just nightly builds)

The above isn't an exhaustive list: there's much more that we have in mind for the future that's not yet scheduled or defined well (e.g. get Eideticker reporting to Treeherder's new performance module). If you have any questions or feedback on anything outlined above I'd love to hear it!

[1]: http://wrla.ch/blog/2012/06/mobile-firefox-measuring-how-a-browser-feels/
[2]: /files/2014/06/eideticker-contacts-flame.png
[3]: http://eideticker.mozilla.org/b2g/#/flame/b2g-contacts-startup/timetostableframe
[4]: https://datazilla.mozilla.org/b2g/?branch=master&device=flame&range=7&test=cold_load_time&app_list=browser,calendar,camera,clock,contacts,email%20FTU,fm_radio,gallery,marketplace,messages,music,phone,settings,template,usage,video&app=phone&gaia_rev=b8f36518696f3191&gecko_rev=c90b38c47a1d&plot=avg
[5]: http://wrla.ch/blog/2014/03/its-all-about-the-entropy/
[6]: https://bugzilla.mozilla.org/show_bug.cgi?id=1028824
[7]: https://bugzilla.mozilla.org/show_bug.cgi?id=1017834
[8]: http://eideticker.mozilla.org/b2g/detail.html?id=2b007f8cfd8b11e3923c10ddb19eacac#/framecannyentropies
[9]: https://bugzilla.mozilla.org/show_bug.cgi?id=1018334
