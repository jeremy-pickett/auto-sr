# Run — seams and blockages

**Document class:** Level 3 — Requirements, first pass · **Status:** draft
**Path:** `01-core/runs.md`
**Cites:** SCR-F v0.2 §7, §10, §19, §24.1, §38.5, §38.6; F-10
**Part of a set.** Written together with `cells.md`, `worlds.md`, `plugins.md`, and `reactor.md`. This document also carries the seam all five found.

> **What this pass is for.** Finding the seams, not drafting the finished document. It resolves nothing, and where it finds an open decision it states what each answer would cost.

---

## What the Run decides

Nothing, at the time it happens. The Run is a record, not an actor.

What it **owns** is more important than what it decides: the Run is the only place where every other component's identity meets. Which mechanism, which setting, which Reactor, which starting state, which random material, which Lab contract, which limits. Nothing else in the platform holds that full set, which makes the Run the one component that can notice when any of it has changed.

And it owns one guarantee: **once complete, it is never edited.** Not corrected, not relabelled, not improved. Later readings may disagree with earlier ones; the thing they disagree about does not move.

There is a design consequence worth keeping deliberately. Because a Run finishes before anyone watches it, playing it back is navigation over a finished record rather than a simulation running alongside a viewer. That is what makes stepping backwards free, makes the same evidence available to a measurement invented years later, and makes two people looking at the same moment actually see the same thing.

---

## What it refuses, and who owns it instead

| Refused | Owner |
|---|---|
| Any claim of robustness, cause, or generality | Study |
| Measurement | Reader |
| What it means | a person, and Readers, separately |
| Its own correction | nobody — corrections attach, they do not overwrite |

**A failed Run is a Run.** The platform distinguishes seven ways to have no result, and the reason is the information. A mechanism refused at the door, a Run that could not finish, and a Run that finished without producing the behaviour someone hoped for are three different findings and must not collapse into one word.

---

## What it needs from its neighbours

- **From the Reactor:** the history, the stopping fact, and its own version.
- **From the World and the Plugin:** version identity precise enough that a later reader can tell whether two Runs are comparable.
- **From whoever owns replay:** a standard. Without one, "this Run is reproducible" has no meaning to test.

---

## Where it hits an open decision

**DEC-2 — replay equivalence.** *This document cannot be finished without it,* because it determines what a Run must store. Exact replay demands enough to reconstruct every value; contract-honouring replay demands enough to reconstruct whatever the contract names, and something must define that. The choice sets storage volume, Reactor version discipline, and how strongly any evidence claim may be worded.

**DEC-1 — mechanism composition.** If several mechanisms participate, the Run binds several, and its provenance has to say which one proposed what — otherwise the record shows what changed and not who changed it.

**DEC-19 — live work.** If anything is ever watched while running, provisional observations need to be visibly provisional. The failure is quiet: an observation that was never marked provisional becomes evidence by default, and nobody notices the moment it happens.

---

## Where SCR-F is incomplete about it

**1. The declaration match is not among the things a Run binds.**

§19 lists mechanism, setting, Reactor, starting conditions, random material, Lab contract, and limits. It does not list the agreed set of declarations — which properties this mechanism was permitted to read and write in this setting.

That agreement is the actual contract the Run executed under. It is implied by the versions of its parts, but only if nothing about the matching process ever changes. The day the check itself is revised, every prior Run becomes ambiguous about what it was allowed to do, and the record does not say.

**2. The stopping reason arrives already interpreted.**

Covered from the other side in `reactor.md`. From the Run's side the concern is narrower and worse: whatever the Reactor called it, the Run stores permanently and immutably. A reading that turns out to be wrong can be superseded. A reading recorded inside immutable evidence cannot.

The rule that follows: **the Run stores the fact and not the name.** *State at step 900 matched state at step 850* is a fact. *Repeating* is a name, and names belong to versioned readings.

**3. What makes two Runs comparable is not stated.**

Every Study pattern rests on comparability, and the platform never defines it. Same Reactor version, or a compatible one? Same World, and by which definition of same — `worlds.md` finds that undefined too. This will be settled in practice by whoever writes the comparison code first, which is the worst possible way for it to be settled.

**4. Nothing is said about the cost of getting the answer.**

How many steps a Run took to reach its stopping point is recorded incidentally, if at all, and treated as an operational statistic. It is better than that. Where a shortcut exists, the answer is cheap; where none does, the answer costs exactly as much computation as it costs. Steps-to-outcome is therefore a rough, honest, already-available measure of how hard the question actually was — and the platform's whole claim is about questions that are hard in that specific way. It costs nothing to keep and nobody has asked for it.

---

## The seam all five documents found

Each of the five approached this from its own side and arrived at the same missing thing.

> The **World** declares what exists. The **Plugin** declares what it uses. The **Reactor** enforces the match and supplies what was promised. The **Run** records the whole arrangement as part of what it binds.

Four components perform four steps of one process, and no document owns the process. What follows is not hypothetical; each of these is a gap already recorded above or in one of the other four:

- Nobody is named as performing the match, so both Generation and the Reactor may each assume the other does it (`plugins.md`, gap 3).
- Nobody owns the set of values a mechanism may read but did not compute, so the set is open and unguarded (`reactor.md`, gap 3).
- Nobody assembles the definition of future-relevant state, though stopping every Run depends on it (`reactor.md`, gap 1).
- Nobody records the agreed declarations, so the contract a Run ran under is inferred rather than stored (gap 1 above).
- Nobody says whether a World may declare more than one kind of Cell, which decides what "the declarations" can even express (`cells.md`, gap 1).

Five holes, one shape. This may be a component nobody has named, or a responsibility that belongs to one of the existing five and has never been assigned. **This pass does not decide which.** It records that the shape is real, that it was found five times independently, and that it is not in the Decision Registry.

---

## What the deep pass owes

- What a Run binds, including the agreed declarations.
- What it records, and what reconstruction from that record guarantees — pending DEC-2.
- Immutability as something the platform enforces, not a convention writers observe.
- The seven failure classes as distinct recorded outcomes, all retained.
- Comparability, defined.
- Steps-to-outcome kept deliberately, as evidence about the question rather than a statistic about the machine.
