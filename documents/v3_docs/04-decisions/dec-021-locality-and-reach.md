# DEC-21 — Locality and reach

**Document class:** Level 2 — Architecture Decision · **Status:** open; leading formulation recorded
**Registered by:** the core contract set, 2026-08-20 (`../01-core/`), following external critique
**Decision:** not made

> **No document may resolve this locally (SCR-F v0.2 F-22, §36.6).** A downstream writer who needs an answer here cites the fork; it does not pick a side. Naming a fork is not deciding it (§40). Resolution requires this record to be decided and adopted, and adoption is a human act (§36.3).

---

## The question

What a mechanism is entitled to observe and affect — and therefore where the word *local* stops meaning anything and the platform stops being a local-mechanism instrument.

## Why it is consequential

*Local* is the platform's identity, and on a lattice it can be expressed as a distance. In a World built on trust relationships, distance is not defined; a rule stated in distances is either meaningless there or is silently reimposing a grid.

Four intended Labs need effects that are not nearest-neighbour: an ember thrown ahead of a fire front, a grain of sand landing past its neighbours, a seed carried away from its parent, a process that scans rather than spreads. A Lab brief found this independently and said plainly that it "stretches the definition of a local mechanism in an interesting and honest way."

SCR-F §45.12 asks reviewers to hunt over-generalisation — where the platform becomes a generic simulator rather than remaining recognisably a local-mechanism instrument. Nothing currently tells them where the line is.

## What is already constrained

**A leading formulation is recorded in `../01-core/plugins.md` §3 (PLUGIN-8, PLUGIN-9), stated so this decision can be made against something concrete rather than in the abstract.** It is not adopted.

Its move is to treat reach as a question of *authority* rather than distance: a mechanism may observe or affect a Cell only by traversing connections the World declared and the Run Contract admitted, and long-range effects are expressed as declared transport connections rather than as unrestricted addressing. The dangerous endpoint on that reading is not a long jump but *"this mechanism may touch Cell N because it knows N exists"* — which breaks locality at any distance.

The formulation has a well-developed ancestry in capability-based protection (Dennis and Van Horn, 1966; Hardy, 1988), cited in that document.

What remains genuinely open: whether declared transport connections are a legitimate expression of locality or a loophole that empties the word; whether reach limits are per-Plugin, per-World, or both; and whether any bound on path length is required beyond the World's declaration.

## What this record constrains

- `../01-core/plugins.md`
- `../01-core/worlds.md`
- `../01-core/reactor.md`
- several Lab papers

## What a decision here owes

- the alternatives actually considered, not only the one chosen;
- the reasoning, in plain language (F-5);
- the reconsideration trigger — what evidence would reopen this (§36.1, Level 2);
- the documents that must be revised when it lands;
- a status change from *open* to *decided*, recorded rather than assumed.
