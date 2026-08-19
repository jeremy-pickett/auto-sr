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

## Phase log

- **Phase 0 (2026-08-19):** git repo initialized (provenance needs the
  revision hash, REQ-12.4), pytest installed, package skeleton, settings
  module, this document.
- **Phase 1 (2026-08-19):** engine core — `cells.py`, `geometry.py`,
  `helpers.py`, `dice.py` with tests.
