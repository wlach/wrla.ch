    Title: Using the dm utility to interact with Android or FirefoxOS devices
    Date: 2012-10-18T00:00:00
    Tags: Android, Mozilla


I promised a few people I&#8217;d blog about this, so here you go. 

To help with the business of making Android or FirefoxOS devices do our bidding, [Mozilla Automation &#038; Tools][1] developed a Python library called [mozdevice][2] which allows you to control these devices either using the Android Debug Bridge protocol (which is actually not Android specific: FirefoxOS devices use it too) or the [System Under Test protocol][3] (a Mozilla-specific thing).

Anyone familiar with debugging these devices is doubtless familiar with adb, which provides a command line interface that allows you to push/pull files, run a shell, etc. To help test our python code (as well as expand the scope of what&#8217;s possible on the command line), I created a similar utility a few months ago called &#8220;dm&#8221; which provides a command-line interface to the aforementioned mozdevice code. It&#8217;s shipped as part of mozdevice, and testing it out is pretty simple if you have virtualenv installed:

```
virtualenv mozdevice
cd mozdevice
./bin/pip install mozdevice
source bin/activate
dm --help
```

I generally use this utility for two things:

  1. Testing out mozdevice code. For example, today we discovered an (unfortunate) [bug][4] in devicemanagerADB&#8217;s killProcess routine. It was easy to verify both the problem and my fix did what I expected by starting my custom build of fennec and running this command:
    
    ```
dm --package-name org.mozilla.fennec_wlach killapp org.mozilla.fennec_wlach
```
    
    (yes, it&#8217;s a bit unfortunate that this bug occurred in the first place: devicemanagerADB really needs unit tests)

  2. Day-to-day menial tasks, like getting device info/status, capturing screenshots, etc. You can get a full list of what this utility is capable of by running &#8211;help. E.g.:
    
    ```
(mozbase)wlach@eideticker:~/src/eideticker$ dm --help
Usage: dm [options] &lt;command> [&lt;args>]

device commands:
  info [os|id|uptime|systime|screen|memory|processes] - get
      information on a specified aspect of the device (if no argument
      given, print all available information)
  install &lt;file> - push this package file to the device and install it
  killapp &lt;process name> - kills any processes with a particular name
      on device
  launchapp &lt;appname> &lt;activity name> &lt;intent> &lt;URL> - launches
      application on device
  ls &lt;remote> - list files on device
  ps  - get information on running processes on device
  pull &lt;local> [remote] - copy file/dir from device
  push &lt;local> &lt;remote> - copy file/dir to device
  rm &lt;remote> - remove file from device
  rmdir &lt;remote> - recursively remove directory from device
  screencap &lt;png file> - capture screenshot of device in action
  shell &lt;command> - run shell command on device

Options:
  -h, --help            show this help message and exit
  -v, --verbose         Verbose output from DeviceManager
  --host=HOST           Device hostname (only if using TCP/IP)
  -p PORT, --port=PORT  Custom device port (if using SUTAgent or adb-over-tcp)
  -m DMTYPE, --dmtype=DMTYPE
                        DeviceManager type (adb or sut, defaults to adb)
  -d HWID, --hwid=HWID  HWID
  --package-name=PACKAGENAME
                        Packagename (if using DeviceManagerADB)
```
    
    Before you ask, yes, it&#8217;s technically possible to do much of this with the original adb utility. But (1) some of our internal stuff can&#8217;t use adb a variety of reasons and (2) some of the tasks above (e.g. launching an app, getting a screenshot) involve considerably more typing with adb than with dm. So it&#8217;s still a win. </li> </ol> 
    
    Happy command-lining!

 [1]: https://wiki.mozilla.org/Auto-tools
 [2]: https://github.com/mozilla/mozbase/tree/master/mozdevice
 [3]: https://wiki.mozilla.org/Auto-tools/Projects/SUTAgent
 [4]: https://bugzilla.mozilla.org/show_bug.cgi?id=803177