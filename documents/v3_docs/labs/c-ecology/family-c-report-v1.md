# Family C — Ecology
## Lab Knowledge Report v1

### Invasion Ecology · Forest Gap Dynamics · Pest Outbreak · Coral Reef Competition · Mycelial Networks · Seed Dispersal and Recruitment

**Document class:** Level 5 — Lab Papers (family report, pre-fit) · **Status:** draft
**Path:** `labs/c-ecology/family-c-report-v1.md`
**Catalog:** SCR Lab Catalog v0.1, Family C (entries 14–19)
**Framework:** `../../00-start-here/irreducibility-and-what-cellular-means.md`
**Conventions:** `../README.md` — four axes, Lab roles, visualization credibility class
**Reviewed against:** `../../01-core/labs.md` — LAB-5's ten fit questions, including LAB-6/LAB-7
**Supersedes:** first-pass briefs 14–19 in `../short-lab-definitions/`
**Responds to:** `../../critiques/SCR_Labs_11-20_Critique_v0.1.md`
**Cites:** SCR-F v0.2 §11, §15, §18.5, §29, §30, §38.6, §41–43; F-7, F-9, F-17 · LAB-5 to LAB-8, LAB-16 · DEC-1, DEC-3, DEC-21, DEC-24
**Fit reviews (§30):** none performed. **Nothing here establishes fit.**

---

## What this family is

Ecology gives SCR its best-posed Lab and two of its most useful architectural failures, which is an unusually informative combination.

Three things run through the family:

**Observation and state come apart, and it matters operationally.** An invasion has *established* populations and *detected* populations. A beetle outbreak has a living population now and visible tree mortality a year later. These are not interface concerns — they are separate experimental states, and the family supplies strong **non-security** evidence that limited and delayed observation is a general platform requirement rather than an adversarial special case. Three states may need representing: what the system actually contains, what an observer can detect, and what the Reactor records.

**Long-tail transport is the family's defining mechanism and its defining problem.** Four of six entries turn on rare long-distance events, and in every case the tail rather than the mean decides the outcome. This is the reach question (DEC-21) arriving with real consequence attached.

**The incumbents here are often peers, not shortcuts.** Ecology already does spatially explicit simulation. Family A mostly competed against closed forms; this family frequently competes against other simulations, which is a weaker pitch and must be said plainly.

**References.** **[V]** checked against a primary or authoritative source; **[D]** described generically, background only.

---

## Lab 14 — Invasion Ecology

| | |
| :--- | :--- |
| **Role** | **Flagship** mechanism-supply / management-Study Lab |
| **Catalog status** | Standalone Lab |
| **Standing** | [strong], inherited; not re-derived |
| **Abstraction level** | A habitat patch holding occupancy and suitability. *Lost at this level:* individual dispersal behaviour and within-patch demography. |
| **Falsifiable question** | Does a barrier or eradication strategy hold across the plausible range of dispersal mechanisms, or only under thin-tailed dispersal? |
| **Mechanism fit** | High |
| **Validation class** | **Direct observational** — annually mapped range expansions over a century |
| **Rediscovery risk** | Low |
| **Practical need** | High — agencies spend real money on barrier and eradication strategy |
| **Reach** | Neighbour-local **plus a fat-tailed jump that dominates the outcome** |
| **Topology** | Fixed |
| **Drivers** | Habitat suitability as **static World condition**; climate-driven shift would be an external input |
| **Visual credibility** | Class 1 — a front sweeping a rendered map reads as a forecast |

**The phenomenon.** A species arrives, establishes, and spreads. Sometimes as a smooth front at steady speed. Sometimes not at all like that: decades at low density then eruption; or disconnected satellite colonies that grow and coalesce so the range expands far faster than any front could travel; or advance that stops at an invisible line. Which you get changes what management does — a steady front can be met with a barrier, a jumping invasion cannot.

**The established shortcut, and it is famous.** Fisher and Kolmogorov–Petrovsky–Piskunov (both 1937) showed that a population with logistic growth and diffusion advances as a travelling wave at speed 2√(rD) [12]. **Skellam (1951)** applied diffusion theory to the muskrat's spread through central Europe from 1905, finding range expansion in concentric circles closely matching a theoretical population [1]. This is a textbook success.

