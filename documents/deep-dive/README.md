# ASR Deep-Dive Series

**Release 2.2.1** — documented as of 2026-08-20.

Six subsystem-level technical deep-dives on Autonomous Semantic Ruliology (ASR), written for upload
as knowledge files into a Claude.ai Project. Each is self-contained — real code quoted with
`file:line` citations, `REQ-` identifiers cited from `documents/asr-requirements-v3.md` for
rationale, no repo access assumed on the reader's side.

Every document carries a version banner naming the release it describes and what changed in that
subsystem for that release. A document marked **unchanged** for a release was re-verified against
the source at that release, not merely left alone.

## Versioning, and what "2.2.1" refers to

**2.2.1 is the product release** — the deployed application as it stands. It is not the same
number as, and does not track, either of the other two version series in this repository:

| Series | Example | What it numbers |
|---|---|---|
| **Product release** | **2.2.1** | The deployed app. What this series documents. |
| Omnibus requirements | `asr-requirements-v3.md` (v3, folding to v4) | The requirements *contract*. `REQ-` identifiers live here. |
| Uplift proposals | `frontend-vis-uplift-2.2.1.md` (uplift 2.2) | Proposed spec additions, numbered independently of the omnibus. |

The product release and the uplift document happen to share the digits `2.2.1` because this
release shipped that uplift's §8; the two numbering schemes are still independent and will
diverge. Per `CLAUDE.md`, a **major** version bump denotes a new product (a ground-up rewrite),
not an increment on this app.

## The documents

| # | Document | Covers | 2.2.1 |
|---|---|---|---|
| 1 | [`01-engine-internals.md`](01-engine-internals.md) | State model, geometry, bound helpers, the `Dice` facade, tick order, computational vs. pattern fingerprints, the run loop, the classifier. Includes a hand-traced tick of `life`. | unchanged |
| 2 | [`02-storage-and-transport.md`](02-storage-and-transport.md) | SQLite schema/WAL, immutability, tick encoding (snapshot/sparse/dense), reconstruction + cache, REQ-11.5.1 binary framing, engine revision stamping. Includes a case study on the zstandard thread-safety incident. | **updated** — three session tables and the history/telemetry boundary |
| 3 | [`03-contract-and-sandboxing.md`](03-contract-and-sandboxing.md) | The restricted namespace, the full Stage C validation pipeline (structure → static AST → declaration match → load → trial run → reproducibility → repair), the child-process runner (rlimit, wall-clock kill), what happens to rejections. | unchanged |
| 4 | [`04-generation-pipeline.md`](04-generation-pipeline.md) | The coverage map, Stage A/B prompt construction, user-signal exclusion (REQ-8.5/8.6), gating, the `claude-opus-5` default and its refusal-fallback behavior. Includes a real coverage map and rendered prompt pulled from `library.db`. | **updated** — the `emit()` instrumentation wrapper |
| 5 | [`05-api-and-auth.md`](05-api-and-auth.md) | Full route inventory, the SSE-over-POST streaming design (REQ-11.4.1), the `PATCH /runs/{id}` immutability boundary, Firebase Auth Phase 1, the system routes, and the session-tracking middleware. | **updated** — `/system/*`, `try_resolve_uid`, `track_request` |
| 6 | [`06-frontend.md`](06-frontend.md) | App structure, the dark-observatory design system, the run player's binary-framing → canvas pipeline and its six render styles, the Invent view's SSE consumption, library browsing, Firebase sign-in, the System view. | **updated** — render styles, System view, palette, dev proxy |

## Release log

### 2.2.1 — 2026-08-20

Two feature families landed on top of the 2.2.0 baseline the series was first written against.

**Observability — the system page.** A live pipeline/process-map dashboard at `#/system`, backed
by `GET /system/status` and `GET /system/sessions` (`backend/asr/api/system.py`), over two new
tables: `generation_sessions` (one row per `POST /rules/generate`) and `http_sessions` (one row
per session cookie, touched by middleware on every request). A first attempt at presence — an
`app_sessions` table fed by a client heartbeat — was built, hit repeated client-side bugs, and was
replaced wholesale by the cookie-plus-middleware design; its table is left in the schema, unused.
Covered in documents 2 (tables), 4 (the `emit()` wrapper that fills `generation_sessions`), 5
(routes, middleware, `try_resolve_uid`), and 6 (the view).

**Visualization — uplift 2.2's §8 render styles.** `activity` (REQ-13.17), `kind-stable`
(REQ-13.18), a rebuilt `trails` (REQ-13.19) and a real gradient/normal/light `relief`
(REQ-13.20), plus a replaced kind palette. Covered in document 6.

Not in this release: the recurrent-structure detector (REQ-19.x, §4–7 of the same uplift). It is
specified but unstarted, and no document in this series describes it as existing.

### 2.2.0 — 2026-08-20

The baseline this series was originally written against: all seven build phases, Firebase
Authentication Phase 1, comments, profiles, favorites, slugs, RSS, preview images, and the
zstandard thread-safety fix documented as a case study in document 2.

## Published Artifacts

These were published from the 2.2.0 text and **have not been redeployed for 2.2.1**. Republishing
each from its updated file — same URL, via the Artifact tool's update flow — is the remaining step
to bring the Claude Project knowledge base in line with this directory.

1. Engine internals — https://claude.ai/code/artifact/8c42c7ce-7bf2-4acd-b254-d8adec29ec87
2. Storage & transport — https://claude.ai/code/artifact/7f1a1018-e2d6-4c8c-865d-a3fba75e9db4
3. Contract & sandboxing — https://claude.ai/code/artifact/b55911a4-d01d-4263-89eb-bbb23046dbb8
4. Generation pipeline — https://claude.ai/code/artifact/1b3b096e-cdc3-4158-8975-596fb39c5792
5. API & auth — https://claude.ai/code/artifact/c14a6367-b051-4ec7-a927-a87533592f86
6. Frontend — https://claude.ai/code/artifact/58980105-e322-4f0f-8e81-45ebe963b646
