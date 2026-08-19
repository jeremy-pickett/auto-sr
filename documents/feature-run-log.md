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

### Rule naming / metadata — in progress next.

(rest updated as work proceeds)
