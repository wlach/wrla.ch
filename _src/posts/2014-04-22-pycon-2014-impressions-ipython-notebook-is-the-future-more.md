    Title: PyCon 2014 impressions: ipython notebook is the future &#038; more
    Date: 2014-04-22T00:00:00
    Tags: Montreal, Mozilla, Python


This year&#8217;s PyCon US ([Python][1] Conference) was in my city of residence (Montr&eacute;al) so I took the opportunity to go and see what was up in the world of the language I use the most at Mozilla. It was pretty great!

**ipython**

The highlight for me was learning about the possibilities of [ipython notebooks][2], an absolutely fantastic interactive tool for debugging python in a live browser-based environment. I&#8217;d heard about it before, but it wasn&#8217;t immediately apparent how it would really improve things &#8212; it seemed to be just a less convenient interface to the python console that required me to futz around with my web browser. Watching a few presentations on the topic made me realize how wrong I was. It&#8217;s already changed the way I do work with Eideticker data, for the better.  
<figure id="attachment_1042" style="width: 848px" class="wp-caption alignnone">[<img src="/files/2014/04/eideticker-ipython.png" alt="Using ipython to analyze some eideticker data" width="848" height="842" class="size-full wp-image-1042" srcset="/files/2014/04/eideticker-ipython-150x150.png 150w, /files/2014/04/eideticker-ipython-300x297.png 300w, /files/2014/04/eideticker-ipython.png 848w" sizes="(max-width: 848px) 100vw, 848px" />][3]<figcaption class="wp-caption-text">Using ipython to analyze some eideticker data</figcaption></figure>  
I think the basic premise is really quite simple: a better interface for typing in, experimenting with, and running python code. If you stop and think about it, the modern web interface supports a much richer vocabulary of interactive concepts that the console (or even text editors like emacs): there&#8217;s no reason we shouldn&#8217;t take advantage of it.

Here are the (IMO) killer features that make it worth using:

  * The ability to immediately re-execute a block of code after editing and seeing an error (essentially merging the immediacy of the python console with the permanency / cut &#038; pastability of an actual script) 
  * Live-printing out graphs of numerical results using [matplotlib][4]. ZOMG this is so handy. Especially in conjunction with the live-editing outlined above, there&#8217;s no better tool for fine-tuning mathematical/statistical analysis. 
  * The shareability of the results. Any ipython notebook can be saved and then saved to a public website. Many presentations at PyCon 2014, in fact, were done entirely with ipython notebooks. So handy for answering questions like &#8220;how did you get that&#8221;? 

To learn more about how to use ipython notebooks for data analysis, I highly recommend Julie Evan&#8217;s talk [Diving into Open Data with IPython Notebook &#038; Pandas][5], which you can find on pyvideo.org.

**Other Good Talks**

I saw some other good talks at the conference, here are some of them:

  * [All Your Ducks In A Row: Data Structures in the Standard Library and Beyond][6] &#8211; A useful talk by Brandon Rhoades on the implementation of basic data structures in Python, and how to select the ones to use for optimal performance. It turns out that lists aren&#8217;t the best thing to use for long sequences of numerical data (who knew?)
  * [Fast Python, Slow Python][7] &#8211; An interesting talk by Alex Gaynor about how to write decent performing pure-python code in a single-threaded context. Lots of intelligent stuff about producing robust code that matches your intention and data structures, and caution against doing fancy things in the name of being &#8220;pythonic&#8221; or &#8220;general&#8221;.
  * [Analyzing Rap Lyrics with Python][8] &#8211; Another data analysis talk, this one about a subject I knew almost nothing about. The best part of it (for me anyway) was learning how the speaker (Julie Lavoie) narrowed her focus in her research to the exact aspects of the problem that would let her answer the question she was interested in (&#8220;Can we automatically find out which rap lyrics are the most sexist?&#8221;) as opposed to interesting problems (&#8220;how can I design the most general scraping library possible?&#8221;) that don&#8217;t answer the question. In my opinion, this ability to focus is one of the key things that seperates successful projects from unsuccessful ones.

 [1]: http://python.org
 [2]: http://ipython.org/
 [3]: /files/2014/04/eideticker-ipython.png
 [4]: http://matplotlib.org/
 [5]: http://pyvideo.org/video/2657/diving-into-open-data-with-ipython-notebook-pan-0
 [6]: http://pyvideo.org/video/2571/all-your-ducks-in-a-row-data-structures-in-the-s
 [7]: http://pyvideo.org/video/2627/fast-python-slow-python
 [8]: http://pyvideo.org/video/2658/analyzing-rap-lyrics-with-python