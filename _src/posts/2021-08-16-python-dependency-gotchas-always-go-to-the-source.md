    Title: Python dependency gotchas: always go to the source
    Date: 2021-08-16T16:06:09
    Tags: Mozilla, Python

Getting back into the swing of things at Mozilla after my extended break.
I'm currently working on enhancing and extending [Looker] support for Glean-based applications, which eventually led me back to working on [bigquery-etl], our framework for creating derived datasets in our data lake.

I spent some time working on improving the initial developer experience of bigquery-etl early this year, so I figured it would be no problem to get going again despite an extended hiatus from it (I think it's probably been ~2-3 months since I last touched it).
Unfortunately the first thing I got after creating a fresh virtual environment (to pick up the new dependency updates) was this exciting looking error:

```
wlach@antwerp bigquery-etl % ./bqetl --help
Traceback (most recent call last):
  ...
  File "/Users/wlach/src/bigquery-etl/venv/lib/python3.9/site-packages/google/cloud/bigquery_v2/types/__init__.py", line 16, in <module>
    from .encryption_config import EncryptionConfiguration
  File "/Users/wlach/src/bigquery-etl/venv/lib/python3.9/site-packages/google/cloud/bigquery_v2/types/encryption_config.py", line 26, in <module>
    class EncryptionConfiguration(proto.Message):
  File "/Users/wlach/src/bigquery-etl/venv/lib/python3.9/site-packages/proto/message.py", line 200, in __new__
    file_info = _file_info._FileInfo.maybe_add_descriptor(filename, package)
  File "/Users/wlach/src/bigquery-etl/venv/lib/python3.9/site-packages/proto/_file_info.py", line 42, in maybe_add_descriptor
    descriptor=descriptor_pb2.FileDescriptorProto(
TypeError: descriptor to field 'google.protobuf.FileDescriptorProto.name' doesn't apply to 'FileDescriptorProto' object
```

## What I did

Since we have pretty decent continuous integration at Mozilla, when I see an error like this I am usually pretty sure it's some kind of strange interaction between my local development environment and whatever dependencies we've specified for the repository in question.
Usually these problems are pretty easy to solve.

First thing I tried was to type the error into Google, to see if this had come up for anyone else before.
I tried several variations of `TypeError: descriptor to field` and `FileDescriptorProto` and nothing really turned up.
This strategy almost always turns up _something_.
When it doesn't it usually indicates that something pretty strange is happening.

To see if this was a strange problem particular to _us_, I asked on our internal channel but no one had offhand seen or heard of this error either.
One of my colleagues (who had a working setup on a Mac, the same environment I was using) suggested I set up [pyenv] to isolate my development environment, which was a good idea but did not seem to solve the problem: both Python 3.8 and 3.9 installed via pyenv ran into the exact same issue.

After flailing around trying a number of other failed approaches (maybe I need to upgrade the version of virtualenv that we're using?), I broke down and looked harder at the error itself.
It seemed to be some kind of typing error in Google's protobuf library, which google-cloud-bigquery is calling.
If this sort of thing was happening to _everyone_, we probably would have seen it happening more broadly.
So my guess, again, was that it was happening due to an obscure interaction between some variable on my machine and this particular combination of dependencies.

At this point, I systematically went through our set of python dependencies to see what might be the matter.
For the most part, I found nothing surprising or suspicious.
`google-api-core` was at the latest version, as was `google-cloud-bigquery`.
However, I _did_ notice that the version of [protobuf](https://pypi.org/project/protobuf/) we were using was a little older (3.15.8 when the latest "official" version on pypi was 3.17.3).

![](/files/2021/08/pypi-screenshot.png)

It seemed like a longshot that the problem was there, but it seemed like upgrading the dependency was worth a try just in case.
So I bumped the version of protobuf to the latest version in my local checkout (`pip install protobuf==3.17.3`)...

... and sure enough, after doing so, the problem was fixed and `./bqetl --help` started working again:

```
wlach@antwerp bigquery-etl % ./bqetl --help
Usage: bqetl [OPTIONS] COMMAND [ARGS]...

  CLI tools for working with bigquery-etl.

...
```

After doing so, I did up a quick [pull request](https://github.com/mozilla/bigquery-etl/pull/2266) and the problem is now fixed, at least for me.

It's a bit unfortunate that [dependabot] (which we have configured for this repository) didn't send an update for protobuf, which would have fixed this problem earlier.[^1]
It seems like it's not completely reliable for python packages, for whatever reason: I have also noticed this problem with [mozregression].

I _suspect_ (though can't confirm) that the problem here is a backwards-incompatible change made to either `protobuf` or one of the packages that uses it.
However, the nature of the incompatibility seems subtle: bigquery-etl works fine with the old set of dependencies we run in continuous integration and it appears to only come up in specific circumstances (i.e. mine).
Unfortunately, I need to get back to what I was _actually_ planning to work on and don't have time to unwind the rather set of complex interactions going on here.
Maybe later!

[^1]: As an aside, the main reason we use dependabot and aggressively update packages like `google-api-core` is due to a [bug in pip](https://github.com/pypa/pip/issues/9644).

## What I would have done differently

This kind of illustrates (again) to me that while some shortcuts and heuristics can save a bunch of time and mental effort (Googling things all the time is basically standard practice in the industry at this point), sometimes you really just need to start a little closer at the problem to find a solution.
I was hesitant to do this in this case because I'm never sure where those kinds of rabbit holes are going to take me (e.g. I [spent several days] debugging a bad interaction between Kubernetes and our airflow cluster in late 2019 with not much to show for the effort), but often all it takes is understanding the general shape of the problem to move you to a quick solution.

## Other lessons

Here's a couple of other things this experience reinforced for me (these are more subjective, take them or leave them):

- Local development environments are kind of a waste of time. The above work took me several hours and it's going to result in ~zero user-visible improvements for anyone outside of Mozilla Data Engineering. I'm excited about the potential productivity improvements that might come from using tools like [GitHub Codespaces].
- While I can't confirm this was the source of the problem in this particular case, in general backwards compatibility _on every level_ is super important when your software has broad reach and doubly so if it's a widely-used dependency of other software (and is thus hard to reason about in isolation). In these cases, what seems like a trivial change (e.g. improving the type signatures inside a Python library) can squander many hours of people's time if you're not careful. Backwards-incompatible changes, however innocuous they may seem, should always invoke [a major version bump].
- Likewise, bugs in software that have broad usage (like dependabot) can have big downstream impacts. If dependabot's version bumping for python was more reliable, we likely wouldn't have had this problem. The glass-half-full interpretation of this is that fixing these types of issues would have an outsized benefit for the commons.

[looker]: https://looker.com/
[bigquery-etl]: https://mozilla.github.io/bigquery-etl/
[pyenv]: https://github.com/pyenv/pyenv
[spent several days]: https://github.com/mozilla/telemetry-airflow/issues/844
[dependabot]: https://docs.github.com/en/code-security/supply-chain-security/keeping-your-dependencies-updated-automatically/about-dependabot-version-updates
[a major version bump]: https://semver.org/
[mozregression]: https://github.com/mozilla/mozregression
[github codespaces]: https://github.com/features/codespaces
