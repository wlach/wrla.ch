# wrla.ch ActivityPub Worker

This directory contains the small stateful half of the blog's ActivityPub
feed. The site generator publishes the actor, outbox, post objects, and
manifest. This Python Worker handles discovery, inbox traffic, collections,
scheduled publication, and signed delivery. D1 holds only federation state.
Pydantic models validate all remote protocol objects and the deployed manifest;
unknown ActivityPub extension fields are preserved for interoperability.

The design and its intentional limitations are recorded in
[`idrs/202608240235-add-activitypub-feed.md`](../idrs/202608240235-add-activitypub-feed.md).

## Repository safety

`public-key.pem` is public by design and is safe to commit. `private-key.pem`,
`.dev.vars`, local Wrangler data, Cloudflare credentials, and the production D1
identifier are not safe to commit. Git ignores the local secret-bearing files.
Never paste the private key into `wrangler.toml`.

## One-time setup

Run these commands from the `activitypub` directory so Wrangler discovers this
Worker's `wrangler.toml`. The `uv --project activitypub` option selects a Python
project but does not change Wrangler's working directory.

```sh
cd activitypub
```

1. Create the D1 database:

   ```sh
   uv run pywrangler d1 create wrla-ch-activitypub
   ```

2. Replace `REPLACE_WITH_D1_DATABASE_ID` in `wrangler.toml` with the returned
   database ID. The ID is not secret and may be committed.
3. Apply migrations:

   ```sh
   uv run pywrangler d1 migrations apply wrla-ch-activitypub --remote
   ```

4. Install the signing key as a Worker secret without printing it:

   ```sh
   uv run pywrangler secret put ACTIVITYPUB_PRIVATE_KEY < private-key.pem
   ```

   Confirm that the secret exists without displaying its value:

   ```sh
   uv run pywrangler secret list
   ```

5. Deploy once with `OUTBOUND_DELIVERY_ENABLED = "false"`, then configure the
   Worker Builds Git integration to use
   `activitypub` as its root directory. The deployment command is
   `uv run pywrangler deploy`.

6. Verify WebFinger and follow the actor from an account you control. Once the
   actor and stored follower look correct, change `OUTBOUND_DELIVERY_ENABLED`
   to `"true"` and deploy again. While disabled, the cron still initializes and
   synchronizes post state, but no `Accept`, `Create`, or `Delete` is sent.

The checked-in public key was derived from the ignored local private key. If
the private key is lost before it is installed in Cloudflare, generate a new
pair and replace `public-key.pem` before publishing the actor. Rotating a key
after federation begins requires retaining the old key long enough for remote
servers to refresh the actor document.

## Local development

Create `activitypub/.dev.vars` containing the multiline secret
`ACTIVITYPUB_PRIVATE_KEY`, then run from the repository root:

```sh
cd activitypub
uv sync
uv run pywrangler d1 migrations apply wrla-ch-activitypub --local
uv run pywrangler dev --test-scheduled
```

The production cron runs every five minutes. A newly observed post remains
pending for fifteen minutes. The Worker re-fetches its deployed Note just
before delivery, so edits during that window are included.

## Redacting a post

Remove the Markdown source, add an entry to `redactions.json`, and deploy the
site:

```json
{
  "source_id": "20260101000000-example-post",
  "deleted": "2026-08-24T12:00:00Z"
}
```

Both steps matter. Removing the source takes the article off the blog; the
explicit record creates its tombstone and triggers federation. Absence alone
never triggers a federated Delete. On its next scheduled runs, the Worker sends
the explicit Delete to every inbox that successfully received the original
Create and retries temporary failures.

## Operational care

This is deliberately “houseplant software.” Normal operation should require no
attention. Delivery is bounded to 50 attempts per invocation and eight tries
per destination, with capped exponential backoff. Terminal failures and retry
history remain queryable in the `deliveries` table and appear in Worker logs.
The inbox is limited to 120 requests per minute in each Cloudflare location.
Remote documents must arrive within ten seconds and may contain at most 512
KiB. Wrangler also enables persisted Worker observability. Occasional
inspection of failed deliveries, rate-limit responses, and D1 storage is
sufficient.
