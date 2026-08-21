# DEC-16 — How do we contain code we didn't write?

*Formal name: security isolation. Cite this record as **DEC-16**.*

**Status:** open; narrowed to the mechanism (2026-08-21) · **Who decides:** the project owner · **Kind:** boundary — the obligations are now requirements; the mechanism waits for a real deployment

> **In one sentence:** every experiment runs code that was written on demand, by a machine, minutes ago — the earlier system contained it with measures sized for one trusted user on one machine, and production needs a boundary sized for strangers.

---

## What this is about

Anyone who has run a network knows the difference between two kinds of protection: the rules that say what *should* happen (policy, permissions, code review) and the walls that hold when the rules fail (segmentation, isolation, blast-radius limits). You need both, and confusing them is how breaches become disasters.

This platform has the first kind in depth, and it is settled law: generated rules operate under a declared contract — restricted operations, checked declarations, memory and time limits, execution in a separate contained process. **We deliberately do not call that a sandbox**, because that word promises the second kind of protection, and an enforced contract is not a wall. It is input validation, done seriously. Every security practitioner knows input validation is not a firewall.

The earlier system could get away with a modest wall because of what it was: one trusted user, one machine, nothing at stake beyond that machine. That assumption is listed in the founding document as *inheritance, not a requirement* — and the moment this platform serves strangers, hosts Labs that model security incidents, or holds data anyone cares about, it's gone.

One principle is already fixed and worth repeating, because the pressure against it will come dressed as a reasonable request: **studying attackers never justifies loosening the contract.** A rule that models an intruder gets its hostile conditions — stale views, timing gaps, partial knowledge — as declared features of the experimental setting. It never gets extra freedom on the actual machine.

## What's open — narrowed by the split of 2026-08-21

This record was split the same way DEC-7 was, by the owner's decision: **the obligations are separated from the mechanism.**

**Obligations — no longer open.** What the boundary must guarantee is requirements work, owned by `../02-platform/execution-safety.md`: the boundary assumes the code it contains is hostile; blast radius is bounded per experiment; the boundary fails closed; limits are recorded in each Run's contract. Writing those does not guess at deployment architecture — it states what any architecture must satisfy.

**Mechanism — still open, and deliberately so.** Which containment technology, on what infrastructure, at what cost per experiment: a deployment-architecture decision, made when the production deployment is real, against facts instead of guesses.

## What this is blocking right now

- `../02-platform/execution-safety.md` cannot be finished without it.
- Any multi-user deployment. The current single-user posture is documented as temporary.

---

## The precise version

*This is the wording other documents cite.*

What production execution boundary replaces the hardened single-user 2.x host assumption. Constrained by SCR-F §18.4 and F-20 (the generated-code boundary is an explicit contract and execution-safety problem; adversarial Labs never justify a permissive execution surface) and `../01-core/reactor.md` REACTOR-7. Owned jointly with `../02-platform/execution-safety.md`.

**A decision here owes:** the alternatives considered; the reasoning in plain language; what evidence would reopen it; the documents to be revised; and a status change recorded rather than assumed.

---

## Record history

**2026-08-21 — narrowed by decision of the project owner.** Split into obligations (requirements, owned by `../02-platform/execution-safety.md`, writable now) and mechanism (open until a production deployment exists). Same move as DEC-7's contract/notation split. The question, identifier, and constraints are otherwise unchanged.

**2026-08-21 — rewritten for readability.** Plain-question format; question, identifier, status, and constraints unchanged. Prior text is in version history.
