# 22. Cortical Spreading Depression Lab

**Document class:** Lab Knowledge Brief · **Status:** draft
**Catalog:** SCR Lab Catalog v0.1 #22, Family D · **Standing:** ungraded
**Cites:** SCR-F v0.2 §11, §29, §30, §41; F-17
**Fit review (§30):** not performed

---

## The phenomenon

A wave of near-complete depolarization travels across the cortex at roughly three millimetres per minute, leaving behind ten to thirty minutes of electrical silence before recovery. It is not an epileptic discharge — it is the opposite, a shutdown — and its speed is thousands of times slower than an action potential.

It was described by Leão in 1944 in rabbit cortex. In humans it is the leading candidate mechanism for **migraine aura**: the slowly expanding scintillating scotoma that patients describe, mapped onto visual cortex, moves at about the same speed. In injured brain — after subarachnoid haemorrhage, traumatic injury, or stroke — recurrent depolarizations are recorded directly and are associated with worse outcomes, apparently because metabolically compromised tissue cannot afford the enormous energy cost of restoring the ion gradients.

## What the domain already knows

**The mechanism is ionic and diffusive.** Potassium and glutamate released from depolarizing cells diffuse into the extracellular space, depolarize neighbours past threshold, and the process propagates. Restoration requires ion pumps working hard, which is why the refractory period is long and why compromised tissue suffers.

**It is an excitable medium**, and the field says so. The three-state structure — resting, depolarized, recovering — is the same as #21, with different constants. Reaction–diffusion models of spreading depolarization are standard, and the propagation speed follows from potassium diffusivity and the release/uptake kinetics in the way a reaction–diffusion wave speed generally does.

**The observational record is unusually direct for a brain phenomenon.** Electrocorticography strips placed on injured human cortex record depolarizations directly, and there is an international collaboration collecting exactly this data *(the COSBID group; attribution from memory, verify)*. In animals, intrinsic optical imaging shows the wave crossing the cortical surface as a visible front.

**The aura mapping is a classic.** Milner in 1958 pointed out that the speed and progression of migraine aura across the visual field, translated into cortical coordinates, matches Leão's wave *(attribution from memory)*. Later functional imaging supported it.

## Where the shortcut holds, and where it breaks

**Reducible.** Propagation speed from diffusion and kinetics — the standard reaction–diffusion result. Refractory duration from pump capacity. Threshold potassium concentration for initiation. Metabolic cost per unit area depolarized. Whether a homogeneous medium supports propagation at all.

**Irreducible.** The clinically interesting questions are all about geometry and repetition:

- **Propagation block at anatomical boundaries.** The wave does not cross everywhere. Sulci, major vessels, and regions of different cell density can block or channel it. Whether a wave crosses a given fold is a specific geometric question, and the pattern of what gets depolarized determines what symptoms a patient experiences.
- **Initiation.** What triggers the first depolarization is genuinely unknown in migraine and only partly understood in injury. Whether a local disturbance exceeds threshold depends on the surrounding tissue state.
- **Recurrence and clustering.** In injured brain, depolarizations come in clusters. Whether the tissue has recovered enough to support the next one, and whether repeated waves progressively damage the penumbra, is a history-dependent question with direct clinical stakes.
- **Interaction with compromised tissue.** A wave crossing tissue that cannot repolarize converts a transient event into permanent injury. Where that boundary sits, and whether it moves with each wave, is exactly the sort of path-dependent question that has to be run.

**The lens, stated plainly.** This Lab is #21 with a different timescale, a different clinical stake, and — importantly — **a much weaker reducible core relative to the questions asked.** Cardiac electrophysiology has restitution curves and alternans criteria; spreading depolarization has propagation speed and not much else that predicts the clinically relevant behaviour. The proportion of the domain that is genuinely open is larger here, which cuts both ways: more room to contribute, less ground to stand on.

## What a Cell would carry

A cortical tissue element: depolarization state, extracellular potassium (or a generic excitatory signal), recovery progress, metabolic reserve, and tissue viability. Bounded scalars; §13.1 met easily.

Layout is nominally a grid, and here the caveat is sharper than in #21. **Cortex is a folded sheet.** The wave travels along the cortical surface, which is a highly convoluted two-dimensional manifold embedded in three dimensions. A flat lattice discards exactly the geometry that determines propagation block — which is one of the two or three questions worth asking. This is a genuine Layout problem, not a refinement.

The metabolic reserve variable is worth naming for a different reason: it is hidden state with clinical consequence. Tissue that has depolarized and not yet restored its gradients looks quiet and is in danger. A view keyed to depolarization alone shows recovery; a view keyed to reserve shows accumulating injury. SCR-F §38.6, again, with the highest stakes it appears at in this catalog.

## Honest strength assessment

*My assessment, not a fit review (§30). It carries no standing and does not promote this entry.*

**Plausible, and mostly worth building as the second member of an excitable-media pair rather than on its own.**

The honest position: this domain and #21 share a mechanism class. Building both means the marginal cost of the second is low and the marginal insight is a genuine test of **cross-Lab mechanism transfer** — the platform's most distinctive potential capability. If a mechanism family retrieved for cardiac wave break also produces propagation block at folded boundaries, that is the corpus doing something no domain-specific model library can do.

Standalone, the case is weaker. The field is small, the incumbents are reaction–diffusion models that already work for the reducible questions, and the folded-sheet geometry problem is serious.

**The upside worth being excited about.** Two genuinely open questions where mechanism supply is defensible. **What initiates a depolarization?** — unknown in migraine, and the population of candidate local triggers is exactly what a generative corpus produces. And **why do depolarizations cluster and why does clustering predict poor outcome?** — a recurrence question, which is a Study over repeated Runs rather than a single simulation.

The data situation is better than most neuroscience: direct human electrocorticographic recordings of the phenomenon exist, with timing and spatial extent, collected prospectively.

**The challenges, in order of severity.**

1. **Medical credibility hazard**, the same as #21 and for the same reasons. Migraine and brain injury are emotive and the misreading risk is high.
2. **Cortex is a folded manifold**, and flattening it removes the geometry that produces the interesting behaviour.
3. **Small field, thin funding**, and few people to review the work.
4. **Initiation is unknown**, so the most interesting question also lacks a reference answer to check against.
5. **Timescale spans a minute-long wave and a week of clustered events.**

## Non-claims

This Lab does not model any patient, does not bear on migraine diagnosis or treatment, does not inform care of brain injury, and produces nothing suitable for any medical decision (§41, §43).
