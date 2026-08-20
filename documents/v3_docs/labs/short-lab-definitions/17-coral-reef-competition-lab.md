# 17. Coral Reef Competition Lab

**Document class:** Lab Knowledge Brief · **Status:** draft
**Catalog:** SCR Lab Catalog v0.1 #17, Family C · **Standing:** ungraded
**Cites:** SCR-F v0.2 §11, §29, §30, §41; F-17
**Fit review (§30):** not performed

---

## The phenomenon

A coral reef is a competition for hard substrate. Corals grow slowly and hold space by being there. Fleshy macroalgae grow fast and overgrow coral when given the chance. Herbivorous fish and urchins eat algae, keeping it cropped and leaving space open for coral recruits to settle.

Remove the grazers, or add nutrients, or kill coral with a bleaching event, and the balance flips. Algae take the space, and — this is the crucial part — they hold it. Algal turf and macroalgae inhibit coral recruitment, so the new state is self-reinforcing. Reefs that flip to algal dominance frequently stay there for decades even after the original stressor is removed.

The Caribbean is the canonical case: a mass die-off of the dominant urchin in the early 1980s, combined with overfishing and coral disease, preceded a widespread shift from coral- to algae-dominated reefs that has largely not reversed.

## What the domain already knows

**The bistability has an explicit model.** Mumby, Hastings, and Edwards published a simple dynamical model of coral–algal–turf competition with grazing around 2007, showing two stable states, hysteresis, and a critical grazing threshold *(attribution from memory, verify)*. It is few-equation, well-cited, and it is the reference for the regime-shift framing. Hughes's 1994 Jamaica work is the observational anchor.

**The reducible answers are the bifurcation answers.** Given grazing intensity, coral growth rate, and algal growth rate, the model says whether coral-dominance is stable, whether algae-dominance is stable, whether both are, and where the tipping points sit. Hysteresis width follows. This is a two- or three-variable ODE and the analysis is complete.

**The regime-shift interpretation is contested.** A serious critique argues that many observed reef declines are better explained by continuous forcing and disturbance than by an alternative-stable-state mechanism, and that demonstrating true bistability in the field is very hard. A Lab here must know that the framing itself is a live argument, not a settled result.

## Where the shortcut holds, and where it breaks

**Reducible.** Everything about the well-mixed system: existence of the two states, the grazing threshold, hysteresis, recovery time from a small perturbation. Bleaching mortality given a thermal exposure. Reef-scale cover trajectories under a specified disturbance regime.

**Irreducible.** Everything spatial, and space is where reef ecology actually lives:

- **Grazing halos.** Herbivores do not graze uniformly. They feed near shelter and avoid open sand, producing measurable halos around reef structure. Grazing pressure is therefore a spatial field determined by the arrangement of habitat, and the well-mixed grazing parameter is a fiction that averages over it.
- **Local refugia.** Coral persisting in a small protected patch can reseed after disturbance. Whether such a patch exists and whether its larvae reach recovering areas is an arrangement question, and it determines whether a reef recovers or converts.
- **Overgrowth is a boundary process.** Algae take space at the coral's edge. Perimeter-to-area ratio matters, which makes colony shape a variable that no mean-field model contains.
- **Larval connectivity.** Coral recruitment comes from a larval pool that may be local or arrive from reefs kilometres away. This is a long-range, current-driven connection, not a neighbour relation.
- **Disturbance patchiness.** Bleaching and storms hit unevenly, and the geometry of what survives determines the recovery path.

**The lens, stated plainly.** This Lab is a case where **the field's own reducible model may be the thing worth testing.** The Mumby-class ODE assumes well-mixed competition, and the strongest critique of the regime-shift framing is essentially that the assumption does not hold. Asking *what happens to the bistability when competition is local* is a real, specific, unanswered question — spatial versions of bistable competition can lose bistability entirely, or gain front-pinning behaviour, or produce coexistence that the ODE forbids.

That is a narrow, honest, and genuinely interesting position for a Lab: not "we simulate reefs," but "we test what the field's canonical simplification discards."

## What a Cell would carry

A patch of substrate: occupant type (coral, macroalgae, turf, bare), coral colony age or size, grazing pressure experienced, and possibly a recruitment or disturbance state. Occupant type is a small enumerated set; §13.1 is met.

Layout is a grid and defensible — reef substrate is a physical surface and overgrowth is genuinely a neighbour interaction. Two qualifications: **grazers move and are not cells**, which is a second mechanism (DEC-1) and possibly an Agent-World concern; and **larval dispersal is long-range and current-driven**, which is neither local nor symmetric.

## Honest strength assessment

*My assessment, not a fit review (§30). It carries no standing and does not promote this entry.*

**Plausible, with a sharper research angle than the catalog entry suggests and a weaker prediction case than its stakes imply.**

The catalog frames this as "local overgrowth rules producing a bistable landscape," which is accurate but undersells the interesting part. The interesting part is that the field's headline claim — reefs have alternative stable states — rests on a well-mixed model whose central assumption this platform is built to violate. That is a clean, falsifiable, contained question.

The prediction case is much weaker. Reef futures depend on ocean temperature, acidification, fishing policy, and disease — none of them local mechanisms, all of them dominant. Any Lab output that looks like a reef forecast would be badly misleading, and reef decline is emotionally and politically charged enough that the misreading is near-certain if the door is left open.

**The upside worth being excited about.** Benthic cover data is genuinely good: long-term monitoring programmes with photo-quadrat time series over decades, plus increasingly high-resolution reef imagery from drones and satellites. Spatial pattern — patch sizes, coral–algal boundary geometry, halo widths — is directly measurable and rarely used as a model target. A mechanism that reproduces observed *spatial* statistics rather than just cover fractions would be checking something the ODE tradition cannot check.

And there is a real Study here: hold the mechanism constant, vary grazer spatial distribution from uniform to strongly clustered, and ask at what point the bistability disappears. If it disappears easily, that is a finding about a widely used model.

**The challenges, in order of severity.**

1. **The dominant drivers are global**, not local. Temperature and acidification do not fit the abstraction at all.
2. **Grazers are agents, not cells** — DEC-1, and possibly the wrong Layout family.
3. **Larval connectivity is long-range and current-driven.**
4. **Timescale spans a bleaching week and a fifty-year regime.**
5. **High emotional and policy charge** makes §30.7 misreading likely and costly.

## Non-claims

This Lab does not assess the condition or future of any real reef, does not evaluate management or fishing policy, and produces nothing suitable for conservation or policy decisions (§41, §43).
