    Title: Perfherder summer of contribution thoughts
    Date: 2015-09-29T00:00:00
    Tags: Community, Mozilla, Perfherder


A few months ago, Joel Maher [announced the Perfherder summer of contribution][1]. We wrapped things up there a few weeks ago, so I guess it&#8217;s about time I wrote up a bit about how things went.

As a reminder, the idea of summer of contribution was to give a set of contributors the opportunity to make a substantial contribution to a project we were working on (in this case, the [Perfherder][2] performance sheriffing system). We would ask that they sign up to do 5-10 hours of work a week for at least 8 weeks. In return, Joel and myself would make ourselves available as mentors to answer questions about the project whenever they ran into trouble.

To get things rolling, I split off a bunch of work that we felt would be reasonable to do by a contributor into bugs of varying difficulty levels (assigning them the bugzilla whiteboard tag [ateam-summer-of-contribution][3]). When someone first expressed interest in working on the project, I&#8217;d assign them a relatively easy front end one, just to cover the basics of working with the project (checking out code, making a change, submitting a PR to github). If they made it through that, I&#8217;d go on to assign them slightly harder or more complex tasks which dealt with other parts of the codebase, the nature of which depended on what they wanted to learn more about. Perfherder essentially has two components: a data storage and analysis backend written in Python and Django, and a web-based frontend written in JS and Angular. There was (still is) lots to do on both, which gave contributors lots of choice. 

This system worked pretty well for attracting people. I think we got at least 5 people interested and contributing useful patches within the first couple of weeks. In general I think onboarding went well. Having good documentation for Perfherder / Treeherder on the wiki certainly helped. We had lots of the usual problems getting people familiar with git and submitting proper pull requests: we use a somewhat clumsy combination of bugzilla and github to manage treeherder issues (we &#8220;attach&#8221; PRs to bugs as plaintext), which can be a bit offputting to newcomers. But once they got past these issues, things went relatively smoothly.

A few weeks in, I set up a fortnightly skype call for people to join and update status and ask questions. This proved to be quite useful: it let me and Joel articulate the higher-level vision for the project to people (which can be difficult to summarize in text) but more importantly it was also a great opportunity for people to ask questions and raise concerns about the project in a free-form, high-bandwidth environment. In general I&#8217;m not a big fan of meetings (especially status report meetings) but I think these were pretty useful. Being able to hear someone else&#8217;s voice definitely goes a long way to establishing trust that you just can&#8217;t get in the same way over email and irc.

I think our biggest challenge was retention. Due to (understandable) time commitments and constraints only one person (Mike Ling) was really able to stick with it until the end. Still, I&#8217;m pretty happy with that success rate: if you stop and think about it, even a 10-hour a week time investment is a fair bit to ask. Some of the people who didn&#8217;t quite make it were quite awesome, I hope they come back some day. 

&#8212;

On that note, a special thanks to Mike Ling for sticking with us this long (he&#8217;s still around and doing useful things long after the program ended). He&#8217;s done [some really fantastic work][4] inside Perfherder and the project is much better for it. I think my two favorite features that he wrote up are the improved test chooser which I talked about a few months ago and a [get related platform / branch][5] feature which is a big time saver when trying to determine when a performance regression was first introduced.

I took the time to do a short email interview with him last week. Here&#8217;s what he had to say:

1. Tell us a little bit about yourself. Where do you live? What is it you do when not contributing to Perfherder?

*I&#8217;m a postgraduate student of NanChang HangKong university in China whose major is Internet of things. Actually,there are a lot of things I would like to do when I am AFK, play basketball, video game, reading books and listening music, just name it ; )*

2. How did you find out about the ateam summer of contribution program?

*well, I remember when I still a new comer of treeherder, I totally don&#8217;t know how to start my contribution. So, I just go to treeherder irc and ask for advice. As I recall, emorley and jfrench talk with me and give me a lot of hits. Then Will (wlach) send me an Email about ateam summer of contribution and perfherder. He told me it&#8217;s a good opportunity to learn more about treeherder and how to work like a team! I almost jump out of bed (I receive that email just before get asleep) and reply with YES. Thank you Will!*

3. What did you find most challenging in the summer of contribution?

*I think the most challenging thing is I not only need to know how to code but also need to know how treeherder actually work. It&#8217;s a awesome project and there are a ton of things I haven&#8217;t heard before (i.e T-test, regression). So I still have a long way to go before I familiar with it.*

4. What advice would give you to future ateam contributors?

*The only thing you need to do is bring your question to irc and ask. Do not hesitate to ask for help if you need it! All the people in here are nice and willing to help. Enjoy it!*

 [1]: https://elvis314.wordpress.com/2015/05/18/a-team-contribution-opportunity-dashboard-hacker/
 [2]: https://wiki.mozilla.org/Auto-tools/Projects/Perfherder
 [3]: https://bugzilla.mozilla.org/buglist.cgi?keywords=%20ateam-summer-of-contribution&#038;keywords_type=allwords&#038;list_id=12578272&#038;resolution=---&#038;resolution=FIXED&#038;resolution=INVALID&#038;resolution=WONTFIX&#038;resolution=DUPLICATE&#038;resolution=WORKSFORME&#038;resolution=INCOMPLETE&#038;resolution=SUPPORT&#038;resolution=EXPIRED&#038;resolution=MOVED&#038;query_format=advanced&#038;bug_status=UNCONFIRMED&#038;bug_status=NEW&#038;bug_status=ASSIGNED&#038;bug_status=REOPENED&#038;bug_status=RESOLVED&#038;bug_status=VERIFIED&#038;bug_status=CLOSED
 [4]: https://github.com/mozilla/treeherder/commits/master?author=MikeLing
 [5]: https://bugzilla.mozilla.org/show_bug.cgi?id=1134780