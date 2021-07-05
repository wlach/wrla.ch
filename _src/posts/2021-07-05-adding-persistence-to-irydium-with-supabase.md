    Title: Adding persistence to Irydium with Supabase
    Date: 2021-07-05T11:09:56
    Tags: Recurse, Irydium

Entering the second week of [Recurse].
Besides orientation and a few adventures in pair programming (special shout out to [Jane Adams] for trying out Irydium with me!), I spent most of my time attempting to get document saving &amp; loading working with Irydium.

I learned from [Iodide] that not having a good document sharing story really inhibits collaboration and sharing, which is something I explicitly want to do here at the Recurse centre (and in general for this project).
That said, this isn't actually an area I want to spend a lot of time on right now: it's the shape of problem I've solved many times before (and that has been solved by many others).
I'd rather spend my time over the next few weeks on things I haven't had much of a chance to look at or pursue in my day-to-day.

So, to try to keep the complexity down, I decided to take the same approach as the [svelte repl], which aims only to allow the reproduction of simple examples.
It allows you to save anything you type in it and also browse anything that you had previously saved.
That's not going to replace GitHub, but it's more than enough to get started.

[recurse]: https://recurse.com
[jane adams]: http://universalities.com/
[iodide]: https://alpha.iodide.io
[svelte repl]: https://svelte.dev/repl

## Supabase

So with that goal in mind, how to do go about it?
If I wanted to completely fall back on my previous knowledge, I could have gone for the tried + true approach of Django / Heroku to add a persistence layer (what I did for Iodide).
That would have had the benefit of being familiar but would also have increased the overall implementation complexity of Irydium considerably.
In the past year, I've become convinced that [serverless] approaches to building web applications are the wave of the future, at least for applications like this one.
They're easier to set up, easier to develop, and (generally speaking) cheaper to deploy.
Just before I launched, I set up [irydium.dev] as a static site on [Netlify] and it's been a great experience: deploys are super fast and it's easy to reason about what's going on "under the hood" (since there's not a much of a hood to look under).

With that in mind, I decided to take a (small) gamble and give [Supabase] a try for this one after determining it would be compatible with the approach I wanted to take.
Supabase bills itself as a "Firebase Alternative" ([Firebase] is another popular solution for bootstrapping simple web applications with persistence).
In contrast to Firebase, Supabase uses a standard database technologies (Postgres!) and has a nice JavaScript SDK and a bunch of well-written tutorials (including [one especially for Svelte](https://supabase.io/docs/guides/with-svelte)).

The naive model for integrating with Supabase is pretty simple:

- Set up a Supabase application, which provides you with a unique API endpoint to make web requests (this endpoint can be exposed publicly).
- Have your client authenticate with an OAuth provider (e.g. GitHub, GitLab), then store an authentication token in localStorage.
- You can then make requests to the above endpoint with the authentication token, which lets Supabase use row-level security to restrict modifications to the database: in this case, we can restrict users to updating their own documents.

I'd say it probably took me 20-30 hours to get the feature working end-to-end (including documentation), which wasn't too bad.
My impressions were pretty positive: the aforementioned tutorial is pretty decent, the supabase-js library provides a nice ORM-like abstraction over SQL and integrates nicely with Svelte.
In general working with Supabase felt pretty familiar to me from previous experiences writing database-backed applications, which I take as a very good sign.

The part that felt the weirdest was writing raw SQL to set up the "documents" table that Irydium uses: SQL is something I'm fairly used to writing because of my experiences at Mozilla, but I imagine this might be off-putting to someone newer to writing these types of things.
Also, I have some concerns of how maintainable a Supabase database is over the long term: while it was easy enough to [document the currently-simple setup instructions in the README](https://github.com/irydium/irydium/blob/f816ea6444c94635972a57bc92d7770398117c1e/README.md#working-on-the-site), I do somewhat fear the prospect of managing my database via their SQL console.
Something like Django's [schema migrations](https://docs.djangoproject.com/en/3.2/topics/migrations/) and [management commands](https://docs.djangoproject.com/en/3.2/howto/custom-management-commands/) would be a welcome addition to Supabase's SDK.

[serverless]: https://en.wikipedia.org/wiki/Serverless_computing
[irydium.dev]: https://irydium.dev
[supabase]: https://supabase.io/
[firebase]: https://firebase.google.com/
[netlify]: https://netlify.com

## Netlify functions

The above approach isn't what most people would consider to be "best practice"[^1].
In particular, storing credentials in localStorage is probably not the best idea for an application presenting interactive content like Irydium: it wouldn't be particularly difficult for a malicious document to steal someone's secret and send it somewhere it shouldn't be.

I'm not _so_ worried about it at this stage of the project, but one intriguing possibility here (that's compatible with our current deploy set up) would be to write some simple [Netlify Functions] to do the actual interaction with Supabase, while delegating to Netlify for the authentication itself (using [Netlify Identity]).

I experimented writing a simple function to prove out this approach and it seems to work quite well ([source](https://github.com/irydium/irydium/blob/fecea66a1cd0bedaaab4a3e6502413c55d34ec11/packages/site/netlify_functions/post.js), [example](https://irydium.dev/.netlify/functions/post?id=65107940-dd88-11eb-866c-0a4e9a1089db)).
This particular function is making an anonymous query to the database, but I see no obstacle to handling authenticated ones as well.
Having an API under a `.netlify` namespace seems kinda weird on first blush, but I can probably get used to it.

I want to move on to other things now (parsers! document state visualizations!) but might poke at this more later.
In the mean time, if you write/build something cool at [irydium.dev/repl](https://irydium.dev/repl), let me know!

[netlify functions]: https://www.netlify.com/products/functions/
[netlify identity]: https://docs.netlify.com/visitor-access/identity/

[^1]: See, for example, [Please Stop Using Local Storage](https://dev.to/rdegges/please-stop-using-local-storage-1i04)
