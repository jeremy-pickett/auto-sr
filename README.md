# Autonomous Semantic Ruliology

A single-user, local web app where a language model invents cellular-automaton
rules — Stage A describes one in plain English, Stage B implements it in
Python — and a harness validates it, runs it, and records everything, including
the failures, in a permanent SQLite library. The library is the product: a
growing corpus linking natural-language ideas about local rules to the behavior
those rules actually produce.

Inspired by Stephen Wolfram's work on cellular automata — not a reproduction of
it, and claiming no coverage of any rule space.

**`documents/asr-requirements-v3.md` is the single source of truth.** Every
requirement carries a stable `REQ-` identifier; commits and issues cite those
instead of describing behavior in prose. `documents/architecture.md` records
the implementation decisions and the phase log.

## Running it

Backend (from `backend/`, Python 3.12):

```
.venv/bin/python -m asr.seed                      # seed the reference rules
.venv/bin/python -m uvicorn asr.api.app:app       # serve on :8000
```

Frontend (from `frontend/`, Node 24):

```
npm install
npm run dev        # Vite dev server on :5173, proxying the backend routes
```

The dev server proxies `/rules /runs /catalog /library /system /profile
/comments` to `:8000` and binds `0.0.0.0` — add a proxy entry whenever a new
top-level backend route appears, or it will 404 in dev only.

Sign-in is optional and off by default: the app runs anonymously with every
rule public, exactly as it did before auth existed. To enable it, set
`FIREBASE_PROJECT_ID` in `backend/.env` and the `VITE_FIREBASE_*` values in
`frontend/.env` (see `frontend/.env.example`).

Generation needs `ANTHROPIC_API_KEY` in `backend/.env`. The generator model is
`ANTHROPIC_MODEL` (default `claude-opus-5`); every rule records the model,
prompts, and responses that produced it.

## Tests

```
cd backend && .venv/bin/python -m pytest
```

Harness tests run against the hand-written reference rules (`life`,
`majority`, `walker`, plus the test-only `slow_burn`) — never against
generated rules (REQ-15.1).

## The shape of the system

- **Engine** (`backend/asr/engine/`) — grids are parallel NumPy arrays, never
  cell objects. A rule proposes each next grid; the harness applies every
  modifier gate and performs every random draw in a fixed order, so a run
  replays exactly from its seed.
- **Contract** (`backend/asr/contract/`) — generated code executes in a child
  process (memory limit, per-tick wall-clock kill) inside a restricted
  namespace of allowlisted builtins and NumPy operations. Contract
  enforcement, not a sandbox.
- **Stopping** — a run stops when its *computational* state exactly recurs
  (`frozen`, `looping`), the tick budget runs out, or a tick blows the clock.
  Nothing ever stops a run because the picture went quiet.
- **Storage** (`backend/asr/storage/`) — snapshots plus sparse/dense deltas,
  Zstandard-compressed; derived arrays are reconstructed, not stored.
- **Generation** (`backend/asr/generation/`) — Stage A reasons over a
  fixed-size coverage map (attempts / successes / rejections per cell), never
  a rule list and never user signals. One repair attempt; broken rules stay
  in the library as generator-quality data.
- **Frontend** (`frontend/`) — the dark observatory: canvas playback of stored
  runs, cell inspection, the numbers panel, and a live view of the generation
  pipeline streaming over `fetch()`. Six render styles layer over the default
  view without touching it — including one that lights only the cells computing
  this tick, and one that glows where a cell's kind held still while its hidden
  state kept moving.
- **System page** (`#/system`) — a live pipeline map and a browsable history of
  generation and HTTP sessions. Unauthenticated and globally visible, like the
  rest of this single-user app; it needs an access check before this ever goes
  multi-user.

## Version

**2.2.1** — the product release, the app as deployed. This is a different
series from the requirements spec's `v3` (which numbers the contract, not the
product) and from the uplift documents in `documents/requirements/`. A major
version bump means a new product, not an increment on this one.
`documents/deep-dive/` documents each subsystem at this release, with a
per-release change log in its `README.md`.
