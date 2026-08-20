# 34. Battery Dendrite Lab

**Document class:** Lab Knowledge Brief · **Status:** draft
**Catalog:** SCR Lab Catalog v0.1 #34, Family E · **Standing:** ungraded
**Cites:** SCR-F v0.2 §11, §29, §30, §41; F-17
**Fit review (§30):** not performed

---

## The phenomenon

Charging a lithium battery moves lithium ions to the negative electrode. In a graphite anode they intercalate harmlessly between carbon layers. But if charging is too fast, too cold, or the cell is too full, lithium plates out as metal on the surface instead — and metal deposition from solution is unstable in the same way every diffusion-limited growth process is. A bump reaches fresher electrolyte, grows faster, becomes a spike.

Grown far enough, the spike bridges to the other electrode and short-circuits the cell. The stored energy discharges through the short, the cell heats, and in the worst case thermal runaway follows. This is the mechanism behind a significant class of battery fires.

It is also the barrier to the next generation of batteries. Lithium metal anodes would substantially increase energy density; they are not commercial precisely because dendrites form. The same problem afflicts solid-state cells, where lithium penetrates along grain boundaries and cracks in the ceramic electrolyte rather than growing through liquid.

## What the domain already knows

**There is a classical closed-form onset condition.** In a dilute binary electrolyte under high current, ion concentration at the electrode falls to zero after a characteristic time — **Sand's time** — after which the interface becomes unstable and dendrites initiate. Sand's expression scales inversely with the square of current density. Chazalviel's model in 1990 connected concentration depletion, space charge, and dendrite initiation *(attributions from memory, verify)*. Below the limiting current, growth is expected to be stable and mossy rather than dendritic.

**The instability is the familiar one.** Deposition limited by transport to the interface is Mullins–Sekerka unstable, exactly as in solidification (#29), tumour margins (#23), and biofilms (#25). Electrochemical deposition was in fact one of the classic experimental systems for studying diffusion-limited aggregation in the 1980s, producing textbook fractal deposits in thin-cell electrodeposition experiments.

**And the classical theory does not describe real cells.** Commercial electrolytes are concentrated, not dilute. The lithium surface is covered by a **solid electrolyte interphase** — a passivating film formed by electrolyte decomposition — whose mechanical and transport properties largely control where deposition occurs. Real deposits are frequently mossy, whisker-like, or dead-lithium fragments rather than the tree-like dendrites the name implies. Sand's time predicts onset in conditions no commercial cell operates in.

That gap is the single most important thing this Lab must know.

## Where the shortcut holds, and where it breaks

**Reducible.** Sand's time and limiting current in dilute solution. Linear stability onset for a transport-limited interface. Bulk capacity fade from lithium inventory loss. Diffusion-limited aggregation fractal dimension for the extreme case. Thermal runaway energetics once a short exists.

**Irreducible.** Essentially everything that governs real cells:

- **Where nucleation happens.** Deposition initiates at defects, at cracks in the interphase film, at grain boundaries, at points of high local current. Which sites activate depends on the specific arrangement of a heterogeneous film that itself formed stochastically.
- **The film's feedback loop.** Deposition strains and cracks the interphase; cracks expose fresh lithium; fresh lithium reacts and reforms film, consuming electrolyte; the reformed film is heterogeneous. This is a self-modifying substrate with memory across hundreds of cycles.
- **Cycle-to-cycle accumulation.** Dendrites that dissolve on discharge do not dissolve uniformly, leaving disconnected "dead lithium" and roughened surfaces that seed the next cycle worse. Cell failure is a slow accumulation over hundreds of cycles, not a single event.
- **Penetration in solid electrolytes.** Lithium filling a crack generates pressure that extends the crack — a coupled electrochemical–mechanical process, with the non-locality problem of #31 attached.
- **Whether a given cell fails.** Nominally identical cells fail at very different cycle counts. The distribution is wide and the tail is what safety engineering cares about.

**The lens, stated plainly.** This is a domain where **the analytic result exists, is famous, and does not apply to the case anyone cares about.** Sand's time governs dilute solutions at high current; commercial cells are concentrated, interphase-controlled, and cycled thousands of times. The reducible core is therefore large in the literature and nearly empty in practice — an unusual and favourable configuration for an instrument that studies mechanisms rather than deriving them.

## What a Cell would carry

A site in the electrode–electrolyte region: deposited lithium present, ion concentration, local potential or overpotential, interphase film thickness and integrity, and possibly accumulated damage. Bounded scalars; §13.1 met.

Layout is a grid, physically reasonable for a cross-section of an electrode surface. Two serious qualifications.

**The electric field is global.** Deposition rate depends on local overpotential, which depends on the potential field solved across the whole electrolyte given the current geometry of the deposit. Like elasticity in #31 and flow in #18, this is a globally-computed driver of a locally-applied rule. Diffusion-limited aggregation gets away with a local proxy (random walkers), which reproduces the morphology class; whether a local proxy preserves the *cycling* behaviour is unknown and is the Lab's central mechanism-fit question.

**Deposition and dissolution alternate.** Charge and discharge run the mechanism in opposite directions, and the asymmetry between them creates the dead lithium that drives failure. A Run that only deposits is modelling one half of the phenomenon.

## Honest strength assessment

*My assessment, not a fit review (§30). It carries no standing and does not promote this entry.*

**Plausible, with the highest stakes in Family E and a strong argument I would rank it above #29, #30, #32, and #33.**

The distinguishing feature is the mismatch between theory and practice. Most of Family E has mature theory covering the questions people ask; this one has mature theory covering conditions nobody operates in, and an urgent, funded, unsolved practical problem in the regime that matters. That is exactly the configuration where a cheap mechanism-supply instrument has room.

**The upside worth being excited about.** The interphase film is the crux and it is genuinely under-modelled: a heterogeneous, self-repairing, stochastically-formed layer that determines where deposition occurs and is modified by the deposition it controls. Asking **what local rules for film cracking, repair, and preferential deposition produce the observed transition from mossy to dendritic growth, and what makes accumulation across cycles benign or catastrophic** is a legitimate, ensemble-shaped question. Nobody can derive the answer; several groups are simulating candidate mechanisms one at a time.

The cycle-accumulation framing also suits the platform structurally. Failure here is not an event but a **distribution over hundreds of cycles**, and the safety-relevant quantity is the tail. That is a Study over many Runs, which is the platform's shape, and the failures-stay principle (F-14) is directly relevant: mechanisms that never produce failure are as informative as those that do.

Data is unusually good: operando X-ray tomography and cryo-electron microscopy now image real lithium deposits directly, and cycling data with failure statistics exists in quantity.

**The challenges, in order of severity.**

1. **Safety-critical credibility hazard, and it is severe.** Batteries catch fire. Any output resembling a safety assessment of a real cell chemistry would be dangerous and would be over-read. This Lab needs Family-H-strength non-claims language.
2. **The potential field is global**, and the local proxy's validity for cycling behaviour is unknown.
3. **The interphase chemistry is complex and poorly characterized**, so calibration targets are soft.
4. **Solid-state penetration adds mechanics**, inheriting #31's non-locality problem.
5. **Timescale spans a second-scale deposition event and a year of cycling.**
6. **Commercially sensitive domain** — much of the relevant data is proprietary.

## Non-claims

This Lab does not assess the safety, performance, or lifetime of any real battery or chemistry, does not bear on cell design or qualification, and produces nothing suitable for engineering or safety decisions (§41, §43).
