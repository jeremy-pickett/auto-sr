# Visual Idioms Across Six Domains
## Raw material for the SCR visualization program — v0.1

**Status:** Draft — brainstorm, not requirements
**Date:** 2026-08-20
**Relates to:** SCR-F v0.2 Part III (§24–26), especially §25's roadmap candidates

A survey of how six unrelated fields actually draw information. The point is not to admire them; it is to find idioms SCR could steal, and to notice which of our "new" ideas already have century-old names and conventions we would be foolish to reinvent badly.

Entries marked **→** are ones I think transfer directly. They are argued at the end, not here.

---

## 1. Bioscience

**Kymograph** — One spatial line sampled repeatedly, stacked into an image with time as the second axis; motion becomes a slope, stalling becomes a vertical line. **→**

**Sequence logo** — Stacked letters at each position where letter height is information content in bits, so conservation and variability are legible at a glance. **→**

**Volcano plot** — Effect size against statistical significance, so the things that are both large and trustworthy fly to the upper corners.

**Manhattan plot** — Genome position along x, significance along y; the skyline shape gives the plot its name and makes real signals obvious against noise.

**Circos diagram** — The genome as a ring with arcs connecting distant related loci, turning long-range relationships into visible chords.

**Clustergram** — A heatmap with dendrograms attached to both margins, so the clustering that reordered the rows is shown rather than assumed. **→**

**Hi-C contact map** — A symmetric matrix of pairwise contact frequency; folded domains appear as bright squares along the diagonal.

**Pseudotime trajectory** — Cells with no timestamps ordered along an inferred developmental path, then plotted as if that ordering were time.

**Waddington landscape** — A rolling terrain where valleys are stable fates and ridges are decisions; a metaphor drawn so often it became an analysis tool.

**Flow cytometry gating** — Successive 2D scatter plots where each hand-drawn region feeds the next, making the analyst's reasoning chain part of the figure. **→**

---

## 2. Information security

**Attack graph** — Nodes are system states and edges are exploits, so an attack is a path and defense is edge removal. **→**

**BloodHound path view** — Active Directory relationships rendered as a graph where the shortest path to Domain Admin is computed and highlighted, which turned an audit problem into a graph query. **→**

**ATT&CK Navigator layer** — A tactics-by-techniques matrix colored by coverage, detection, or observed use; the same grid overlaid with different meanings. **→**

**Super-timeline** — Every timestamped artifact from every source merged into one ordered forensic sequence, deliberately mixing evidence types.

**East-west chord diagram** — Internal traffic between segments drawn as chords around a ring, which makes unexpected lateral flows visually loud.

**Punchcard heatmap** — Hour-of-day against day-of-week as a grid of dots, exposing automation and off-hours activity by shape alone.

**Blast radius diagram** — Concentric reachability from a compromised asset, drawn to answer "if this falls, what else does."

**Treemap of assets** — Nested rectangles sized by count and colored by risk, used when hierarchy plus magnitude matters more than relationship.

**Threat "pew-pew" map** — Arcs flying across a world map in real time; almost pure theater, retained here as the domain's boundary marker for visuals that impress and inform nobody.

---

## 3. Materials science

**Ashby chart** — Two material properties on log axes with each material family as a labeled bubble, plus guide lines showing which envelope a design requirement selects. **→**

**Phase diagram** — Composition against temperature partitioned into labeled regions, the field's foundational map of what exists where.

**TTT curve** — Time against temperature with a nose-shaped boundary, showing that the same material transforms differently depending on the path taken through the diagram. **→**

**EBSD orientation map** — Grains colored by crystallographic orientation, so a microstructure's texture is directly visible as a patchwork.

**Pole figure** — Orientation density projected onto a sphere and flattened, summarizing texture across a whole sample.

**Stress-strain curve** — Load against deformation, where the shape of the curve after the peak is the story rather than the peak itself.

**Weibull plot** — Failure probability on transformed axes so that a straight line means one failure mechanism and a kink means two. **→**

**Tomographic slice stack** — A 3D scan navigated one plane at a time, with the slider through depth doing the same work SCR's slider does through time. **→**

**Radial distribution function** — Neighbor density against distance, collapsing a whole structure into one curve that distinguishes crystal, glass, and gas.

---

## 4. CAD/CAM

**Zebra stripe analysis** — Reflected stripes rendered on a surface, where a kink or break in a stripe reveals curvature discontinuity invisible in the shaded model. **→**

**Curvature comb** — Normal curvature drawn as a fringe of spikes along a curve, turning a derivative into something you can see at a glance. **→**

**Exploded view** — Assembly components displaced along their assembly vectors, showing structure and order simultaneously.

**Section and cutaway** — A clipping plane through solid geometry, with capped faces so the cut reads as material rather than a hole.

**Toolpath preview** — The cutter's route drawn in space before anything is cut, colored by operation, feed rate, or rapid-versus-cutting moves.

**Material removal simulation** — Stock progressively carved by the simulated tool, with gouges and collisions flagged where they occur. **→**

**Swept volume** — The total space a moving tool or mechanism occupies over its full motion, collapsed into one solid. **→**

**Deviation map** — Measured geometry colored by signed distance from nominal, so error becomes a temperature map on the part itself. **→**

