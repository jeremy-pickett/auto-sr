# Execution safety

**Document class:** Level 3 — Requirements · **Status:** draft
**Path:** `02-platform/execution-safety.md`
**Identifier namespace:** `SAFE-` — reserved to this document. Identifiers are permanent and never reused.
**Cites:** SCR-F v0.2 §18.4, §33, §39; F-20 · DEC-16 (narrowed 2026-08-21) · `../01-core/plugins.md`, `../01-core/reactor.md`, `../01-core/generation.md`
**Standing constraint (§33):** Platform Services support the conceptual platform and must not define its scientific assumptions accidentally.

> Every experiment here executes code that was written on demand, usually by a machine, minutes before it runs. This document owns the wall that holds when everything else about that code goes wrong.

---

## 1. Two protections, never confused

Anyone who runs systems for a living keeps two kinds of protection apart: the rules that say what *should* happen — permissions, review, checked inputs — and the walls that hold when the rules fail. Both are necessary. Confusing them is how incidents become disasters.

**SAFE-1.** The platform maintains both, and never represents one as the other:

- **The contract** — declarations checked at admission, restricted operations, per-step limits — says what a mechanism *may* do. It is specified in `../01-core/plugins.md` and enforced by the execution authority.
- **The boundary** — this document — is what contains the mechanism when the contract fails: a defect in enforcement, an operation nobody anticipated, a hostile construction that passes every check.

**SAFE-2.** The contract is never called a *sandbox* — in interfaces, documents, or code. That word promises a security boundary, and an enforced contract is not one; it is input checking done seriously, and every security practitioner knows input checking is not a firewall (`../00-start-here/language-rules.md`). The boundary in this document is the thing entitled to security vocabulary, and only once DEC-16's mechanism is chosen and shown to earn it.

---

## 2. The assumption

**SAFE-3.** The boundary assumes the code it contains is **hostile** — regardless of who or what wrote it, what checks it passed, or how many times it has run before. Machine-written, human-edited, Lab-shipped: one assumption for all (PLUGIN-5).

This is not pessimism about any author. It is the only assumption that doesn't rot: every other trust basis — "generation checked it," "a person reviewed it," "it ran fine yesterday" — decays quietly, and a boundary built on a decayed assumption is a boundary that was never tested until the day it mattered.

---

## 3. The obligations

These are the requirements the DEC-16 split made writable: what any containment mechanism must satisfy, stated without choosing one. Four of them are the oldest established principles in protection design — least privilege, fail-safe defaults, complete mediation, economy of mechanism — applied to this platform's specific shape.[^ss]

**SAFE-4. Bounded blast radius.** One experiment's misbehaviour cannot affect another experiment, the platform's own code or records, or the host beyond that experiment's recorded allocation. The worst case for any single Run is the loss of that Run.

**SAFE-5. Fail closed.** On any containment doubt — a limit tripped, an operation that should be impossible, a boundary error — the experiment stops and the stop is recorded as an execution fact, distinguishable from every other stopping fact (REACTOR-6 discipline). No experiment continues optimistically past a boundary event.

**SAFE-6. Nothing ambient.** Contained code holds exactly what was handed to it, and nothing by virtue of where it runs: no reachable filesystem beyond its allocation, no network, no clock authority, no view of the platform, no other experiment. This is the same authority-by-possession discipline the contract already applies to reach (PLUGIN-8), applied one layer down.

**SAFE-7. Everything mediated.** Every interaction between contained code and the platform crosses one checked interface. There is no second path — no shared memory reached around the interface, no side door for performance that bypasses the checks.

**SAFE-8. Limits enforced from outside.** Memory, wall-clock time, and effect budgets are imposed by the containing side and recorded in the Run Contract. Contained code cannot raise, suspend, or observe its way around its own limits.

**SAFE-9. Small enough to review.** The boundary's own machinery stays small and inspectable. A containment layer too complex to review is a contract wearing a wall's costume.

**SAFE-10. Boundary events are evidence when they touched evidence.** A containment event that affected an experiment's outcome is an execution fact in that Run's permanent record. One that affected nothing is operational telemetry (`observability.md`). The line is: did it touch evidence?

---

## 4. No exceptions for interesting subjects

**SAFE-11.** No Lab, subject, or research purpose relaxes the boundary. A mechanism modelling an attacker receives its hostile conditions — stale views, timing gaps, partial knowledge — as declared features of the experimental setting (WORLD-11, REACTOR-7), never as freedom on the actual machine.

This is restated here, third document and counting, because the pressure against it will arrive dressed as a reasonable request from a legitimate Lab, one case at a time. F-20's answer does not change with the quality of the argument.

**SAFE-12.** Generation's checks are preflight, never boundary (GEN-8). A mechanism that passed every check still runs contained. The checks reduce how often the wall is tested; they are not the wall.

---

## 5. What remains open, and what the earlier system proves

**DEC-16, narrowed:** the containment mechanism — which isolation technology, on what infrastructure, at what per-experiment cost — is decided when a production deployment exists, against facts instead of guesses.

**SAFE-13.** The earlier system's posture is recorded as evidence, not requirement (§39): one trusted user, one hardened host, generated code in a separate contained process with memory and time limits, inside a restricted operation set. Adequate for what it was; listed as inheritance the moment the platform serves anyone else. Any multi-user deployment waits on DEC-16's mechanism — that gate is deliberate.

---

## Sources

[^ss]: Jerome H. Saltzer and Michael D. Schroeder, "The Protection of Information in Computer Systems," *Proceedings of the IEEE* 63, no. 9 (September 1975): 1278–1308. The named principles — least privilege, fail-safe defaults, complete mediation, economy of mechanism — are among the paper's eight design principles.

Bibliographic details were checked against published sources rather than recalled (`../00-start-here/language-rules.md`).
