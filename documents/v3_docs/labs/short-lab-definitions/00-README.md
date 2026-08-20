# Lab Knowledge Briefs — reading guide and cross-catalog findings

**Document class:** Index · **Status:** draft
**Covers:** SCR Lab Catalog v0.1 entries 1–60
**Cites:** SCR-F v0.2 §11, §29, §30, §41; *A Card Catalog for Emergence* v0.1 §5
**Fit reviews (§30):** none performed

---

## What these documents are

Sixty briefs, one per catalog entry, written through the lens of **computational irreducibility and cellular automata**. Each answers one question: *what does this Lab need to know?* — the domain science, the established modelling, the prior art, and above all where the domain's existing shortcuts hold and where they stop.

They are **not** feature specs, design documents, or implementation plans. They contain no requirements and no code.

Two entries — #1 Wildfire and #47 Lateral Movement — replace earlier fit-frame documents that posed the §30 questions rather than answering the knowledge question. The originals are preserved alongside as `*.fit-frame.md`; they were not deleted and they remain useful for what they were for.

## The organizing spine

Every brief carries the same load-bearing section: **Where the shortcut holds, and where it breaks.**

> A domain's most important knowledge is which regime it is standing in. Every domain has a part with a closed form, a formula, an exact law, or a solved algorithm — and a part where the only way to know is to run it. **SCR has nothing to offer in the first and exists for the second.**

That split does more work than any other analytical move available. It produces the strength verdict almost mechanically: **a Lab is strong when its irreducible regime is large, checkable, and currently underserved.** Wildfire scores on all three. Water distribution scores on none.

## Assessment status

Standings in brackets are **inherited** from the position paper's eighteen graded verticals and are not re-derived. The "Honest strength assessment" section in each brief is **my judgment, explicitly labelled, carrying no standing** — it is not a fit review, and it does not promote an ungraded entry. Forty-three entries had no opinion attached before these briefs; they now have a first one, clearly marked as such.

Literature is cited from knowledge with uncertain attributions flagged inline. Anything marked *(attribution from memory, verify)* should be checked before these documents are cited outward.

---

## Five distinct reasons a Lab fails

The single most useful finding from writing all sixty. A catalog that can name *why* an entry fails is a sharper instrument than one that only says "poor fit":

1. **The agents use global information.** Decisions depend on a view no local participant has. — #60 (cleanest case), #39's scheduler.
2. **The driving physics is a global solve.** The mechanism looks local but its driver is computed over the whole World. — #42 power flow, #43 hydraulics, #31 elasticity, #18 network flow, #34 potential field, #9 water level.
3. **The mathematics is already closed-form and the real problem is measurement.** — #51; also the reducible cores of #30 and #33.
4. **The substrate is non-stationary.** The system changes faster than evidence about it accumulates. — #49, partly #50.
5. **The process is a plan, not a phenomenon.** Someone designed the mechanism, so there is nothing to infer. — #53, #44, #39.

