# 1. Wildfire Lab

**Document class:** Lab Knowledge Brief · **Status:** draft
**Catalog:** SCR Lab Catalog v0.1 #1, Family A · **Standing:** [strong] (inherited, not re-derived)
**Cites:** SCR-F v0.2 §11, §29, §30, §41; F-17
**Fit review (§30):** not performed

---

## The phenomenon

Fire moves across terrain as a front. Fuel ignites, burns, is consumed; heat passes to adjacent material by radiation and convection; wind and slope bias which neighbours receive it. At landscape scale this produces front shape, rate of spread, fingering, patchy unburnt islands, self-extinction, and spotting — embers lofted ahead of the front to start new fires across unburnt ground. None of this is written into any single ignition.

## What the domain already knows

Wildfire is the most heavily modelled domain in this catalog, and a Lab here must know the incumbents before it opens its mouth.

**Rothermel (1972)** gives a semi-empirical steady-state rate of spread from fuel bed properties, moisture, wind, and slope. It is a *closed-form shortcut*: no simulation required. **Huygens-style wavelet propagation** (the FARSITE lineage) grows a fire perimeter by treating each point as the source of an elliptical wavelet whose size comes from Rothermel. Operational fire behaviour analysis largely runs on this stack. Fuel moisture is not one number: dead fuels are tracked in 1-hour, 10-hour, 100-hour, and 1000-hour timelag classes with different response rates, and the difference between them is often what decides whether a fire runs.

**Lattice models have their own lineage.** The Drossel–Schwabl forest-fire model (1992) is a canonical self-organized-criticality toy producing power-law fire-size distributions; percolation-theoretic fire spread predicts a critical fuel density below which fire cannot cross the landscape at all. Both are established physics, not novelties.

## Where the shortcut holds, and where it breaks

This is the section that decides whether the Lab is worth building.

**Reducible.** Steady spread through homogeneous fuel under steady wind on uniform slope has a formula. Whether a fire percolates through random fuel at density *p* is a phase-transition question with known critical behaviour. Mean fire-size distributions over long horizons are statistical-mechanical results. In all three regimes SCR would be laboriously rediscovering closed forms — and would be *checked against them*, which is useful as calibration and worthless as contribution.

**Irreducible.** The shortcut degrades exactly where fire behaviour analysts say it does:

- **Heterogeneity near the percolation threshold.** Away from critical fuel density, mean-field arguments work. Near it, whether the fire crosses depends on the specific arrangement of fuel, and the only way to know is to run it. Real landscapes are near-critical constantly — that is what fuel breaks are for.
- **Feedback onto the driving field.** Plume-dominated fires modify the wind that drives them; junction fires (two fronts merging) accelerate far beyond what either front's spread rate predicts; canyon eruptions and fire whirls are coupled-system behaviour. The Rothermel–Huygens stack assumes the wind field is an input, not an output.
- **Spotting.** A firebrand lofted a kilometre ahead is not a local interaction. It is the domain's own honest statement that fire is not purely local, and how the Lab handles it — long-range connection, stochastic seeding, or an admitted boundary — is the single most informative thing about SCR's abstraction.
- **Path dependence in burnout.** Which islands survive unburnt depends on the order in which the front arrived at their edges. That ordering has no closed form.

**The lens, stated plainly.** Computational irreducibility is not a property of wildfire; it is a property of *particular regimes* of wildfire. This Lab's job is to know which regime it is in. Producing a beautiful front in the reducible regime is a demo. Producing a candidate mechanism in the irreducible regime is the product.

## What a Cell would carry

Terrain patch: remaining fuel, moisture, slope, burn state, accumulated heat. All bounded scalars — this Lab clears the §13.1 ceiling easily. The honest difficulty is not state complexity but *meaning*: one `moisture` scalar standing in for four timelag classes is a collapse the fit review must defend or reject.

One mechanism worth naming because it generalizes: fuel that is drying under neighbour heat but has not ignited is computationally live and visually inert. A view keyed to burn state alone shows nothing happening. This is SCR-F §38.6 appearing as a domain fact rather than a platform curiosity, and wildfire is the cleanest place in the catalog to demonstrate it.

## Honest strength assessment

*My assessment, not a fit review (§30). It carries no standing and does not promote this entry.*

**Strong, and strong for a specific reason: this is the only Lab in Family A that can be graded rather than admired.** Documented fire perimeters exist (MTBS, incident perimeter archives). Experimental burns exist. Operational model outputs exist to compare against. A wildfire mechanism that reproduces a known perimeter's fingering under known wind is checkable in a way that almost nothing else in this catalog is.

That makes it the platform's **calibration anchor**: the Lab whose purpose is partly to prove SCR's evidence chain works at all, on a domain where being wrong is detectable.

**The upside worth being excited about.** Fire science has a long-standing gap between fast operational models that assume the wind field and expensive coupled fire–atmosphere simulations that nobody runs at scale. SCR sits in neither place; it could supply *candidate local rules for the regimes where the fast models are known to fail* — junction acceleration, near-critical crossing, spotting-driven jumps — cheaply, in bulk, with the failures retained. "Here are forty local mechanisms that produce junction-fire acceleration, eleven mechanism families that never did, and the runs for all of them" is a thing no fire ecologist can currently get.

**The challenges, in order of severity.**

1. **Anisotropy artifact.** Eight-neighbour spread on a square lattice produces octagonal fronts. The field has documented correction factors for discrete direction sets; a Lab that does not know this will render lattice geometry and its viewers will read it as wind.
2. **Step duration is unresolved and dimensional claims depend on it.** Flame-front dynamics live in minutes; incidents live in days. Rate of spread in cells-per-step has no defensible translation to metres-per-hour until this is settled (§30.4, DEC-3).
3. **The picture is too persuasive.** A rendered fire spreading across terrain will be read as a forecast regardless of caption. This is the sharpest §30.7 risk in Family A.
4. **Wind, terrain, and fire are at least two mechanisms.** Blocked on DEC-1.

## Non-claims

This Lab does not forecast fire behaviour, does not predict any real fire, and produces nothing suitable for operational or safety decisions. Established fire modelling is calibrated and this is not; the plausible complementary position is mechanism supply upstream of calibration, and it is untested (§41, §43).
