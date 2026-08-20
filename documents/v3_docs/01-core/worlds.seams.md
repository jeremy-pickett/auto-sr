# World — seams and blockages

**Document class:** Level 3 — Requirements, first pass · **Status:** draft
**Path:** `01-core/worlds.md`
**Cites:** SCR-F v0.2 §14, §15, §18.5, §19, §20.1, §39; F-8
**Part of a set.** Written together with `cells.md`, `plugins.md`, `reactor.md`, and `runs.md`.

> **What this pass is for.** Finding the seams, not drafting the finished document. It resolves nothing, and where it finds an open decision it states what each answer would cost.

---

## What the World decides

The World decides everything about the setting, and nothing about what happens in it.

- **Which Cells exist**, and what properties each carries.
- **How they are arranged** — the Layout, which the World owns outright.
- **Who can reach whom**, and by what kind of connection.
- **What conditions apply** across the setting.
- **What is observable**, and by what.
- **How it starts.**
- **Which execution capabilities it requires** — in particular, whether it needs anything beyond every Cell updating at once.

Layout being a property rather than a sibling is deliberate and worth restating, because it is doing real work. There is no independent Layout to pair wrongly with a World, so an arrangement that contradicts its own setting — distance-based neighbourhoods in a World built on relationships — has no slot to exist in. It is prevented by structure rather than by a rule someone has to remember.

---

## What it refuses, and who owns it instead

| Refused | Owner |
|---|---|
| The mechanism that acts on the setting | Plugin |
| What actually happens, and in what order | Reactor |
| The clock, even where the World asks for a non-simple one | Reactor |
| What a property means | Lab |
| Whether the result is interesting | Reader, Study |

The World may **require** a capability. It may never **provide** one. Requiring delayed observation is a statement about what this experiment needs; supplying delayed observation is execution, and execution has one owner.

---

## What it needs from its neighbours

- **From the Reactor:** an honest answer to "do you offer what I require?", given before a Run starts rather than discovered during one. A World requiring something the Reactor cannot do must fail loudly and early.
- **From the Plugin:** a statement of what kind of World it can act on. See the compatibility gap below.
- **From the Cell:** nothing. The World declares the Cell, not the reverse.
- **From the Run:** version identity. Two Worlds that differ in any declared way are different Worlds, and comparing across them without noticing is a silent error.

---

## Where it hits an open decision

**DEC-1 — mechanism composition.** *This is the decision that most changes this document.* At stake: whether a condition that acts over time — a current, a wind, a drift — is a property of the setting or a second mechanism participating in the Run.

- *If conditions are World properties:* the World gets substantially more complicated. It must express things that change over time, which means it needs its own update rules, which means it is a mechanism wearing a setting's name. The boundary against the Plugin gets blurry exactly where it needs to be sharp.
- *If conditions are mechanisms:* the World stays simple and static — it describes a stage, and everything that moves is a Plugin. But then "hold the World constant and vary the mechanism" no longer means what it sounds like, because the wind is now one of the mechanisms being varied.
- *If composition is refused entirely:* several named Labs cannot be expressed at all. Wind, terrain, and fire are at least two mechanisms; the wildfire brief already records itself as blocked here.

**DEC-8 — World storage.** A representation that suits a lattice will quietly make relational Worlds second-class, and that distortion then spreads into Layout families, measurements, and views without anyone choosing it.

**DEC-3 — temporal semantics.** Which capabilities a World may require is DEC-3's to say. That the World *requires* and the Reactor *owns* is already settled and is not reopened here.

---

## Where SCR-F is incomplete about it

**1. The starting state has two owners, and the conflict is not visible.**

§14 says the World owns what the starting state is. In the earlier system, the mechanism produced the starting state — it was the one place a mechanism was permitted to use randomness. Both readings are present in the material and they cannot both be right.

This is not a tidiness question. One of the named Study patterns holds the World constant and compares mechanisms. If the mechanism generates the start, that comparison is invalid on its face: each mechanism was handed a different starting arrangement, and any difference in outcome could be the start rather than the mechanism. The Study pattern only works if the World owns the start.

The counter-argument is real and should be recorded rather than dismissed. A mechanism often knows things about a sensible starting arrangement that a generic World description does not — which cells should be alive, where a seed belongs, what density makes anything happen at all. Moving start generation to the World means the World must be told those things, by someone, in some form.

A likely shape of the answer, offered as a starting point rather than a resolution: the World owns the starting state, and a mechanism may **propose** one the way it proposes anything else — which the World may adopt, and which is then recorded as part of the World rather than as part of the mechanism. That keeps the comparison honest and keeps the knowledge where it is. It needs a decision, not a paragraph.

**2. There is no statement of when two Worlds are the same World.**

Half the value of a Study rests on holding the World constant, and nothing says what constant means. Same Layout? Same Layout and same conditions? Same starting state? A Repeat Test deliberately varies the starting state while claiming the World is unchanged, which means the starting state is *not* part of World identity — but that is inferred from a Study pattern, not stated anywhere, and inference is how a tree of documents ends up with two definitions.

**3. Four Layout families, one of which has been built.**

Grid, Network, Identity, and Agent are offered as starting families. Only the first has ever been implemented, and the other three are where nearly all the interesting Labs live. Everything this set says about arrangement, reach, and connection is therefore better tested against the lattice than against the cases that matter. That is not a defect in SCR-F; it is a warning about how much confidence any of these five documents has earned.

**4. Observability is listed and never developed.**

§14 includes what is observable in the World's list and says nothing further. Whether a mechanism sees stale values, partial views, or a filtered subset of its neighbours is one of the sharper capabilities the platform could offer, and it is the difference between expressing several named Labs and not. It appears once, as a noun.

---

## The shared seam

The World is the first link in the declaration chain running through this whole set: it declares what exists, the Plugin declares what it uses, the Reactor enforces the match, the Run records the arrangement. Nobody owns the chain. See `runs.md`.

---

## What the deep pass owes

- The World contract: Cells, properties, Layout, connections, conditions, observability, starting state, required capabilities.
- Layout families as concrete arrangements rather than four names, with the three unbuilt ones treated as unproven.
- World identity — what makes two Worlds the same one — resolved and stated.
- How a semantic description of a setting becomes an exact stored World that a person can inspect.
- Explicit refusal of the earlier system's fixed grid and fixed wrapping as anything other than one available Layout.
