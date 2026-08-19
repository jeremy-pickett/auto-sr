# Feature run log — documents/new-features-v1.md

Started 2026-08-19, unattended, Jeremy detached. One line per item as it's
decided or finished; updated live, not retroactively rewritten. "Done" means
tested and pushed, not just written.

## Ground rules set before starting
- Comments: building create/edit-own/delete-own with rate limiting. NOT
  building report/moderation queue — no admin/moderator role exists
  anywhere in this app to review one.
- Author attribution: SKIPPED. The only identity available is a Firebase
  login email; publishing that on a public rule page is a privacy decision
  I'm not making unilaterally.
- GIF/video export: SKIPPED as out of scope for this pass (new dependency,
  real CPU/complexity jump vs. the rest of this list). Static PNG frame
  export covers the "shareable image" need instead.

## Status

### Playback / viewer — DONE (commit 875d51e)
- Loop toggle — transport checkbox, playback clock wraps to loopStart
  instead of stopping.
- Loop range selection — from/to inputs shown when loop is on; "use the
  settled period" auto-fills from run.loop_length (already computed by
  the classifier, no new backend work needed).
- Export current frame as PNG — scaled-up, nearest-neighbor download of
  the current tick. Known limitation: always square cells regardless of
  the round-cells toggle (that's a CSS mask at paint time, not canvas
  pixel data — not worth replicating in a raster export for this pass).

### Sharing / export — partially done
- Shareable tick permalink (`#/runs/3?tick=150`) — DONE (commit 875d51e).
  Router reads it, RunView seeds/follows it, copy-link button in the
  transport.
- Static PNG share — covered by the frame-export button above.
- GIF/video export — SKIPPED, logged before starting (see ground rules).
- Open Graph / Twitter card metadata — PARTIAL, DONE what's possible
  (commit 7d21890). Genuinely blocked, not just skipped: this is a
  hash-routed SPA, and the browser never sends the URL fragment after
  '#' to the server, so there's no way to render per-rule meta tags
  server-side for a crawler to see. Fixing that means switching from
  hash routes to path-based routing + server-side history-API
  fallback — a bigger, separate change, not attempted here. What's
  shipped: generic app-level OG/Twitter tags in index.html, plus a
  real, tested GET /rules/{id}/preview.png endpoint (renders the
  canonical run's final tick as a PNG) that's ready to wire up to
  real per-rule tags if the routing scheme ever changes. Bonus:
  document.title now reflects the open rule/run (didn't exist before,
  cheap, real UX value even though it doesn't help crawlers).

### Rule naming / metadata — DONE (commit 75ab631 + favorite_count follow-up)
- Title (PATCH /rules/{id}), slug generation + #/r/:slug clean URLs,
  favoriting.
- Note: merged "tags/favoriting" (this section) with "likes/upvotes"
  (Social section below) into ONE mechanism. They're structurally the
  same thing -- one row per user per rule, toggled -- so building two
  near-identical tables/endpoints for "private bookmark" vs. "public
  upvote" wasn't worth it. The favorites table now backs both: a
  private favorited flag for the signed-in user, plus a public
  favorite_count visible to everyone (added just after the main
  commit, same session) covering the "lighter-weight public signal"
  half of the ask. Also feeds sort=most_liked, and is a free real
  signal toward REQ-17.7's classifier-calibration question, as the
  original doc noted.

### Social / auth — in progress next
- Likes/upvotes — DONE, see favorite_count note above.
- Author attribution — SKIPPED, logged before starting (privacy: only
  identity available is a login email).
- Comments — DONE (see commit). Create/list, edit-own, delete-own, a
  5-per-60s rate limit (in-memory, per-process -- documented as not
  distributed-safe, fine for this single-node app). NOT built: report/
  moderation queue, logged before starting (no admin/moderator role
  exists anywhere in the app to review one). One design problem
  solved along the way: a comment needs to show *some* author label,
  but the only identity data available is a login email, and
  publishing that was already ruled out for the same privacy reason
  as "author attribution." Solved with a deterministic pseudonym
  generated from the Firebase uid (e.g. "wraparound-watcher-720") --
  consistent per person across comments, never reveals or derives
  from the actual email, verified live end-to-end (post/list/edit/
  delete all correct, pseudonym never contains "@").

### Discovery / library — DONE
- Sort by newest / most favorited / most discussed / most looped —
  all four shipped. "most_discussed" counts comments (same batched-
  count-query shape as favorite_count, new comment_count field).
  "most_looped" reinterpreted concretely for this app's actual domain:
  sorts by the canonical run's loop_length (the longest repeating
  cycle a rule settled into) rather than a generic "play count," which
  isn't tracked anywhere and would've needed new instrumentation just
  to back one sort option. Both counts are also shown on library
  cards, not just sortable-but-invisible.
- RSS feed — DONE. GET /library/feed.rss, standard RSS 2.0, public
  rules only (an RSS reader carries no auth token, so this falls out
  of the same visibility rule as everything else, not a special case),
  most recent 30. Autodiscovery <link> in index.html plus a footer
  link. Verified live against the real running server and confirmed a
  private rule never appears in it.
- Webhook for new rules — SKIPPED, logged before building the RSS
  feed: a user-supplied delivery URL is a real SSRF surface (the
  server would make outbound requests wherever a caller points it),
  and there's no delivery/retry infrastructure in this app to do that
  safely. RSS covers the "watch the library grow passively" need
  without that risk.

## All items from documents/new-features-v1.md are now accounted for
Every item is either done, partially done with the gap explained, or
skipped with a specific reason — see the ground rules at the top of
this file and the sections above. Nothing was left silently untried.