**And the domain published exactly where it fails.** **Kot, Lewis and van den Driessche (1996)** showed with integrodifference equations that measured dispersal curves are typically leptokurtic rather than normal, that invasion speed is **extremely sensitive to the precise shape of the tail**, and that fat-tailed kernels and Allee effects provide alternative explanations for the accelerating spread observed in many invasions [2]. The failure of the shortcut is not conjecture here — it is a result.

**Reducible.** Front speed in homogeneous habitat with thin-tailed dispersal. Whether a population establishes at all. Equilibrium range extent under a suitability map — a per-cell calculation with no interaction.

**Irreducible.** Stratified dispersal, where long jumps found satellites that grow and merge, so spread rate depends on the *arrangement* of successful jumps rather than their frequency. Fragmented habitat, where crossing is a percolation question and near threshold the outcome turns on specific arrangement. Allee effects with heterogeneity, producing pinning geometry. Founder effects at the expanding edge — gene surfing, measured and real. Eradication timing, which depends on whether satellite colonies exist below detection.

**Correction from the first pass.** The claim that "everything management actually faces" lies outside Fisher–KPP is rhetorically effective and too broad — some real management scenarios are adequately approximated by front models. The defensible version:

> **Many of the management cases where strategy matters most — fragmentation, long-distance dispersal, Allee effects, hidden satellite colonies — sit outside the homogeneous Fisher–KPP regime.**

**The observation model.** A patch holding a small undetected population is computationally live and observationally silent. *Established* and *detected* are different states, and the gap between them is the operational crux: eradication succeeds or fails on colonies nobody has seen.

**Cell state.** *Persistent:* occupancy or density, established state, detected state, seed bank or propagule pressure. *Static:* habitat suitability. *Derived:* local colonization probability.

**Assessment.** *(judgment, no standing)* **Top-tier flagship candidate — probably the best-posed Lab in the catalog.** Nearly everything SCR wants is present: a famous closed-form baseline, a famous published boundary where it fails, real spatial locality, a long-range exception whose importance is known rather than guessed, hidden observational state, a century of mapped range data, an ensemble-shaped management question, and genuine negative-space value. Unlike Plankton (entry 13), the long-distance dispersal problem is **one mechanism class SCR must model honestly, not evidence that the whole substrate is wrong.**

---

## Lab 15 — Forest Gap Dynamics

| | |
| :--- | :--- |
| **Role** | Benchmark · negative-space research Lab |
| **Catalog status** | Standalone; possible merge with 19 under a broader forest spatial dynamics Lab |
| **Standing** | Ungraded |
| **Abstraction level** | A patch of forest floor, roughly one canopy footprint. *Lost at this level:* light geometry, individual-tree competition, and within-patch species coexistence. |
| **Falsifiable question** | Which local competition and dispersal rule families fail to maintain a rare species under a realistic disturbance history? |
| **Mechanism fit** | Good for gap dynamics, weak for light geometry |
| **Validation class** | **Direct observational, outstanding** — stem-mapped plots remeasured for decades |
| **Rediscovery risk** | Medium |
| **Practical need** | Research-support, not product |
| **Reach** | Neighbour-local plus seed shadow |
| **Topology** | Fixed |
| **Drivers** | Storms, drought, fire as **external input** |
| **Visual credibility** | Class 3 |

**The phenomenon.** A canopy tree falls; light reaches the floor for the first time in a century; suppressed saplings release and pioneers germinate. One stem wins the gap and closes it. A mature forest is a mosaic of such gaps at every stage, and the **gap-phase dynamic** is the standard account of how old-growth forests keep species diversity without any species winning outright. Gap *size* decides composition — small gaps favour shade-tolerant species already present, large gaps favour pioneers — so the disturbance size distribution determines the species mix.

**The established shortcut, and the incumbent is a peer.** **Botkin, Janak and Wallis (1972)** published JABOWA, the first individual-based tree demography model for mixed-species stands, simulating individual trees on small plots as a function of forest structure and environment [3]. It founded the "gap model" tradition, which is now forty years deep, calibrated against forest inventory, and extended by spatially explicit successors that track crown position and light interception [11].

**This matters for the pitch.** SCR would not be supplying mechanism to a field that lacks it. It would be supplying *more* mechanisms to a field with a good one — a weaker argument than in domains where the incumbent is an analytic shortcut with known limits, and one this Lab must make honestly.

**Reducible.** Successional sequence from shade-tolerance ordering. Mean stand basal area and biomass at equilibrium. Time to canopy closure for a gap of given size. Species composition as a function of the disturbance regime — a statistical argument, not a spatial one. Most forestry questions live here.

