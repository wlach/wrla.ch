    Title: mozregression update May 2021
    Date: 2021-05-10T09:56:43
    Tags: Mozilla, Glean, Telemetry, mozregression

Just wanted to give some quick updates on the state of [mozregression](https://mozilla.github.io/mozregression).

## Anti-virus false positives

One of the persistent issues with mozregression is that it seems to be [persistently
detected as a virus by many popular anti-virus scanners](https://bugzilla.mozilla.org/show_bug.cgi?id=1647533). The causes for this are
somewhat complex, but at root the problem is that mozregression requires fairly broad
permissions to do the things it needs to do (install and run copies of Firefox) and thus its behavior is hard to distinguish from a piece of software doing something malicious.

Recently there have been a number of mitigations which seem to be improving this situation:

- :bryce has been submitting copies of mozregression to Microsoft so that Windows Defender (probably the most popular anti-virus software on this platform) doesn't flag it.
- I recently [released mozregression 4.0.17](https://github.com/mozilla/mozregression/releases), which upgrades the GUI dependency for pyinstaller to a later version which sets PE checksums correctly on the generated executable ([pyinstaller/pyinstaller#5579](https://github.com/pyinstaller/pyinstaller/issues/5579)).

It's tempting to lament the fact that this is happening, but in a way I can understand it's hard to reliably detect what kind of software is legitimate and what isn't. I take the responsibility for distributing this kind of software seriously, and have pretty strict limits on who has access to the mozregression GitHub repository and what pull requests I'll merge.

## CI ported to GitHub Actions

Due to changes in Travis's policies, we needed to migrate continuous integration for mozregression to GitHub actions. You can see the gory details in [bug 1686039](https://bugzilla.mozilla.org/show_bug.cgi?id=1686039). One possibly interesting wrinkle to others: due to Mozilla's security policy, we can't use (most) external actions inside our GitHub repository. I thus rewrote the logic for uploading a mozregression release to GitHub for MacOS and Linux GUI builds (Windows builds are still happening via [AppVeyor](https://www.appveyor.com/) for now) [from scratch](https://github.com/mozilla/mozregression/blob/495ef37e701709dce3a4b76ea67ec5b1f26043be/.github/workflows/build.yml#L86). Feel free to check the above out if you have a similar need.

## MacOS Big Sur

As of version 4.0.17, the mozregression GUI now works on MacOS Big Sur. It is safe to ask community members to install and use it on this platform (though [note the caveats](https://mozilla.github.io/mozregression/install.html#mozregression-gui) due to the bundle being unsigned).

## Usage Dashboard

Fulfilling a promise I implied last year, I created a [public dataset](https://docs.telemetry.mozilla.org/cookbooks/public_data.html) for mozregression and created an [dashboard tracking mozregression use](https://observablehq.com/@wlach/mozregression-public-usage-dashboard) using [Observable](https://observablehq.com/). There are a few interesting insights and trends there that can be gleaned from our telemetry. I'd be curious if the community can find any more!
