# Family A — Fire, land, and surface processes
## Lab Knowledge Report v1

### Wildfire · Smouldering and Peat Fire · Landslide · Dune and Ripple · Coastal Erosion · River Braiding · Karst Dissolution · Permafrost Thaw

**Document class:** Level 5 — Lab Papers (family report, pre-fit) · **Status:** draft
**Path:** `labs/a-fire-land-and-surface/family-a-report-v1.md`
**Catalog:** SCR Lab Catalog v0.1, Family A (entries 1–8)
**Framework:** `../../00-start-here/irreducibility-and-what-cellular-means.md` — reducibility, reach classes, driver classes, time, geometry, the helper boundary
**Conventions:** `../README.md` — four axes, Lab roles, visualization credibility class
**Reviewed against:** `../../01-core/labs.md` — LAB-5's ten fit questions, including the tenth (LAB-6, LAB-7, the reducibility audit). This report frames those questions; it does not answer them.
**Supersedes:** first-pass briefs 01–08 in `../short-lab-definitions/`, retained as historical reference
**Responds to:** `../../critiques/SCR_Labs_01-10_Critique_v0.1.md`
**Cites:** SCR-F v0.2 §11, §15, §18.5, §29, §30, §38.6, §41–43; F-7, F-9, F-17 · LAB-5 to LAB-8, LAB-16 · DEC-1, DEC-3, DEC-21, DEC-24
**Fit reviews (§30):** none performed. **Nothing here establishes fit.**

---

## What this report is

Eight Labs examined through computational irreducibility and cellular automata, asking one question of each: *what does this Lab need to know?*

It is not a feature spec, a requirements document, or a fit review. It contains no requirements identifiers.

The shared framework is **not** restated here — it lives at Level 1 and this report cites it. What remains is what is specific to these eight domains.

**References are verified.** Items marked **[V]** were checked against a primary or authoritative source; **[D]** items are described generically and are background, not citable claims. The verification pass changed content, not formatting: Rothermel's report number was wrong in the first pass (INT-116 → **INT-115**) [1]; the peat ignition moisture limit was a guess and is **125 ± 10% of dry mass** [16]; the 1997 Indonesian peat fire release is **0.81–2.57 Gt C, 13–40% of mean annual global fossil fuel emissions** [15]; and Ashton's third author is **Arnoult**, corrected by a *Nature* erratum the first pass reproduced [9a].

---

## What this family has in common

These are **surface and near-surface processes on real terrain**, and that gives the family a shared shape worth stating once.

**Adjacency is physically real.** In every entry here, two cells interact because they are next to each other in the world — heat crosses a boundary, sediment moves downslope, water drains from one depression into the next. That is the selection rule the framework §8 identifies, and it is why this family fits the platform better than most.

**The forcing is almost always external.** Wind, rainfall, wave climate, warming, and discharge drive seven of these eight domains, and none of them reacts to the simulated state in the ordinary case. Under the framework's driver classes these are **external inputs**, not second mechanisms — which dissolves most of the DEC-1 blockages the first pass recorded. The genuinely interactive couplings that remain are few and specific: fire altering airflow, burnt peat altering drainage, thaw altering drainage, bed evolution altering flow routing.

**Time is the family's hardest common problem.** Six of eight span at least three orders of magnitude between the fastest process and the horizon of interest. This is the framework §5 scale-span problem and it recurs so consistently that Family A is probably the right place to test whatever DEC-3 offers.

**Validation quality varies more than fit does.** Two entries here can be checked against controlled experiments and satellite time series; two cannot be checked at all. That spread is the family's most important internal distinction and it does not correlate with mechanism fit.

---

## Lab 1 — Wildfire

| | |
| :--- | :--- |
| **Role** | Calibration anchor · mechanism-supply candidate |
| **Standing** | [strong], inherited from *A Card Catalog for Emergence* v0.1 §5; not re-derived |
| **Falsifiable question** | Which local interaction rules produce junction acceleration or spotting-driven pattern change under *fixed* wind forcing? |
| **Mechanism fit** | High |
| **Validation class** | **Direct observational** — mapped perimeters, plus operational-model comparison |
| **Rediscovery risk** | Low |
| **Practical need** | Real |
| **Reach** | Neighbour-local, plus bounded transport for embers |
| **Drivers** | Wind and terrain as **external input**; fire–atmosphere coupling as **interactive mechanism** |
| **Geometry** | Square grid, anisotropy correction mandatory |
| **Visual credibility** | **Class 1** |

**The phenomenon.** Fire moves as a front: fuel ignites, burns, is consumed; heat passes by contact and short-range radiation; wind and slope bias direction. Front shape, fingering, unburnt islands, self-extinction, and spotting follow from local transitions repeated.

