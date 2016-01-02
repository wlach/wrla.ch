    Title: Simple command-line ntp client for Android and FirefoxOS
    Date: 2013-07-08T00:00:00
    Tags: Android, Eideticker, FirefoxOS, Mozilla, Time


Today I did a quick port of Larry Doolittle&#8217;s [ntpclient program][1] to Android and FirefoxOS. Basically this lets you easily synchronize your device&#8217;s time to that of a central server. Yes, there&#8217;s lots and lots of Android &#8220;applications&#8221; which let you do this, but I wanted to be able to do this from the command line because that&#8217;s how I roll. If you&#8217;re interested, source and instructions are here:

<https://github.com/wlach/ntpclient-android>

For those curious, no, I didn&#8217;t just do this for fun.  For next quarter, we want to write some Eideticker-based responsiveness tests for FirefoxOS and Android. For example, how long does it take from the time you tap on an icon in the homescreen on FirefoxOS to when the application is fully loaded? Or on Android, how long does it take to see a full list of sites in the awesomebar from the time you tap on the URL field and enter your search term?

Because an Eideticker test run involves two different machines (a host machine which controls the device and captures video of it in action, as well as the device itself), we need to use timestamps to really understand when and how events are being sent to the device. To do that reliably, we really need some easy way of synchronizing time between two machines (or at least accounting for the difference in their clocks, which amounts to about the same thing). NTP struck me as being the easiest, most standard way of doing this.

 [1]: http://doolittle.icarus.com/ntpclient/