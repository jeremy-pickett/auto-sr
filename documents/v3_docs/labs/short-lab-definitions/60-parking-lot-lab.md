# 60. Parking-Lot Lab

**Document class:** Lab Knowledge Brief · **Status:** draft
**Catalog:** SCR Lab Catalog v0.1 #60, Family I · **Standing:** **[insane]** (inherited, not re-derived)
**Cites:** SCR-F v0.2 §11, §15, §29, §30, §41; F-17
**Fit review (§30):** not performed

> **This entry is retained deliberately as the catalog's boundary marker.** It is not a candidate. It exists so that the platform's edge has a named location, and so the fit review has a case where the correct answer is obviously "no." SCR-F §30 treats a failed Lab as useful evidence about SCR's boundary; this is the clearest available instance.

---

## The phenomenon

Cars enter a car park, drivers look for a space, and occupancy patterns form — spaces near the entrance and near the shop door fill first, distant rows stay empty until the lot is nearly full, and there are waves of arrival and departure through a day.

Superficially this looks like an occupancy field evolving on a grid, with local rules about which space a driver takes.

## What the domain already knows

There is a parking literature and it is mostly not about this. It concerns pricing (the argument that on-street parking should be priced to maintain a target vacancy rate), search traffic (a substantial fraction of urban congestion is drivers cruising for parking), demand estimation, and facility sizing. These are economics and operations problems and they are addressed with those tools.

Where individual choice is modelled at all, it is modelled as **discrete choice**: a driver evaluates the available options against a utility function combining walking distance, search time, and cost, and picks the best. That framework is standard in transport economics and it fits, because it matches what drivers actually do.

## Why this fails, precisely

The catalog's stated reason is the correct one: *"drivers decide using global information — entrance location, visible vacancy across the whole lot — so a local-rule model of it is a diorama, not a mechanism."*

It is worth stating the failure in the terms this catalog has been using throughout, because doing so makes the boundary sharper.

**The interaction structure is not the spatial adjacency.** A driver's choice is not influenced by the cars in adjacent spaces. It is influenced by the position of the building entrance, the visible extent of vacancy across the whole lot, and the driver's plan. Adjacency in the model does not correspond to influence in the world, which is the failure of the position paper's selection rule at its most direct.

**There is no local mechanism to be irreducible about.** Throughout this catalog the interesting cases are those where a local rule, iterated, produces something no shortcut reaches. Here there is no local rule to iterate. Occupancy is the aggregate of independent decisions each made against a global view. Aggregate independent choices are describable statistically — occupancy by distance from the entrance is a curve, and it can be fitted.

**Where computation is genuinely required, it is optimization.** Assigning drivers to spaces to minimize total walking is an assignment problem with a polynomial algorithm. Cruising-for-parking dynamics is a queueing and search problem with its own tractable treatments.

So the domain fails on all three axes this catalog has used: the topology is wrong, the mechanism is not local, and the residual computation is a solved optimization rather than an irreducible process.

## The distinct rejection reasons this catalog has now named

This entry's value is as the terminal case in a set. Writing the sixty briefs surfaced **five structurally different reasons a Lab fails**, and it is worth recording them here because a catalog that can distinguish them is a better instrument than one that only says "poor fit":

1. **The agents use global information.** Decisions depend on a view no local participant has. *This entry; also #39's central scheduler.*
2. **The driving physics is a global solve.** The mechanism is local-looking but its driver is computed over the whole World — power flow, hydraulics, elasticity, network flow. *#42, #43, #31, and partly #18 and #34.*
3. **The mathematics is already closed-form and the real problem is measurement.** *#51; also the reducible cores of #30 and #33.*
4. **The substrate is non-stationary.** The system being modelled changes faster than evidence about it accumulates. *#49, and partly #50.*
5. **The process is a plan, not a phenomenon.** Someone designed the mechanism, so there is nothing to infer. *#53, #44, and #39 again.*

Parking lots fail on the first, most cleanly of any entry. That is the job this brief exists to do.

## What a Cell would carry

A parking space: occupied or vacant, distance to entrance, time of occupancy. This is trivially bounded and it is not the problem. **A Lab can meet §13.1 comfortably and still be a poor fit**, and stating that here is useful: the computational ceiling is a necessary condition, not a sufficient one, and the fit review should not be reassured by passing it.

## Honest strength assessment

*My assessment, not a fit review (§30). It carries no standing.*

**Insane, as inherited, and the grade should not be softened.**

There is no narrow framing that rescues this. Every other weak entry in this catalog has some residue worth stating — #57 has superspreading, #58 has co-evolving networks, #59 has agent-plus-field architecture, #51 has deletion racing re-derivation. This one has nothing, and that is precisely its usefulness. A boundary needs a point that is unambiguously outside it.

**The upside worth being excited about.** Only one, and it is about the catalog rather than the domain: **an honest catalog needs a floor.** Sixty entries in which every domain turns out to be interesting under some framing would be evidence of a reviewer who cannot say no, and would make the [strong] grades meaningless. This entry is the calibration that gives the other fifty-nine their scale.

It also demonstrates a discipline the platform claims and should be seen to practise: SCR-F §30 says Labs are allowed to fail their fit reviews, and §41–§43 insist the platform makes fewer claims rather than more. Retaining an entry solely to mark where the approach stops is that discipline made visible.

**The challenges.** Not applicable. The correct action is to build nothing and to keep the entry as a reference point.

## Non-claims

This Lab does not model any real car park, does not inform facility design, pricing, or operations, and is retained solely as a boundary marker (§30, §41, §43).