**The established shortcut.** **Rothermel (1972)** gives a quasi-empirical steady-state rate of spread from fuel bed properties, moisture, wind, and slope [1] — the most widely used wildfire behaviour tool in the world, embedded in dozens of operational systems [2]. **FARSITE** grows a perimeter by treating each perimeter vertex as the source of an elliptical wavelet dimensioned by Rothermel — Huygens' principle applied to fire [3]. Dead fuel moisture is tracked in 1-, 10-, 100-, and 1000-hour timelag classes with different response rates [20]. Separately, the **Drossel–Schwabl** lattice fire model (1992) is a canonical self-organized-criticality object producing power-law cluster size distributions [4] — established physics, and not a fire behaviour model.

**Reducible.** Steady spread through homogeneous fuel under steady wind on uniform slope. Perimeter growth under a prescribed wind field. Whether fire percolates through random fuel at a given density. Long-horizon fire-size distributions.

**Irreducible.** Heterogeneity near the percolation threshold, where crossing depends on the specific fuel arrangement — and real landscapes sit near-critical constantly, which is what fuel breaks are for. Junction fires, where two merging fronts accelerate beyond either front's predicted rate. Path dependence in burnout: which islands survive depends on the order in which the front reached their edges.

**The line this Lab must draw.** Once fire alters wind strongly, a local mechanism may no longer be the right abstraction. Three regimes must be separated before anything is claimed:

1. local front mechanisms under **prescribed or weakly coupled** wind — defensible;
2. **reduced two-way coupling** SCR can represent honestly — the open question;
3. **full fire–atmosphere dynamics** requiring CFD — outside SCR.

"Candidate mechanism supply" must not become a licence to imitate plume physics with arbitrary local heuristics.

**Cell state.** *Persistent:* remaining fuel, moisture, burn state, accumulated pre-heat. *Static World data:* slope. Fuel drying under neighbour heat but not yet ignited is computationally live and visually inert — §38.6 as a domain fact, and the cleanest instance in the family.

**Assessment.** *(judgment, no standing)* The strongest all-around Lab in the family and the platform's proposed calibration anchor. The upside is specific: fire science has a gap between fast models that prescribe the wind field and expensive coupled simulations nobody runs at scale, and candidate local rules for regimes where the fast models are known to fail is defensible upstream work — provided regime 3 stays out of bounds.

---

## Lab 2 — Smouldering and Peat Fire

| | |
| :--- | :--- |
| **Role** | Integrity and architecture demonstrator (hidden state) |
| **Standing** | Ungraded |
| **Falsifiable question** | What local rules for depth-resolved moisture and heat produce re-emergence far from the ignition point? |
| **Mechanism fit** | Good |
| **Validation class** | **Qualitative only** at depth; direct experimental at laboratory scale |
| **Rediscovery risk** | Low — no canonical lattice model |
| **Practical need** | Real, small audience |
| **Reach** | Neighbour-local in three dimensions |
| **Drivers** | Weather as **external input**; peat consumption altering drainage as **interactive mechanism** |
| **Geometry** | Layered 3-D — see below |
| **Visual credibility** | Class 3 |

**The phenomenon.** Flameless, oxygen-limited combustion on porous fuel, propagating at centimetres per hour, downward and sideways through the ground. It survives conditions that extinguish flame — rain, snow, winter — and re-emerges months later. The surface can look cool and green while a front advances a metre below.

**The established shortcut.** A heat balance: exothermic char oxidation against conduction, radiation, and the latent heat of evaporating fuel moisture. Everything turns on moisture as a fraction of dry mass, with a hard threshold — **smouldering ignition requires moisture below 125 ± 10% dry base** [16]. Critically, *once ignited*, a self-sustained front can dry and propagate through layers wetter than that limit [16], a hysteresis that matters. Mineral content acts as a heat sink; bulk density controls oxygen supply and thermal inertia non-monotonically. The consequences are not small: the 1997 Indonesian peat and forest fires released an estimated **0.81–2.57 Gt C** [15].

**Reducible.** One-dimensional steady front velocity through homogeneous fuel. Whether a fuel can smoulder at a given moisture and density. Total carbon released given burn depth and area.

**Irreducible.** Path selection through heterogeneous subsurface moisture — a percolation-like search whose route decides where the fire surfaces. Re-emergence location. Overwintering, a marginal heat balance integrated over months. Coupling back to hydrology as burnt peat lowers the surface.

**Correction from the first pass.** "3D or nothing" was rhetorically strong and analytically lazy. Three representations must be distinguished before the fit review, because a reduced one may be honest for some questions:

- **true volumetric 3-D** — required for re-emergence path questions;
- **layered 2.5-D** — plausibly sufficient for depth-of-burn and carbon questions;
- **reduced depth columns with lateral coupling** — sufficient for landscape-scale extent.

