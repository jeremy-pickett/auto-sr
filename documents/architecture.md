# Architecture

Durable record of design decisions for the build. The requirements spec
(`asr-requirements-v3.md`) is the contract; this file records how we are
implementing it and the choices the spec left open. Keep it current every
phase — chat sessions are not durable, this file is.

## Decisions (2026-08-19, with Jeremy)

| Decision | Choice | Notes |
|---|---|---|
| UI direction | **Dark observatory** | Near-black (#0a0e14) canvas-first UI. The automaton is the glowing hero; luminous cell palette, cyan/amber accents, instrument-panel stats, smooth motion. The frontend is the Wow factor and gets a real design system from day one. |
| Build sequencing | **Vertical slice** | Engine + fixtures → storage → API → frontend player, so gliders are visible in the real UI before any LLM call. Generation pipeline after. |
| Default generation model | **`claude-opus-5`** | Explicit `ANTHROPIC_MODEL` config, recorded per rule (spec §3.9). |

## Repository layout

```
backend/
  pyproject.toml           package "asr"; pytest config
  asr/
    config.py              env-backed settings (spec §3.9)
    engine/                Cells, geometry, bound helpers, Dice, tick, fingerprints, run loop, classifier
    contract/              restricted namespace, AST validator, child-process runner
    storage/               SQLite WAL schema, tick payload encoding, reconstruction + cache
    generation/            prompt template files, coverage map / Stage A context, pipeline, modifier catalog
    api/                   FastAPI app, routes, SSE generation stream, binary grid framing
    fixtures/              life, majority, walker (ship with the system, §14)
  tests/                   fixtures/slow_burn (test-only), bad_rules/, per-phase suites
frontend/                  Vite + React 19; canvas renderer; design system per UI decision
documents/                 the spec, this file
```

## Implementation choices within the spec

- **Helpers bound at namespace-build time.** `bind_helpers(neighbors, reach)`
  returns the spatial helper functions with the declared neighborhood baked in
  (REQ-6.2.1). Generated code receives them pre-bound in its execution
  namespace; fixtures call the same factory. There is no unbound helper
  surface anywhere.
- **`Cells` is write-protected at runtime too.** Attribute assignment raises;
  the harness mutates through a private `_set`. The AST validator remains the
  primary enforcement (REQ-4.5), this is a second net.
- **`step()` returns a rule-owned-only grid.** Generated `step` builds its
  proposal with `make_cells` (rule-owned arrays only); the harness re-attaches
  modifier/slot arrays and computes derived arrays inside `apply_tick`. This
  keeps `make_cells` the single construction path (REQ-6.2) and makes it
  structurally impossible for a rule to alter a modifier array.
- **Offset convention.** An offset is `(down, right)`. `look` follows the
  spec sentence exactly: positive `down` brings the upstairs neighbor's value
  into this cell's position (`np.roll` semantics). Neighbor tallies are
  symmetric over the offset set, so the convention does not affect them.
- **Draw dtypes.** `Dice.integers`/`choice` return int32; rule code casts into
  its uint8 arrays with `astype` (which is on the approved surface).
- **ASSIGN entry format.** The spec leaves the modifier-draw declaration
  loosely specified; we mirror the slot form (REQ-5.5.2): each entry is
  `{"value": v, "chance": p}` — an affected cell gets `v` with probability
  `p`, its identity value otherwise.
- **Fixed draw order** (REQ-4.6, reproducibility): modifiers in name-sorted
  order, then semantic slots in name-sorted order; at tick 0 all `start`
  draws happen before all `birth` draws.
- **Catalog `assign_when`/availability** (spec table 5.4 leaves them open):
  `weight` birth, `stubbornness` birth, `rate` start (terrain-like — a
  cell's schedule shouldn't change under it mid-run), all three
  `sometimes(0.3)`. Definitions live in `engine/modifiers.py`;
  `generation/catalog.py` will consume the same specs for Stage A gating.

## Calibration notes (REQ-17 open items)

Hooks for the measurements the spec says to take once real data exists.
Update in place as numbers land.

- **REQ-17.1 `SNAPSHOT_EVERY=50`:** untuned. Measure: average payload
  bytes per tick by encoding (`SELECT payload_encoding, AVG(LENGTH(payload_blob)) FROM ticks GROUP BY 1`)
  against reconstruction latency in `reconstruct_range` before changing.
- **REQ-17.2 `structured` detection:** REQ-9.16 row 7 is a threshold
  heuristic, always reported low-confidence. `runs.user_behavior`
  accumulates the labeled examples a better detector would train on.
- **REQ-17.3 `rate` × `age`:** a cell gated off a tick still ages
  (REQ-4.3.1, asserted in tests). Watch generated rules that read `age`
  under `rate` for confusion before considering an `updates` counter.
- **REQ-17.4 slot degeneration:** kill criterion is REQ-5.5.3 (80% of
  200 slot-declaring rules where slot is determined by kind). Query
  when the count approaches 200.
- **REQ-17.7 classifier thresholds:** first guesses, calibrated against
  nothing; re-derive from the first two hundred canonical runs and
  record the revision here.
- **REQ-17.8 `MAX_TICKS=500` cost:** with `visually_frozen` removed,
  more runs reach `ran_out`. First data point: the first generated rule
  (cyclic succession) looped at tick 9 — cheap. Track mean ticks_run.

## Phase log

- **Phase 0 (2026-08-19):** git repo initialized (provenance needs the
  revision hash, REQ-12.4), pytest installed, package skeleton, settings
  module, this document.
- **Phase 1 (2026-08-19):** engine core — `cells.py`, `geometry.py`,
  `helpers.py`, `dice.py` with tests.
- **Phase 2 started (2026-08-19):** `modifiers.py` (v1 catalog specs),
  `declaration.py`, `fingerprint.py` (computational vs pattern, scheduler
  phase, RNG state, stubbornness age clamp), `tick.py` (REQ-4.6 init
  sequence + REQ-6.4 tick order).
- **Phase 2 complete (2026-08-19):** `run.py` (stopping precedence, per-tick
  stats, pattern_settled_at), `classify.py` (REQ-9.16 rows), `contract/child.py`
  (fork + pipe streaming, parent-owned tick timeout, RLIMIT_AS), fixtures
  life/majority/walker + test-only slow_burn. Verified empirically: majority
  freezes at tick 13, walker loops at exactly grid width, a glider on an 8x8
  torus loops at exactly 32 with 5 live cells throughout (REQ-14.2), slow_burn
  flips at tick 60 (REQ-15.8), rate prevents false loops (period 12 not 4),
  stochastic settle reaches frozen. 88 tests.
- **Phase 3 (2026-08-19):** `storage/` — SQLite WAL schema per §12, tick
  payload encoding (snapshot every `SNAPSHOT_EVERY`, sparse changed-index vs
  dense-XOR deltas, whichever is smaller, zstd), reconstruction with derived
  arrays rebuilt and an LRU byte-budget cache. REQ-15.4 verified across all
  three encodings.
- **Phase 4 (2026-08-19):** backend API (`api/app.py`, `routes.py`,
  `framing.py` binary grid wire format REQ-11.5.1, fixture seeding via
  `asr.seed`) and the dark-observatory frontend player: hash router
  (Library / RunView / Catalog), canvas renderer blitting decoded binary
  grids through `ImageData` with kind palette + age/level brightness,
  transport (play/pause/step/scrub/speed), SVG sparklines for `variety` /
  `cells_changed` / `kind_quiet_for` with current tick + `pattern_settled_at`
  markers, paused-cell inspector with neighbor patch and whole-run history
  strip, display-mapping precedence user → `SUGGESTED_DISPLAY` → kind/age
  (REQ-13.2), REQ-13.11 quiet-but-alive messaging, REQ-0.3 credit line.
  Grid chunks fetched 250 ticks at a time with prefetch. 104 tests;
  `npm run build` clean.
- **Phase 5 (2026-08-19):** generation pipeline. `contract/namespace.py`
  (exact §7.9 allowlists; `load.py` now executes all rule source —
  fixtures included — under the restricted builtins and NumPy proxy),
  `contract/validator.py` (REQ-7.8 steps 1–3: structure, every static
  check, declaration match incl. READS), runtime input-mutation
  enforcement (run loop freezes every grid array before the rule sees
  it, so REQ-7.5 violations raise in the child), prompt templates as
  files (`generation/prompts/`), `catalog.py` (availability gating,
  ≤1 non-always modifier per generation), `context.py` (coverage map
  with three counts, Stage A context in budget, fixed 8-word concept
  vocabulary; `/library/summary` now shares this one implementation),
  `shape.py` (static inference, small-model fallback via new
  `SHAPE_MODEL` setting, default claude-haiku-4-5), `pipeline.py`
  (A→B→C with one repair, full provenance, canonical run), and
  `api/stream.py` (SSE from POST, REQ-11.4 event sequence). Tests:
  14 bad rules (REQ-15.5, one per rejection path), namespace, pipeline
  against a fake model, REQ-8.6 canonical-only coverage. 136 tests.
  Milestone hit live: claude-opus-5 invented a 4-kind cyclic-succession
  rule, it validated, ran 200×200, classified `repeats`/high.
- **Phase 6 (2026-08-19):** full UI. `views/Invent.jsx` consumes the
  generation stream via streaming `fetch()` + `ReadableStream` (never
  EventSource, REQ-11.4.1): stage lamps (inventing → implementing →
  validating → running) with breathing active state, the proposal shown
  as it lands, validation failures and the repair attempt surfaced,
  tick progress, and the outcome panel for ok / broken / failed.
  `views/RuleView.jsx` (#/rules/:id): description, reasoning, source,
  error text for broken rules, runs list, rerun, and full provenance —
  hashes, model, and the rendered prompts + raw responses behind folds.
  Library cards click through to the canonical run (or details when
  broken) with a separate details link; Invent wired into nav and the
  library header button.
- **Phase 7 (2026-08-19):** README at the repo root, CLAUDE.md brought
  up to date, the calibration-notes section above for the REQ-17 open
  items, and the conformance spot-check: banned jargon grep clean
  (standard terms appear once, in comments), every §15 REQ has a named
  test, and the PATCH is the only endpoint that mutates a stored run.
  All phases complete.
- **Phase 8, Firebase Authentication Phase 1 (2026-08-19):** optional
  multi-user support layered on the single-user app, deliberately
  conservative — added, not decided by, this phase: OAuth providers,
  per-user run corrections, TLS. By default every rule is still global
  and anonymous, exactly as before.

  Design: a two-column additive migration (`rules.owner_uid`,
  `rules.visibility`, default `'public'`) via a new idempotent
  `db._ensure_columns` step, since `CREATE TABLE IF NOT EXISTS` is a
  no-op against a database that already has the table — the SCHEMA
  string alone can't carry a change like this to an existing
  `library.db`. `api/auth.py`'s `get_current_user` is an optional
  FastAPI dependency verifying a Bearer ID token via `google-auth`'s
  `verify_firebase_token` — no service-account secret, only the
  (public) Firebase project ID; absent header is anonymous, a present
  but invalid token is always a hard 401, never silently downgraded.
  Every read endpoint touching a rule or its runs 404s — identical
  wording to a genuine not-found — for a private rule's non-owner;
  `GET /rules` defaults to public-only regardless of auth state, with
  `mine=true` as the personal-library filter. `POST /rules/generate`
  resolves identity in the route handler (the pipeline runs in a
  worker thread with no `Request` to derive it from later) and accepts
  an optional `{"visibility": "private"}` body — `Body(default=None)`,
  not a defaulted model instance, is what keeps accepting today's bare
  bodyless POST unchanged. `generation/context.py`'s coverage map,
  totals, and Stage A example blocks all filter to public rules —
  extending REQ-8.5's "user signal never enters generation context" to
  another user's private content, verified by asserting a marked-
  private rule's description never appears in the rendered Stage A
  prompt text at all, not just hidden from a UI.

  Frontend: `firebase` (modular JS SDK), `src/lib/firebase.js`
  (`useAuth()` wrapping `onAuthStateChanged`; no Context — the app had
  none and Firebase's `getAuth()` is already a singleton), the
  Email/Password-only `AuthControl` in the topbar, a shared
  `authorizedFetch` in `api.js` (every export now goes through it
  rather than a bare `fetch()`, with no signature changes — anonymous
  requests stay byte-identical), a `mine` prop reusing `Library.jsx`
  for `#/mine` rather than forking the view, and a Public/Private
  choice in `Invent.jsx`, shown only when signed in.

  Step 0 spike (run before writing `auth.py` for real): Firebase
  Email/Password was chosen over OAuth specifically because the
  droplet has no domain or TLS yet — OAuth's redirect flow needs a
  domain on Firebase's authorized-domains allowlist (bare IPs aren't
  accepted there), while Email/Password is a direct API call with no
  such check. Confirmed by creating a real throwaway account via the
  Identity Toolkit REST API and feeding the token to
  `verify_firebase_token` two ways: a real token accepted with correct
  `aud`/`iss`/`sub` claims, a hand-tampered one rejected outright.

  Verified live, not just by test: the schema migration ran against
  the actual `library.db` (backed up first) — all 28 pre-existing
  rules landed `visibility='public'`, `owner_uid=NULL`, unchanged. A
  real anonymous generation ran end-to-end through the live SSE
  endpoint and Anthropic, landing public/no-owner as before. A real
  sign-up through the actual browser-side JS SDK (not REST) produced a
  token that the live backend accepted over HTTP, correctly scoped
  (`mine=true` → the new user's own, empty, list); no token still
  401s with a sign-in prompt; a garbage token still hard-401s rather
  than silently passing as anonymous. 26 new backend tests (162 total);
  frontend build and lint clean.

  Known limitations, carried forward deliberately: Bearer tokens
  travel over plain HTTP until TLS exists — dev/trusted-network auth
  only, not yet safe for a hostile network. A private generation
  attempt that fails still nudges the shared coverage map as an
  anonymous count (no text, no attribution) via the pre-existing
  rejections table, which has no owner/visibility concept in this
  phase — judged consistent with "content excluded," not a violation
  of it, but a judgment call rather than a settled question.
