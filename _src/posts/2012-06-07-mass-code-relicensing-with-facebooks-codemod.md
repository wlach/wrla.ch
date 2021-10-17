    Title: Mass code relicensing with facebook's codemod
    Date: 2012-06-07T00:00:00
    Tags: Mozilla

Recently the Firefox source repository (mozilla-central) was converted over recently to a new license with a [lovely short boilerplate][1]. This is great, but here in [automation and tools][2], we have a fairly large number of projects that live outside of the main tree but for which the new license still applies. A few weeks ago, I wanted to move one our projects over (mozbase), but didn't want to spend hours manually editing text files. I understand that a script was used to convert mozilla-central, but a quick google didn't turn it up. **[ edit:** thanks to Ed Morley for pointing out to me that it lives here: <http://hg.mozilla.org/users/gerv_mozilla.org/relic/> **]**

I surely could have asked about where this script is, but this problem gave me an excuse to try something that I'd been meaning to for a while: Facebook's [codemod][3]. Codemod is a neat little command-line utility which aims to help with mass refactorings of code. All you have to do is provide a few regular expressions to replace, and off it goes. I tried it out with mozbase, and the results were great: 5 minutes spent coming up with a regular expression and jiggering with command line options, and the job was done.

I had the desire to do this again today for [Eideticker][4], and decided to document the (extremely simple) process for posterity. I just used this simple command line&#8230;

`../codemod/src/codemod.py --extensions py -m '# \*\*\*\*\* BEGIN LICENSE.*END LICENSE BLOCK \*\*\*\*\*' '# This Source Code Form is subject to the terms of the Mozilla Public\n# License, v. 2.0. If a copy of the MPL was not distributed with this file,\n# You can obtain one at http://mozilla.org/MPL/2.0/.'`

&#8230; et voila, out popped [shiny new boilerplate][5].

[1]: http://www.mozilla.org/MPL/headers/
[2]: https://wiki.mozilla.org/Auto-tools
[3]: https://github.com/facebook/codemod
[4]: http://github.com/mozilla/eideticker
[5]: https://github.com/mozilla/eideticker/commit/9456933670fb4590af3060f4ff40d11271859b8d