Making full volumetric simulation a precondition would foreclose testing whether simpler abstractions preserve the mechanism.

**Cell state.** *Persistent:* organic mass remaining, moisture fraction, accumulated heat, combustion state. *Static:* mineral fraction, bulk density. *Derived:* oxygen availability.

**Assessment.** *(judgment, no standing)* **Classify primarily as architecture and integrity value.** Validation is qualitative only and structurally unlikely to improve — subsurface fronts cannot be instrumented at the resolution a model would need. But this is the cleanest hidden-state demonstrator in the catalog: a Run where the surface view shows nothing and the state view shows an advancing front is a two-frame argument for §38.6, on a domain where the confusion kills people who declare fires out.

---

## Lab 3 — Landslide and Debris Flow

| | |
| :--- | :--- |
| **Role** | Mechanism-supply candidate (narrow) |
| **Standing** | Ungraded |
| **Falsifiable question** | Does local load transfer improve the spatial and size statistics of failures beyond uncoupled susceptibility mapping? |
| **Mechanism fit** | **Contested** — see below |
| **Validation class** | **Indirect statistical** — post-storm inventories |
| **Rediscovery risk** | Medium |
| **Practical need** | Real |
| **Reach** | Neighbour-local (contested) |
| **Drivers** | Rainfall and shaking as **external input** |
| **Geometry** | Square grid |
| **Visual credibility** | Class 3 |

**The phenomenon.** A slope holds until it does not, and the failed mass loads what is below it. The population-level fact is as interesting as any single event: landslide areas from a triggering event are well described by a three-parameter inverse-gamma distribution — power-law decay with exponent about **−2.40** for medium and large slides, and an exponential **roll-over** at small areas [5].

**The established shortcut.** The **infinite-slope factor of safety** is what practising engineers use, and coupled to a hydrological model it becomes the operational susceptibility tool (the SHALSTAB/SINMAP lineage) [19]. Runout distance is predicted from volume by empirical angle-of-reach relations [20]. Note what this means: **the incumbent is a per-cell calculation with no interaction at all.**

**The precedent that must be confronted first.** The **Bak–Tang–Wiesenfeld sandpile** (1987) is the founding model of self-organized criticality and the reason anyone reaches for a cellular model here [6]. But laboratory granular piles largely failed to reproduce clean SOC: the rice-pile experiments found power-law avalanches **only for elongated grains**, with rounded grains showing a characteristic scale [7]. That result showed SOC depends on the mechanism of energy dissipation rather than being insensitive to system details. **The sandpile is a good theory of criticality and a poor theory of sand.** A Lab here must open by distinguishing itself from it rather than borrowing its glamour.

**Reducible.** Whether a *given* slope with known properties fails. Susceptibility mapping. Runout from volume. Regional magnitude–frequency.

**Irreducible.** Load transfer cascades, where whether failure arrests depends on the arrangement of marginal cells. Progressive failure and strain softening — a non-monotone feedback the static calculation cannot represent by construction. Entrainment, where runout depends on path and path depends on runout. Rainfall sequencing, where identical totals in different order produce different failure populations.

**The claim this Lab must choose.** Stress redistribution in real slope materials depends on geometry, constitutive behaviour, and continuum mechanics. A local transfer rule may be a useful toy mechanism, a defensible reduced model, or physically misleading. **The Lab must state which claim it is making before it runs anything.** The defensible version is narrow: SCR's entire potential contribution here is the *coupling term*.

**Cell state.** *Persistent:* saturation or pore pressure, accumulated load from upslope failures, failure state, accumulated damage. *Static:* slope, cohesion, strength. *Derived:* factor of safety.

**Assessment.** *(judgment, no standing)* **Plausible only if narrowly targeted at cascade structure rather than general slope stability.** The stress non-locality objection is real and shared with Fracture (Family E). Inventory data is genuinely good.

---

## Lab 4 — Dune and Ripple

| | |
| :--- | :--- |
| **Role** | Rediscovery benchmark · architecture stress test (bounded transport) |
| **Standing** | [plausible], inherited; not re-derived |
| **Falsifiable question** | Can Generation recover a Werner-class mechanism family from a semantic request, without being handed the implementation? |
| **Mechanism fit** | Excellent |
| **Validation class** | **Direct observational** — satellite imagery of dune fields worldwide |
| **Rediscovery risk** | **High** |
| **Practical need** | Low |
| **Reach** | **Bounded transport** — the defining case |
| **Drivers** | Wind regime as **external input** |
| **Geometry** | Square grid, directionally asymmetric connections |
| **Visual credibility** | Class 3 |

