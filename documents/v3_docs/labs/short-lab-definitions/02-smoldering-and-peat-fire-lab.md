# 2. Smoldering and Peat Fire Lab

**Document class:** Lab Knowledge Brief · **Status:** draft
**Catalog:** SCR Lab Catalog v0.1 #2, Family A · **Standing:** ungraded
**Cites:** SCR-F v0.2 §11, §29, §30, §38.6, §41; F-17
**Fit review (§30):** not performed

---

## The phenomenon

Smoldering is flameless combustion on the surface of a porous fuel. It is slow — centimetres per hour rather than metres per minute — oxygen-limited, and it burns *downward and sideways through the ground*. Peat, coal seams, duff layers, and organic soils sustain it for months or years. The Centralia, Pennsylvania coal seam fire has burned since 1962. Indonesian peat fires released, by widely-cited estimates, carbon on the scale of a large industrial economy's annual emissions during the 1997 event.

Two properties make it strange. It can survive conditions that extinguish flame — rain, snow, winter — and re-emerge months later; boreal "overwintering" or zombie fires do exactly this. And it is invisible: the surface can look extinguished, cool, and green while the front advances a metre below.

## What the domain already knows

Smoldering combustion is a small, well-defined field; the modern peat work is associated with Guillermo Rein and colleagues at Imperial College *(attribution from memory, verify)*. The physics is a heat balance: exothermic oxidation of char against conduction, radiation, and the enormous latent heat cost of evaporating water in the fuel. Everything turns on **moisture content**, expressed as a fraction of dry mass, and peat can hold several times its own dry weight in water. There is a critical moisture above which smoldering cannot sustain, and it is high — a few hundred percent dry mass is in the plausible range, but the exact figure is fuel-specific and I would not assert one.

Inorganic content matters too: mineral fraction acts as a heat sink, and heavily mineral peat resists ignition. Bulk density controls both oxygen supply and thermal inertia, and the dependence is non-monotone — too loose and heat escapes, too dense and oxygen cannot reach the char.

Lattice modelling here is thin. This is not a domain with a canonical CA the way traffic or grain growth is, which cuts both ways: less risk of rediscovery, less precedent to lean on.

## Where the shortcut holds, and where it breaks

**Reducible.** One-dimensional steady smolder front velocity through homogeneous fuel is well characterized by laboratory correlation and by reaction-front analysis. Whether a given fuel *can* smolder at a given moisture and density is a threshold question with an experimental answer. Total carbon released given burn depth and area is arithmetic. Nothing in that list needs a simulation.

**Irreducible.** The interesting behaviour is all three-dimensional and all heterogeneous:

- **Path selection through variable moisture.** Peat deposits are not uniform. The front advances where it can and stalls where it cannot, and the resulting burn geometry is a percolation-like search through a heterogeneous field. Which route it takes depends on the specific arrangement, and there is no shortcut short of following it.
- **Re-emergence far from origin.** A front that travels laterally underground and resurfaces kilometres away is the same computation continuing, not a new event. Predicting *where* requires knowing the subsurface path, which requires running it.
- **Overwintering.** Survival through a season is a marginal heat-balance question integrated over months of hostile conditions. Small differences in insulating snow cover, depth, or local density decide it.
- **Coupling back to hydrology.** Burning away peat lowers the surface, changes drainage, and dries adjacent material. Fuel and moisture are not fixed inputs; they are outputs.

**The lens, stated plainly.** This Lab's whole claim rests on one distinction the platform already owns: **a quiet picture is not a stopped computation** (SCR-F §38.6). In wildfire that principle is a caveat. Here it is the phenomenon. A surface rendering keyed to visible burning shows an extinguished landscape while the state evolves underneath — and the domain's real, costly, recurring mistake is exactly that misreading, made by people declaring fires out.

## What a Cell would carry

A subsurface volume element rather than a surface patch, which is itself a modelling commitment worth stating. Candidate bounded scalars: organic mass remaining, moisture fraction, mineral fraction, temperature or accumulated heat, oxygen availability, combustion state. All primitive and bounded; the §13.1 ceiling is not the constraint here.

The real difficulty is **dimensionality**. Smoldering propagates in depth as much as laterally. A two-dimensional layout loses the mechanism; a three-dimensional one multiplies cost and complicates every view. Whether a layered pseudo-3D arrangement is honest or a fudge is a genuine Layout question.

## Honest strength assessment

*My assessment, not a fit review (§30). It carries no standing and does not promote this entry.*

**Moderate as a domain, high as a demonstrator.**

The domain case is real but narrow. Smoldering is understudied, physically local in the way this platform wants, and has a genuine irreducible regime in 3D heterogeneous fuel. Against that: the audience is small, the calibration data is sparse (you cannot easily instrument a fire two metres underground), and the timescales — months — make step duration awkward in the way SCR-F §30.4 warns about.

**The upside worth being excited about.** This is the cleanest hidden-state case in the entire catalog. If SCR wants one Lab that demonstrates why computational state and visual appearance are different facts, and demonstrates it with a domain where the confusion has real consequences, this is it. A run where the surface view shows nothing and the state view shows an advancing front is a two-frame argument for the platform's most subtle principle. That is worth more than the Lab's standalone domain value.

There is also a genuine open question SCR is shaped to attack: **what local rules produce re-emergence far from origin?** Fire managers know it happens and cannot predict where. Supplying candidate mechanisms for that, in bulk, with the failures retained, is the position paper's pitch in its purest form.

**The challenges, in order of severity.**

1. **Validation is close to impossible.** Subsurface fronts are not observable at the resolution a model would need. Thermal remote sensing sees the surface. This Lab may be unable to earn accuracy (§30.6) at all, and should say so early rather than discover it late.
2. **3D or nothing.** The mechanism lives in depth. Any flat abstraction is a different phenomenon.
3. **Timescale span is extreme.** Front advance in hours, overwintering in months, seam fires in decades. One tick cannot mean all three.
4. **Thin precedent.** No canonical lattice model to check against, which removes both a competitor and a safety net.

## Non-claims

This Lab does not predict where or whether any real fire will re-emerge, produces nothing suitable for fire management or safety decisions, and makes no claim about carbon accounting. Mechanisms it generates are candidate explanations requiring domain validation (§41, §43).
