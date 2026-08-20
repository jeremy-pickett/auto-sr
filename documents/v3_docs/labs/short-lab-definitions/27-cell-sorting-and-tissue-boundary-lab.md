# 27. Cell Sorting and Tissue Boundary Lab

**Document class:** Lab Knowledge Brief · **Status:** draft
**Catalog:** SCR Lab Catalog v0.1 #27, Family D · **Standing:** ungraded
**Cites:** SCR-F v0.2 §11, §29, §30, §41; F-17
**Fit review (§30):** not performed

---

## The phenomenon

Take two tissues from an early embryo, dissociate them into individual cells, mix them together, and let them sit. They do not stay mixed. The cells sort themselves — one type gathers into a ball, the other surrounds it, and a sharp boundary forms between them. The final arrangement often reproduces the layered organization the cells had in the embryo.

Nothing directs this. No cell knows where it is supposed to end up. The sorting comes from cells preferring to stick to some neighbours more than others, plus enough random motion to let them rearrange.

The same mechanism keeps tissue boundaries sharp during development. Compartment boundaries in the fly wing and vertebrate hindbrain stay crisp for hours despite cells dividing and jostling, because cells of different types adhere differently and pull the interface taut.

## What the domain already knows

**Steinberg's differential adhesion hypothesis (from the early 1960s) is the classical answer and it is essentially a thermodynamic argument.** Treat the cell populations as immiscible liquids with surface tensions set by adhesion strength. The final configuration is the one that minimizes total interfacial energy, and the ordering of which tissue engulfs which is transitive and predictable from measured tensions *(attribution from memory, verify)*. Steinberg's group later measured tissue surface tensions directly and found the predicted ordering.

That is a strong reducible result and it needs to be stated first, because it constrains what this Lab can claim.

**The Glazier–Graner cellular Potts model (1992) is the canonical lattice implementation** — cells as domains of lattice sites, an energy functional with adhesion terms and a volume constraint, updated by Metropolis dynamics *(attribution from memory, verify)*. It reproduces sorting, engulfment, and boundary sharpening, and it is now one of the most widely used frameworks in computational developmental biology. This is the incumbent and it is a lattice model.

**Adhesion is not the whole story.** Later work established that cortical tension and active cell contractility contribute at least as much as adhesion to interfacial tension, and that boundary sharpness in some systems depends on active mechanisms (Eph/ephrin repulsion, actomyosin cables) rather than passive differential adhesion. The field has moved on from a purely adhesive account.

## Where the shortcut holds, and where it breaks

**Reducible — and this is the Lab's central problem.** The *outcome* of sorting is predictable from an equilibrium argument. Which tissue ends up inside, whether they sort completely or form partial mixtures, and the ordering across multiple tissue types all follow from the surface tension hierarchy without running anything. Steinberg's contribution was precisely to show that the answer is thermodynamic.

So the endpoint is a shortcut, and a good one.

**Irreducible.** What is left is the kinetics and the failures:

- **Whether sorting completes, and how long it takes.** Reaching the minimum-energy configuration requires cells to rearrange, and rearrangement can be slow or blocked. Real aggregates get stuck in configurations that are not the global minimum, and whether they do depends on the initial arrangement and the amount of motion available.
- **Coarsening dynamics.** Small clusters merge into larger ones over time with a characteristic growth law, and the exponent depends on the mechanism of rearrangement. This is a genuine dynamic question with no equilibrium answer.
- **Boundary maintenance under division.** Cells divide, which injects disorder continuously. Whether a boundary stays sharp is a competition between disordering and sharpening rates — a dynamic balance, not a minimum.
- **Active versus passive boundaries.** When active repulsion contributes, the system is no longer minimizing a passive energy, and equilibrium arguments do not apply at all.

**The lens, stated plainly.** This is the catalog's cleanest example of a domain where **the equilibrium is reducible and only the path to it is not.** That is a much weaker position than a domain where the outcome itself is unpredictable, and it should be stated up front rather than discovered by a reviewer. A Lab here can honestly study kinetics, trapping, and the effects of continuous division — but it cannot claim to predict sorting outcomes, because thermodynamics already does.

## What a Cell would carry

A site: cell type identity, adhesion parameters to each other type, and possibly a motility or contractility value. Very small; §13.1 met trivially.

There is a representational subtlety worth naming. In the cellular Potts tradition, **one biological cell occupies many lattice sites**, which is what allows cells to change shape and to have a meaningful surface. A one-cell-per-site lattice cannot represent cell shape, and shape is part of the mechanism — interfacial tension is a property of a surface, and a surface needs geometry. Whether SCR's Cell can carry this at all is a real mechanism-fit question (§30.3), and the honest answer may be that the platform's Cell and the domain's cell are at different scales.

## Honest strength assessment

*My assessment, not a fit review (§30). It carries no standing and does not promote this entry.*

**Weak as a research Lab, and I would grade it so. Worth building only for a specific structural reason.**

The case against is strong and I do not want to soften it. The outcome is predicted by a sixty-year-old thermodynamic argument. The canonical model is already a lattice model, widely used, well understood, with an established community. The mechanism requires representing cell shape, which needs many sites per cell, which is a different Cell contract than SCR appears to have. And the biology has moved past the pure adhesion account that a simple local rule would express.

**What is nonetheless valuable here.** Two things, both about the platform rather than the domain.

First, this is the catalog's best worked example of a **reducible-endpoint domain**, and having one is useful. Most Labs have irreducible outcomes and reducible margins; this one is the reverse. Writing it honestly gives the fit-review process a calibration case for "the answer is already known and only the journey is open," which is a verdict the review needs to be capable of reaching.

Second, the **many-sites-per-cell** question is a genuine architectural probe. If SCR cannot represent an entity that occupies a variable region of the World and has a surface, that is a real boundary on the Cell abstraction (§13, §13.1) — and it is the same boundary that would block any Lab needing deformable objects. Better to discover it here, on a domain where nothing is lost, than in a Lab that matters.

**The upside worth being excited about.** Modest and honest: the **kinetic trapping** question is real and under-studied. Aggregates that fail to sort are usually treated as experimental noise; whether particular local rules make trapping likely, and whether trapped configurations are reproducible, is a legitimate question that an ensemble instrument answers naturally. Hanging-drop aggregate experiments are cheap and quantitative, so it is checkable.

**The challenges, in order of severity.**

1. **The outcome is already predicted** by differential adhesion thermodynamics.
2. **Cells need shape**, which needs many sites per cell — possibly outside the platform's Cell contract.
3. **The canonical model is already a lattice model** with a large user base.
4. **The biology has moved on** from passive adhesion to active contractility.
5. **Timescale is hours**, which is convenient, and the only thing in this Lab's favour operationally.

## Non-claims

This Lab does not model development in any organism, makes no claim about tissue biology, and produces nothing suitable for biological or medical conclusions without domain validation (§41, §43).