**The phenomenon.** Wind moves sand in hops — saltation. Out of that come structures at two widely separated scales: **ripples**, centimetres apart, forming in minutes; and **dunes**, tens to hundreds of metres, migrating over years. Dune types classify by wind regime.

**The established shortcut.** **Bagnold (1941)** established the physics of blown sand and transport rate scaling [18]. **Werner (1995)** introduced the first cellular-automaton dune model: sand slabs on a lattice, moved downwind a fixed distance (typically five sites), deposited with probability depending on whether the landing site is already sandy, plus an avalanche rule enforcing the angle of repose [8]. That handful of rules reproduces barchan, transverse, linear, and star dunes in three dimensions [8]. Ripple wavelength at onset follows from saltation trajectory length via linear stability [20]; dune migration speed is inversely proportional to height [20].

**Reducible.** Saltation threshold, transport rate, initial ripple wavelength, dune celerity, and the wind-regime-to-dune-type classification. A model reproducing these has reproduced textbook content.

**Irreducible.** Pattern coarsening — dune fields do not settle at the initially selected wavelength; spacing grows through a history of merges and splits. Dune collisions, where the outcome depends on size ratio and offset. Barchan field persistence, unexplained by the single-dune solution. Sand supply, vegetation, and topography.

**The two-scale problem, resolved.** The critique proposed splitting this into separate Ripple and Dune Labs. **Kept as one Lab with two declared mechanism classes and two time fits**, because the hazard identified is real — one Plugin contract must not be forced to explain both instabilities merely because the words share a domain — but a standalone Ripple Lab has almost no content of its own. Declaring the pairing explicitly closes the hazard at lower cost.

**Cell state.** *Persistent:* sand height or slab count. *Derived:* local slope, shadow state — both computable from height. The smallest state in the family.

**Assessment.** *(judgment, no standing)* **Role is benchmark, not frontier — and that is a legitimate role.** Its architectural value is disproportionate: dune fields are one of the few natural systems where a non-neighbour transport hop is *physically correct*, so this is the honest test of whether SCR can express bounded transport without collapsing into a general simulator. That answer matters to wildfire spotting, ecological dispersal, and scanning worms.

---

## Lab 5 — Coastal Erosion

| | |
| :--- | :--- |
| **Role** | Rediscovery benchmark · architecture stress test (global-read boundary) |
| **Standing** | Ungraded |
| **Falsifiable question** | In the high-angle unstable regime, which local transport rules reproduce observed cape spacing and spit geometry? |
| **Mechanism fit** | Good in the unstable regime |
| **Validation class** | **Direct observational** — satellite shoreline series, a century of aerial photography |
| **Rediscovery risk** | Medium-high |
| **Practical need** | High and rising |
| **Reach** | Neighbour-local for transport; **global read** for shadowing unless mediated |
| **Drivers** | Wave climate as **external input** |
| **Geometry** | Plan-view grid (2-D) or shoreline curve (1-D) — different Worlds |
| **Visual credibility** | **Class 1** — the family's most consequential misreading |

**The phenomenon.** Waves at an angle drive sand along the shore; convergence builds, divergence erodes. Over decades this builds spits and capes, migrates barrier islands, and opens inlets. A storm can breach an island overnight; ordinary drift reshapes a coast over a lifetime.

**The established shortcut.** The CERC equation relates alongshore flux to breaking wave height and wave-shoreline angle; with sediment continuity it gives the "one-line" model, the coastal engineering workhorse [20]. Shoreline retreat under sea-level rise is predicted by the **Bruun rule** — and its criticism is mainstream, not fringe: Cooper and Pilkey (2004) argued it has no predictive power and should be abandoned [10].

**The cellular precedent is excellent and under-appreciated.** Ashton, Murray and Arnoult (2001) showed that when waves approach at sufficiently large angle, the standard transport relation makes a straight shoreline **unstable** — perturbations grow, and a simple cellular model spontaneously produces capes, spits, and cuspate forelands resembling the Carolina capes [9]. That is a first-rate case of a simple local rule generating large-scale geomorphology previously attributed to inherited geology.

**Reducible.** Transport rate from wave conditions. Shoreline change in the **low-angle** regime, where the system is diffusive and a straight coast stays straight. Equilibrium beach profiles. Volume budgets.

**Irreducible.** The high-angle regime: instability analysis says the coast becomes unstable, not what you get. Which features survive, at what spacing, and whether capes merge is nonlinear. Breaching, a discrete threshold event that permanently changes connectivity. Storm sequencing, where recovery between events is incomplete.

**The architectural point.** Shadowing — a cape blocking waves from reaching the coast behind it — is not a "strain on locality." Depending on implementation it is a **global geometric visibility calculation**, the fifth reach class. If needed, it belongs to the World or Reactor as a declared capability, never as arbitrary global access granted to a Plugin. Whether visibility is *generic enough* to be a helper is a genuine open question, and this Lab is where it must be answered.

