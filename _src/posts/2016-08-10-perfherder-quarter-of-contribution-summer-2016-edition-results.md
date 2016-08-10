    Title: Perfherder Quarter of Contribution: Summer 2016 Edition Results!
    Date: 2016-08-10T13:38:49
    Tags: Mozilla, Perfherder

Following on the footsteps of Mike Ling's [amazing work](/blog/2015/09/perfherder-summer-of-contribution-thoughts/) on [Perfherder](https://wiki.mozilla.org/ngineeringProductivity‎/Projects/Perfherder) in 2015 (he's gone on to do a GSOC project), I
got two amazing contributors to continue working on the project for
a few weeks this summer as part of our [quarter of
contribution](https://wiki.mozilla.org/Auto-tools/New_Contributor/Quarter_of_Contribution) program: Shruti Jasoria and Roy Chiang.

Shruti started by adding a feature to the treeherder/perfherder backend (ability
to enable or disable a new performance framework on a tentative basis), then
went on to make all sorts of improvements to the Treeherder / Perfherder frontend,
fixing bugs in the performance sheriffing frontend, updating code to use more
modern standards (including a gigantic patch to enable a bunch of eslint rules
and fix the corresponding problems).

Roy worked all over the codebase, starting with some simple frontend fixes
to Treeherder, moving on to fix a large number of nits in Perfherder's alerts
view. My personal favorite is the fact that we now paginate the list of alerts
inside this view, which makes navigation waaaaay back into history possible:

<a href="/files/2016/08/perfherder-alert-pagination.png"><img src="/files/2016/08/perfherder-alert-pagination.png" alt="alert pagination" width="300px"/></a>

You can see a summary of their work at these links:

* [Shruti Jasoria](https://github.com/mozilla/treeherder/commits/master?author=SJasoria)
* [Roy Chiang](https://github.com/mozilla/treeherder/commits/master?author=crosscent)

Thank you Shruti and Roy! You've helped to make sure Firefox (and Servo!)
performance remains top-notch.