    Title: Launching random web browsers on Android
    Date: 2012-05-04T00:00:00
    Tags: Android, Mozilla

Ok, this is somewhat mundane, but I've already had to do it twice (and helped someone do something similar on #mobile), so I figured I might as well blog about it for posterity.

For various automation tasks (notably the [Eideticker dashboard][1] and the [cross-browser startup tests][2]), we need to be able to launch an Android browser on the command line (via adb shell or our own custom SUTAgent). This is a bit of a black art, but you can find references on how to do this on stackoverflow and other places. The magic incantation is:

```
am start -a android.intent.action.VIEW -n &lt;application/intent&gt; -d &lt;url&gt;
```

So, for example, to launch Fennec, you'd run this on the Android command prompt:

```
am start -a android.intent.action.VIEW -n org.mozilla.fennec/.App -d http://mygreatsite.info
```

Ok, easy enough, but what if we want to launch a new browser that we just downloaded (e.g. Google Chrome)? Where do we get the application and intent names?

The short answer is that you need to reach into the apk and dig. 😉 There's probably many ways of doing this, but here's what I do (which has the distinct advantage of not needing to compile, download or run weird java applications):

1. Copy the apk onto your machine (the apk should be in /data/app: if you have a rooted phone, you should be able to copy that off to your machine).

2. Extract _AndroidManifest.xml_ from the apk (it's just a .zip) and run [axml2xml.pl][3] on it.

3. Examine the resultant xml file and look for the **<manifest>** tag. It should have a property called **<package>** which is the package name. For example:

We can see pretty clearly that the application name in this case is **com.android.chrome** (you can also get this by running ps when using the application)

4. Finally, look for a tag called **<intent filter>** with an **<action>** tag with **<android.intent.action.VIEW>** as the **android-name** property. Scan up for the overarching **activity** tag, whose **android-name** property. This is the activity name. For example:

Likewise here we see that the activity name we want is **.Main** (which Android explicitly expands out to **com.android.chrome.Main**)

Armed with this information, you should now have enough information to launch the application. Furthering the example above, here's how to start Chrome on Android via adb's shell:

```
am start -a android.intent.action.VIEW -n com.android.chrome/.Main -d http://mygreatsite.info
```

Hope this helps someone, somewhere.

[1]: http://wrla.ch/eideticker/dashboard/
[2]: http://mrcote.info/phonedash/#/rawfennecstartup
[3]: http://android-random.googlecode.com/svn/trunk/axml2xml/axml2xml.pl
