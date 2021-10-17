    Title: Catching problems early with python
    Date: 2012-10-15T00:00:00
    Tags: Mozilla, Python

Just a few quick notes on how to avoid a class of errors I've been seeing in Mozilla's automation over the last year. Since python interprets code dynamically, it's pretty easy for problems like undefined variables to slip through, especially if they're in a codepath that isn't frequently tested. The most recent example I found was in some cleanup-after-error code for remote mochitest/reftest, which tried to call "self.cleanup" from a standalone method.

```
def main():
      ...
      try:
        dm.recordLogcat()
        retVal = mochitest.runTests(options)
        logcat = dm.getLogcat()
      except:
        print "TEST-UNEXPECTED-FAIL | %s | Exception caught while running tests." % sys.exc_info()[1]
        mochitest.stopWebServer(options)
        mochitest.stopWebSocketServer(options)
        try:
            self.cleanup(None, options)
        except:
            pass

```

[testing/mochitest/runtestsremote.py][1]

We're calling cleanup as if it were a class variable, but we're not inside any class! It's easy to see what will happen if you try to run some similar code from the python console:

```
>>> self.cleanup()
Traceback (most recent call last):
  File "&lt;stdin>", line 1, in &lt;module>
NameError: name 'self' is not defined
```

However, because we're in a blanket try...except, we will never see an error. The cleanup code will never be called, instead the exception is immediately caught and subsequently ignored. Probably not the end of the world in this case (there are other parts of our mobile automation which will perform the same cleanup later), but it's easy to imagine where this would be a more serious problem.

There's two very easy ways to help stop errors like this before they hit our code:

1. Try to avoid using a blanket try...except. In addition to catching legitimate problems which we want to ignore (in the remote case for example, devicemanager exceptions), it also catches (and thus obscures) things like syntax, name, or type errors. Instead, try just catching the specific exception you're looking for. For example, we might rewrite the case above as:

   ```

   ```

try:
mochitest.cleanup(None, options)
except devicemanager.DMError:
print "WARNING: Device error while cleaning up"

````

  2. pyflakes, pyflakes, pyflakes. [Pyflakes][2] is a fantastic tool for analyzing your python code for common problems. It's kind of analagous to [jslint][3], for those of you familiar with that. Here's what happens when we run pyflakes against the offending code:

    ```
wlach@eideticker:~/src/mozilla-central$ pyflakes testing/mochitest/runtestsremote.py
testing/mochitest/runtestsremote.py:7: 'time' imported but unused
testing/mochitest/runtestsremote.py:481: undefined name 'self'
testing/mochitest/runtestsremote.py:500: undefined name 'self'
````

    I've found pyflakes to be an indispensable part of my workflow. I generally run it after making any substantial change to a python file, and certainly before pushing anything to be consumed by others.

Ultimately there's no substitute for actually thoroughly testing your code, no matter what language you're using. But using the right techniques and tools can certainly make your life easier.

[ for those wondering, a fix for the issue mentioned in this post is part of [bug 801652][4] ]

[1]: http://hg.mozilla.org/mozilla-central/file/942ed5747b63/testing/mochitest/runtestsremote.py#l481
[2]: http://pypi.python.org/pypi/pyflakes
[3]: http://www.jslint.com/
[4]: https://bugzilla.mozilla.org/show_bug.cgi?id=801652