**Cell state.** *Persistent:* sediment volume or shoreline position, barrier or dune state. *Static:* elevation, sediment type. *Derived:* shadow state, local shoreline orientation.

**Assessment.** *(judgment, no standing)* Stronger than a framing as "time-fit stress test" suggests, because it has what most of this family lacks: **a documented case where a simple local rule overturned a domain assumption** [9]. A *named instability threshold* cleanly separates the reducible and irreducible regimes, which is rare. Requires unusually strict visualization labelling.

---

## Lab 6 — River Braiding

| | |
| :--- | :--- |
| **Role** | Rediscovery benchmark · calibration candidate |
| **Standing** | Ungraded |
| **Falsifiable question** | Which local rule structures control avulsion timing and channel capture? |
| **Mechanism fit** | Excellent |
| **Validation class** | **Direct experimental** (flume) **and direct observational** (satellite) — the strongest stack in the family |
| **Rediscovery risk** | **High** |
| **Practical need** | Modest, small audience |
| **Reach** | Neighbour-local with state-dependent connection weights |
| **Drivers** | Discharge and sediment supply as **external input**; bed evolution as **interactive mechanism** |
| **Geometry** | Square grid |
| **Visual credibility** | Class 3 |

**The phenomenon.** A river carrying more sediment than it can move deposits some; the deposit splits the flow; the split channels deposit and split again. The result reorganizes continuously — **even under constant discharge and sediment supply.** That restlessness under steady forcing is the phenomenon.

**The established shortcut.** Whether a river braids at all has a reduced answer: the **Leopold–Wolman** slope–discharge threshold (1957) separates braided from meandering channels, with braided rivers steeper at the same discharge [11]. Sediment transport has empirical formulas [20]; hydraulic geometry relations give equilibrium form [20].

**The cellular precedent is a landmark.** **Murray and Paola (1994)** routed water downslope across a grid of bed elevations by simple discharge-partitioning rules, transported sediment as a nonlinear function of local discharge, and updated the bed — producing braiding, bar formation, migration, and avulsion [12]. Their conclusion is the load-bearing one: *the only factors essential for braiding are bedload sediment transport and laterally unconstrained free-surface flow* [12]. A landform previously explained through detailed fluid mechanics falls out of local rules.

**Reducible.** Braided-versus-meandering classification. Bulk sediment flux. Equilibrium channel geometry. Average braiding intensity.

**Irreducible.** Avulsion — when and where a channel abandons its course, a threshold crossed by accumulated deposition history, with no formula for the date or the location. Bar and channel identity, decided by small differences amplified through flow partitioning. Bifurcation instability, where small asymmetries grow and one branch captures the flow.

**The reusable phrase this Lab contributes:** *classification is reducible, realization is not.*

**Correction from the first pass.** The first pass said connections are directed and the direction depends on state, implying a changing graph. That is probably the wrong abstraction and would make dynamic connections far more complicated than necessary. **Distinguish dynamic connection *existence* from dynamic connection *strength or direction*.** In a grid, all adjacent edges can exist permanently while the Reactor or Plugin computes which carry flow, from elevation. Only the second is needed here.

**Cell state.** *Persistent:* bed elevation, sediment availability. *Derived:* water depth, discharge share, flow direction — all computable from elevation and routing. Storing them would hide mechanism complexity in state.

**Assessment.** *(judgment, no standing)* **Validation is the strongest in the family** — flume experiments reproduce braiding at tabletop scale under controlled conditions, *and* satellite imagery gives multi-decade time series of real braid plains, *and* a canonical cellular baseline exists to compare against. A superb platform benchmark with one real open question attached.

---

## Lab 7 — Karst Dissolution

| | |
| :--- | :--- |
| **Role** | Architecture stress test (Network World) · sensitivity demonstrator |
| **Standing** | Ungraded |
| **Falsifiable question** | Which local competition rules produce observed conduit network topology statistics from plausible fracture populations? |
| **Mechanism fit** | Excellent |
| **Validation class** | **Qualitative only** — direct observation structurally unavailable |
| **Rediscovery risk** | Low |
| **Practical need** | Small, academic |
| **Reach** | **Path-local** — influence follows the fracture graph |
| **Drivers** | Recharge and base level as **external input**; aperture widening as **interactive mechanism** |
| **Geometry** | **Network** — inherited fracture geometry, not a lattice |
| **Visual credibility** | Class 3 |

**The phenomenon.** Water charged with carbon dioxide dissolves limestone. It enters through a dense network of nearly identical hairline fractures. Over tens of thousands of years, a handful become caves and the rest become nothing. **That selection is the phenomenon.**

