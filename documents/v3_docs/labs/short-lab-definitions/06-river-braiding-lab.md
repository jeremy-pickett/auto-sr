# 6. River Braiding Lab

**Document class:** Lab Knowledge Brief · **Status:** draft
**Catalog:** SCR Lab Catalog v0.1 #6, Family A · **Standing:** ungraded
**Cites:** SCR-F v0.2 §11, §29, §30, §41; F-17
**Fit review (§30):** not performed

---

## The phenomenon

A river carrying more sediment than it can move deposits some of it. The deposit splits the flow. The split channels are individually weaker, deposit more, and split again. The result is a braided river — a shifting anastomosing network of channels and bars occupying a wide valley floor, reorganizing continuously, with individual channels appearing and vanishing over seasons.

Braided rivers do not settle. Even with constant discharge and constant sediment supply the pattern keeps rearranging. That perpetual restlessness under steady forcing is the phenomenon of interest.

## What the domain already knows

**Whether a river braids at all has a reducible answer.** The Leopold–Wolman threshold (1957) separates braided from meandering channels in slope–discharge space, and later refinements add grain size and width-depth ratio *(attribution from memory)*. Given the controlling variables, the planform class is predictable. This is a regime diagram, and it works.

**Sediment transport has formulas.** Meyer-Peter–Müller, Einstein, and their descendants relate transport rate to excess shear stress. These are empirical but well-established.

**The cellular precedent is a landmark.** Murray and Paola published a cellular braided-river model in Nature in 1994 *(attribution from memory, verify)*. Water is routed downslope across a grid of bed elevations by simple discharge-partitioning rules; sediment is transported as a function of local discharge; the bed updates. That is essentially the whole model, and it braids — producing bar formation, channel migration, avulsion, and the characteristic restlessness, with statistics comparable to real rivers and to flume experiments.

It is one of the most cited demonstrations that a landform previously explained through detailed fluid mechanics falls out of local rules. Anyone building this Lab must know it, because it is both the proof of concept and the incumbent.

## Where the shortcut holds, and where it breaks

**Reducible.** Braided-versus-meandering classification from slope and discharge. Bulk sediment flux for a given hydraulic condition. Equilibrium channel geometry (the hydraulic geometry relations). Average braiding intensity for a given regime. If the question is "what kind of river is this and how much sediment does it move," no simulation is required.

**Irreducible.** Everything about *where* and *when*:

- **Avulsion.** A channel abandons its course for a new one, sometimes abruptly and catastrophically. Whether and where avulsion occurs depends on accumulated deposition in the current channel relative to the surrounding floodplain — a threshold crossed by history. No formula gives the date or the location.
- **Bar and channel identity over time.** Which bar grows and which erodes is decided by small differences amplified through flow partitioning. Two nearly identical initial beds diverge.
- **Sensitivity of the split.** Flow partitioning at a bifurcation is famously unstable: small asymmetries grow, and one branch tends to capture the flow. That instability is the engine of the whole pattern and it is exactly where prediction fails.
- **Response to changed supply.** A river adjusting to a dam, a landslide input, or gravel mining reorganizes over years through a path-dependent sequence.

**The lens, stated plainly.** This Lab illustrates a general principle worth stating once and reusing across the catalog: **classification is reducible, realization is not.** The domain can tell you reliably that you will get a braided river. It cannot tell you which channel will be running next spring. SCR has nothing to add to the first and is squarely aimed at the second — but the second is also where validation is hardest, because "the model produced a braided pattern with realistic statistics" is a much weaker claim than "the model predicted this channel."

## What a Cell would carry

A patch of valley floor: bed elevation, water depth or discharge share, sediment size or availability, and possibly vegetation. Very low state complexity — Murray–Paola works on elevation plus routed discharge. §13.1 is trivially met.

The Layout has a genuine subtlety: **discharge routing is not a symmetric neighbour interaction.** Water moves downslope, so Connections are directed and the direction depends on the state (elevation) rather than being fixed by the World. That is a more dynamic notion of Connection than a static lattice, and it is worth flagging as a real modelling question rather than a detail.

## Honest strength assessment

*My assessment, not a fit review (§30). It carries no standing and does not promote this entry.*

**Strong on mechanism, narrow on audience, and squarely in rediscovery territory.**

Everything about the physics suits this platform: genuinely local rules, spectacular emergent structure, restless dynamics under steady forcing, a real irreducible core in avulsion and bifurcation instability. The problem is that Murray and Paola established this thirty years ago and the field absorbed it. SCR entering here does not find an unmodelled domain; it finds a well-modelled one with a small research community.

**The upside worth being excited about.** Braided rivers are among the best-observed landforms available: flume experiments reproduce them at tabletop scale under controlled conditions, and satellite imagery gives multi-decade time series of real braid plains. That combination — controlled experiment *plus* field observation *plus* an established cellular baseline — is rare, and it makes this an unusually honest place to test whether SCR-generated mechanisms are any good. If the corpus cannot rediscover something Murray–Paola-shaped when asked for restless self-organizing channel networks, that is a finding about the platform, cheaply obtained.

There is also a real open question the field cares about: **what local rule structure controls avulsion timing?** Supplying candidate mechanisms there is defensible upstream work.

**The challenges, in order of severity.**

1. **Rediscovery.** The canonical cellular model exists and is good.
2. **Directed, state-dependent Connections.** Flow routing is not a fixed neighbourhood, which is a modelling commitment the platform has not settled.
3. **Water and sediment are arguably two mechanisms** — DEC-1.
4. **Step duration spans floods and decades**, the recurring Family A problem.
5. **Small audience.** Fluvial geomorphology is not a large market.

## Non-claims

This Lab does not predict the behaviour of any real river, does not assess flood or erosion hazard, and produces nothing suitable for engineering or land management decisions (§41, §43).