**Draft and thickness analysis** — The part recolored by moldability or wall thickness, using the same geometry to answer a manufacturing question rather than a shape question. **→**

**Feature history tree** — The parametric operations that built the model, listed in order and re-playable, so the model carries its own construction provenance. **→**

---

## 5. Cosmology

**Redshift wedge** — A pie-slice of sky with distance as radius, which is how the cosmic web's filaments and voids first became visible in survey data. **→**

**Lightcone diagram** — Space against conformal time, drawn so that causal reachability is a geometric fact you can read off the figure. **→**

**Mollweide all-sky map** — The whole celestial sphere in one equal-area ellipse, the standard canvas for CMB and full-sky surveys.

**Angular power spectrum** — Sky structure decomposed by angular scale, converting a mottled map into a curve whose peaks carry the physics.

**N-body volume render** — Simulated matter rendered as luminous density, where filaments, nodes, and voids emerge without being drawn.

**Merger tree** — Halo assembly history as a branching diagram running down the page in time, showing what merged into what. **→**

**Convergence map** — Reconstructed mass from weak lensing distortion, an image of something that emits nothing.

**Phase-space plot** — Position against velocity rather than position against position, where structure invisible in real space (the Gaia snail spiral) appears immediately. **→**

**Hubble diagram** — Distance against recession velocity, one scatter plot that carried an entire cosmological claim.

---

## 6. Movies

**Color script** — The whole film as a strip of small paintings in sequence, so emotional and chromatic arc can be judged before anything is animated. **→**

**Movie barcode** — Every frame averaged to one column and stacked, turning a two-hour film into a single legible image of its palette over time. **→**

**Animatic** — Storyboards cut to timing with scratch audio, testing pacing while changes are still cheap.

**Onion skin** — Adjacent frames ghosted behind the current one so an animator can see motion rather than position. **→**

**Timing and spacing chart** — Tick marks showing where a drawing falls between extremes; the entire feel of a motion encoded as spacing between marks.

**Graph editor curves** — Animation parameters as editable splines over time, where the shape of the curve is the performance. **→**

**AOV passes** — The same render decomposed into depth, normal, ID, lighting, and other channels, each a different truth about one image. **→**

**Cryptomatte** — Object identity encoded as color so any element can be isolated afterward without re-rendering. **→**

**Wedge render** — The same shot rendered across a grid of parameter values and viewed side by side to choose a setting. **→**

**False color exposure** — The monitor image remapped so each brightness zone gets an arbitrary flat color, making exposure judgeable rather than guessable. **→**

**Waveform and vectorscope** — Luminance and chrominance plotted as distributions beside the picture, because the eye is unreliable about both.

---

## 7. What SCR should actually steal

**Idioms we are already reinventing, and should adopt the names for.** The kymograph is SCR-F §25.2's Time View, invented in cell biology decades ago; the redshift wedge and lightcone are the same family. Adopting the existing vocabulary costs nothing and buys instant legibility with scientific users. The tomographic slice stack is our slider with a different axis, and the feature history tree is our provenance chain drawn as a navigable object rather than stored as a record.

**The strongest single steal is the AOV/cryptomatte pattern.** Film renders decompose one image into many channels — depth, normal, object ID, lighting — each a separate honest truth about the same frame, recombined at will afterward. That is exactly SCR-F §24.2's "styles are lenses" argument, but film production went further: the passes are *stored*, not recomputed, and downstream work operates on them. If Runs stored kind, activity, hidden-state, and structure-ID as separate channels the way a render stores AOVs, most of §25's Views become compositing rather than analysis. Cryptomatte in particular is the answer to "let me click that structure and follow it," and it works because identity was written at render time rather than inferred later.

**The wedge render is Try Many Settings with better ergonomics.** Film artists have solved the presentation problem for parameter sweeps — a grid of the same shot at varying values, viewed simultaneously rather than sequentially. SCR-F §25.5's Behavior Map is the abstract version; the wedge is the concrete one, and it is more immediately useful.

**False color exposure is the honest answer to a problem we already have.** It remaps a signal into flat arbitrary bands precisely because perceptual gradients lie. Any SCR view that maps a scalar to brightness inherits that lie, and the film industry's fix — banded, labeled, deliberately ugly — is better than a prettier ramp.

**Two idioms carry the epistemics we care about.** The sequence logo makes uncertainty structural: letter height is information content, so a low-information position is *visibly* low-information rather than quietly asserted. Flow cytometry gating puts the analyst's reasoning chain in the figure, which is what SCR-F §21 asks for when it says Readers must not become invisible truth layers. Both are worth copying as patterns, not just as pictures.

**Two warnings.** The Weibull plot exists because a straight line means one mechanism and a kink means two — a diagnostic we would want for Study results, and a reminder that transformed axes are a legitimate tool rather than a distortion. And the pew-pew map is what SCR-F §12 is trying to prevent: maximum motion, minimum information, universally beloved by people who do not use it. Our Corpus View (§25.6) is one bad decision away from being it.

**The idiom nobody in our six domains has** is the one SCR-F §3 needs: a view of *intent against outcome*. Volcano plots come closest by crossing effect size with significance, and Ashby charts by crossing two properties with a requirement envelope drawn over them. Neither plots what someone meant against what happened. That gap is either a real opening or a sign the axis is harder to draw than it is to describe.
