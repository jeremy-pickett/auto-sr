# Reactor — seams and blockages

**Document class:** Level 3 — Requirements, first pass · **Status:** draft
**Path:** `01-core/reactor.md`
**Cites:** SCR-F v0.2 §6, §18, §18.1–§18.5, §38.2, §38.6; F-9, F-20
**Part of a set.** Written together with `cells.md`, `worlds.md`, `plugins.md`, and `runs.md`.

> **What this pass is for.** Finding the seams, not drafting the finished document. It resolves nothing, and where it finds an open decision it states what each answer would cost.

---

## What the Reactor decides

Everything that actually happens.

- Which proposals are admitted, and which are refused.
- The order in which anything is applied.
- Every random draw, and when it is taken.
- What one step means, and what "later" means where later exists.
- Which values a mechanism did not compute but is entitled to read.
- How much time, memory, and effect any participant gets.
- **When the Run stops, and why.**
- What must be captured for the Run to be replayable.
- Its own version identity.

The Reactor is the only component that knows what happened, and it only knows because it ran. That is not a limitation to engineer around. It is the platform's entire premise: where a shortcut existed, nobody would need this component at all.

---

## What it refuses, and who owns it instead

| Refused | Owner |
|---|---|
| What a connection or a property means | Lab |
| Inventing or repairing a mechanism | Generation |
| What the result signifies | Reader, Study |
| Whether the outcome is interesting | a person |

The third row has a boundary that needs drawing, and it is drawn in the wrong place today. See gap 2.

**Hostile conditions are not an exception to any of this.** A Lab studying adversarial behaviour gets its stale observations, its partial visibility, and its timing differences as *declared capabilities of the setting* — never as a loosened contract for the mechanism. A mechanism studying an attacker is not an attacker, and must not be given an attacker's freedoms.

---

## What it needs from its neighbours

- **From the World:** what exists, who may reach whom, what conditions apply, and which execution capabilities are required.
- **From the Plugin:** complete and honest declarations. The contract is only enforceable against what was declared.
- **From the Run:** nothing. The Reactor produces; the Run records.
- **From whoever owns the declaration chain:** a definition of which state is future-relevant. See gap 1 — this is the sharpest thing missing.

---

## Where it hits an open decision

**DEC-2 — replay equivalence.** *The most consequential for this document.*

- *Exact replay to the last value:* the Reactor's version becomes rigid. Any change to how a value is computed — the order of a sum, a change in the underlying numeric library — makes prior Runs unreproducible. In exchange, the strongest possible evidence claim.
- *Replay that honours the contract:* the Reactor can be improved without invalidating history, and "the same Run" now needs a definition that says which differences are acceptable. Somebody has to write that definition, and every argument about whether a Run reproduced becomes an argument about it.

Neither is obviously right, and the choice is not reversible once a large body of evidence exists under one of them.

**DEC-3 — temporal semantics.** Which execution models are offered. The constraint is already fixed and is not negotiable under any answer: replay and determinism hold for every model on offer. A model that cannot be replayed is not one the Reactor may provide.

**DEC-16 — the execution boundary.** Shared with `../02-platform/execution-safety.md`.

**DEC-1 — mechanism composition.** If several mechanisms act in one Run, the Reactor gains ordering and conflict resolution — and whatever it does there *is* a mechanism, one that no one wrote and no one declared.

---

## Where SCR-F is incomplete about it

**1. Nobody owns the definition of future-relevant state, and stopping depends on it.**

A Run stops when nothing further can change, or when the state has been seen before. Deciding that requires knowing exactly which state matters for what comes next — every value that could influence a later step, and no value that could not.

That set is assembled from pieces the Reactor did not author: properties the World declared, values the mechanism declared it writes, whatever the Reactor itself maintains, where any scheduler stands, and the state of the random source when it is still capable of affecting anything. The Reactor must compute a single answer from four other components' declarations, and no document says how, or who is accountable when the answer is wrong.

Getting it wrong is quiet in both directions. Include too little and the platform announces a finished Run that was still moving. Include too much and nothing ever reaches a settled state, because some irrelevant counter keeps ticking.

One inherited detail shows how fine-grained this is. In the earlier system, a random draw was skipped entirely when nothing was born that step — and that skip is precisely what allowed a mechanism using randomness to reach a settled state at all. If the draw had happened anyway, the random source would have advanced every step, the state would never have repeated, and no random mechanism could ever finish. A decision that looks like an optimisation was load-bearing semantics. There are almost certainly others like it, and they are currently in nobody's document.

*This is the largest gap in this document. It reads like an implementation detail and is not one.*

**2. The line between an execution fact and an interpretation is drawn too generously.**

§18.3 permits the Reactor to record "minimal execution facts such as completion or explicit stop conditions," and that is right. But the earlier system's stopping states carry names that sound like conclusions — *settled*, *repeating* — and once a name like that is attached by the component that owns execution, it is very hard for anything downstream to treat it as anything but ground truth.

The honest split: *the state at step 900 is identical to the state at step 850* is an execution fact, produced by comparison, and belongs to the Reactor. *This mechanism is a stable oscillator* is a reading, belongs to a Reader, and should carry a version so it can be disagreed with later.

This matters because of something the platform already knows: a display can go quiet while the state underneath keeps changing. If the Reactor is allowed to publish conclusions, that distinction erodes from the most authoritative end of the system.

**3. What a mechanism is entitled to read but did not compute is unnamed.**

The Reactor maintains values the experiment needs and the mechanism did not produce — how long something has held its state, what changed on the previous step. A mechanism declares it needs them. Nothing says what the available set is, who may extend it, or whether a Lab may add its own. If the set is open, it is a second contract surface nobody is guarding.

**4. Budgets are named for one case and needed for all.**

Effects scheduled for later are to be counted against ordinary per-participant budgets. The phrase implies budgets already exist for everything else. They are not described anywhere.

---

## The shared seam

The Reactor is the third link in the declaration chain, and the only one that must *enforce* it: the World declares, the Plugin declares, the Reactor holds them to it, the Run records the result. Gap 1 above is the chain's most damaging unowned consequence. See `runs.md`.

---

## What the deep pass owes

- The execution contract: admission, ordering, randomness, timing, visibility, limits, stopping, capture.
- Future-relevant state — how it is determined, from whose declarations, and who is accountable.
- The fact-versus-reading line, drawn explicitly, with the stopping vocabulary rewritten to sit on the correct side of it.
- The available derived values, as a closed set with a rule for extending it.
- Budgets, for every kind of effect and not only scheduled ones.
- Version identity, and the rule that the same mechanism under a different Reactor is a different experiment.
