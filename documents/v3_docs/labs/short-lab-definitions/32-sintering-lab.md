# 32. Sintering Lab

**Document class:** Lab Knowledge Brief · **Status:** draft
**Catalog:** SCR Lab Catalog v0.1 #32, Family E · **Standing:** ungraded
**Cites:** SCR-F v0.2 §11, §29, §30, §41; F-17
**Fit review (§30):** not performed

---

## The phenomenon

Press a powder into a shape and heat it below its melting point. The particles bond where they touch, the bonds thicken into necks, the pores between particles shrink and round off, and the compact densifies — shrinking, sometimes by a fifth of its linear dimension, into a solid body.

This is how most ceramics, many metal parts, and every powder-metallurgy component are made. It is also the consolidation step in metal 3D printing.

The process is driven by surface energy: a powder has enormous surface area, and the system reduces it by eliminating particle surfaces in favour of grain boundaries and then eliminating those. Material moves by diffusion — along surfaces, along grain boundaries, or through the lattice — and which path dominates decides whether the compact densifies or merely coarsens without shrinking.

The failure modes are geometric. Pores that detach from grain boundaries become nearly impossible to remove, leaving permanent porosity. Regions that densify at different rates warp the part.

## What the domain already knows

**Classical sintering theory gives scaling laws.** Two-particle neck growth follows a power law in time whose exponent identifies the dominant diffusion mechanism — different exponents for surface diffusion, grain boundary diffusion, and lattice diffusion. Herring's scaling laws relate sintering rates across particle sizes. Coble's analysis of intermediate and final stage sintering gives densification kinetics. This is a mature, half-century-old body of theory.

**Sintering maps exist.** Ashby-style diagrams identify which mechanism dominates for a given material, particle size, and temperature — a genuine reduced answer to "what is happening."

**Pore–boundary separation is the known failure mechanism and has a criterion.** A pore is dragged along by a moving grain boundary only if the boundary moves slowly enough; past a critical grain growth rate the boundary breaks away and the pore is stranded in a grain interior where its only escape route is slow lattice diffusion. This criterion is classical and it explains why final-stage densification is hard.

**Lattice modelling is established.** Kinetic Monte Carlo and Potts-type models of sintering — closely related to the grain growth models of #30, with added vacancy and pore dynamics — are standard research tools, alongside phase-field and discrete element approaches.

## Where the shortcut holds, and where it breaks

**Reducible.** Neck growth exponent and mechanism identification. Densification kinetics for idealized geometries. Herring scaling across particle sizes. Grain growth during sintering (see #30). The pore–boundary separation criterion. Final density from a given schedule, approximately, via established models.

**Irreducible.** What idealized geometry assumes away:

- **Real packing.** A powder compact is a disordered arrangement of particles with a distribution of sizes and coordination numbers. Which pores close and which survive depends on the specific local packing — a large pore surrounded by many particles is far more stable than the average theory suggests.
- **Differential densification and warping.** If one region densifies faster it pulls on its neighbours, generating stresses that distort the part. Whether a shape survives sintering with its geometry intact is an arrangement-dependent, whole-body question and is a genuine industrial problem, especially in binder-jet and metal-injection-moulded parts.
- **Pore stranding realization.** The criterion says when separation is likely; it does not say which pores strand in a given compact.
- **Coupled grain growth and densification.** These compete: grain growth removes the boundaries that densification needs. The trajectory through that competition depends on history, which is why sintering *schedules* rather than temperatures are the industrial control variable.

**The lens, stated plainly.** Sintering divides much like grain growth (#30): **the mechanism is theoretically well understood, and what remains is the consequence of real disordered geometry.** But there is one important difference. Grain growth's residual questions are academic; sintering's are commercially painful. Warping and residual porosity cost real money in additive manufacturing right now, and neither is predicted well from a schedule.

## What a Cell would carry

A volume element: material or pore state (or a density value), grain orientation label, vacancy concentration, and local curvature or coordination. Bounded scalars; §13.1 met.

Layout is a grid. Two problems, both real.

**Sintering shrinks.** The body's dimensions change by tens of percent, which means the World's geometry is not fixed during the Run. A lattice with a fixed number of sites and fixed spacing cannot represent a body that contracts, unless shrinkage is expressed indirectly through density rather than geometry — which discards exactly the warping question that matters commercially.

**Mass conservation with directed transport.** Material moves from one place to another along specific diffusion paths, and the destination is not always a neighbour — surface diffusion follows the pore surface, which is a connected structure determined by the current state. A neighbour-local rule can approximate this; whether the approximation preserves pore-stranding behaviour is unknown.

## Honest strength assessment

*My assessment, not a fit review (§30). It carries no standing and does not promote this entry.*

**Weak to plausible, and the weakest interesting entry in Family E. I would not build it before #25 or #33.**

The theory is mature. The lattice models exist. The residual questions require representing a shrinking body, which the platform's fixed World does not obviously support. And the catalog's own framing — "the interesting structure is again the void space rather than the material" — while true, is shared with karst (#7) and does not by itself distinguish this Lab.

**The upside worth being excited about.** There is one commercially live thread: **additive manufacturing has revived sintering as an active problem.** Binder jetting and metal injection moulding produce green parts that must be sintered, and predicting the final shape — which requires predicting differential densification and warping — is an unsolved, expensive, current problem. Manufacturers currently handle it by empirical compensation: print a distorted part so it sinters into the right one.

That is a genuine gap, and it is the shape of question SCR could address in the ensemble sense: which local densification rules produce warping that scales with feature size, which do not, and what the negative space looks like. But it requires the shrinking-World problem to be solved first, and that is an architecture question, not a Lab question.

The other honest value is as a **companion to #30**: the two share a mechanism (boundary motion) and a canonical model family (Potts), and pairing them tests whether a mechanism retrieved for one is useful for the other. That is cheap because the second Lab reuses most of the first.

**The challenges, in order of severity.**

1. **The World shrinks.** A fixed lattice cannot represent the geometry change that carries the commercially interesting question.
2. **Mature theory** covering the standard questions.
3. **Diffusion paths follow the pore network**, which the mechanism itself creates — the self-constructed-topology problem from #18.
4. **Established lattice incumbents** in the kinetic Monte Carlo tradition.
5. **Manufacturing credibility hazard** if output resembles a shrinkage prediction (§30.7).

## Non-claims

This Lab does not predict densification, shrinkage, or distortion in any real component, and produces nothing suitable for manufacturing or engineering decisions (§41, §43).
