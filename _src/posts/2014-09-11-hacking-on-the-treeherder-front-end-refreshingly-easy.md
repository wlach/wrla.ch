    Title: Hacking on the Treeherder front end: refreshingly easy
    Date: 2014-09-11T00:00:00
    Tags: Mozilla


Over the past two weeks, I&#8217;ve been working a bit on the [Treeherder][1] front end (our interface to managing build and test jobs from mercurial changesets), trying to help get things in shape so that the sheriffs can feel comfortable transitioning to it from [tbpl][2] by the end of the quarter.

One thing that has pleasantly surprised me is just how easy it&#8217;s been to get going and be productive. The process looks like this on Linux or Mac:

`<br />
git clone https://github.com/mozilla/treeherder-ui.git<br />
cd treeherder-ui/webapp<br />
./scripts/web-server.js<br />
`

Then just load http://localhost:8000 in your favorite web browser (Firefox) and you should be good to go (it will load data from the actually treeherder site). If you want to make modifications to the HTML, Javascript, or CSS just go ahead and do so with your favorite editor and the changes will be immediately reflected.

We have a fair backlog of issues to get through, many of them related to the front end. If you&#8217;re interested in helping out, please have a look: 

[https://wiki.mozilla.org/Auto-tools/Projects/Treeherder#Bugs\_.26\_Project_Tracking][3]

If nothing jumps out at you, please drop by irc.mozilla.org #treeherder and we can probably find something for you to work on. We&#8217;re most active during Pacific Time working hours.

 [1]: http://treeherder.mozilla.org
 [2]: https://tbpl.mozilla.org/
 [3]: https://wiki.mozilla.org/Auto-tools/Projects/Treeherder#Bugs_.26_Project_Tracking