**Irreducible.** Gap coalescence, where adjacent falls produce an opening unlike the sum of separate gaps. Contagious windthrow — a tree exposed by an adjacent fall is likelier to fall next, which is what turns scattered mortality into blowdown patches. Seed shadow geometry, where which species can colonize depends on which adults are within range. Spatial storage of diversity.

**Correction from the first pass.** "Persistence of the rare cannot be shortcut" is too absolute — metapopulation theory, coexistence theory, and demographic stochastic models answer parts of that question analytically or statistically. The stronger claim:

> **Specific persistence under a spatially explicit disturbance history is not captured by aggregate equilibrium summaries.**

**A state-scale problem the Lab must confront early.** One dominant species per patch may be too coarse for the exact diversity question the Lab wants to ask. If species coexist *within* a patch, Cell state complexity rises quickly and pushes against the semantic ceiling. That is an abstraction-level decision, not a detail.

**Cell state.** *Persistent:* canopy state, occupant species and size, time since disturbance, seed bank composition. *Derived:* light availability.

**Assessment.** *(judgment, no standing)* **Plausible benchmark and research-support Lab; not a first-wave product opportunity.** The data is exceptional — stem-mapped censuses of hundreds of thousands of individually tagged trees, remeasured over decades — and the genuinely novel contribution is negative space in a contested coexistence literature.

---

## Lab 16 — Pest Outbreak

| | |
| :--- | :--- |
| **Role** | Mechanism-supply · hidden-observation Lab |
| **Catalog status** | Standalone Lab |
| **Standing** | Ungraded |
| **Abstraction level** | **A forest stand, annual step.** *Lost at this level:* within-season mass-attack mechanics at individual-tree scale — see the scoping problem below. |
| **Falsifiable question** | Which local conditions produce front pinning or outbreak collapse while susceptible host remains? |
| **Mechanism fit** | Good at the landscape level |
| **Validation class** | **Direct observational** — annual aerial mortality mapping over decades |
| **Rediscovery risk** | Low |
| **Practical need** | High |
| **Reach** | Neighbour-local plus long-distance flight founding satellites |
| **Topology** | Fixed |
| **Drivers** | Drought and winter cold as **external input** — and they set the threshold |
| **Visual credibility** | Class 1 |

**The phenomenon.** Bark beetles live at densities nobody notices, then in some years and some stands cross a line and kill healthy trees across millions of hectares. The mechanism behind the threshold is **mass attack**: a healthy conifer floods a single boring beetle with resin, but attacking beetles release aggregation pheromone and past some number of simultaneous attackers the defence is exhausted. Per-capita success *increases* with density, producing bistability — below threshold, endemic indefinitely; above it, eruption sustained while host remains.

**Reducible.** The bistability itself — a well-mixed model gives the threshold and the two stable states. Host susceptibility from stand age and composition, a per-cell map. Winter mortality from temperature. Total mortality given duration and host availability.

**Irreducible.** Where the eruption starts — bistable systems tip locally first, and which stand crosses depends on the coincidence of susceptible host, drought-weakened neighbours, and enough local beetles. Propagating bistable fronts, which can advance, retreat, or **pin** on heterogeneous host — directly relevant to whether an outbreak stops at a valley. Satellite coalescence from long-distance flight. Feedback onto the host, since post-outbreak stands are non-susceptible for decades and the system carries memory that steers the next outbreak.

**The scoping problem the Lab must resolve, and it cannot dodge it.** Mass attack happens at individual-tree scale within a season. A stand-level Cell with annual steps can represent the landscape front while abstracting away the very mechanism that creates the threshold. The Lab must state whether:

- the threshold is an **input** — a known local law supplied to the model; or
- SCR is expected to **discover** the mass-attack mechanism itself.

**It cannot honestly do both at the same abstraction level**, and choosing is a fit-review obligation rather than an implementation detail.

**The observation model, and it is the catalog's cleanest example.** An endemic population is present, viable, and invisible. Aerial survey detects trees that are *already dead*, so observation lags the mechanism by roughly a year. A view keyed to visible mortality shows a landscape that was true last season — §38.6 with a management consequence attached.

**Cell state.** *Persistent:* host density or basal area, tree defensive capacity, beetle population, time since mortality. *Derived:* attack pressure, visible mortality (the observable state, lagged from the true state).

