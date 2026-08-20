# Plugin — seams and blockages

**Document class:** Level 3 — Requirements, first pass · **Status:** draft
**Path:** `01-core/plugins.md`
**Cites:** SCR-F v0.2 §2, §6, §17, §18.5, §20.1; F-2, F-9
**Part of a set.** Written together with `cells.md`, `worlds.md`, `reactor.md`, and `runs.md`.

> **What this pass is for.** Finding the seams, not drafting the finished document. It resolves nothing, and where it finds an open decision it states what each answer would cost.

---

## What the Plugin decides

One thing, narrowly: **given what it is permitted to see, what changes to propose.**

That is the whole of it, and the narrowness is the point. The Plugin is the only component in this set that is written by a machine on demand, which means it is the only one that cannot be trusted by construction. Everything else in the platform is fixed code that a person reviewed. The contract exists because of that asymmetry.

The Plugin also **declares** — what state it reads, what it writes, how far it needs to see, which helpers it uses. Declarations are not decisions; they are promises the Reactor holds it to.

---

## What it refuses, and who owns it instead

| Refused | Owner |
|---|---|
| Randomness of its own | Reactor |
| The order things are applied in | Reactor |
| The clock, and what "later" means | Reactor |
| How fresh its observations are | World declares, Reactor supplies |
| Reaching a Cell it was not given | World, through the Layout |
| When the Run stops | Reactor |
| The record of what happened | Run |
| Any hidden state the experiment does not know about | nobody — it simply may not exist |

The last row is the one that is easy to violate and hard to detect. State the experiment does not know about is state that is not in the fingerprint, which means the Reactor's stopping logic is blind to it, which means a Run can be declared finished while something is still changing.

**Where the Reactor offers a clock beyond simple simultaneous update, the Plugin proposes an effect for later exactly as it proposes anything else.** It names an offset; the Reactor decides what that offset means, when it lands, in what order, and whether the budget allows it. Scheduling is a write. Writes are counted. There is no mechanism-owned clock for the recursion to hide in.

---

## What it needs from its neighbours

- **From the World:** what exists, what may be read, and how far it can see.
- **From the Reactor:** every helper it uses, all randomness, and any derived value it declared a need for.
- **From Generation:** a check, before anything expensive runs, that its declarations match a World that actually exists.

---

## Where it hits an open decision

**DEC-7 — the contract surface.** This record governs this document. Recently amended: it now covers *what capabilities a mechanism may use*, with the choice of notation separated out and pushed down a level.

**DEC-1 — mechanism composition.** *The costliest one for this document.*

- *One mechanism per Run:* the contract stays as it is. Several named Labs cannot be expressed.
- *Several mechanisms:* the contract must gain a whole dimension it does not have. Do they see each other's proposals or only the resulting state? Does one run before another, and if so who decides the order — because whoever decides it has authored a mechanism nobody wrote. What happens when two propose contradictory changes to the same Cell? Every one of those is a semantic decision that changes results, and none of them belongs to a Plugin.

**DEC-3 — temporal semantics.** The proposal shape above is already settled as placement. What an offset means, how finely it can be expressed, and what it costs against a budget are open.

**DEC-18 — direct edits by a person.** A mechanism edited by hand no longer matches the intent recorded against it, and nothing currently updates.

---

## Where SCR-F is incomplete about it

**1. There is no statement of which Worlds a Plugin can act on.**

A mechanism is written against a *kind* of setting, not one specific setting. Nothing in SCR-F says how that kind is expressed, or how a mismatch is caught.

This blocks a named Study pattern outright. Comparing one mechanism across different Worlds requires knowing which Worlds it is entitled to be compared across. Without a compatibility statement, the platform either runs it anywhere and produces meaningless comparisons, or refuses everything but an exact match and makes the pattern useless.

The declaration list in §17 is the raw material — a mechanism that reads three named properties and needs to see one step in four directions has nearly said which Worlds suit it. But "nearly" is doing the work, and nobody has said whether compatibility is derived from declarations or stated separately.

**2. How far a mechanism may see is not decided anywhere, and it is not in the Decision Registry.**

There is a spectrum, and every point on it has a Lab that needs it:

> its immediate neighbours → a bounded distance → a fixed-length jump to somewhere not adjacent → any connection the World declares → everything at once

The third point is where it gets interesting, and a Lab brief already found it independently: wind-blown sand moves in hops that land past the neighbours, and the brief says plainly that this "stretches the definition of a local mechanism in an interesting and honest way." The same shape recurs — embers thrown ahead of a fire front, seeds carried away from a parent, a process that scans rather than spreads. Four named Labs, one unanswered question.

Somewhere on that spectrum the word *local* stops meaning anything, and the platform stops being a local-mechanism instrument and becomes a general simulator with a restrictive vocabulary. Reviewers are asked to hunt exactly this failure. Nothing tells them where the line is.

*Not registered. Should be. This document cannot proceed far without it.*

**3. Declarations are checked by someone, and it is not said who.**

A mechanism declares it reads a property. The World declares which properties exist. Someone compares the two. Generation could, at validation. The Reactor could, at load. Both could, and probably should, for different reasons — but "probably" is not a contract, and a check that two components each assume the other performs is a check nobody performs.

**4. The readability requirement was stated in terms of a language, and has been corrected.**

The requirement that survives is the property: a representation a competent person can read, change, and hand to someone else without the platform's help. *This document may name the notation it chooses — a Level 3 document may. The requirement it satisfies may not be stated in terms of one.* The amendment is recorded in `../00-start-here/glossary.md` and on DEC-7.

---

## The shared seam

The Plugin is the second link in the declaration chain: the World declares what exists, the Plugin declares what it uses, the Reactor enforces the match, the Run records it. Gap 3 above is this document's view of a chain nobody owns. See `runs.md`.

---

## What the deep pass owes

- The declaration set: what a mechanism must state before it may run.
- The permitted capabilities, and the rule that adding one is a contract change rather than a convenience.
- The refusals above as things the platform prevents, with what each violation produces.
- The compatibility statement — how a mechanism says which Worlds it suits.
- Reach, once decided.
- The readability requirement as a property, with the notation named separately and replaceable.
