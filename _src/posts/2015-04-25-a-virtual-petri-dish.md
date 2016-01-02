    Title: A virtual petri dish
    Date: 2015-04-25T00:00:00
    Tags: Data Visualization


Was feeling a bit restless today, so I decided to build something on a theme I&#8217;d been thinking of since, oh gosh, I guess high school &#8212; an ecosystem simulation.

My original concept for it had three different types of entities &#8212; grass, rabbits, and foxes wandering around in a fixed environment. Each would eat the previous and try to reproduce. Both the rabbits and foxes need to continually eat to survive, otherwise they will die. The grass will just grow unprompted. I think I may have picked up the idea from elsewhere, but am not sure (it&#8217;s been nearly 17 years after all).

I suppose the urge to do this comes from my fascination with the concepts of birth, death, and rebirth. Conway&#8217;s [game of life][1] is probably the most famous computer representation of this sort of theme, but I always found the behavior slightly too contrived and simple to be deeply satisfying to me (at least from the point of view of representing this concept: the game is certainly interesting for other reasons). Conway&#8217;s simulation is completely deterministic and only has one type of entity, the cell. There&#8217;s an element of randomness and hierarchy in the real world, and I wanted to represent these somehow.

It was remarkably easy to get things going using my preferred toolkit for these things (Javascript and Canvas) &#8212; about 3 hours to get something on the screen, then a bunch of tweaking until I found the behavior I wanted. Either I&#8217;m getting smarter or the tools to build these things are getting better. Probably the latter.

In the end, I only wound up having rabbits and grass in my simulation in this iteration and went for a very abstract representation of what was going on (colored squares for everything!). It turns out that no more than that was really necessary to create something that held my interest. Here&#8217;s a screenshot (doesn&#8217;t really do it justice):

[<img src="/files/2015/04/Screen-Shot-2015-04-25-at-10.24.21-PM.png" alt="Screen Shot 2015-04-25 at 10.24.21 PM" width="1002" height="1006" class="alignnone size-full wp-image-1198" srcset="/files/2015/04/Screen-Shot-2015-04-25-at-10.24.21-PM-150x150.png 150w, /files/2015/04/Screen-Shot-2015-04-25-at-10.24.21-PM-298x300.png 298w, /files/2015/04/Screen-Shot-2015-04-25-at-10.24.21-PM.png 1002w" sizes="(max-width: 1002px) 100vw, 1002px" />][2]

If you&#8217;d like to check it out for yourself, I put a copy on my website [here][3]. It probably requires a fairly fancy computer to run at a decent speed (I built it using a 2014 MacBook Pro and made very little effort to optimize it). If that doesn&#8217;t work out for you, I put up a [video capture of the simulation on youtube][4].

The math and programming behind the simulation is completely arbitrary and anything but rigorous. There are probably a bunch of bugs and unintended behaviors. This has all probably been done a million times before by people I&#8217;ve never met and never will. I&#8217;m ok with that.

**Update**: [Source now on github][5], for those who want to play with it and submit pull requests.

 [1]: http://en.wikipedia.org/wiki/Conway%27s_Game_of_Life
 [2]: /files/2015/04/Screen-Shot-2015-04-25-at-10.24.21-PM.png
 [3]: http://wrla.ch/eco
 [4]: https://youtu.be/LwLFw1_GGnU
 [5]: https://github.com/wlach/ecoautomata