**Assessment.** *(judgment, no standing)* **Strong candidate, especially as a hidden-observation and bistable-front Lab.** The domain question is genuinely ensemble-shaped: nobody credible claims to predict which stand erupts, but agencies want to know whether a containment strategy works across plausible mechanisms. There is also a live scientific question with real stakes — **why do outbreaks stop, while susceptible trees remain?** — where candidate mechanism supply is defensible.

---

## Lab 17 — Coral Reef Competition

| | |
| :--- | :--- |
| **Role** | Canonical-model challenge · hypothesis-test Lab |
| **Catalog status** | Standalone, **narrowly scoped** |
| **Standing** | Ungraded |
| **Abstraction level** | A patch of hard substrate holding an occupant type. *Lost at this level:* grazer movement, larval transport, and colony three-dimensional structure. |
| **Falsifiable question** | Does spatially clustered grazing destroy the canonical coral–algae bistability? |
| **Mechanism fit** | Good for overgrowth; poor for grazers and larvae |
| **Validation class** | **Direct observational** — photo-quadrat time series over decades |
| **Rediscovery risk** | Low for the spatial question |
| **Practical need** | Scientific, not predictive |
| **Reach** | Neighbour-local for overgrowth; long-range for larvae |
| **Topology** | Fixed |
| **Drivers** | Temperature, acidification, fishing as **external input** — and they dominate real outcomes |
| **Visual credibility** | Class 1 — reef decline is emotionally and politically charged |

**The phenomenon.** A reef is a competition for hard substrate. Corals hold space by being there; fleshy macroalgae grow fast and overgrow coral given the chance; herbivores crop algae and leave space for coral recruits. Remove the grazers, add nutrients, or kill coral with bleaching, and the balance flips — and the new state is self-reinforcing, because algae inhibit coral recruitment. Reefs that flip frequently stay flipped for decades.

**The established shortcut.** **Mumby, Hastings and Edwards (2007)** modelled coral–algal–turf competition with grazing and showed that Caribbean reefs became susceptible to alternative stable states once the 1983 mass mortality of the urchin *Diadema antillarum* confined most grazing to parrotfishes; they defined critical thresholds of **both grazing and coral cover** beyond which resilience is lost [4]. Hughes (1994) is the observational anchor for the Caribbean shift [10].

Given grazing intensity and growth rates, this two- or three-variable model says whether coral-dominance is stable, whether algae-dominance is stable, whether both are, and where the tipping points sit. Hysteresis follows. **The analysis is complete for a well-mixed system.**

**The framing is contested, and the Lab must know it.** A serious critique argues many observed reef declines are better explained by continuous forcing and disturbance than by alternative stable states, and that demonstrating true bistability in the field is very hard [11].

**Irreducible.** Grazing halos — herbivores feed near shelter and avoid open sand, so grazing pressure is a *spatial field* determined by habitat arrangement, and the well-mixed grazing parameter averages over exactly that. Local refugia and whether their larvae reach recovering areas. Overgrowth as a boundary process, which makes perimeter-to-area ratio matter and colony shape a variable no mean-field model contains. Disturbance patchiness determining the recovery path.

**The scoping statement this Lab must make explicitly.** There is an apparent inconsistency in saying the dominant real drivers are global and outside the abstraction while also claiming spatial competition is scientifically meaningful. It is not actually contradictory, but it must be scoped in writing:

> **We are not explaining reef futures. We are testing the robustness of one canonical local competition hypothesis under spatial structure.**

That makes the narrowness a strength rather than an evasion.

**On grazers.** Treating grazing pressure as a **precomputed external field** is sufficient for the first Study and avoids introducing an Agent World prematurely. Only if grazer *movement itself* becomes the hypothesis does the Lab need agents — a DEC-24 expenditure that should not be made casually.

**Cell state.** *Persistent:* occupant type, coral colony age or size, recruitment state. *External field:* grazing pressure. *Derived:* overgrowth probability.

**Assessment.** *(judgment, no standing)* **Plausible-to-strong as a hypothesis-testing Lab; weak as a predictive domain Lab.** The research angle is sharp — *what happens to the canonical bistability when competition becomes spatial?* — and if it disappears easily under clustered grazing, that is a finding about a widely used model rather than a claim about any reef.

---

## Lab 18 — Mycelial Network

