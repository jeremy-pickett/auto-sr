# Feature run log — documents/new-features-2.md

Second pass, same discipline as documents/feature-run-log.md: implement what's
reasonably scoped, log/skip anything that needs a product or privacy call
rather than guessing. This session picked up mid-flight after a disconnect;
the items below marked "done (pre-disconnect)" were already implemented and
tested in the working tree when this log was started.

## Status, one line per item from new-features-2.md

1. 502 error — SKIPPED, logged rather than guessed: no repro detail (which
   page, which action, when). Jeremy confirmed on resume: log it and move on
   rather than spending unbounded time guessing at a cause with no report to
   go on. If it recurs, the browser network tab (which request 502'd) and
   the backend log at that timestamp would make this tractable.
2. "Mine" showing the full library — INVESTIGATED, not a leak. Added
   `test_mine_does_not_show_someone_elses_public_rule` (backend/tests/
   test_visibility.py), which nails down the actual leak case (a public
   rule owned by someone else) and passes against current code. The
   original report matched a library where nearly every rule happened to
   be owned by the one signed-in user — expected behavior, not a bug.
3. PNG link / export doesn't work — DONE. Found and fixed a real bug:
   `exportFramePNG` / `exportFull` in RunView.jsx built a download `<a>`
   and called `.click()` on it without ever attaching it to the document.
   That's a known cross-browser gotcha (some browsers, notably older
   Safari, silently no-op a detached anchor's click instead of erroring) —
   matches "the button doesn't seem to do anything" exactly. Fixed with a
   shared `downloadBlobUrl()` helper that appends-clicks-removes.
4. Title not showing in every rule view — DONE. RunView's header and
   document title didn't use `rule.title` at all; Library cards and
   RuleView already did (from commit a2c084e). Wired RunView the same way.
5. Anonymous name / profile mechanism — DONE, scoped narrowly. See below.
6. Modifier/behavior tooltips — DONE. `frontend/src/lib/behaviorBlurbs.js`
   (static) and `modifierCatalog.js` (fetches the existing
   `GET /catalog/modifiers` blurb field, cached) wired as `title=` attrs on
   every chip in Library, RuleView, and RunView.
7. Comments in details/runs/rules — DONE. RuleView already had the
   `Comments` component; RunView didn't — added. Library (the list view)
   already surfaces `comment_count` per card from the discovery batch.
8. Copy-link button — DONE. `frontend/src/lib/clipboard.js`'s `copyText()`
   tries `navigator.clipboard.writeText` then falls back to a hidden
   textarea + `execCommand('copy')`, and only claims success if one of them
   actually worked (the old code changed the URL bar regardless).
9. "Run again" tooltip — DONE, plain-English `title=` on both instances
   (RuleView, RunView).
10. Pagination not showing in Library — DONE. `page_size` default dropped
    from 50 to 24 (`GET /rules`); the pagination footer only renders when
    `total > page_size`, so with a library under 50 rules it never
    appeared. 24 makes it show up at a realistic library size.
11. Profile link — DONE, folded into item 5.
12. Zoom in/out on the canvas (stretch) — DONE. See below.
13. RSS feed broken — DONE. Item links were built from `request.base_url`
    (this API's own origin — a bare JSON server, 404s on `/`). Now built
    from a new `settings.frontend_url` (`FRONTEND_URL` env var, defaults to
    the Vite dev origin) so links open the actual app.
14/15. Social share buttons + "normal way to post" — DONE, partial by
    necessity. See below.

## Profile mechanism (items 5, 11)

Scoped to what doesn't require a new product surface or exposing anything
private: a signed-in user can set an optional display name that overrides
their comment pseudonym everywhere it's shown. NOT built: a broader
"profile page" with bio/avatar/history — nothing in the spec or the feature
list asked for that beyond "a place to change bits like the anonymous name,"
and inventing more surface unprompted isn't this pass's job.

- `user_profiles(uid TEXT PRIMARY KEY, display_name TEXT)`, additive
  migration, same style as the owner_uid/visibility migration from Firebase
  auth Phase 1.
- `GET/PUT /profile` (auth required — 401 anonymous). Display name: 1-40
  chars, printable, server-trimmed; empty clears it back to the pseudonym.
- `comments.py`'s `_comment_row` prefers the profile display name over
  `pseudonym(uid)` when one is set.
- Frontend: `#/profile` view (nav link, signed-in only), reachable the same
  way `#/mine` is.

## Zoom to inspect cells (item 12, explicitly "stretch")

Scroll-wheel zoom + a reset button on the run canvas (`grid-shell`), CSS
transform on the canvas element, clamped 1x-8x. Deliberately not a new
renderer or a pan/zoom minimap — the ask was "inspect cells," which
scroll-zoom-then-click-to-inspect (existing feature) already satisfies.

## Social sharing (items 14, 15)

- DONE: share-intent buttons for X/Twitter and Facebook on RunView — these
  are plain `https://twitter.com/intent/tweet?...` / `https://www.facebook.
  com/sharer/sharer.php?u=...` links opened in a new tab, prefilled with the
  run's tick-permalink URL and a short text blurb. No API keys or OAuth
  needed; this is the same mechanism every "share on X" button on the web
  uses.
- DONE: the existing PNG frame export (item 3) doubles as the "larger
  version of the thumbnail" ask — already scaled up to ~800px, nearest-
  neighbor for crispness.
- SKIPPED, logged rather than guessed: actual automated posting ("a normal
  way to post with the thumbnail, title, blurb") to any of these platforms.
  That needs a registered app + OAuth per platform (Meta app review for
  Facebook/Instagram, a paid X API tier for programmatic posting) — real
  credentials this app doesn't have, not a code gap. Same category of skip
  as GIF/video export in the first pass: a new integration surface, not a
  bug or a small feature. Instagram specifically has no web share-intent
  URL at all (mobile-app-only sharing), so even the lightweight version
  isn't available there.
- Per-rule Open Graph image is still the same architectural gap documented
  in the first pass (hash routing means no server-side per-route meta) —
  unchanged by this pass, not re-litigated here.