A sixth, milder pattern recurs without being fatal: **universality flattens mechanism differences** (#33, #35), which is a direct challenge to the corpus's premise that different mechanisms are worth cataloguing separately.

## Recurring architectural questions the catalog forces

These appear across families and are not resolvable in any Lab document (§36.6, F-22):

- **Non-local reach.** Wildfire spotting, dune saltation hops, invasion long-distance dispersal, seed kernels, pest flight, scanning worms. Six Labs, one question: *is a bounded-range jump a local mechanism?* #19 is the cheapest place to force an answer, because there the kernel *is* the phenomenon.
- **Self-constructed topology.** Mechanisms that create or destroy the World's Connections — #18 mycelium, #48 identity grants, #56 dependency edges, #58 co-evolving networks. #58 is the cheapest test; #48 has the highest stakes.
- **Motile participants.** Entities whose state travels rather than sitting in a Cell — #17 grazers, #26 immune cells, #39 robots, #40 evacuees, #59 ants, #47 attackers. #59 is the smallest honest test case with a published reference experiment.
- **Changing participant count.** #20 growing embryos, #24 dividing cells, #32 shrinking bodies, #50 written memory items.
- **Bounded belief (§13.1).** #40 and #47 share the same ceiling problem — an agent's knowledge is naturally unbounded and is exactly the state that drives behaviour. **They should be fit-reviewed together.**
- **DEC-3 forcing cases.** #46 (asynchronous message passing *is* the protocol), #44 (clock-scheduled events), #45 (timeouts are the substance), #52 (the defender's stale picture). A lockstep-only platform cannot express these honestly.

## Cross-Lab mechanism families

The catalog's family grouping is thematic and hides the mechanism structure. Four families cut across it, and **noticing them is the platform's most distinctive potential capability** — a corpus indexed by mechanism rather than by field is uniquely able to surface them:

- **Diffusion-limited fingering** — #23 tumour margins, #24 wound-edge leaders, #25 biofilm branching, #29 dendrites, #34 battery dendrites, #10 snow crystals. Six Labs, four disciplines, one instability. #29 has the rigorous theory; the biology Labs have the data.
- **Excitable media** — #21 cardiac tissue, #22 cortical depolarization, #35 catalytic surfaces, and arguably #11 open-cell convection. The last is the surprising member and the best test of transfer.
- **Bistability and tipping fronts** — #12 vegetation, #16 pest outbreaks, #17 coral reefs, #45 service cascades, #44 freight gridlock. All share hysteresis: fast to collapse, slow to recover.
- **Contamination on a trust graph** — #49, #50, #51, #54, #55. Better built as **one World with several mechanisms** than as five Labs.

## Where I would start, and why

*My judgment, not a fit review.*

**Calibration anchors — build these to prove the evidence chain works.** #1 Wildfire (plausibility, documented perimeters), #37 Highway Traffic (best data in the catalog; loop detectors everywhere), #30 Grain Growth (**correctness**: the von Neumann–Mullins relation is an exact per-step law a generated mechanism either satisfies or does not), #25 Biofilm (a controlled reference experiment that costs a few pounds and takes a day).

**The sleeper.** #45 Service Cascade is, in my assessment, the strongest ungraded entry in the catalog — ahead of most of Family H and Family G. The mechanism is genuinely local *and genuinely known* (a retry policy is a local rule someone wrote); the topology is importable from production telemetry; metastability is the purest irreducibility structure available; the data is exceptional; the question is Study-shaped; and there is no dominant incumbent modelling tool.

**Family H's honest position.** The family is ungraded and the catalog expects it may grade weak. My reading: the naive framings are weak everywhere, and two entries have strong narrow framings. **#48 Identity and Privilege** is the best in the family, because the domain's core question is *provably undecidable* (Harrison–Ruzzo–Ullman, 1976) and the field's entire apparatus consists of restrictions adopted to escape that — the gap is precisely locatable. **#47 Lateral Movement** is second, on the same structure one level down: the field knowingly traded away non-monotonicity for polynomial tractability, and studying what that trade discards is a real question a graph query cannot ask. #55 is the family's best *demonstrator* — it exercises Study, Small-Change Test, ambient-sensitivity context, and modest statistics more than any other entry. #54 is the only Family H entry with **real quantitative reference data** (network telescope traces), which makes it the family's only calibration candidate.

**What I would not build.** #43 Water Distribution and #53 Patch Propagation, on the grounds stated in their briefs — not because they are hard but because the questions are not open. #31 Fracture, because elasticity's non-locality is a theorem rather than an approximation, and the Lab would produce convincing pictures from wrong mechanics in a safety-critical domain. #60, by design.

## Credibility hazards, ranked

Several Labs can produce visually convincing output about consequential subjects. In rough order of how much harm a misreading could do:

1. **#36 Crowd Egress** — life-safety, and the domain is *operationally used*, which makes SCR look adjacent to legitimate practice in a way it is not.
2. **#57 Epidemic Spread** — the catalog's most likely to cause real harm, not through direct misuse but through **decontextualized circulation**: an epidemic animation escapes its caption within a day.
3. **#21 Excitable Media**, **#23 Avascular Tumor** — medical, and the distance between a rendered spiral and a clinical claim is shorter than it looks.
4. **#34 Battery Dendrite**, **#31 Fracture**, **#28 Corrosion** — safety-critical engineering.
5. **Family H throughout** — commercial over-claiming pressure, plus the standing misreading that "no path found" means "secure."
6. **#42 Power Grid** — where a published paper already made this exact mistake and was rejected by the affected engineering community.

## File map

`NN-<slug>-lab.md`, numbered to match the catalog. `01` and `47` also have `.fit-frame.md` companions holding the earlier §30-framing versions.

| Family | Entries |
|---|---|
| A — Fire, land, surface | 01–08 |
| B — Ice, water, atmosphere | 09–13 |
| C — Ecology | 14–19 |
| D — Cells, tissue, disease | 20–27 |
| E — Materials | 28–35 |
| F — Movement and crowds | 36–40 |
| G — Cities and infrastructure | 41–46 |
| H — Information security | 47–56 |
| I — Weak fits and boundary markers | 57–60 |

## What these briefs do not do

They do not perform fit reviews, resolve any DEC-owned question, or promote any entry. Nothing here establishes that SCR models any domain usefully. Every brief carries its own non-claims section and they should be read as binding (§41, §43).