| | |
| :--- | :--- |
| **Role** | **Dynamic-topology architecture stress test** |
| **Catalog status** | Architecture-test Lab; weak standalone domain case |
| **Standing** | Ungraded |
| **Abstraction level** | **Unresolved and consequential** — a substrate patch and a network segment are not interchangeable representations. |
| **Falsifiable question** | Does a local approximation to flow reinforcement reproduce measured network transport efficiency and damage resilience? |
| **Mechanism fit** | **Blocked on two architectural questions** |
| **Validation class** | **Direct experimental** — fungal networks grow on agar in weeks and are directly imaged |
| **Rediscovery risk** | Low |
| **Practical need** | Low |
| **Reach** | Path-local, over a topology the mechanism itself builds |
| **Topology** | **Constructed** — the defining case |
| **Drivers** | Resource distribution as **static World condition** |
| **Visual credibility** | Class 3 |

**The phenomenon.** A fungus growing through soil is a search. Hyphal tips extend, branch, and fuse; where the network finds food the connecting cords thicken and carry resource back; where it finds nothing the branches are abandoned and reabsorbed. Two features make it distinctive among growth processes: the network **fuses**, creating cycles, so it is not a tree; and it **withdraws**, reclaiming material, so growth is not monotone.

**The established shortcut.** Optimal network problems have answers — shortest path, minimum spanning tree, and Steiner tree are solved or well-approximated. **Tero and colleagues (2010)** showed *Physarum polycephalum* forms networks with comparable efficiency, fault tolerance, and cost to the Tokyo rail system, and gave a flow-reinforcement model in which tubes carrying more flow thicken while others decay [5]. Fungal network work is a separate literature that images and quantifies cord-forming networks against theoretical optima [11].

**Correction from the first pass — twice.**

The first pass said that when terminals must be found rather than given, "running is the only method." Too strong: search and foraging problems have algorithmic methods too. The real distinction:

> **The organism does not receive the complete optimization problem in advance. Topology is created online, under partial information and resource constraints.**

And the first pass leaned on *Physarum* as evidence about fungi. It flagged the problem; the deep paper must actually enforce it. **A slime mould is not a fungus** and the Tokyo result is not fungal evidence.

**Irreducible.** Foraging without knowing where the food is — the network built is a record of the search, and which regions get explored before resources run out is path-dependent. Reinforcement and withdrawal together, making the process non-monotone: removing one connection changes flow everywhere, which changes what decays next. Damage rerouting, which depends on the cycle structure earlier growth happened to create.

**The two architectural questions this Lab exists to force.**

**Constructed topology.** The mechanism literally creates and destroys the network it later acts through. That is a distinct class from the fixed topology of a lattice and the state-weighted topology of river flow routing (entry 6). If SCR supports it, the Run Contract must say who may create connections, which Cell types may connect, what the connection-state ceiling is, whether creation counts against budgets, whether topology is future-relevant state, and how Readers compare networks whose node and edge counts change. **This is not a small feature**, and it is a DEC-24 expenditure.

**Globally computed local drivers.** Determining flow through each cord requires solving a network flow problem over the whole structure — the Physarum model does exactly that every step. The framework's helper boundary applies: a generic global constraint the Reactor computes over a domain-neutral property may be acceptable; a bespoke fungal transport model is a subject solver and would make SCR a wrapper around domain simulators.

**Cell state.** *Persistent:* hyphal presence and cord thickness, local resource, time since reinforcement. *Derived or globally computed:* flow carried — and *which* it is decides whether the Lab is viable.

**Assessment.** *(judgment, no standing)* **Keep as an architectural stress-test Lab even if domain fit remains weak.** The domain case is thin — small audience, optimization framing covers much of it, and the famous result belongs to a different organism. But the reason it fails is the valuable part, and it probes two boundaries that recur in supply chains, routing, and developmental biology. **A Lab that cannot fit without spending the last of the budget may be telling the platform something more valuable than a Lab that fits comfortably** (LAB-16).

---

## Lab 19 — Seed Dispersal and Recruitment

