# Documentation ideas worth keeping

**Status:** working notes · **Date:** 2026-08-20
**Context:** brainstorm toward SCR 3.x documentation, prompted by the "What a Cell would carry" section of `documents/v3_docs/labs/short-lab-definitions/04-dune-and-ripple-lab.md`
**Cites:** SCR-F v0.2 §13.1, §25.3, §30, §41–43, §45.12; F-7, F-17

---

## The move that section makes

"What a Cell would carry" is where the brief stops describing sand and asks what the *domain forces the abstraction to hold* — and then lets the domain push back. Directional asymmetry is "a real requirement rather than a preference." The hop "stretches the definition of a local mechanism in an interesting and honest way." That's a Lab testing the platform instead of the platform absorbing the Lab, and it's the same instinct behind §30's "Labs should be allowed to fail these reviews."

---

## The load-bearing reframe

Both briefs independently arrived at the same sentence, in slightly different words:

> **Computational irreducibility is not a property of a domain. It is a property of a regime.**

That is the platform's whole value proposition, and it's currently nowhere in SCR-F. Stated plainly: **if a shortcut exists, SCR is worthless there.** Rothermel gives steady spread in homogeneous fuel; Bagnold gives transport rate; ripple wavelength has a linear-stability answer. In all of those SCR is laboriously rediscovering closed forms. SCR earns its keep only where the shortcut has broken — near percolation thresholds, in dune collisions, in path-dependent burnout ordering.

The dune brief calls the failure mode by name: **rediscovery, not discovery.** If SCR produces barchans, the honest reading is "the platform works," not "we learned about sand."

---

## What irreducibility means at each tentpole

| Component | The irreducibility angle |
|---|---|
| **Cell** | The §13.1 ceiling is an *irreducibility guarantee*, not just tidiness. Unbounded state lets you smuggle the answer into the cell — emergence you didn't actually compute. |
| **World** | Reducibility is partly a Layout property. Near a percolation threshold you must run it; far from it, mean-field works. A World should record where it sits relative to known critical points. |
| **Generation** | Should be biased *toward* the irreducible. A generator that keeps producing rules with closed-form behavior is burning money. |
| **Plugin** | Readability is the anti-shortcut guarantee — you can see whether it iterates or looks up an answer. A Plugin calling a closed-form solver is a shortcut wearing a mechanism's clothes. |
| **Reactor** | The only component permitted to know the outcome, and it only knows by having run. Determinism is what makes irreducibility *measurable* rather than confusable with noise. |
| **Run** | The receipt for work that could not be skipped. Ticks-to-outcome is an unused measurement of what the answer cost. |
| **Study** | **A Study is an admission of irreducibility.** If you could compute the answer you wouldn't run twenty starts. |
| **Reader** | A Reader is a *discovered pocket of reducibility* — a compression of a whole history into a fact. |
| **Corpus** | Not a shortcut around irreducibility — **amortization** of it. "We can't predict it, but we already ran it." |
| **Search** | What irreducibility forces you into. You can't derive the rule that branches, so you retrieve one that did. |
| **Visualization** | The eye is a Reader with no version number — and the one instrument that finds structure no analytic method does. Also the one that can *manufacture* apparent reducibility. |
| **Lab** | Owns the reducibility audit for its domain. Currently doing it by instinct in two briefs, mandated nowhere. |

---

## The five ideas I'd actually pursue

**1. The five properties that make it "cellular" — and which four 3.x is already negotiating away.**

A CA is: discrete cells · bounded local state · one uniform rule everywhere · simultaneous update · local interaction. Line them up against the registry:

- discrete cells, bounded state → §13.1, decided
- **uniform rule everywhere → DEC-1** (multiple Plugins = a non-uniform rule)
- **simultaneous update → DEC-3**
- **local interaction → not registered anywhere**

Four of five are in play and nobody has written that down. §45.12 asks reviewers to hunt over-generalization; this is the checklist that hunt needs. It also gives an honest answer to "when does SCR stop being ruliology and become a generic simulator" — when you've spent all five.

**2. The reach question is a missing DEC.**

The dune brief found it: a saltation hop is *non-local by design*. And then it noticed the shape generalizes — wildfire spotting, ecological dispersal, scanning worms. There's a spectrum: nearest neighbor → bounded reach → fixed-length hop → arbitrary graph edge → global broadcast. Somewhere on it, "local mechanism" stops meaning anything. That line is undrawn and consequential — it constrains the Plugin contract, every Layout family, and at least four Labs. Strongest DEC candidate I've seen so far.

**3. Readers as a catalog of discovered shortcuts.**

If a Reader reliably says "traveler, speed 2, period 4," it has found a pocket where the system *is* predictable. Where a Reader stops working is the boundary of that pocket — and that boundary is a **research finding**, not a QA note. This inverts how Reader coverage gets treated: "this Reader works on 60% of runs" currently reads as a weakness; it should read as a map.

**4. Studies as an empirical irreducibility instrument.**

The Small-Change Test is already a direct probe: flip one cell, watch whether divergence is bounded or total. §25.3's ambient sensitivity is the other half — and it's currently framed defensively, as deception-avoidance. It's better than that. **Uniform sensitivity across a sample of comparable changes is a measurement of the system's irreducibility**, producible cheaply, from evidence you already have. §25.3 even says "uniform sensitivity is itself the finding" — it just doesn't say what the finding *is*.

**5. The claim SCR should refuse to make.**

Wolfram's Principle of Computational Equivalence says most non-trivial systems are equivalently sophisticated. If SCR leans on that, it loses the ability to say some Labs fit better than others — everything's equally irreducible, so nothing is distinctive. SCR should take the **weaker, more defensible claim**: what predicts fit isn't computational class, it's whether *adjacency in the model corresponds to adjacency in the world*. The wildfire brief already states this as the selection rule. Making the refusal explicit costs nothing and inoculates the platform against its most tempting overreach.

---

## Where this lands as documentation

Three shapes, roughly in order of leverage:

- **A tenth §30 question — the reducibility audit.** §30 asks about domain fit, world fit, mechanism fit, time, evidence, accuracy, failure boundaries, comparison to tools, transfer limits. None asks *"where does this domain already have a formula?"* §30.8 is adjacent but not the same — the established tool might be another simulation. Two briefs invented this question independently; that's the signal it belongs in the platform. Amending §30 is an SCR-F amendment, so it's a DEC-shaped move, not an edit.
- **A Level 1 document on irreducibility and what "cellular" means** — idea 1 and idea 5, in `00-start-here/`. It's the missing intellectual spine: the tree currently explains what the components are and never explains why local mechanisms are the right instrument at all.
- **Two new DEC records** — the reach question, and possibly Reader-coverage-as-finding.
