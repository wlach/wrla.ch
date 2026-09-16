---
tags: [activitypub]
---

# A couple quick notes on ActivityPub

A few weeks ago, I made this site publish to ActivityPub (really mostly thinking
about Mastodon, although as an open standard other software can consume it).
Just wanted to write down a few notes on the experience for posterity.

*tl;dr: At this time, a pure-static ActivityPub site isn't possible but the dynamic parts aren't particularly complicated and can be implemented with relatively minimal effort and compute.*

## Mechanism

There are really two parts to publishing, the static feed and the notification mechanism.

The feed itself is a collection of files, published statically: just like this post. 
Similarly, the [WebFinger] portions of the site, which allows Mastodon to discover metadata about the publisher, can be static. 
No reason it can't be the same every time this blog is published.

The dynamic and complicated portions come from the "social" features of ActivityPub.
To track followers and syndicate "likes", "quotes", and "boosts", you need both internal storage (to track the actions and who they should be distributed to)
and a mechanism to "push" them to whoever has subscribed.
To prevent impersonation, ActivityPub specifies that the messages pushed should be cryptographically signed (= generating and using RSA keys).

## Implementation

I was already using Cloudflare pages to deploy this blog, so building on top of their infrastructure was the obvious choice.

The non-dynamic parts of the implementation just used this site's (very boring) Python code to write things out into the ActivityPub format Mastodon expected.

The dynamic parts were written using a Cloudflare worker, running on python / [pyodide].
Backing store was [D1], an sqlite-like database.

I got an LLM (GPT 5.6ish) to write most of it, based on [an idr](https://github.com/wlach/wrla.ch/blob/8a8683d351bf2d6a71f11d7e72d44279dd65ae7c/idrs/202608240235-add-activitypub-feed.md).
I wasn't tracking precisely, but my guess is the implementation took four to six hours.
If I didn't care about making the output coherent and legible to myself, it probably could have been done in about half the time.

As software goes, I'm pretty happy with the result.
It's simple, cheap, and probably portable elsewhere without too much trouble if I ever get sick of Cloudflare.

## Payoff

Honestly pretty marginal so far.
You can follow `@wrlach@wrla.ch` from your favorite ActivityPub implementation and get post summaries as they are published.
If you wish, you can also boost/quote/like them.
As of 2026-09-16 I appear to be the only one who has done this. 

Viable alternatives to what I did:

* RSS: much, much simpler-- just a XML feed of posts. Venerable. Interoperable. Downside is that it's one way publishing. You can use [bridgy.fed] to syndicate content from an RSS feed to both ActivityPub and ATProto (aka Bluesky).
* Manual linking by posting from my `@wlach@cosocial.ca` account: for the amount of time I took to build this, I could have done this literally hundreds of times. 

## Coda

This wasn't *too* hard, but to make social publishing truly accessible, I feel like the direction to go is handling the social aspects via *the consuming application* (Mastodon and friends) rather than forcing each publisher to reinvent the wheel.
bridgy.fed is cool, but it feels a bit bolted-on.

If you enjoyed this post, you might find [Static ActivityPub Publishing](https://socialwebfoundation.org/2026/09/04/static-activitypub-publishing/) interesting.

[WebFinger]: https://docs.joinmastodon.org/spec/webfinger/
[pyodide]: https://pyodide.org/en/stable/
[D1]: https://developers.cloudflare.com/d1/
[bridgy.fed]: https://fed.brid.gy/