**The established shortcut, and it is counterintuitive.** Calcite dissolution is first-order far from equilibrium but switches near saturation to a **slow fourth-order rate law** [13]. The consequence, developed by Dreybrodt and colleagues, is that nearly-saturated water dissolves slowly rather than stopping, penetrating deep into a fracture while still slightly aggressive and widening it along its whole length. **Without that nonlinearity, caves would not form.** With it there is a **breakthrough time** after which flow increases dramatically through positive feedback, and analytical expressions exist; depending on fracture length and hydraulic gradient, breakthrough ranges from **10⁴ to several 10⁶ years** [13].

**Reducible.** Breakthrough time for a single fracture of known geometry under known gradient. Whether a water chemistry is aggressive. Bulk dissolution rate. Onset of the reactive-infiltration fingering instability.

**Irreducible.** Which fracture wins. Network topology — single trunk, maze, or dendritic. Capture events, where one conduit intersects another and steals its flow, abruptly changing the system's hydraulics. Base level changes moving the outlet during formation.

**Correction from the first pass, and it applies beyond this Lab.** The first pass treated extreme sensitivity to tiny initial differences as sufficient evidence of computational irreducibility. **It is not** (framework §1.2). The defensible claim, which is enough:

> Exact conduit realization depends on the iterated competition among fractures and cannot be obtained from the single-fracture breakthrough shortcut.

No philosophical claim is needed and none should be made. *(The same overreach was present in the first-pass Wildfire, Coastal, and River briefs and has been corrected in all of them.)*

**Cell state.** *Persistent:* aperture or void fraction, water saturation state relative to equilibrium. *Static:* rock solubility, initial fracture geometry. *Derived:* local flow.

**Assessment.** *(judgment, no standing)* The strongest **Network World** argument in the family — using a grid here would be actively dishonest, since dissolution follows joints and bedding planes inherited from tectonics. But **validation is qualitative only and will not improve**: nobody will watch a cave form, and cave surveys are biased toward passages humans can enter. **Keep for architecture and demonstration value; weak candidate for early external validation.**

---

## Lab 8 — Permafrost Thaw

| | |
| :--- | :--- |
| **Role** | Mechanism-supply candidate — the strongest in the family |
| **Standing** | Ungraded |
| **Falsifiable question** | What local coupling rules produce the wetting-versus-draining connectivity transition under fixed warming? |
| **Mechanism fit** | Good |
| **Validation class** | **Direct observational** — InSAR subsidence, multi-decade imagery, documented polygon succession |
| **Rediscovery risk** | Low |
| **Practical need** | High |
| **Reach** | Neighbour-local |
| **Drivers** | Warming as **external input**; drainage reorganization as **interactive mechanism** |
| **Geometry** | Grid, with inherited polygon structure as a World template |
| **Visual credibility** | **Class 1** — mistakable for a climate projection |

**The phenomenon.** Frozen ground contains ice; when it thaws the ice volume is lost and the surface **collapses**. Thermokarst is not gradual warming but abrupt, localized subsidence producing pits, troughs, and thaw lakes. Depressions collect water, which conducts heat better than air and absorbs more radiation, so they thaw faster — *or* connected troughs drain the surface and dry it, slowing thaw. **Which happens is a connectivity question.**

**The established shortcut.** Vertical thaw depth has a closed form: the Stefan solution gives thaw depth growing as the square root of accumulated degree-days [20].

**The gap, stated carefully.** The first pass claimed abrupt thaw is under-represented in models generally. The safer and now-citable claim: Turetsky et al. (2020) state that **large-scale models currently simulate only gradual changes in seasonally thawed soil**, and estimate that abrupt thaw will occur in **under 20% of the permafrost zone but could affect half of permafrost carbon** [14].

**The observational anchor.** Liljedahl et al. (2016) documented pan-Arctic ice-wedge degradation since 1950 across ten localities, and described exactly the sequence this Lab is about: **initial thaw drains polygon centres and forms disconnected troughs holding isolated ponds; continued melting increases trough connectivity and drains the landscape overall** [17]. The connectivity transition is not hypothesized — it is observed.

**Reducible.** One-dimensional thaw depth from surface temperature. Bulk carbon release given thawed volume and carbon density. Equilibrium permafrost extent for a given climate.

**Irreducible.** Drainage connectivity — a percolation transition whose crossing flips the landscape between wetting and drying trajectories with opposite carbon consequences. Neighbour-driven thaw, where a collapsed cell warms its neighbours and thaw spreads laterally, which no column model represents. Thaw lake lifecycle, including catastrophic drainage. Irreversibility: ice lost is not recovered, so the system has memory the forcing does not.

**Cell state.** *Persistent:* ice content, thaw depth, surface elevation, water accumulation, soil carbon. *Derived:* albedo, thermal conductivity.

