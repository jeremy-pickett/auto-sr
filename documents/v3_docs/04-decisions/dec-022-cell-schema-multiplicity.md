# DEC-22 — Must every participant be the same kind of thing?

*Formal name: Cell schema multiplicity. Cite this record as **DEC-22**.*

**Status:** open; lean recorded · **Who decides:** the project owner · **Kind:** boundary — it decides whether three of the four planned world-shapes are honest or nominal

> **In one sentence:** in a terrain experiment every participant really is the same kind of thing — a patch of ground — but in a hospital, or a network, the participants are patients *and* staff *and* rooms *and* equipment, and pretending they're one kind of thing with one list of properties is a lie with consequences.

---

## What this is about

Every participant in an experiment carries a declared list of simple properties. For map-shaped worlds this is naturally uniform: every patch of terrain has fuel, moisture, slope. One kind, one list, done — and the earlier system was built exactly this way.

Now model infection moving through a hospital ward. The participants are patients, staff members, rooms, and shared equipment. A room has an air-handling status; a patient has an infection status; a staff member moves between rooms; equipment gets shared and cleaned. **These are different kinds of things with different properties.** Forcing them into one universal list means every participant carries every property — rooms with vaccination status, patients with air-handling — most of it meaningless, all of it noise.

Same in an identity-security world: accounts, groups, roles, and resources are four kinds of participant. Anyone who administers such systems knows they are not interchangeable.

## Your options

### One kind per world (the inherited answer)
Simple, uniform, trivially checkable. Cost: three of the four planned world-shapes — network, identity, agent — get a bloated everything-list, which is support in name only. The map-shaped worlds stay first-class; everything else limps.

### Several declared kinds per world (the recorded lean)
Each kind gets its own short property list; connections declare which kinds they may join (a *treats* connection joins staff to patients, not rooms to rooms). Honest for every planned world-shape. Cost: checking, storage, measurement, and display all get harder — and there's a slope to police, because "several kinds" must not slide into "arbitrary object structures."

**The guard against that slide is already law and is not up for grabs:** whatever kinds exist, every property is still a simple bounded value — a number, a yes/no, a small fixed set of options. Multiple kinds never becomes freedom of kind.

## What would make this easy to decide

> **Look at the Lab catalog and count.** If the Labs you actually want live mostly on maps, the inherited answer holds a while longer. If they live in hospitals, networks, and org charts — and the catalog's most commercially interesting family (security) certainly does — then several-kinds is the price of admission, and the remaining work is engineering the checks.

## What this is blocking right now

- Honest design of every non-grid Lab.
- `../01-core/worlds.md` WORLD-1 says "of which kinds" and holds the plural open; `../01-core/cells.md` §6 holds both futures.

---

## The precise version

*This is the wording other documents cite.*

Whether one World may declare more than one kind of Cell, each with its own bounded set of properties. Constrained regardless of the answer: the semantic ceiling (`../01-core/cells.md` CELL-5) holds for every schema — a property is a number, a whole number from a declared finite set, or a true/false value; multiplicity of schemas never becomes freedom of kind. Lean recorded, not adopted: several bounded schemas, with connection classes declaring which kinds they may join, and representation staying columnar and bounded rather than becoming a graph of objects.

**A decision here owes:** the alternatives considered; the reasoning in plain language; what evidence would reopen it; the documents to be revised; and a status change recorded rather than assumed.

---

## Record history

**2026-08-21 — rewritten for readability.** Plain-question format; question, identifier, status, and the recorded lean unchanged. Prior text is in version history.
