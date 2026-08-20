# World

**Document class:** Level 3 — Requirements · **Status:** draft
**Path:** `01-core/worlds.md`
**Identifier namespace:** `WORLD-` — reserved to this document. Identifiers are permanent and never reused.
**Cites:** SCR-F v0.2 §14, §15, §18.5, §19, §20.1, §39; F-8 · DEC-1, DEC-3, DEC-8, DEC-21, DEC-22, DEC-23
**Supersedes:** the first-pass seam document, preserved at `worlds.seams.md`.
**Part of the core contract set:** `cells.md`, `plugins.md`, `reactor.md`, `runs.md`.

> A **World** is the complete setting for an experiment. It decides everything about the setting and nothing about what happens in it.

---

## 1. What the World owns

**WORLD-1.** A World declares, in advance and completely: which Cells exist and of which kinds; how they are arranged; which connections are possible and between which kinds; which conditions apply; what each participant is permitted to observe; which external inputs feed the experiment; and which execution capabilities it requires.

**WORLD-2.** The **Layout** — how Cells are arranged and which local interactions are possible — is a property of the World, never a separable thing paired with it.

That subordination does real work. There is no independent Layout to combine wrongly with a World, so an arrangement that contradicts its own setting — geometric distance governing a World built on trust relationships — has no slot in which to exist. It is prevented by structure rather than by a rule someone must remember.

**WORLD-3.** A World may **require** an execution capability. It may never **provide** one. Requiring delayed observation is a statement about what this experiment needs; supplying it is execution, and execution has exactly one owner (`reactor.md`).

---

## 2. What the World refuses

| Refused | Owner |
|---|---|
| Any mechanism that acts on the setting | Plugin |
| What actually happens, and in what order | Reactor |
| The clock, including where the World requires an unusual one | Reactor |
| The realized starting values | Starting State (§4) |
| What a property or connection means | Lab |
| Whether the outcome is interesting | Reader, Study |

---

## 3. What the World requires

- **From the Reactor:** an honest answer to *"do you supply what I require?"*, given at admission and never discovered mid-Run.
- **From the Plugin:** a statement of what it needs, so mechanical compatibility can be decided rather than assumed (`plugins.md` §5).
- **From the Run Contract:** permanent record of the World as it actually stood, so no later reader has to reconstruct it from whatever the platform does now.

---

## 4. What the World produces

A declared, inspectable setting — and, deliberately, **not** the values it starts with.

### 4.1 World and Starting State are separate inputs

SCR-F §14 places the starting state inside the World. The earlier system had the mechanism generate it, in the one place a mechanism was permitted to use randomness. Both readings are present in the material, they contradict each other, and the contradiction is not cosmetic.

One of the platform's own Study patterns holds the World constant and compares mechanisms. If each mechanism generates its own start, that comparison is invalid on its face: every mechanism was handed a different arrangement, and any difference in outcome could be the start rather than the mechanism.

The resolution adopted here separates the two rather than choosing between them:

> **WORLD-4.** The **World** is the durable setting: Cell kinds and schemas, Layout, connections, static conditions, observation rules, declared external inputs, and required capabilities.
>
> **WORLD-5.** The **Starting State** is the realized set of opening values for one Run or one family of Runs. It is a separate input to a Run, recorded separately in the Run Contract.

This makes an ordinary sentence mean what it sounds like. *Hold the World constant and vary the Starting State* is exactly what a Repeat Test wants, and it is now expressible without equivocation. *Hold the World and Starting State constant and vary the mechanism* is a valid Plugin Comparison, and it is now checkable.

**WORLD-6.** A Plugin or a Lab may supply a **start recipe** — a described procedure for producing a valid Starting State. A recipe is not a Starting State. The realized values are produced under the Reactor's controlled randomness, recorded exactly, and bound to the Run alongside the recipe that generated them.

This keeps the knowledge where it lives. A mechanism often does know what a sensible opening arrangement looks like, and WORLD-6 lets it say so without owning the result. It also improves the record: a random start is no longer "seed 1234" but the exact realized values *and* the recipe and seed that produced them.

**Status.** DEC-23 owns this. The requirements above state the leading candidate and its consequences so the decision can be made against something concrete; they are not an adopted resolution.

---

## 5. External inputs and reactive mechanisms

Whether a wind, a current, or a drift belongs to the setting or is a second mechanism has been carrying more weight than it can hold. The useful cut is not *what kind of thing is it* but *what does its future depend on*:

> **WORLD-7.** An **external input** is a value or schedule, declared in advance, whose future values do not depend on the simulated state. It belongs to the World.
>
> **WORLD-8.** Anything whose future behaviour depends on the simulated state is a **mechanism**. It is not part of the World, whatever it is named.

A recorded wind field played back over time, a fixed tide schedule, a planned maintenance window, a scheduled credential expiry — all inputs. Fire altering the airflow that drives it, fish depleting a resource that then redirects the fish, a defender reacting to an observed compromise — all mechanisms.

The test is mechanical, which is the point: read the definition and ask whether the simulated state appears in it. This does not decide DEC-1, and it is not offered as a decision. It removes the easy half of DEC-1 from the argument so the hard half can be argued on its own.