Polygonal cracking is **inherited geometry**, not emergent from this mechanism. It has its own pattern-formation literature and conflating the two would misrepresent the domain — it belongs as a World template.

**Assessment.** *(judgment, no standing)* **Validation is the best in the family for a climate-adjacent domain** — subsidence, lake area, and trough connectivity are all directly measurable. The scientific gap is real and sourced. **Strong candidate for an early serious Lab, with unusually strict non-claim and visualization controls** — output will be read as a carbon-feedback projection, and the topic is publicly charged.

---

## Family findings

### Regression targets

Three entries here have famous local-rule precedents. **Do not merely cite them — use them.** Each becomes a platform regression question that tests SCR rather than the domain:

| Lab | Benchmark | Regression question |
| :--- | :--- | :--- |
| Dune | Werner (1995) [8] | Can Generation, without being handed the implementation, produce a mechanism family whose behaviour falls in the known morphology classes? |
| River braiding | Murray & Paola (1994) [12] | Same, for braiding from bedload transport plus unconstrained flow. |
| Coastal | Ashton et al. (2001) [9] | Does the high-angle instability emerge, or must it be prescribed? |

Two further tests apply to all three — **Search:** when asked for the observed behaviour, does the Corpus retrieve those mechanisms? **Negative space:** does the record show *failed* mechanism families, or only noise?

These Labs may tell us more about SCR's quality than about their domains. That is a reason to build them, stated honestly.

### Build priority within the family

Roles and sequencing, **not** scientific worth, and **not** fit grades.

**First.** **Wildfire** (calibration anchor; best combined case). **Permafrost** (real sourced gap, strong data, clean Study structure). **River braiding** (best validation stack; one real open question).

**For a stated role.** **Coastal erosion** (good instability regime and data; forces the global-read boundary). **Dune** (benchmark and the bounded-transport test). **Landslide** (good coupling question, substantial abstraction risk).

**Architecture and integrity value.** **Smouldering** (best hidden-state demonstrator; validation qualitative only). **Karst** (Network World stress test; validation unavailable).

### What this family demands of the platform

| Question | Owner | Raised by |
| :--- | :--- | :--- |
| **External input vs interactive mechanism vs static condition** | **DEC-1** | Seven of eight. Highest leverage, and separable from the full composition question — resolving the external-input category alone dissolves most of this family's apparent blockage. |
| **Reach** — bounded transport, path-local, unrestricted addressing | **DEC-21** | Dune (bounded transport, physically correct), Wildfire (embers), Karst (path-local), Coastal (visibility) |
| **Geometry families** — network, layered 3-D | *unregistered* | Karst, Smouldering. Grid must not mean square grid. |
| **Dynamic connection strength vs existence** | *unregistered* | River braiding. Weight changes with state; the edge set does not. |
| **Multi-rate temporal semantics** | **DEC-3** | Six of eight span three or more orders of magnitude |
| **Generic helpers vs subject solvers** | *unregistered* | Coastal (visibility geometry) |
| **Validation standing as a searchable property** | *unregistered* | The family's widest internal spread: two entries checkable against controlled experiment, two uncheckable |
| **The cellular budget** | **DEC-24** | Per LAB-16 each Lab reports its own spending. This family spends mainly against *local interaction*: Dune and Karst both need reach beyond declared neighbours, and neither is asking frivolously. |

**The tenth fit question is no longer a proposal.** `../../01-core/labs.md` LAB-5.10 adopts the reducibility audit as a requirement, with LAB-6 requiring the regimes be named separately and LAB-7 requiring the audit be stated **per regime, never per subject**. Every Lab above is written to satisfy LAB-7: each has a *Reducible* and an *Irreducible* section rather than a verdict on the domain. The matching amendment to SCR-F §30 is proposed in that document, not applied.

### What this report deliberately does not do

No fit grades. No Reactor model chosen per Lab. No DEC-owned question resolved locally (§36.6, F-22). No final Cell properties. No Readers designed. No validation datasets selected. No market positioning.

---

## References

**[V]** checked against a primary or authoritative source during this revision. **[D]** described generically; background, not a citable claim.

