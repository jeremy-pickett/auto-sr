# 21. Excitable Media Lab

**Document class:** Lab Knowledge Brief · **Status:** draft
**Catalog:** SCR Lab Catalog v0.1 #21, Family D · **Standing:** **[strong]** (inherited, not re-derived)
**Cites:** SCR-F v0.2 §11, §29, §30, §41; F-17
**Fit review (§30):** not performed

---

## The phenomenon

An excitable medium has three states and one rule. A resting element does nothing until a neighbour excites it. Once excited it fires, exciting its own neighbours. Then it becomes refractory — temporarily unable to fire again — before returning to rest.

From those three states you get travelling waves that annihilate on collision rather than passing through, and, if a wave is broken so that one end is free, **spiral waves** that rotate indefinitely around a core, re-exciting tissue as fast as it recovers.

In heart muscle this is not an abstraction. A normal heartbeat is a wave sweeping the tissue once. A spiral is a re-entrant circuit driving the tissue far faster than the sinus node — tachycardia. When the spiral breaks into many wavelets, the result is fibrillation, and ventricular fibrillation is fatal in minutes. The same physics runs the Belousov–Zhabotinsky chemical reaction, calcium waves in cells, and — the connection the catalog's family grouping hides — arguably open-cell cloud convection (#11).

## What the domain already knows

**The cellular-automaton formulation is canonical and old.** Wiener and Rosenblueth described cardiac excitation in essentially these terms in 1946. Greenberg and Hastings gave the minimal three-state CA in 1978, and it produces spiral waves from a broken wavefront with a rule that fits in a sentence *(attributions from memory, verify)*. This is one of the strongest cases in existence that a trivial local rule captures a real and clinically important phenomenon.

**Continuum theory supplies reducible results.** FitzHugh–Nagumo is the standard reduced model. Plane wave speed is a computable function of the medium's properties. The **eikonal relation** — wave speed decreases with front curvature — is closed-form and explains why waves cannot turn arbitrarily sharply and why there is a minimum core size for a spiral. Spiral rotation period follows from wavelength and refractory period.

**Restitution is the clinical bridge.** The action potential duration depends on the preceding rest interval, and the slope of that restitution curve predicts **alternans** — beat-to-beat alternation — which is a documented precursor of wave break. The alternans-slope criterion is a genuine analytic prediction of instability onset and is used clinically.

**The incumbents are strong.** Detailed ionic models of cardiac cells (the Luo–Rudy lineage and successors) coupled into anatomically realistic tissue meshes are the research standard, run on large machines. They are far more faithful than any CA, and far more expensive.

## Where the shortcut holds, and where it breaks

**Reducible.** Plane wave speed. Curvature–speed relation. Minimum spiral core radius. Spiral period from wavelength and refractoriness. Whether a given restitution slope predicts alternans. Whether a medium is excitable at all. Conditions for one-dimensional conduction block. A substantial and clinically useful body of results.

**Irreducible.** The initiation and the breakup, which are the two things that matter:

- **Wave break initiation.** A spiral needs a broken wavefront. Breaks arise when a wave meets tissue that is partly refractory — at a scar, a fibrotic patch, a region of altered ion channel expression. Whether a given premature beat at a given phase breaks against a given heterogeneity is a specific, arrangement-and-timing-dependent question with no closed form. This is the clinical question: why did *this* patient's arrhythmia start?
- **Spiral breakup into fibrillation.** The transition from one rotating spiral to many wavelets is a nonlinear instability whose onset and character depend on the detailed dynamics. Analytic criteria exist and are partial.
- **Anchoring and drift.** Spirals pin to anatomical obstacles, drift in gradients, and meander in complicated trajectories. Where a spiral ends up determines whether the arrhythmia is stable or self-terminates.
- **Defibrillation.** Whether a shock terminates fibrillation depends on the instantaneous configuration of all wavelets. This is the strongest possible statement that the state matters and the parameters do not suffice.

**The lens, stated plainly.** This domain divides with unusual clarity: **propagation is reducible, initiation and destabilization are not.** And the reducible half is the half nobody dies of. The clinical question — what tissue configurations permit re-entry to start — is a question about specific spatial arrangements interacting with specific timing, which is the definition of a case where you must run it.

## What a Cell would carry

A tissue element: excitation state (resting, excited, refractory), a recovery timer, and local excitability or coupling strength. Possibly a scar or fibrosis flag. Extremely small state — the Greenberg–Hastings model uses a single integer. §13.1 is met more easily here than anywhere in the catalog.

Layout is a grid, defensibly, with one real caveat: **cardiac tissue is anisotropic.** Fibres conduct several times faster along their axis than across it, and fibre orientation rotates through the ventricular wall. That anisotropy is not an artifact to be minimized — it is physiology, and it drives real arrhythmia mechanisms. A Lab that ignores it is modelling a different tissue.

## Honest strength assessment

*My assessment, not a fit review (§30). It carries no standing and does not promote this entry.*

**Strong, and among the very best entries in the catalog — with the highest consequence-of-misuse of any Lab outside Family H.**

The fit is close to ideal. The canonical model of this domain *is* a cellular automaton, published in 1978, still cited. The state is minimal. The mechanism is genuinely local — cardiac coupling is through gap junctions between adjacent cells. The reducible boundary is well mapped. The irreducible remainder is the clinically important part and is openly acknowledged as open. And the phenomenon is temporal in a way that makes the platform's stored-history playback genuinely valuable rather than decorative: spiral formation is a *sequence*, invisible in any single frame.

**The upside worth being excited about.** Optical mapping experiments produce exactly the data this platform consumes: high-speed movies of voltage across a tissue surface, frame by frame, with spiral cores visible. Comparing a Run's stored history against an optical mapping recording is a genuine like-for-like comparison, which almost nothing else in this catalog offers.

The scientific opening is real. Detailed ionic models are expensive enough that broad exploration of *mechanism space* is not routinely done — investigators simulate the mechanisms they already suspect. Supplying many candidate local rules for wave-break initiation, cheaply, with the failures retained, is precisely the position paper's argument in the domain where it is most defensible.

And the cross-Lab connection is real: the same abstract mechanism describes cardiac tissue, chemical reactions, calcium signalling, cortical spreading depression (#22), and possibly cloud convection (#11). If SCR ever demonstrates that a mechanism retrieved for one Lab illuminates another, this family is where it happens.

**The challenges, in order of severity.**

1. **Medical credibility hazard, and it is severe.** Output that resembles a cardiac simulation will be read as one. Nothing this Lab produces can bear on any patient, any device, or any therapy, and the distance between a rendered spiral and a clinical claim is shorter than it looks. This deserves the strongest §30.7 language in the catalog outside Family H.
2. **Fibre anisotropy is physiology**, not artifact, and ignoring it changes the phenomenon.
3. **The three-dimensional wall matters** — scroll waves in 3D behave differently from spirals in 2D, and filament dynamics have no 2D analogue.
4. **Strong, well-funded incumbents** with anatomically realistic models.
5. **One tick is milliseconds**; long-horizon questions are expensive.

## Non-claims

This Lab does not model any patient, does not bear on diagnosis, device design, drug effect, or therapy, and produces nothing suitable for any medical or clinical decision (§41, §43).
