# 26. Immune Response Lab

**Document class:** Lab Knowledge Brief · **Status:** draft
**Catalog:** SCR Lab Catalog v0.1 #26, Family D · **Standing:** ungraded
**Cites:** SCR-F v0.2 §11, §29, §30, §41; F-17
**Fit review (§30):** not performed

---

## The phenomenon

An infection begins locally. Tissue-resident cells detect it and release signals; those signals recruit circulating immune cells to the site; the recruited cells kill infected cells and release more signals. If it works, the pathogen is cleared and the signals subside.

When it does not work, the response organizes into a structure instead. A **granuloma** is a ball of immune cells walled around a pathogen the body cannot eliminate — the characteristic lesion of tuberculosis. It is a containment, not a cure: the pathogen persists inside, sometimes for decades, and can escape if the structure breaks down. Roughly a quarter of the world's population is estimated to carry latent tuberculosis in this state.

The granuloma is a genuinely emergent object. Nobody designs it; it arises from cells following local rules about where to move, what to secrete, and when to kill.

## What the domain already knows

**Within-host dynamics have a reduced form.** Target-cell-limited ODE models — susceptible cells, infected cells, free pathogen, effector cells — are the standard framework, and they give clearance criteria, peak viral load timing, and the basic reproductive number within a host. This is well-established immunological modelling and it works for systemic, well-mixed infections.

**Granuloma modelling is explicitly agent-based, and has been for twenty years.** Kirschner, Segovia-Juárez, and colleagues built spatial agent-based models of tuberculosis granuloma formation in the mid-2000s, with macrophages, T cells, bacteria, and diffusing chemokines on a grid, and used them to ask which local rules produce containment versus dissemination *(attribution from memory, verify)*. This is the incumbent, it is the same class of model, and it is well funded.

**Immunology's central difficulty is not the mechanism, it is the parameters.** Rates of recruitment, killing efficiency, and cytokine diffusion in vivo are poorly measured and vary enormously between individuals. Models are typically calibrated loosely and used qualitatively.

## Where the shortcut holds, and where it breaks

**Reducible.** Clearance versus persistence in a well-mixed within-host model. Peak load timing. Threshold effector-cell density for control. Bulk cytokine concentration at steady state. Basic competition between pathogen replication and immune killing.

**Irreducible.** What space adds, which in this domain is a lot:

- **Containment as a geometric outcome.** A granuloma works because of its structure — a killing zone surrounding a protected core. Whether that structure forms, and whether it holds, depends on the arrangement and timing of cell arrivals. A well-mixed model cannot represent containment at all; it can only represent clearance or failure.
- **Sanctuary by geometry.** Pathogen inside a granuloma survives partly because immune cells and drugs penetrate poorly. That is the same spatial-refuge mechanism as tumour hypoxia (#23) and biofilm interiors (#25), and it is why tuberculosis treatment takes months.
- **Recruitment feedback.** Signals attract cells which release signals. This is short-range activation with a delay, and it can produce oscillation, overshoot, and self-sustaining inflammation with no pathogen left — which is the mechanism of a class of immunopathology.
- **Tipping between control and dissemination.** Granulomas can fail. Whether a specific one does depends on accumulated local state and is history-dependent.

**The lens, stated plainly.** This Lab has a strong argument on structure and a fatal weakness on validation, and the two must be stated together. **The emergent object — the granuloma — is exactly the kind of thing local rules produce and mean-field models cannot express.** But the parameters that would decide which local rules are right are largely unmeasured, and the observations available are endpoint histology: a slice through a lesion at the moment of death or biopsy, not a time course.

So the irreducible content is real and the ability to check any of it is very poor. That combination is the worst case for §30.6.

## What a Cell would carry

A tissue site: occupancy by cell type (uninfected, infected, macrophage, effector, dead), pathogen load, local signal concentrations, and activation or exhaustion state. Bounded if cell types stay a small enumerated set; §13.1 met with that qualification.

**The Layout question is genuinely awkward, and the catalog names it: "Cells here are literal cells, which is either clarifying or a trap."** It is mostly a trap. An SCR Cell is a fixed location; an immune cell *moves*. Representing motile cells as lattice occupancy that hops between sites is standard practice in the incumbent models, but it means the World's Cells are locations and the domain's cells are contents — a distinction that is easy to state and easy to lose, and losing it produces confused vocabulary in exactly the way SCR-F §5 warns about.

There is a second problem: **circulating cells arrive from outside the World.** Recruitment is an inflow from a vasculature that is not modelled. That is a boundary condition, not a local mechanism, and it is the dominant control on the outcome.

## Honest strength assessment

*My assessment, not a fit review (§30). It carries no standing and does not promote this entry.*

**Weak to plausible. I would place it below the rest of Family D, and I would not build it early.**

The mechanism argument is good and the emergent structure is real. Everything else is against it. The incumbent is the same kind of model with two decades of domain expertise behind it. The parameters are unmeasured. The observations are static snapshots of a dynamic process. The dominant driver — recruitment from circulation — sits outside the abstraction. And the vocabulary collision between "cell" as a lattice site and "cell" as an immune cell is a standing hazard for a platform whose central principle is that meaning stays visible.

**The upside worth being excited about — and it is narrow but real.** The **spatial sanctuary** question connects this Lab to #23 and #25, and in all three the mechanism is the same: a population survives treatment because of where it is, not what it is. If SCR can show that one family of local rules produces treatment-tolerant refuges across tumours, biofilms, and granulomas, that is a genuinely interesting cross-domain observation, and it is the kind of thing a corpus indexed by mechanism rather than by field is uniquely able to notice.

The granuloma itself is also a good demonstration object for a different reason: it is a case where **the picture and the state diverge in a clinically consequential way.** A stable-looking granuloma with live bacteria inside is the definition of latent infection. A view keyed to visible structure shows containment; a view keyed to pathogen load shows a reservoir. SCR-F §38.6 with a billion-person consequence attached.

**The challenges, in order of severity.**

1. **Validation is close to unavailable.** Endpoint histology cannot check a time course.
2. **Parameters are unmeasured** and individually variable, so calibration is out of reach.
3. **Recruitment comes from outside the World**, and it dominates.
4. **Motile agents versus fixed Cells** — a Layout mismatch and a vocabulary trap (§5).
5. **Established agent-based incumbent** doing the same thing with domain expertise.
6. **Medical credibility hazard**, as throughout Family D.

## Non-claims

This Lab does not model immunity in any organism, does not bear on infection, vaccination, or treatment, and produces nothing suitable for any medical decision (§41, §43).
