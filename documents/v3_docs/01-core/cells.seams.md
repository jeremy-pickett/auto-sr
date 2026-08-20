# Cell — seams and blockages

**Document class:** Level 3 — Requirements, first pass · **Status:** draft
**Path:** `01-core/cells.md`
**Cites:** SCR-F v0.2 §13, §13.1, §14, §15, §30.2, §45.2; F-7
**Part of a set.** Written together with `worlds.md`, `plugins.md`, `reactor.md`, and `runs.md`. Those five are one contract with five names on it, and they only make sense read together.

> **What this pass is for.** Not a short draft of the finished document. Its job is to find the seams — what this component decides, what it refuses, what it needs from its neighbours, and where it runs into a question nobody has answered yet. It resolves nothing. Where it finds an open decision it states what each possible answer would cost, so the decision becomes concrete instead of abstract.

---

## What the Cell decides

Nothing.

This is worth saying first because it is the most useful fact about the component and the easiest to miss. Every other member of this set decides something: the World decides what exists, the Plugin decides what to propose, the Reactor decides what actually happens, the Run decides nothing but records everything. The Cell is not an actor. It has no behaviour of its own. Behaviour belongs to the mechanism; arrangement belongs to the World; order belongs to the Reactor.

What the Cell owns is a **constraint**:

> A Cell's state is a bounded set of simple values, declared in advance.

That constraint is load-bearing in a way that is not obvious. It is what stops the platform from cheating. If a Cell could hold unbounded structure, an embedded program, or open-ended memory, then behaviour that looks emergent could have been carried in the state all along rather than produced by repeated local steps. The ceiling is what makes "this came out of the rule" a claim anyone can check.

**The deep pass owes the numbers.** SCR-F establishes that a ceiling exists and explicitly assigns the actual limits to a requirements document. This is that document.

---

## What it refuses, and who owns it instead

| Refused | Owner |
|---|---|
| Behaviour | Plugin |
| Arrangement, and who can reach whom | World |
| Order of application, and timing | Reactor |
| What any of it means | Lab |
| What the state is worth | Reader |

---

## What it needs from its neighbours

- **From the World:** the declaration of which properties exist and what range each may hold. A Cell does not declare its own shape; it is shaped by the experiment it is part of.
- **From the Reactor:** enforcement. A declared ceiling that nothing checks is a comment.
- **From Generation:** a check that a proposed mechanism's declared reads and writes match properties that actually exist.

---

## Where it hits an open decision

**No registered decision blocks this document.** That is unusual in this set and worth stating plainly, because it means the Cell's own contract can be written now, while four of its neighbours wait.

Two open questions touch it lightly. If more than one mechanism can act in a Run (DEC-1), the Cell's state may need to record which mechanism wrote what, or it may not — that is a provenance question that lands here only if the answer is "several mechanisms, sharing state." And the unregistered reach question described in `plugins.md` affects what a Cell can be affected *by*, not what it holds.

---

## Where SCR-F is incomplete about it

Three gaps, in order of how much trouble they will cause.

**1. Cells are assumed to be all the same shape, and some Worlds cannot honour that.**

§13 describes the Cell as one kind of thing with one declared state. That is true of a grid of terrain patches, where every Cell is a patch. It is false the moment the arrangement stops being a lattice. In a World built on relationships, the participants are not interchangeable: an account, a group, and a permission are three different kinds of thing carrying three different sets of properties, and forcing them into one declared shape means every Cell carries every property and most of them are unused and meaningless.

SCR-F does not say whether a World may declare more than one kind of Cell. Both answers are defensible and they lead to different platforms. One shape is simpler, enforces the ceiling trivially, and quietly makes three of the four named Layout families second-class. Several shapes is honest about what those Worlds are, and makes the ceiling, the declaration match, and every measurement noticeably harder.

*This is the largest gap this document found, and it is not in the Decision Registry.*

**2. The ceiling has no named enforcer.**

§13.1 says the ceiling exists and that a Lab failing it fails its fit review. Fit review happens once, when a Lab is designed, by people. That does not cover a generated mechanism declaring state at load time. Whether the ceiling is checked at Lab design, at mechanism validation, at execution, or at all three is unstated, and "the fit review owns it" is not an answer for anything the fit review never sees.

**3. "Bounded" is not said to be bounded by what.**

Per property, per Cell, per World, or per Run? A ceiling of ten properties per Cell means something very different in a World of four hundred Cells and a World of four million. The deep pass cannot write the numbers without knowing which quantity they are numbers of.

---

## A seam this document shares with the rest of the set

There is a chain running through all five documents that no single component owns:

> The **World** declares what exists → the **Plugin** declares what it uses → the **Reactor** enforces the match and supplies what is needed → the **Run** records the whole arrangement as part of what it binds.

Four components each perform one step of a single process, and no document owns the process itself. The Cell sits at the front of it, since its properties are what everything downstream is declaring against. Every document in this set found the same chain from its own side. See `runs.md` for the collected version.

---

## What the deep pass owes

- The ceiling's exact limits, and the quantity they bound.
- How Cell state is declared, and what a declaration looks like.
- Where the ceiling is enforced, and what a violation produces at each point.
- Whether a World may declare more than one kind of Cell — pending gap 1 above being registered and decided.
- The refusals above, expressed as things the platform prevents rather than things a writer is advised against.
