    Title: Using Flexbox in web applications
    Date: 2014-09-29T00:00:00
    Tags: Mozilla, Web


Over last few months, I discovered the joy that is CSS Flexbox, which solves the &#8220;how do I lay out this set of div&#8217;s in horizontally or vertically&#8221;. I&#8217;ve used it in three projects so far:

  * Centering the timer interface in my [meditation app][1], so that it scales nicely from a 320&#215;480 FirefoxOS device all the way up to a high definition monitor
  * Laying out the chart / sidebar elements in the [Eideticker dashboard][2] so that maximum horizontal space is used
  * Fixing various problems in the [Treeherder UI][3] on smaller screens (see [bug 1043474][4] and its dependent bugs)

When I talk to people about their troubles with CSS, layout comes up really high on the list. Historically, basic layout problems like a panel of vertical buttons have been ridiculously difficult, involving hacks involving floating divs and absolute positioning or [JavaScript layout libraries][5]. This is why people write articles entitled [&#8220;Give up and use tables&#8221;][6].

Flexbox has pretty much put an end to these problems for me. There&#8217;s no longer any need to &#8220;give up and use tables&#8221; because using flexbox is pretty much just \*like\* using tables for layout, just with more uniform and predictable behaviour.  They&#8217;re so great. I think we&#8217;re pretty close to Flexbox being supported across all the major browsers, so it&#8217;s fair to start using them for custom web applications where compatibility with (e.g.) IE8 is not an issue.

To try and spread the word, I wrote up [a howto article on using flexbox for web applications on MDN][7], covering some of the common use cases I mention above. If you&#8217;ve been curious about flexbox but unsure how to use it, please have a look.

 [1]: http://wrla.ch/blog/2014/08/a-new-meditation-app/
 [2]: http://eideticker.mozilla.org
 [3]: http://treeherder.mozilla.org
 [4]: https://bugzilla.mozilla.org/show_bug.cgi?id=1043474
 [5]: http://layout.jquery-dev.com/
 [6]: http://uxmag.com/articles/give-and-use-tables
 [7]: https://developer.mozilla.org/en-US/docs/Web/Guide/CSS/Using_flexbox_to_lay_out_web_applications