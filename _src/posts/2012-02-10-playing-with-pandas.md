    Title: Playing with pandas
    Date: 2012-02-10T00:00:00
    Tags: Android, Mozilla, Pandaboard


For the last few days I&#8217;ve been experimenting with getting a Pandaboard running Android 4.0, continuing the work that Clint Talbert [started in the fall][1] to get these boards for use as a replacement for the Tegra in Mozilla&#8217;s android automation. The first objective is to get a reproducible build going, after that we&#8217;ll try to get some of our custom tools ([SUTAgent][2] &#038; friends) installed by default.

So far this has been&#8230; interesting. Much as Clint did before, I thought I&#8217;d document some of the notes on what I did in the hopes that they&#8217;ll be helpful to other people trying to do similar things. 

Getting things up and running is a two step process. First, you build the beast. This part is straightforward, just follow the instructions here:

At least the build part is more or less straightforward. Just follow the instructions here:

  * <http://source.android.com/source/building.html>
  * <http://source.android.com/source/building-devices.html>

Note that you almost certainly want to build in the &#8220;eng&#8221; configuration, which is rooted and (apparently) has some extra tools installed.

Installing it is a little more tricky. The way they want you to do this is put the pandaboard into a special mode and copy the stuff you built onto an sdcard. Seem a little funny to you? Yeah, it does to me too. Why not just build an sdcard image directly?  
Nonetheless, this is the officially supported way of imaging a pandaboard, so let&#8217;s just follow it until we can think of a better way of doing things.  The instructions for doing this on the pandaboard are located in the source tree here:

`<a href="http://source-android.frandroid.com/device/ti/panda/README">device/ti/panda/README</a>`

These are mostly correct as far as I can tell, but there&#8217;s a few gotchas. First, you need to run the commands mentioned as root unless you&#8217;ve configured USB to be configurable by your user. Second, most of those commands are not in the path by default so you&#8217;ll need to specify the full path to e.g. the fastboot utility. The instructions [here][3] cover these exception cases: I recommend following them instead. 

One thing which neither document mentions is that you really need to make sure your sdcard is wiped completely clean before using fastboot. The &#8220;oem format&#8221; step only recreates the partition table, it doesn&#8217;t delete any corrupted partitions. If you reboot while these are still in place, it will try to bring up your corrupted version of Android, not the fastboot console. I spent quite some time debugging why I couldn&#8217;t properly flash the operating system before realizing this. Easiest way to get around this is to dd `/dev/zero` onto the sdcard before beginning the flashing process.

Also, while not strictly necessary to get something up and running, I recommend highly getting an HDMI monitor as well as a serial<->USB adapter. The former is useful to see if your Android device actually successfully booted up, the latter is useful for debugging boot issues where you don&#8217;t get that far (the serial console is always available from boot).

So, after painfully learning about the above caveats, I have managed to get things mostly working. I can see the ICS homescreen on my attached HDMI monitor and interact with it if I attach a USB mouse. The one gotcha is that both ethernet and WIFI networking are totally broken. Plugging in an ethernet cable or connecting to a WIFI network seems to result in the machine randomly rebooting, with the logs saying nothing useful. Both of these things are ostensibly supposed to be working according to the latest I&#8217;ve read from Google so I&#8217;m not exactly sure what&#8217;s going on. Investigations will continue.

 [1]: http://cmtalbert.wordpress.com/2011/10/12/pandaboard-status/
 [2]: https://wiki.mozilla.org/Mobile/Fennec_Unittests/Remote_Testing
 [3]: http://fosiao.com/node/19