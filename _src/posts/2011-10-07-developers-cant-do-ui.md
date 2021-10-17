    Title: Developers can't do UI
    Date: 2011-10-07T00:00:00
    Tags: Mozilla, Usability

Despite making a dramatic shift from front-end development to [back-end stuff][1] since I started at Mozilla a few months ago, I've still had occasion to have to do a fair bit of user-facing code, even if an audience of other developers is a bit more limited than what I've been used to. Since my mission is to make the rest of Mozilla more productive, it's worth putting a bit of time and intention into the user interface for my stuff. If I can reduce learning curves or streamline day-to-day workflows, that's a win for everyone since they can spend that much more time rocking at their jobs (whether that be release engineering, platform work, or whatever). This brings up a point that I've had in the back of my mind for a while:

_Despite conventional wisdom, developers can design half-decent user interfaces (if they try)!_

I used to be certain that a project really needed graphic designers and/or usability experts to provide guidance on UI issues, but my experience over the last few years with iOS/web development has made me reconsider. Sure, pixel pushing and vector art is never going to be a programmer's strong suit (and there's certain high-level techniques that take years of study to acquire/understand), but the basic principles behind good UI design are accessible to anyone. There's really only three core skills:

- An ability to put yourself in the shoes of the user. Who are you designing for, and what are they trying to accomplish? How can I streamline my UI to help them quickly solve the task at hand? This is one of the reasons why I find [user stories][2] so helpful.

- An understanding of common vocabulary for describing/designing applications and knowing what is "good". Unfortunately I haven't found anything like this for the web, but [Apple's human interface guidelines][3] have some good general advice on this (just ignore the stuff specific to phones/tablet apps if that's not what you're doing).

- A willingness to iterate. The best ideas usually aren't apparent immediately, and may only come out of a back forth. It's been my experience that the more constructive dialog there is between people actively involved in the project on user experience issues, the better the end result is likely to be.

For example, one of the things that release engineering has found most useful in the GoFaster Dashboard has been the [build charts][4]. Believe it or not, the idea for that view started out as this [useless piece of junk][5] (I can say that because I created it). It was only after a good half hour back and forth on irc between myself, jgriffin, and jmaher (all of us backend/tool developers) that we came up with the view that inspired so much [good analysis][6] on the project.

All this is not to say that usability experts and graphic designers don't have special skills that are worthy of respect. Indeed, if you're a designer and would like to get involved with our work, please [join us][7], we'd love your help. My only point is that on a project where a design resource isn't available, thinking explicitly about usability is still worthwhile. And even where you have a UX expert on staff, programmers can have useful feedback too. Good UI is everyone's responsibility!

[1]: https://wiki.mozilla.org/Auto-tools
[2]: http://en.wikipedia.org/wiki/User_story
[3]: http://developer.apple.com/library/ios/#documentation/UserExperience/Conceptual/MobileHIG/UEBestPractices/UEBestPractices.html#//apple_ref/doc/uid/TP40006556-CH20-SW1
[4]: http://brasstacks.mozilla.com/gofaster/#/buildcharts
[5]: http://people.mozilla.com/~wlachance/overall-build-and-test-area.png
[6]: http://jagriffin.wordpress.com/2011/09/06/gofaster-deeper-data-analysis/
[7]: https://wiki.mozilla.org/Auto-tools#Want_to_Help.3F