| | |
| :--- | :--- |
| **Role** | **Reach and locality decision case**; likely merge candidate |
| **Catalog status** | **Do not build standalone.** Merge with 14 or 15, or retain as a decision-forcing brief. |
| **Standing** | Ungraded; I would grade it **weak** as a standalone Lab |
| **Abstraction level** | A patch of ground holding establishment state. *Lost at this level:* disperser behaviour, which is not a kernel. |
| **Falsifiable question** | Under multi-generation feedback, which local recruitment rules maintain species coexistence that mean-field models forbid? |
| **Mechanism fit** | The central mechanism is **non-local by definition** |
| **Validation class** | Direct observational, but requires decades of census |
| **Rediscovery risk** | High — the single-generation case is a convolution |
| **Practical need** | Low as a standalone |
| **Reach** | **The reach question in its purest form** |
| **Topology** | Fixed |
| **Drivers** | Dispersal kernel — **and what kind of thing that is, is the open question** |
| **Visual credibility** | Class 3 |

**The phenomenon.** A plant cannot move, so its whole spatial strategy is executed once, by its seeds. The landing distribution is usually sharply peaked near the parent with a long tail. Near the parent, seed density is highest and so is mortality, because specialized herbivores and pathogens concentrate where their host is dense — the **Janzen–Connell hypothesis** (both 1970–71), the standard candidate explanation for why tropical forests hold so many species [11].

**Reducible, and this is the problem.** Expected seed shadow from a known adult distribution is a **convolution**. Multiply by a survival function and you have expected recruitment. Mean dispersal distance, tail behaviour, and colonization probability at distance are closed-form for standard kernels. Spatial point-process theory handles clustered patterns and pair correlation analytically — **the domain already has a mathematics for this.**

**Irreducible.** Multi-generation feedback, where this generation's recruits become next generation's parents so the adult map producing the seed shadow was itself produced by earlier seed shadows. Multi-species Janzen–Connell, where the contested sufficiency question is about dynamics rather than equilibrium. Disperser behaviour, which does not follow a kernel — it follows an animal that visits fruiting trees, moves along routes, and defecates at perches, producing structured clustering no kernel captures.

**Correction from the first pass.** The first pass asserted that "a kernel is a World property, not a mechanism." That is not obviously true, and it should not have been settled casually. A dispersal kernel can be a fixed transport rule, a Plugin behaviour, an external stochastic operator, or the emergent result of agent behaviour — **and which it is depends on the hypothesis being tested.** That ambiguity is not a defect in the brief; it is exactly the architectural question this Lab exposes, and it belongs to DEC-21 rather than to any Lab document.

**Why it is the purest reach case.** Six entries across Families A–C need long-range transport — wildfire spotting, dune saltation, invasion satellites, beetle flight, and this. In every other one it is a complication at the edge of the phenomenon. **Here it *is* the phenomenon**, so the question cannot be avoided or approximated away. It is the cheapest place to force a decision and the hardest place to fudge one.

**Cell state.** *Persistent:* established occupant and species, seed bank by species. *Static:* habitat suitability. *Derived:* local pathogen or seed-predator pressure, expected seed rain.

**Assessment.** *(judgment, no standing)* **Do not build as a standalone early Lab. Retain as a reach and locality decision case, or merge with Invasion (14) or Forest Gap Dynamics (15).** Its strongest contribution is forcing the reach question, and that may be reason enough to keep the brief even if the Lab is never built. The document's willingness to recommend its own merger is the right instinct and should be preserved rather than argued away.

---

## Family findings

### The observation model — general, not adversarial

Entries 14 and 16 supply the family's most transferable platform lesson. A Lab may need to represent three distinct things:

| State | Meaning |
| :--- | :--- |
| **True state** | What the simulated system actually contains |
| **Observable state** | What an observer or participant can detect |
| **Recorded state** | What the Reactor knows and stores |

Invasion distinguishes *established* from *detected*. Pest outbreak distinguishes the living beetle population from visible tree mortality a year later. **These are separate experimental states, and ecology provides strong non-security evidence that the distinction is general** — limited and delayed observation must not be treated as a security-only feature (§18.5).

### Catalog governance: not every Lab is a product commitment

This family is the first where consolidation is worth recommending, and the catalog should be able to record more outcomes than *fits* and *fails*:

- standalone Lab;
- sub-Lab or mechanism profile inside a broader Lab;
- benchmark-only Lab;
- architecture stress test;
- rejected fit.

Candidate consolidations from this batch: **Seed Dispersal (19) into a broader dispersal family with Invasion (14)**, or into Forest Gap Dynamics (15) if the real interest is multi-generation coexistence. Do not merge merely to reduce the count — but sixty Labs should not become sixty product commitments, and the catalog should be allowed to discover that some ideas belong together.

### What this family demands of the platform

