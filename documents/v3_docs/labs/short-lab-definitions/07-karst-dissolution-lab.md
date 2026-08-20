# 7. Karst Dissolution Lab

**Document class:** Lab Knowledge Brief · **Status:** draft
**Catalog:** SCR Lab Catalog v0.1 #7, Family A · **Standing:** ungraded
**Cites:** SCR-F v0.2 §11, §29, §30, §41; F-17
**Fit review (§30):** not performed

---

## The phenomenon

Rainwater picks up carbon dioxide, becomes mildly acidic, and dissolves limestone. Water enters a rock mass through a dense network of nearly identical hairline fractures. Over ten to a hundred thousand years, a handful of those fractures become caves and the rest become nothing.

That selection is the whole phenomenon. The fractures start almost the same. One widens slightly faster, carries more flow, dissolves faster still, and captures the drainage of its neighbours. What emerges is a conduit network, sinkholes at the surface where conduits collapse, springs where they discharge, and an aquifer whose behaviour is dominated by a few pipes rather than by the bulk rock.

## What the domain already knows

**The dissolution kinetics are the key fact, and they are counterintuitive.** Calcite dissolution rate is roughly linear in undersaturation when the water is fresh, but near saturation the rate law becomes strongly nonlinear — commonly described as fourth-order *(Plummer–Wigley–Parkhurst lineage; attribution from memory, verify)*. The consequence, developed extensively by Dreybrodt and colleagues, is that water which has nearly saturated dissolves *very* slowly rather than stopping. It therefore penetrates deep into a fracture while still slightly aggressive, widening it along its entire length rather than only at the inlet.

Without that nonlinearity, caves would not form: dissolution would be confined to the first few metres and the fracture would never break through. With it, there is a **breakthrough time** after which flow increases catastrophically and widening accelerates. Dreybrodt-style analysis gives estimates of breakthrough time from fracture aperture, length, and hydraulic gradient — a genuine analytic result.

**Lattice precedent is modest but relevant.** Dissolution-front instability has been studied with pore-network and lattice models, and the phenomenon belongs to the same family as viscous fingering, invasion percolation, and diffusion-limited aggregation — reactive infiltration instability, where a dissolving front spontaneously breaks into fingers rather than advancing uniformly.

## Where the shortcut holds, and where it breaks

**Reducible.** Breakthrough time for a *single* fracture of known geometry under known gradient. Whether a given water chemistry is aggressive. Bulk dissolution rate. Equilibrium chemistry. The onset condition for the fingering instability, which is a linear stability question. These are real answers and they are enough for many practical purposes.

**Irreducible.** Everything about competition:

- **Which fracture wins.** This is the domain's defining question and it is a textbook case of sensitive dependence. A population of fractures differing by a few percent in aperture, evolving under positive feedback for fifty thousand years, produces a specific network. The winner is decided early by differences too small to measure and amplified relentlessly. There is no shortcut; you follow it.
- **Network topology.** Whether the result is a single trunk conduit, a braided maze, or a branching dendritic pattern depends on the fracture geometry, the gradient field, and the recharge distribution interacting over the full history.
- **Capture events.** When one conduit intersects another it steals its flow, abruptly changing the whole system's hydraulics and redirecting subsequent dissolution. Discrete, path-dependent, consequential.
- **Base level changes.** Sea level and valley incision move the outlet during cave formation, so the boundary condition itself has a history.

**The lens, stated plainly.** If the catalog needs one entry to illustrate computational irreducibility in its purest form, this is it. The mechanism is simple and known. The feedback is positive. The horizon is 10⁴–10⁵ years. The outcome is decided by initial differences below the resolution of any possible measurement. **Every ingredient of irreducibility is present, and the domain openly says so** — cave scientists do not claim to predict which fracture becomes a cave, and they are right not to.

That is intellectually beautiful and practically awkward, which is exactly the tension this Lab must state honestly.

## What a Cell would carry

A fracture segment or rock volume: aperture or void fraction, local flow, water saturation state (how close to chemical equilibrium), and rock solubility. Bounded scalars; §13.1 is met.

The Layout is genuinely contested. Karst is a **fracture network**, not a lattice — dissolution follows pre-existing joints and bedding planes whose geometry is inherited from tectonics. A Network World is arguably more honest than a Grid World, and this is one of the few Family A entries where the non-grid Layouts (§15) are the right answer.

## Honest strength assessment

*My assessment, not a fit review (§30). It carries no standing and does not promote this entry.*

**Intellectually excellent, practically weak, and worth keeping for the first reason.**

The domain fit is genuinely superb. Local rule, positive feedback, extreme sensitivity, emergent network — this is what the platform is for, and the domain's own literature frames it in compatible terms.

The practical case is poor and should not be oversold. The audience is small. The timescale makes validation impossible in the direct sense: no one will ever watch a cave form. Validation must be indirect — comparing statistical properties of simulated networks against mapped cave surveys — and cave surveys are biased toward passages humans can physically enter, which is a real and known sampling problem.

**The upside worth being excited about.** Two things, and the second is bigger than the domain.

First, karst aquifers supply drinking water to a large fraction of the world's population and behave badly — contaminants travel through conduits at hundreds of metres per hour rather than the metres per year that porous-medium models predict. Understanding what conduit *topologies* arise from what fracture populations is a real question with real consequence, and it is a network-statistics question rather than a prediction question, which suits an ensemble instrument.

Second, and more valuable to the platform: this Lab is a **clean irreducibility demonstrator**. Run the same mechanism from initial fracture apertures differing by one part in a thousand and get different cave systems. That is the Influence View (§25.3) with a domain that makes the point honestly, including the ambient-sensitivity context the platform requires — because here, *every* perturbation matters, and saying so is the finding.

**The challenges, in order of severity.**

1. **Validation is structurally unavailable.** No direct observation is possible at any useful scale.
2. **Cave survey data is biased** toward human-passable passages.
3. **Not a lattice.** Fracture networks are inherited geometry; a grid misrepresents them.
4. **Tiny audience**, mostly academic.
5. **Timescale is extreme** even by Family A standards.

## Non-claims

This Lab does not predict conduit locations, sinkhole formation, or contaminant transport at any real site, and produces nothing suitable for water resource, geotechnical, or hazard decisions (§41, §43).
