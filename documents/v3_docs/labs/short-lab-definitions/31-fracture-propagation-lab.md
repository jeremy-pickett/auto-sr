# 31. Fracture Propagation Lab

**Document class:** Lab Knowledge Brief · **Status:** draft
**Catalog:** SCR Lab Catalog v0.1 #31, Family E · **Standing:** ungraded
**Cites:** SCR-F v0.2 §11, §29, §30, §41; F-17
**Fit review (§30):** not performed

---

## The phenomenon

Load a solid and it deforms elastically. Load it further and, somewhere, a crack starts — usually at a flaw. The crack concentrates stress at its own tip, so the material there sees far more load than the average, and the crack extends. Extending sharpens the concentration further.

In a uniform material a crack takes a smooth, predictable path. In a real material — with grains, inclusions, pores, and varying strength — it wanders, branches, and sometimes arrests. Whether a structure fails gradually or shatters, and whether a crack stops at a boundary or runs through it, is decided by that interaction between the crack and the heterogeneity in front of it.

At the population level, the acoustic emissions from micro-cracking before failure come in bursts whose sizes follow a heavy-tailed distribution — the same statistical signature seen in earthquakes and in many other threshold-driven cascade systems.

## What the domain already knows

**Griffith (1921) gave the energy criterion**: a crack grows when the elastic energy released exceeds the energy cost of new surface. That single argument explains why materials are far weaker than their atomic bonds suggest and why strength depends on flaw size rather than on the material alone.

**Linear elastic fracture mechanics is the engineering framework.** The stress intensity factor characterizes the crack-tip field; failure occurs when it reaches a material's fracture toughness. Handbooks tabulate stress intensity solutions for standard geometries, and design codes use them directly. This is a mature, calibrated, closed-form-where-possible discipline.

**Crack path selection has a principle.** In a homogeneous isotropic material a crack propagates so as to keep the tip in pure opening mode — the principle of local symmetry — which determines the path deterministically.

**Statistical lattice models are an established physics tradition.** The **random fuse model** — a lattice of fuses with random thresholds carrying current, burning out one at a time — is the canonical minimal model of disordered fracture, and the **fiber bundle model** is its mean-field cousin. Both produce avalanche statistics and size effects. This literature is decades deep and is genuinely lattice-based.

**Fracture surface roughness has a contested universal exponent.** Measured fracture surfaces are self-affine with an exponent reported near 0.8 across many materials, a result that has been both celebrated as universality and criticized as an artifact of measurement range *(attribution from memory; the controversy is real, the numbers should be verified)*.

## Where the shortcut holds, and where it breaks

**Reducible.** Failure load for a known flaw in a known geometry — LEFM, from handbooks. Crack path in homogeneous material — local symmetry. Weibull statistics of brittle strength — the weakest-link argument, closed form and used industrially. Mean-field avalanche exponents from fiber bundle models. Energy release rates.

**Irreducible.** What heterogeneity does:

- **Path selection through disorder.** Whether a crack deflects around a hard inclusion, penetrates it, or is trapped by it depends on the specific local arrangement and on the crack's own history of deflection. Toughening mechanisms in composites and bone work exactly this way.
- **Arrest and restart.** A crack that stops at a boundary may restart under increased load, or may blunt. Which happens is threshold-crossing on a heterogeneous field.
- **Avalanche sequence.** Which microcrack goes next, and whether the sequence cascades to failure, is a load-redistribution problem on a specific configuration. Mean-field gives exponents; it does not give the event.
- **Branching and fragmentation.** Fast cracks become unstable and branch, and the resulting fragment size distribution is history-dependent.

**The lens, stated plainly — and this Lab's central problem.** **Elasticity is not local.** When a crack extends, the stress field changes *everywhere* in the body, instantaneously in the quasi-static limit. Load redistributes to all remaining material according to a long-range kernel, not to neighbours.

That is why the random fuse model is instructive: it is a lattice model, but each step requires solving a global linear system for the current distribution. The lattice provides the *geometry*; the physics is solved globally. A strictly neighbour-local rule cannot represent stress transfer, and a Lab that pretends otherwise is modelling a fiction — one that will still produce convincing crack-like pictures, which makes it worse.

## What a Cell would carry

A material element: intact or broken state, local strength threshold, accumulated damage, and local stress. Bounded scalars; §13.1 met — the state is not the problem here.

Layout is a grid. The lattice-anisotropy warning applies and is severe: **crack paths on a square lattice prefer lattice directions**, and path geometry is the measurement. The field knows this; random fuse model studies use triangular lattices and other arrangements for exactly this reason.

## Honest strength assessment

*My assessment, not a fit review (§30). It carries no standing and does not promote this entry.*

**Weak, and I would grade it so — for a reason that is structural rather than incidental, and that the catalog already half-names.**

The catalog says "whether a lattice can carry stress honestly is the fit question." My answer is that it cannot, without a global solve at every step — and once there is a global solve at every step, the Plugin is not expressing a local mechanism and the platform's central premise is not being exercised. This is a cleaner failure than most, and it should be recorded as one.

The alternative — a local load-transfer rule where a broken element dumps its load onto neighbours — is exactly what the sandpile does for landslides (#3), and it inherits the same objection: it produces plausible avalanche statistics from unphysical mechanics. Getting the exponents right does not mean getting the physics right, and in a domain where engineers make safety decisions, that gap is dangerous.

**The upside worth being excited about — narrow, and worth stating.** This Lab is the catalog's sharpest instance of a boundary the platform needs to draw explicitly: **mechanisms whose driver is a globally-computed field.** It appears in five other entries — pond water level (#9), coastal shadowing (#5), mycelial flow (#18), power flow (#42), and load transfer (#3) — and nowhere is it as unambiguous as here, because elasticity's non-locality is not an approximation but a theorem.

Writing this Lab honestly gives the fit-review process a worked example of a **defensible rejection**, which SCR-F §30 explicitly says is valuable evidence about the platform's boundary. A catalog whose Labs all pass is not a catalog that has learned anything.

There is one genuinely legitimate narrow use: **as a demonstrator of the failure mode**, showing side by side that a local load-transfer rule and a globally-solved elastic model produce similar avalanche statistics and different crack paths. That is a real, publishable methodological point and it argues for SCR's discipline rather than for its predictive reach.

**The challenges, in order of severity.**

1. **Stress is long-range.** Not an approximation issue; a structural mismatch with the platform's premise.
2. **Convincing pictures from wrong mechanics.** The most dangerous combination in the catalog after Family H.
3. **Safety-critical audience.** Engineers make load-bearing decisions; §30.7 applies at maximum force.
4. **Lattice anisotropy corrupts crack path**, the headline output.
5. **LEFM is a mature, calibrated incumbent** for the questions that get asked.

## Non-claims

This Lab does not predict fracture in any real component, does not bear on structural integrity, design, or safety, and produces nothing suitable for engineering use (§41, §43).