1. **[V]** Rothermel, R. C. (1972). *A mathematical model for predicting fire spread in wildland fuels.* Res. Pap. **INT-115**. USDA Forest Service, Intermountain Forest and Range Experiment Station. — research.fs.usda.gov/treesearch/32533 *(First pass cited INT-116. Corrected.)*
2. **[V]** USDA Forest Service, Missoula Fire Sciences Laboratory (2022). *The Rothermel Fire Spread Model: A 50-year milestone in fire research.*
3. **[V]** Finney, M. A. (1998). *FARSITE: Fire Area Simulator — model development and evaluation.* Res. Pap. RMRS-RP-4. USDA Forest Service. *(Elliptical wavelet propagation from perimeter vertices, after Richards 1990.)*
4. **[V]** Drossel, B. & Schwabl, F. (1992). Self-organized critical forest-fire model. *Physical Review Letters* **69**(11), 1629–1632.
5. **[V]** Malamud, B. D., Turcotte, D. L., Guzzetti, F. & Reichenbach, P. (2004). Landslide inventories and their statistical properties. *Earth Surface Processes and Landforms* **29**, 687–711. *(Inverse-gamma; power-law exponent −2.40; exponential roll-over.)*
6. **[D]** Bak, P., Tang, C. & Wiesenfeld, K. (1987). Self-organized criticality: an explanation of 1/f noise. *Physical Review Letters* **59**, 381.
7. **[V]** Frette, V., Christensen, K., Malthe-Sørenssen, A., Feder, J., Jøssang, T. & Meakin, P. (1996). Avalanche dynamics in a pile of rice. *Nature* **379**, 49–52. *(Power-law avalanches for elongated grains only.)*
8. **[V]** Werner, B. T. (1995). Eolian dunes: computer simulation and attractor interpretation. *Geology* **23**, 1107–1110. *(Slab transport ~5 lattice sites; reproduces barchan, transverse, linear, star dunes in 3-D.)*
9. **[V]** Ashton, A., Murray, A. B. & Arnoult, O. (2001). Formation of coastline features by large-scale instabilities induced by high-angle waves. *Nature* **414**, 296–300.
   **9a. [V]** Erratum (2002), *Nature* **415**, 666 — third author corrected from "Arnault" to "Arnoult". *(The first pass reproduced the misspelling.)* See also Ashton & Murray (2006), *J. Geophys. Res. Earth Surface* **111**, parts 1 and 2.
10. **[V]** Cooper, J. A. G. & Pilkey, O. H. (2004). Sea-level rise and shoreline retreat: time to abandon the Bruun Rule. *Global and Planetary Change* **43**, 157–171.
11. **[V]** Leopold, L. B. & Wolman, M. G. (1957). *River channel patterns: braided, meandering and straight.* USGS Professional Paper **282-B**.
12. **[V]** Murray, A. B. & Paola, C. (1994). A cellular model of braided rivers. *Nature* **371**, 54–57.
13. **[V]** Dreybrodt, W. (1996). Principles of early development of karst conduits under natural and man-made conditions revealed by mathematical analysis of numerical models. *Water Resources Research* **32**(9). *(Fourth-order rate law near equilibrium; breakthrough 10⁴–10⁶ years.)* See also Dreybrodt (1990), *Journal of Geology* **98**(5).
14. **[V]** Turetsky, M. R. et al. (2020). Carbon release through abrupt permafrost thaw. *Nature Geoscience* **13**(2), 138–143.
15. **[V]** Page, S. E., Siegert, F., Rieley, J. O., Boehm, H.-D. V., Jaya, A. & Limin, S. (2002). The amount of carbon released from peat and forest fires in Indonesia during 1997. *Nature* **420**, 61–65. *(0.81–2.57 Gt C; 13–40% of mean annual global fossil fuel emissions.)*
16. **[V]** Rein, G. et al. (2008), on the critical moisture content for peat smouldering ignition: **125 ± 10% dry base**; once ignited a self-sustained front can propagate through wetter layers. See also Frandsen (1997). *(First pass gave no figure and guessed "a few hundred percent". Corrected.)*
17. **[V]** Liljedahl, A. K. et al. (2016). Pan-Arctic ice-wedge degradation in warming permafrost and its influence on tundra hydrology. *Nature Geoscience* **9**, 312–318.
18. **[D]** Bagnold, R. A. (1941). *The Physics of Blown Sand and Desert Dunes.* Methuen.
19. **[D]** SHALSTAB / SINMAP lineage of shallow-landslide susceptibility mapping (Montgomery & Dietrich 1994; Pack, Tarboton & Goodwin 1998).
20. **[D]** Dead fuel moisture timelag classes; CERC alongshore transport formula (USACE *Shore Protection Manual*); Stefan solution for phase-change front depth; Meyer-Peter–Müller bedload transport; angle-of-reach runout relations; eolian ripple wavelength from saltation trajectory length; dune celerity inverse to height.

---

## Non-claims

This report performs no fit reviews and establishes no fit. None of these Labs forecasts, predicts, or assesses anything in any real system. No output described here is suitable for operational, safety, engineering, environmental, or policy decisions. Mechanisms these Labs would generate are candidate explanations requiring domain validation in domain tooling (§41, §43). Standings in brackets are inherited from *A Card Catalog for Emergence* v0.1 §5 and are not re-derived; assessments are the author's judgment, carry no standing, and do not promote any entry.
