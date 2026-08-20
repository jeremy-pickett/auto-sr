# 36. Crowd Egress Lab

**Document class:** Lab Knowledge Brief · **Status:** draft
**Catalog:** SCR Lab Catalog v0.1 #36, Family F · **Standing:** **[strong]** (inherited, not re-derived)
**Cites:** SCR-F v0.2 §11, §29, §30, §41; F-17
**Fit review (§30):** not performed

---

## The phenomenon

People leaving a room through a door do not form an orderly queue. They form an **arch** — a load-bearing structure of bodies pressing around the opening, in which each person is held in place by the others, and through which flow is intermittent rather than steady. The arch collapses, a burst of people passes, and it reforms.

At higher density the behaviour gets worse in a specific and counterintuitive way. **Faster is slower**: people trying harder to escape produce more friction and jamming at the exit, and total evacuation time increases. Above a further density threshold the crowd stops behaving like a flowing medium at all and develops involuntary shockwaves — "crowd turbulence" — in which people are moved by pressure from behind rather than by their own steps. This is the regime in which crowd disasters kill, and they kill by compressive asphyxia rather than by trampling.

The relevance is direct: this behaviour determines exit width requirements in building codes, and it determines whether a venue's crowd management plan works.

## What the domain already knows

**Two model families dominate, and both are established.** The **social force model** (Helbing and Molnár, 1995) treats pedestrians as particles with attraction to their goal and repulsion from others. **Floor field cellular automata** (Burstedde, Klauck, Schadschneider, and Zittartz, 2001) discretize space into cells and let pedestrians hop according to a static field encoding distance to the exit and a dynamic field encoding where others have recently walked — a stigmergic trail *(attributions from memory, verify)*. The floor field model is a genuine CA and is widely used.

**Faster-is-slower was published as a modelling result and then confirmed.** Helbing, Farkás, and Vicsek's 1998–2000 work on escape panic predicted that increased desired speed lowers flow through a bottleneck, and the effect has since been reproduced experimentally, including with granular analogues and with animals.

**The fundamental diagram is the reducible core.** Pedestrian flow versus density has a measured, roughly universal shape, and specific flow rates through doors — persons per metre of width per second — are tabulated. Fruin's level-of-service classification from the 1970s remains the practical vocabulary. **Building codes are calibrated on these numbers.**

**Crowd disasters have been analysed from video.** Helbing's analysis of the 2006 Hajj disaster identified the transition from laminar to stop-and-go to turbulent flow directly from crowd video, which is one of the more sobering pieces of empirical work in the field.

## Where the shortcut holds, and where it breaks

**Reducible.** Total evacuation time for a given population through a given total exit width, at the tabulated specific flow rate. Queue formation times. Density from area and headcount. Whether a plan meets code. **This is what egress engineering actually computes, and it is adequate for compliance.**

**Irreducible.** What the flow-rate calculation assumes away:

- **Arch formation and intermittency.** Flow through a narrow exit is not a rate; it is a sequence of bursts and blockages, and the burst size distribution is heavy-tailed. Whether a long blockage occurs during an evacuation is a tail question, not a mean question.
- **Faster-is-slower.** The effect is nonlinear and arises from the interaction of individual behaviour with local geometry. It cannot be derived from a fundamental diagram, and it inverts the intuition the diagram encourages.
- **Geometry interaction.** Where a column, a corner, or a counterflow appears changes everything locally. The famous, contested, and repeatedly-reproduced result that **an obstacle placed in front of an exit can increase flow** by breaking up the arch is exactly this kind of finding — non-obvious, geometric, and invisible to a rate calculation.
- **Route choice under partial information.** People choose the exit they came in by, not the nearest. This is a behavioural fact that dominates real evacuations and is not a physics parameter.
- **The transition to turbulence.** Where and when a dense crowd stops being a flow and starts being a pressure medium is a threshold crossing on a specific configuration, and it is where people die.

**The lens, stated plainly.** This domain has an unusually clean and consequential split: **codes are written on the reducible answer, and disasters happen in the irreducible regime.** Nobody dies because a fundamental diagram was slightly wrong. People die because a crowd configuration crossed into a state the diagram does not describe. That is a strong argument for an instrument aimed at the second regime — and simultaneously the reason the safety hazard here is at maximum.

## What a Cell would carry

A floor cell: occupancy, and the floor field values (static distance-to-exit, dynamic recent-traffic trace). Occupants carry a desired direction and possibly a patience or panic level. Bounded and small; §13.1 met.

Layout is a grid, and it is standard practice in this field — floor field CA use square lattices with cells roughly 40 cm on a side, the space a standing person occupies. That is a rare case of a **physically motivated cell size**.

Two honest qualifications. **People are not lattice-aligned**, and diagonal movement on a square grid produces speed anisotropy that matters when comparing routes. And crucially, **the dangerous regime is a contact-mechanics problem**: in crowd turbulence, bodies transmit force, and force in a packed medium is transmitted through chains that are not nearest-neighbour interactions. That is the same non-locality that damages #31, and it appears precisely in the regime that kills.

## Honest strength assessment

*My assessment, not a fit review (§30). It carries no standing and does not promote this entry.*

**Strong, the inherited grade is right, and this is the catalog's second calibration anchor — with the highest duty of care of any Lab outside Family H.**

The case is unusually complete. The canonical model of the domain is a cellular automaton. The cell size is physically meaningful. The phenomenon is operationally used — egress design is a real profession using these tools. Controlled experiments exist: people have been paid to walk through corridors and doorways under instrumentation, repeatedly, in Germany and Japan and elsewhere, producing quantitative flow and trajectory data. Almost nothing else in this catalog has *controlled human experiments* as reference data.

**The upside worth being excited about.** The obstacle-before-the-exit result is the perfect illustration of what this platform is for: a counterintuitive, geometry-dependent, mechanism-level finding that a flow calculation cannot produce and that a corpus of many mechanisms could surface systematically. "Which local behavioural rules make an obstacle help, and which make it hurt" is a real question, it is contested in the literature, and it is ensemble-shaped.

The negative space is also unusually valuable: venue designers make irreversible physical decisions. Knowing that a class of layout never produced improved flow under any behavioural rule tried is directly useful, and no literature publishes failed layouts.

**The challenges, in order of severity.**

1. **Life-safety credibility hazard — the highest in the catalog outside Family H.** People design real evacuation routes. Any output that looks like an egress assessment could contribute to a decision that kills someone. This Lab must carry non-claims language at maximum strength, and the temptation to soften it will be strong because the domain is *operationally used*, which makes SCR look adjacent to legitimate practice in a way it is not.
2. **The dangerous regime is contact mechanics**, and force chains are not local interactions.
3. **Behaviour dominates and behaviour is not physics.** Route choice, group cohesion, and the tendency to return the way you came are the real drivers, and they are not local rules in any clean sense.
4. **Panic is largely a myth** in the crowd-science literature — real crowds are more cooperative than models assume, and a Lab that generates "panic" mechanisms will be modelling folklore.
5. **Established, validated incumbents** in both social force and floor field traditions.

## Non-claims

This Lab does not assess the safety of any real venue, does not evaluate evacuation plans, does not inform building design or code compliance, and produces nothing suitable for any life-safety decision (§41, §43).
