    Title: Eideticker areas to explore
    Date: 2011-12-09T00:00:00
    Tags: Mozilla


So I got some nice feedback on my [Eideticker post][1] yesterday on various channels. It seems like some people are interested in hacking on the analysis portion, so I thought I&#8217;d give some quick pointers and suggestions of things to look at. 

  1. As I mentioned yesterday, the frame analysis is rather stupid. We need to come up with a better algorithm for disambiguating input noise (small fluctuations in the HDMI signal?) from actual changes in the page. Unfortunately the breadth of things that Eideticker&#8217;s meant to analyze makes this a bit difficult. I.e. edge detection probably wouldn&#8217;t work for something like Microsoft&#8217;s [psychedelic browsing demo][2]. I suspect the best route here is to put some work into better understanding the nature of this &#8220;noise&#8221; and finding a way to filter it out explicitly. 
  2. Our analysis code is still rather slow, and is crying out to be parallelized (either by using multiple cores of the same CPU or a GPU). Burak Yiğit Kaya recommended I look into [PyCuda][3] which looks interesting. It looks like there are other possibilities as well though.
  3. Clipping capture by green screen/red screen. This should be doable by writing some relatively simple code to detect large amounts of green and red and then ignoring previous/current/subsequent frames as appropriate. 
  4. Moar test cases! It was initially suggested to use some of the classic benchmarks, but these only seem to barely work on Fennec (at least with the setup I have). I don&#8217;t know if this is fixable or not, but until it is, we might be better off coming up with more reasonable/realistics measures of visual performance.

You might be able to find other inspiration on the [Eideticker project page][4] (note that some of this is out of date).

You obviously need the decklink card to perform captures, but the analysis portion of Eideticker can be used/modified on any machine running Linux (Mac should also work, but is untested). To get up and running, just follow the instructions in [README.md][5], dump a pregenerated capture into the captures/ directory (here&#8217;s [one][6] of a clock), and off you go! The actual analysis code (such as it is) is currently located in [src/videocapture/videocapture/capture.py][7] while the web interface is in <https://github.com/mozilla/eideticker/blob/master/src/webapp>.

I&#8217;m going to be out later today (Friday), but I&#8217;m mostly around on IRC M-F 9ish-5ish EST on irc.mozilla.org #ateam as \`wlach\`. Feel free to pester me with questions!

P.S. I didn&#8217;t really cover infrastructure/automation portions above as I suspect people will find that less interesting (especially without a video capture card to test with), but you can look at my [newsgroup post][8] from yesterday if you want to see what I&#8217;ll likely be up to over the next few weeks.

 [1]: http://wrla.ch/blog/2011/12/eideticker-update/
 [2]: http://ie.microsoft.com/testdrive/performance/psychedelicbrowsing/Default.html
 [3]: http://mathema.tician.de/software/pycuda
 [4]: https://wiki.mozilla.org/Project_Eideticker
 [5]: https://github.com/mozilla/eideticker/blob/master/README.md
 [6]: http://people.mozilla.com/~wlachance/clock.zip
 [7]: https://github.com/mozilla/eideticker/blob/master/src/videocapture/videocapture/capture.py
 [8]: http://groups.google.com/group/mozilla.tools/browse_thread/thread/a469b7909af589de#