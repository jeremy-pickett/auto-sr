# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this project is

Autonomous Semantic Ruliology: a single-user, local web app where an LLM invents cellular-automaton rules (Stage A: describe in English → Stage B: implement in Python), the harness validates and runs them, and every result — including failures — accumulates in a permanent SQLite library.

**`documents/asr-requirements-v3.md` is the single source of truth.** It is contract-complete and every requirement has a stable `REQ-` identifier. Read the relevant section before implementing anything; cite `REQ-` identifiers in commits and issues instead of describing behavior in prose. Section 2 records decisions with rationale so they are not re-litigated; Section 16 lists what is deliberately out of scope; Section 18 gives the priority order for foundational work (state model, randomness model, Cells contract, bound helpers, geometry, init sequence, Stage B contract, restricted namespace, runtime enforcement, transport framing — settle these before core abstractions).

## Current state

All seven build phases are complete (engine → storage → API → frontend player → generation pipeline → full UI → docs). `documents/architecture.md` records the layout, the decisions made with the user (dark-observatory UI, `claude-opus-5` default generator model), a calibration-notes section for the REQ-17 open items, and the phase log — keep all of it current.

Beyond the original seven phases, **Firebase Authentication Phase 1** is complete: optional sign-in (Email/Password only — no domain/TLS yet for OAuth's redirect flow), a personal library layered on the global one, and a public/private choice at rule-creation time. Rules stay public/anonymous by default; nothing about the generation architecture changed. See `documents/architecture.md`'s phase log for the full design (schema migration, the auth dependency, per-route access checks, Stage A exclusion) and what's still out of scope (OAuth providers, per-user run corrections, TLS).

Also complete: a **system page** (`#/system`, `backend/asr/api/system.py`) — a live pipeline/process-map dashboard plus browsable history for two session kinds: `generation_sessions` (one row per `POST /rules/generate`, instrumented by wrapping `emit()` once in `generation/pipeline.py` rather than touching each call site) and `http_sessions` — the colloquial HTTP session, not a client heartbeat: a cookie minted and tracked by a middleware in `api/app.py` (`track_request`) that touches `last_seen_at`/`request_count`/`last_path`/IP/User-Agent on every request, automatically, with no client-side code at all. (An earlier `app_sessions` + `lib/usePresence.js` heartbeat design was built, hit a string of client-side bugs, and was fully replaced by this — the table is left in the schema, unused, rather than dropped.) **`/system/*` and `#/system` are intentionally unauthenticated and globally visible** — a deliberate, temporary choice for the single-user phase, same as the rest of the app; if this ever goes multi-user, `/system/*` needs an access check the same way `#/mine` does today.

Also complete: the **render-modes half of uplift 2.2.1** (`documents/requirements/frontend-vis-uplift-2.2.1.md` §8) — `RunView.jsx`'s render-style picker now has `activity` (REQ-13.17: lights where `kind` changed this tick) and `kind_stable` (REQ-13.18: glows where `kind` held but the mapped brightness property changed — the highest value-to-cost item in that document), `trails` rebuilt to a real `TRAIL_WINDOW_TICKS`-tick (40) decaying composite with a REQ-13.19.2 on-screen "not a tick" badge, and `relief` upgraded from a single-neighbor emboss to a real gradient/normal/fixed-light shading pass. `glow` (pre-existing, not in that document) was kept as-is — no REQ covers it, nothing asked to remove it. The recurrent-structure detector (§4-7 of the same document, REQ-19.x) is a separate, not-yet-started plan; none of these render modes depend on it.

- `backend/asr/` — Python package: `config.py` (env-backed settings per spec §3.9), `engine/` (Cells, geometry, bound helpers, Dice, tick, fingerprints, run loop, classifier), `contract/` (restricted namespace, Stage C validator, child-process runner), `storage/` (SQLite WAL, tick encoding, reconstruction + cache), `generation/` (prompt template files, coverage map / Stage A context, gating, pipeline), `api/` (routes, SSE stream, binary framing, `auth.py` — optional Firebase ID-token verification), `fixtures/`, `seed.py`.
- `backend/.venv` — Python 3.12 with fastapi, uvicorn, numpy, zstandard, anthropic, pytest, google-auth, requests, pillow (rule preview-image rendering).
- `frontend/` — Vite + React 19 dark-observatory UI: library browser, run player, rule detail with provenance, Invent view over the generation stream, modifier catalog, Firebase Email/Password sign-in with a personal (`#/mine`) library. The run player (`RunView.jsx`) has a render-style picker (flat/glow/trails/relief) layered on the existing color/brightness display mapping (REQ-13.2) — pure frontend presentation, no backend or spec changes. A rule-suggested style (extending `SUGGESTED_DISPLAY` the way `color`/`brightness` are already suggested — `backend/asr/generation/pipeline.py`, `seed.py`, `storage/db.py`) is a deliberately deferred fast-follow that would need a new REQ-13.x id and prompt-template changes.
- `documents/` — the requirements spec + architecture.md.

## Commands

Frontend (run from `frontend/`):
- `npm run dev` — Vite dev server (proxies `/rules /runs /catalog /library /system /profile /comments` to :8000; `/profile` and `/comments` were missing until 2026-08-20, which is why sign-in profile edits and comment edit/delete were silently broken in dev — watch for this gap again if a new top-level route is added to the backend and forgotten here). `vite.config.js` sets `server.host: true` so it binds `0.0.0.0` instead of loopback-only — this droplet is accessed by external IP, and a plain Vite default (`[::1]` loopback) is unreachable from outside. If the dev server is ever "up but not accessible" again, check `ss -tlnp | grep 5173` for a loopback-only bind before assuming anything else is wrong.
- `npm run build` — production build
- `npm run lint` — oxlint (config in `.oxlintrc.json`)

Backend (run from `backend/`):
- `.venv/bin/python -m pytest` — full test suite
- `.venv/bin/python -m pytest tests/test_helpers.py::test_move_rejects_diagonals_under_plus_4` — one test
- `.venv/bin/python -m asr.seed` — seed reference rules + modifier catalog (idempotent)
- `.venv/bin/python -m uvicorn asr.api.app:app` — serve the API on :8000

Generation needs `ANTHROPIC_API_KEY` in `backend/.env` (never committed). Auth needs `FIREBASE_PROJECT_ID` in `backend/.env` (not secret, but kept out of version control by convention) and the matching `VITE_FIREBASE_*` values in `frontend/.env` (see `frontend/.env.example` for the full list) — neither is required for the app to run anonymously; sign-in just won't work without them.

Harness tests run against the hand-written fixtures (`life`, `majority`, `walker`, plus test-only `slow_burn`), never against generated rules (REQ-15.1).

## Architecture (from the spec — the shape of what gets built)

**Generation pipeline** (`POST /rules/generate`, synchronous, no job queue): Stage A prompt invents a rule from a fixed-size *coverage map* (never a rule list), Stage B implements it, Stage C validates (structure → static AST checks → declaration match → load → trial run at full grid size → reproducibility → one repair attempt). Broken rules and rejections stay in the library as generator-quality data. Prompt templates live in version control as files, and fully rendered prompts are stored per rule.

**Execution model**: a rule is a plugin class with declarations (`KINDS`, `NEIGHBORS`, `REACH`, `USES`, `READS`, `MODIFIERS`, …) and two methods — `make_start` (only place randomness is allowed, via the `Dice` facade) and `step` (strictly deterministic). Generated code runs in a **child process** with memory rlimit and per-tick wall-clock kill, inside a restricted namespace (allowlisted builtins and NumPy surface — this is contract enforcement, **never call it a sandbox**). The harness, not the rule, applies all modifiers (`weight`, `stubbornness`, `rate`) and performs all random draws; grids are parallel numpy arrays, never cell objects. The tick order in REQ-6.4 is part of the spec — changing it changes rule semantics.

**State model** (the subtlest part — read §9.7 before touching run/stop/fingerprint code): the *computational fingerprint* (all future-relevant state: rule-owned + modifier + slot arrays, required derived arrays, scheduler phase when `rate` in scope, RNG state when births declared, exact bytes, floats never quantized) drives stopping (`frozen`/`looping`); the *pattern fingerprint* (`kind` only) is observation only. **Nothing ever stops a run because the picture went quiet** (REQ-9.8.1). Birth draws are skipped when nothing was born, which is what lets stochastic rules reach `frozen`.

**Storage & transport**: runs execute to completion before playback; ticks stored as snapshot every `SNAPSHOT_EVERY` plus sparse/dense deltas, Zstandard-compressed; derived arrays (`age`, `changed_last_tick`) are reconstructed, not stored per tick — except `age` is included in snapshots. Grid payloads use the binary framing in REQ-11.5.1, never nested JSON. The generate endpoint streams `text/event-stream` from a POST, so the frontend must use streaming `fetch()` — `EventSource` cannot POST, and converting to a job model is explicitly forbidden (REQ-11.4.1).

## Destructive commands — hard stop

The user once lost an entire project to an accidental bulk delete. These rules exist so that never happens again.

- **Never run a command that deletes or irreversibly discards files in bulk** — `rm -rf`, `rm` with a glob, `find … -delete`, `git clean`, `git reset --hard`, `git checkout/restore` over `.` or a directory, force pushes, branch deletion — without first listing exactly what will be affected and getting explicit confirmation *in that same message exchange*. A dry run (`git clean -n`, `ls` the glob) comes before the real command, every time.
- This applies **even when the user's own message asks for the deletion**. The whole point is catching accidents: restate what's about to be destroyed and wait for a yes.
- Prefer recoverable moves over deletes: relocate files to the session scratchpad or a `*.bak` path instead of removing them, and let cleanup happen later once nothing is missed.
- Never `rm` anything that isn't committed or pushed. Check `git status` first; uncommitted work is unrecoverable.
- **GitHub is the backup** (`origin` → `github.com/jeremy-pickett/auto-sr`). Push after every commit. If you're one of several instances working concurrently, stage and commit only your own files — never `git add -A` blindly.

## Hard rules that are easy to violate

- **Plain language everywhere** (REQ-0.1): no mathematical jargon in code, property names, UI labels, or docs. Use the plain-English name; mention the standard term once in a comment ("wraps top to bottom" → toroidal).
- Modifier defaults must be identity values — no effect at all (REQ-5.1); every modifier gets a test that default == absent, bit-identical (REQ-15.2).
- User signals (behavior overrides, flags, reruns) never enter Stage A generation context (REQ-8.5, REQ-8.6): coverage counts canonical runs only.
- Additions to the `Dice` surface or the approved builtins/NumPy lists are spec changes requiring new REQ identifiers, not implementation decisions.
- Recorded history is immutable; the only mutating endpoint on runs is `PATCH /runs/{id}` for `user_behavior`/`user_flagged`.
- Every run is stamped with the engine git revision — identical source under different harness revisions is a different experiment (REQ-12.4.2).
- **Version-label fix, apply on sight: "0.3" in documentation means "3.x".** Anywhere a document gives its version as 0.3 (e.g. "SCR-F v0.3"), change it to 3.x when you touch that document. This was a versioning mistake Jeremy made ages ago, not a contract change — it needs no supersede ceremony and no amendment record beyond a one-line note. Historical labels v0.1 and v0.2 stay as they are; they are not retroactively relabeled.
- **Major version numbers denote new products, not this app's evolution.** "3.0" (and any future whole-number bump) means a distinct, ground-up rewrite — never an increment on the current app. This is unrelated to the omnibus requirements spec's own versioning (`asr-requirements-v3.md`, and uplift documents like `frontend-vis-uplift-2.2.1.md` that fold into a future v4) — that numbering tracks the contract, not the product. Don't conflate the two.
