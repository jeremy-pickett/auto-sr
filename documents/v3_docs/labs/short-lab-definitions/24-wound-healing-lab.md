# 24. Wound Healing Lab

**Document class:** Lab Knowledge Brief · **Status:** draft
**Catalog:** SCR Lab Catalog v0.1 #24, Family D · **Standing:** ungraded
**Cites:** SCR-F v0.2 §11, §29, §30, §41; F-17
**Fit review (§30):** not performed

---

## The phenomenon

Make a hole in a sheet of epithelial cells and it closes. Cells at the edge stop being inhibited by neighbours on that side, start crawling into the gap, divide to replace themselves, and stop when they meet cells coming the other way. The tissue is continuous again.

Two mechanisms compete for credit and both are real. In small wounds, cells at the margin assemble a ring of contractile filaments around the hole and pull it shut — the **purse string**. In larger wounds, cells crawl, and the leading edge is not smooth: some cells become **leaders**, protruding ahead and dragging a file of followers behind them, so the closing edge develops fingers.

The stopping rule is what makes this a genuinely local system. Cells stop moving and dividing when surrounded — **contact inhibition** — and the failure of exactly that rule is one of the defining features of cancer.

## What the domain already knows

**The scratch assay is one of the most performed experiments in cell biology.** Scrape a line through a confluent monolayer, photograph it over hours, measure the closing gap. It is cheap, standard, quantified, and used routinely to screen drug effects on cell migration. The data situation for this Lab is exceptional and unusual: thousands of published time-lapse sequences of the exact process, with measurable closure rates and edge geometry.

**Closure has reduced descriptions.** For an expanding cell sheet driven by proliferation and random motility, Fisher–KPP applies and the edge advances at a speed set by growth rate and motility — the same closed form as invasion ecology (#14), in a Petri dish. For purse-string closure, the rate follows from tension and geometry and gives an approximately linear area decrease.

**Leader cells are a documented, active research topic.** They arise spontaneously at the free edge, are morphologically and transcriptionally distinct, and their spacing sets the finger wavelength. Why a particular cell becomes a leader is not settled.

**Lattice precedent is solid.** Cellular Potts models (see #27) and lattice-based collective migration models are standard tools in this field, alongside continuum and vertex models.

## Where the shortcut holds, and where it breaks

**Reducible.** Closure rate for a straight edge driven by proliferation and motility — Fisher-type wave speed. Purse-string closure kinetics for a circular wound. Time to closure as a function of initial gap width. Whether closure occurs at all given a proliferation rate. Most of what a scratch assay is actually used to measure is on this list, which is a warning: **the standard experiment measures the reducible quantity.**

**Irreducible.** What the wave-speed answer discards:

- **Leader cell emergence and spacing.** A smooth edge spontaneously breaks into fingers, and the wavelength is set by a symmetry-breaking process among nominally identical cells. Which cells lead is not predictable from initial conditions in any practical sense — it is amplified fluctuation — and the resulting finger geometry determines the closure geometry.
- **Collective versus individual migration.** Cells pull on each other. Whether a sheet moves as a coherent body, tears, or advances in swirling patches depends on adhesion relative to traction, and these regimes produce different closure dynamics from the same nominal motility.
- **Closure completion.** The last stage — when the two edges meet — depends on how they meet. Fingers interdigitating leave different residual structure than flat edges colliding, and whether small isolated holes persist depends on the arrangement at contact.
- **Contact inhibition failure.** If the stopping rule is imperfect, cells pile up or continue past each other. That failure mode is the interesting one biologically, and it is intrinsically about local state.

**The lens, stated plainly.** This Lab has an unusual and slightly awkward property: **the phenomenon's success is its disappearance.** The catalog notes this and it is more than a curiosity — it means the endpoint is trivially reducible (the hole closes, at a computable rate) and all the informative content is in the *transient*. A Lab here contributes nothing if it reports closure time and everything if it reports edge geometry, finger spacing, and the statistics of leader emergence.

That maps directly onto the platform's strengths: stored history with navigable time, and views keyed to activity rather than final state.

## What a Cell would carry

A site in an epithelial sheet: occupancy, migration state or polarity, contact count with neighbours, division timer, and possibly a leader/follower designation and adhesion strength. Bounded and small; §13.1 met easily.

Layout is a grid, defensibly — this is a physical monolayer. Two qualifications. **Epithelial cells pack hexagonally**, and a six-neighbour arrangement is more faithful than four or eight. And **cells exert force on each other over distance through the sheet**, so mechanical coupling is not strictly nearest-neighbour — a milder version of the stress non-locality that damages #3 and #31, but present.

## Honest strength assessment

*My assessment, not a fit review (§30). It carries no standing and does not promote this entry.*

**Plausible, with the best experimental-validation situation in Family D and a modest ceiling on what it can contribute.**

The data argument is the strong one. This is arguably the most-imaged local biological process in existence: cheap, fast, standardized, quantified, with time-lapse sequences that are *the same data type the platform stores*. A Run's history and a scratch assay movie are structurally the same object — a sequence of frames of a spatial state. That is a rarer alignment than it sounds, and it makes accuracy testing (§30.6) genuinely feasible rather than aspirational.

**The upside worth being excited about.** Leader cell emergence is a real, open, symmetry-breaking question in an actively funded field, and it is exactly the shape of question this platform addresses: not "what is the closure rate" but "what local rule structure causes a uniform edge to select a discrete set of leaders at a characteristic spacing." Many candidate mechanisms, run cheaply, with the failures kept, is a defensible contribution.

There is also a clean cross-Lab connection: leader-cell fingering is the same instability as tumour margin infiltration (#23), biofilm branching (#25), and dendritic growth (#29) — a protruding tip reaching more resource. If the corpus retrieves the same mechanism family for all four, that is the platform's distinctive capability on display, in a group of Labs that share nothing else.

**The challenges, in order of severity.**

1. **The headline measurement is reducible.** Closure rate is a Fisher wave speed and the field already measures it that way, so the Lab must argue for the transient rather than the outcome.
2. **Mechanical coupling is not strictly local**, and forces propagate through the sheet.
3. **Modest ceiling.** Even a good result here is a contribution to a well-served basic-biology question, not a new capability.
4. **Medical framing invites over-reading** — "wound healing" sounds clinical and this is monolayer cell biology (§30.7).
5. **Cell division changes the participant count**, which the platform has not settled.

## Non-claims

This Lab does not model wound repair in any organism, does not bear on any therapy or clinical outcome, and produces nothing suitable for medical decisions (§41, §43).
