Playback / viewer

Loop toggle (you already have play/pause/step/scrub/speed per architecture.md — loop is a natural fifth transport control)
Loop range selection (loop just the settled/interesting window, not the whole run — useful once a run hits repeats with a known period, you could even auto-suggest the loop bounds from the period)
Export current frame as PNG (separate from full canvas share — useful for the paused-cell-inspector view)

Sharing / export

Share canvas as image (static PNG of current frame) or short video/GIF loop of a range — video is what actually reads as "shareable" for something like #26's coarsening pattern
Shareable permalink to a specific tick (not just the rule) — /rules/:id/runs/:runId?tick=N
Open Graph / Twitter card metadata on rule pages so a shared link actually renders a preview image, not just a title

Rule naming / metadata

User-editable display name for a rule, separate from the AI-generated description (keep the generated description as canon/immutable, add a title field users can set)
Slug generation from the name for clean URLs
Tags/favoriting so a user can bookmark rules without it being a public comment

Social / auth

Comments on rules (you said this) — needs: rate limiting, edit/delete own comment, and some minimal moderation (report + hide) since this is public-facing generated content people will screenshot
Likes/upvotes as a lighter-weight signal than comments — useful input to your REQ-17.7 classifier calibration too, actually: user engagement is a free signal for "this one's interesting" separate from the machine's own classification
Author attribution if you ever let logged-in users request/steer a generation (ties to the "influence word" feature we talked about earlier) — who asked for this rule to be born

Discovery / library

Sort by "most discussed," "most looped," "newest," in addition to your existing status/behavior/concept filters
RSS or a simple "new rule" webhook/notification for people who want to watch the library grow passively