**WORLD-9.** An external input's position — how far through its schedule the Run has advanced — is future-relevant state (`reactor.md` §4).

---

## 6. Three kinds of state

Observation appears once in SCR-F, as a noun in a list, and several intended Labs depend entirely on it. Three things are routinely conflated and must not be:

> **WORLD-10.** **World State** — what is actually true in the experiment at a given step.
>
> **WORLD-11.** **Seen State** — what a particular participant or mechanism is permitted to observe at that step. It may be partial, delayed, filtered, or dependent on connection or role. It is declared by the World and supplied by the Reactor.
>
> **WORLD-12.** **Recorded State** — what is captured as evidence. It is complete enough to replay the Run and to serve measurements invented later, and it is never limited to what any participant could see.

**WORLD-13.** A mechanism reads Seen State and only Seen State. It has no access to World State except through what the World permitted it to see.

This is what lets the platform express stale identity data, delayed telemetry, partial knowledge, and hidden state honestly — modelled as declared properties of the setting rather than as a mechanism given extra freedoms. A mechanism studying an adversary is not an adversary, and never receives an adversary's access.

---

## 7. Layout families, and how much they have been tested

Four families are named: arrangements by position, by communication or reachability, by trust and membership relationships, and by messages and shared resources among acting participants.

**WORLD-14.** A Layout declares which connections are possible and between which Cell kinds. A connection is a *declared possibility of local interaction*, not a distance.

**Only the first family has ever been built.** Everything this document says about arrangement, connection, and reach is better tested against a lattice than against the three families where most intended Labs live. That is a statement about how much confidence these requirements have earned, and it should travel with them.

### 7.1 A concrete warning about representation

The earlier system gained real speed from fixed grid-shaped parallel arrays. That is an excellent representation for a lattice and a poor one for a relational World, and adopting it by default would make three families second-class while appearing to support them.

The specific hazard is representing connections as *number of Cells × maximum connections per Cell*. That is efficient only when every Cell has roughly the same number of connections. Real relational systems do not: connection counts in large networks commonly follow a power-law distribution, with a small number of extremely well-connected hubs.[^ba] Identity systems have exactly this shape — identity providers, large groups, shared service accounts, routing nodes. A fixed-width representation sized for the hubs wastes almost all of its space, and one sized for the median cannot hold them.

**WORLD-15.** A World's representation may not assume near-uniform connection counts unless the World family guarantees it. DEC-8 owns the choice; this requirement constrains it.

---

## 8. World identity

**WORLD-16.** Two Worlds are the same World when their **execution identity** matches: Cell kinds and schemas, Layout, connections, conditions, observation rules, external inputs, and required capabilities. Descriptive material that cannot affect execution — names, notes, authorship, presentation preferences — is provenance and does not distinguish two Worlds.

**WORLD-17.** A World's execution identity is recorded in the Run Contract. Whether two Runs may be *compared* is not settled by this requirement; comparison is a question a Study asks, and a Study defines what must match for its own question (`runs.md` §6).

---

## 9. Open decisions

- **DEC-23 — Starting State ownership.** §4 states the leading candidate; the decision is not made.
- **DEC-1 — Mechanism composition.** §5 removes external inputs from its scope. What remains is genuinely hard and untouched.
- **DEC-8 — World storage.** Constrained by WORLD-15.
- **DEC-22 — Cell schema multiplicity.** Determines whether WORLD-1's "of which kinds" is plural in practice.
- **DEC-3 — Temporal semantics.** Which capabilities a World may require.
- **DEC-21 — Locality and reach.** What a declared connection entitles a mechanism to do.

---

## Amendment record

**2026-08-20 — first-pass seam document replaced by this requirements document.** The seam pass is preserved unchanged at `worlds.seams.md`.

Changed as a result of external critique (`../critiques/SCR_Core_Starter_Docs_Critique_v0.1.md`):

- *Starting State separated from World* (§4). The seams pass found the conflict and proposed that the World adopt a mechanism's proposal. The critique offered a cleaner third option — World and Starting State as separate inputs — which makes Repeat Test and Plugin Comparison both expressible without equivocation. Adopted as the leading candidate under DEC-23. WORLD-4 to WORLD-6 are new.
- *External input versus reactive mechanism* (§5). New, from the critique. Removes the easy half of DEC-1 from dispute. WORLD-7 to WORLD-9 are new.
- *Three kinds of state* (§6). New, from the critique. The seams pass noted only that observation "appears once, as a noun." WORLD-10 to WORLD-13 are new.
- *World identity relaxed* (§8). The seams pass said two Worlds differing in any declared way are different Worlds. The critique correctly called this too strict: descriptive material that cannot affect execution should not distinguish them. WORLD-16 corrects it.
- *Representation warning made concrete* (§7.1), with a real citation replacing a general caution.

Unchanged: Layout as a property rather than a sibling; the "everything about the setting, nothing about what happens in it" boundary; the warning that three of four Layout families are untested.

---

## Sources

[^ba]: Albert-László Barabási and Réka Albert, "Emergence of Scaling in Random Networks," *Science* 286, no. 5439 (October 15, 1999): 509–512.

Bibliographic details were checked against published sources rather than recalled (`../00-start-here/language-rules.md`).
