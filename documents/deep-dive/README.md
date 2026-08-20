# ASR Deep-Dive Series

Six subsystem-level technical deep-dives on Autonomous Semantic Ruliology (ASR), written for upload
as knowledge files into a Claude.ai Project. Each is self-contained — real code quoted with
`file:line` citations, `REQ-` identifiers cited from `documents/asr-requirements-v3.md` for
rationale, no repo access assumed on the reader's side.

| # | Document | Covers |
|---|---|---|
| 1 | [`01-engine-internals.md`](01-engine-internals.md) | State model, geometry, bound helpers, the `Dice` facade, tick order, computational vs. pattern fingerprints, the run loop, the classifier. Includes a hand-traced tick of `life`. |
| 2 | [`02-storage-and-transport.md`](02-storage-and-transport.md) | SQLite schema/WAL, immutability, tick encoding (snapshot/sparse/dense), reconstruction + cache, REQ-11.5.1 binary framing, engine revision stamping. Includes a case study on the zstandard thread-safety incident fixed this session. |
| 3 | [`03-contract-and-sandboxing.md`](03-contract-and-sandboxing.md) | The restricted namespace, the full Stage C validation pipeline (structure → static AST → declaration match → load → trial run → reproducibility → repair), the child-process runner (rlimit, wall-clock kill), what happens to rejections. |
| 4 | [`04-generation-pipeline.md`](04-generation-pipeline.md) | The coverage map, Stage A/B prompt construction, user-signal exclusion (REQ-8.5/8.6), gating, the `claude-opus-5` default and its refusal-fallback behavior. Includes a real coverage map and rendered prompt pulled from `library.db`. |
| 5 | [`05-api-and-auth.md`](05-api-and-auth.md) | Full route inventory, the SSE-over-POST streaming design (REQ-11.4.1), the `PATCH /runs/{id}` immutability boundary, Firebase Auth Phase 1 (Email/Password, personal library, Stage A exclusion). |
| 6 | [`06-frontend.md`](06-frontend.md) | App structure, the dark-observatory design system, the run player's binary-framing → canvas pipeline, the Invent view's SSE consumption, library browsing/pagination, Firebase sign-in. Includes case studies on clipboard copy, robust downloads, and a nav-highlight bug fix. |

## Published Artifacts

1. Engine internals — https://claude.ai/code/artifact/8c42c7ce-7bf2-4acd-b254-d8adec29ec87
2. Storage & transport — https://claude.ai/code/artifact/7f1a1018-e2d6-4c8c-865d-a3fba75e9db4
3. Contract & sandboxing — https://claude.ai/code/artifact/b55911a4-d01d-4263-89eb-bbb23046dbb8
4. Generation pipeline — https://claude.ai/code/artifact/1b3b096e-cdc3-4158-8975-596fb39c5792
5. API & auth — https://claude.ai/code/artifact/c14a6367-b051-4ec7-a927-a87533592f86
6. Frontend — https://claude.ai/code/artifact/58980105-e322-4f0f-8e81-45ebe963b646
