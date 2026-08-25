# wrla.ch ActivityPub Worker

This directory contains the small stateful half of the blog's ActivityPub
feed. The site generator publishes the actor, outbox, post objects, and
manifest. This Python Worker handles discovery, inbox traffic, collections,
quote authorization, scheduled publication, and signed delivery. D1 holds only
federation state.
Pydantic models validate all remote protocol objects and the deployed manifest;
unknown ActivityPub extension fields are preserved for interoperability.

The design and its intentional limitations are recorded in
[`idrs/202608240235-add-activitypub-feed.md`](../idrs/202608240235-add-activitypub-feed.md).

## Repository safety

`public-key.pem` and the D1 database identifier are public by design and are
safe to commit. `private-key.pem`, `.dev.vars`, local Wrangler data, and
Cloudflare credentials are not. Git ignores the local secret-bearing files.
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

   Run this again before deploying any revision that adds a migration. Wrangler
   records applied migrations and runs only the new ones. In particular,
   `0002_quote_authorizations.sql` must be present before deploying quote-post
   support.

4. Install the signing key as a Worker secret without printing it:

   ```sh
   uv run pywrangler secret put ACTIVITYPUB_PRIVATE_KEY < private-key.pem
   ```

   Confirm that the secret exists without displaying its value:

   ```sh
   uv run pywrangler secret list
   ```

5. Deploy once with `OUTBOUND_DELIVERY_ENABLED = "false"`, then configure the
   Worker Builds Git integration. If Cloudflare exposes a root-directory
   setting, set it to `activitypub` and use this deploy command:

   ```sh
   uv run --locked pywrangler deploy
   ```

   If the root-directory setting is unavailable, Worker Builds runs from the
   repository root. Change directories in the deploy command instead:

   ```sh
   cd activitypub && uv run --locked pywrangler deploy
   ```

   The `cd` and `pywrangler` parts are both required. `uv --project` changes
   the selected Python project but not the directory where Wrangler searches
   for its configuration. Plain `npx wrangler deploy` does not prepare and
   bundle the packages in `pyproject.toml`.

6. Verify WebFinger and follow the actor from an account you control. Once the
   actor and stored follower look correct, change `OUTBOUND_DELIVERY_ENABLED`
   to `"true"` and deploy again. While disabled, the cron still initializes and
   synchronizes post state, but no `Accept`, `Create`, or `Delete` is sent.

The checked-in public key was derived from the ignored local private key. If
the private key is lost before it is installed in Cloudflare, generate a new
pair and replace `public-key.pem` before publishing the actor. Rotating a key
after federation begins requires retaining the old key long enough for remote
servers to refresh the actor document.

### Worker Builds troubleshooting

The build log should show one of the deploy commands above. Two errors point to
specific configuration mistakes:

- A Pages-project warning followed by `Missing entry-point to Worker script or
  to assets directory` means Wrangler ran from the repository root and found
  the site's root `wrangler.toml`.
- `ModuleNotFoundError: No module named 'pydantic'` during upload validation
  means plain Wrangler ran from `activitypub`. Use `uv run --locked pywrangler
  deploy`; pywrangler vendors the dependencies before passing the deployment to
  Wrangler.

An automatic root-level `uv sync` in the build log is unrelated. It installs
the static site's dependencies into the build machine, not the Python packages
uploaded with the Worker. A failed build leaves the most recent successful
Worker deployment running.

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

## Quote posts

Every generated public Note advertises unconditional automatic quote approval
using the FEP-044f `interactionPolicy`. The policy enables quote controls in
supporting software, but is only advisory. The Worker implements the matching
authorization handshake: it accepts a signed `QuoteRequest`, verifies that the
public quote Note belongs to the signing actor and targets a known local post,
stores a stable approval, and sends a signed `Accept` containing its URL.

Approval stamps are publicly dereferenceable at
`/activitypub/wrlach/quote-authorizations/<id>`. They contain only the local
actor, the public quote URL, and the public quoted-post URL. There is no manual
approval queue or block list: valid public quote requests are approved
unconditionally. D1 persistence makes the response idempotent and leaves room
for explicit revocation later, but no revocation interface is currently
implemented.

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
