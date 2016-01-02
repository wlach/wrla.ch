    Title: An even better way of taking screenshots on Android
    Date: 2012-04-03T00:00:00
    Tags: Android, Mozilla


Just thought I&#8217;d mention this because I found it handy. 

A while back AaronMT [wrote up][1] some clever instructions on taking Android screenshots by dumping the contents of &#8216;/dev/fb0&#8217; and running ffmpeg on the results. This is useful, but you need to know the resolution of the device you have connected to pass the right arguments to ffmpeg. Wouldn&#8217;t it be better if you had just one script that would work for whatever device you had plugged in?

In fact, there is a way to do this using the [monkeyrunner][2] utility. Intended mainly as a tool for synthesizing input on Android (more on that some other time), you can also easily get a capture of the Android screen with its python/jython API (assuming you have the Android SDK installed). Here&#8217;s a quick script which does the job:

```
from com.android.monkeyrunner import MonkeyRunner, MonkeyDevice
import os
import sys

if len(sys.argv) != 2:
    print "Usage: %s &lt;filename>" % os.path.basename(sys.argv[0])
    sys.exit(1)

device = MonkeyRunner.waitForConnection()
result = device.takeSnapshot()
result.writeToFile(sys.argv[1], 'png')
```

Copy that into a file called capture.py (or whatever), then run it like so:  
`<br />
monkeyrunner capture.py screenshot.png<br />
`

And you&#8217;re off to the races! Nice screenshot, no utilities or non-essential command line arguments required!

(credit to [this stackoverflow answer][3] for the idea)

 [1]: http://aaronmt.com/?p=527
 [2]: http://developer.android.com/guide/developing/tools/MonkeyRunner.html
 [3]: http://stackoverflow.com/a/9311243/295132