| Question | Owner | Raised by |
| :--- | :--- | :--- |
| **Reach** — fat-tailed transport where the tail decides the outcome | **DEC-21** | 14, 16, 19. Entry 19 is the purest forcing case. |
| **Topology classes** — fixed / state-weighted / **constructed** | *unregistered* | 18. Constructed topology is a distinct class needing its own Run Contract terms. |
| **Observation model** — true / observable / recorded | *unregistered* | 14, 16. General, not adversarial. |
| **Generic helpers vs subject solvers** | *unregistered* | 18 — network flow |
| **Abstraction-level declaration** | *unregistered* | 15 (patch vs tree), 16 (stand vs tree), 17 (substrate vs grazer), 18 (patch vs segment) |
| **Agent participants** | **DEC-24** | 17 grazers, 19 dispersers. Both avoidable at first via precomputed external fields. |
| **Catalog governance: merge, demote, benchmark-only** | *unregistered* | 13, 19 |
| **Cell state scale under within-patch coexistence** | **CELL ceiling** | 15 |

### Build priority within the family

**Tier A.** **Invasion Ecology** — flagship; best-posed Lab in the catalog. **Pest Outbreak** — excellent Study shape, good data, the cleanest hidden-observation lesson.

**Tier B.** **Coral Reef Competition** — strong hypothesis test, weak prediction position, needs its scoping statement in writing. **Forest Gap Dynamics** — good data and real negative space, but the incumbent is a peer.

**Tier C — architecture value exceeds domain value.** **Mycelial Network** — the constructed-topology stress test. **Seed Dispersal** — the reach forcing case; merge candidate.

---

## References

**[V]** checked against a primary or authoritative source. **[D]** described generically; background, not a citable claim.

1. **[V]** Skellam, J. G. (1951). Random dispersal in theoretical populations. *Biometrika* **38**, 196–218. *(Muskrat spread through central Europe from 1905 in concentric circles, matching a theoretical population.)*
2. **[V]** Kot, M., Lewis, M. A. & van den Driessche, P. (1996). Dispersal data and the spread of invading organisms. *Ecology* **77**(7). *(Measured dispersal curves are leptokurtic, not normal; invasion speed is extremely sensitive to the tail; fat tails and Allee effects are alternative explanations for accelerating spread.)*
3. **[V]** Botkin, D. B., Janak, J. F. & Wallis, J. R. (1972). Some ecological consequences of a computer model of forest growth. *Journal of Ecology* **60**, 849–872. *(JABOWA — the first individual-based tree demography model for mixed-species stands; founded the gap-model tradition.)*
4. **[V]** Mumby, P. J., Hastings, A. & Edwards, H. J. (2007). Thresholds and the resilience of Caribbean coral reefs. *Nature* **450**(7166), 98–101. *(Alternative stable states after the 1983 Diadema antillarum mortality confined grazing to parrotfishes; critical thresholds of both grazing and coral cover.)*
5. **[V]** Tero, A. et al. (2010). Rules for biologically inspired adaptive network design. *Science* **327**(5964), 439–442. *(Physarum networks comparable to the Tokyo rail system in efficiency, fault tolerance, and cost.)* **Physarum is a slime mould, not a fungus.**
6. **[D]** Fisher, R. A. (1937); Kolmogorov, A. N., Petrovsky, I. G. & Piskunov, N. S. (1937) — the travelling-wave speed 2√(rD).
7. **[D]** Janzen, D. H. (1970); Connell, J. H. (1971) — distance- and density-dependent recruitment mortality.
8. **[D]** Hughes, T. P. (1994). Catastrophes, phase shifts, and large-scale degradation of a Caribbean coral reef. *Science* **265**.
9. **[D]** SORTIE and the spatially explicit successors to JABOWA; forest-dynamics plot network (stem-mapped censuses).
10. **[D]** Critiques of the alternative-stable-states framing for reef decline; Fricker and Boddy on fungal network quantification; spatial point-process theory for recruitment patterns.

---

## Non-claims

This report performs no fit reviews and establishes no fit. None of these Labs predicts the spread of any species, assesses invasion or outbreak risk, models any real forest or reef, or bears on conservation, forestry, quarantine, fisheries, or regulatory decisions (§41, §43). Standings in brackets are inherited from *A Card Catalog for Emergence* v0.1 §5 and are not re-derived; assessments are the author's judgment, carry no standing, and do not promote any entry.
