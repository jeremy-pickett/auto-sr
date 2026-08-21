# What the sixty Labs actually need to ingest

**Document class:** Level 5 — Lab Papers (cross-catalog inventory) · **Status:** draft (first pass)
**Path:** `labs/ingestion-inventory.md`
**Source:** the nine family reports in `*/family-*-report-v1.md`, §30.6 accuracy sections
**Cites:** SCR-F v0.2 §30.6, §32, §41–43 · `../01-core/worlds.md` (WORLD-7), `../03-quality/reference-cases.md` (REFCASE-), `../03-quality/synthetic-data.md` (SYNTH-) · DEC-5, DEC-8, DEC-23

> **The headline: most real data never enters the simulation.** Of the datasets the sixty Labs name, roughly two-thirds are **comparison targets** — they are what a result is checked against, not what a Run is built from. The ingestion machinery this catalog needs is therefore much smaller than "ingest data for sixty Labs" implies.

---

## 1. Four pipelines, and how the sixty distribute across them

Ingestion is not one thing. It is four, with four different homes, four different contracts, and very different volumes.

| Pipeline | What it does | Labs demanding it | Home |
| :--- | :--- | :--- | :--- |
| **1. World structure** | For relational Worlds, the data **is** the Layout | 16 named it; **5 have it available and load-bearing** | `worlds.md`, DEC-8 |
| **2. Starting State** | A start recipe whose input is a dataset instead of a seed | ~15 | DEC-23 |
| **3. External inputs** | A recorded tape the World reads; **no Cells involved** | **22 — the largest by demand** | WORLD-7 |
| **4. Reference cases** | Comparison target; never enters the simulation | **~40 — the largest by volume** | REFCASE- |

**The distribution is the finding.** Pipeline 4 dominates and is the cheapest — a reference case needs to be *read and compared against*, not mapped into a declared schema. Pipeline 3 is the most demanded of the pipelines that actually feed a Run, and it is also the simplest: a time series, no Cells, no Layout, no collapse.

**Pipeline 1 is where the real difficulty is, and it is much narrower than it looks.** Sixteen Labs want real topology. Most cannot have it.

---

## 2. Pipeline 1 — World structure

For a relational World there is no separate dataset to load into a Layout. **The data is the Layout.** An auth log is the connection graph; a dependency manifest is the graph; a BGP table is the graph.

### Available, public, and load-bearing — build against these

| Lab | The data | Why it works |
| :--- | :--- | :--- |
| **45 Service Cascade** | Dependency graph emitted by service-mesh telemetry | Machine-readable, current, and produced automatically as a byproduct of running the system |
| **46 Routing Instability** | Autonomous-system graph | Public, inferred continuously, with twenty years of archive |
| **56 Software Supply Chain** | Package registry graph with full version and maintainer history | Completely observable, downloadable, historical |
| **41 Urban Growth** | Land-cover raster **and** road network **and** jurisdiction boundaries | **Needs multiple Connection classes in one World** — the clearest driver for that requirement |
| **37 Highway Traffic** | Road geometry | Trivial structure; the value is in the tape (pipeline 3) |

### Named but unavailable — these are why the synthetic suite exists

| Lab | The data | Why not |
| :--- | :--- | :--- |
| **47 Lateral Movement**, **52 Ransomware**, **55 Segmentation** | Enterprise host/credential/zone topology | **Ground truth does not exist**, even inside the organization. Enterprise trust relationships are famously undocumented. |
| **48 Identity and Privilege** | Directory graph | Exists, and is confidential. Will not be shared. |
| **42 Power Grid** | Transmission topology | Security-restricted in most jurisdictions |
| **44 Freight** | Rail network with schedules | Passenger data public; **freight is proprietary** |
| **39 Warehouse Robot** | Floor layout and task stream | Commercially closed |
| **49 Prompt Injection** | Agent read/write authority graph | Not recorded anywhere as a graph |

**That is the honest case for `SYNTH-3`**, and it is stronger than "synthetic is convenient": for six of these Labs the alternative is not slower, it is *absent*.

### A special case worth naming

**7 Karst** needs a **fracture network** — inherited tectonic geometry, not an emergent structure. It is Layout ingested as data, on a Lab whose validation is otherwise qualitative-only. Structure available, outcomes not.

**36, 38, 40** need **floor plans** — genuinely spatial, genuinely available (any building has drawings), and low-drama to ingest. The easiest pipeline-1 case in the catalog and worth using as the first test.

---

## 3. Pipeline 2 — Starting State from a dataset

An ingestion procedure here is **a start recipe (DEC-23) whose input is a dataset instead of a seed.** Same binding: recipe plus realized values plus source identity, all recorded on the Run.

| Lab | Initial field |
| :--- | :--- |
| 1 Wildfire | Fuel type, load, moisture, terrain |
| 3 Landslide | Slope, cohesion, saturation |
| 4 Dune, 6 River | Bed elevation |
| 5 Coastal | Shoreline position and profile |
| 8 Permafrost | Ice content, polygon geometry |
| 9 Melt ponds | Ice surface topography |
| 12 Vegetation | Terrain and slope |
| 14 Invasion | Habitat suitability and initial occupancy |
| 15 Forest gap | Stem map — **already individually tagged and mapped** |
| 16 Pest | Host density, stand age |
| 17 Coral | Substrate occupancy |
| 18 Mycelial | Resource distribution |
| 19 Seed | Adult positions |
| 21 Excitable | Tissue heterogeneity, fibre orientation, scar geometry |
| 22 CSD | Cortical surface geometry — **folded, and the folding is the mechanism** |
| 41 Urban | Existing developed extent |

Almost all of these are **rasters**, which is convenient: the World's arrangement matches the data's arrangement and there is no structural mapping to argue about — only resolution.

**The two exceptions are the interesting ones.** Entry 15's stem map is a point set, not a raster, and forcing it to a lattice is a modelling choice. Entry 22's cortical surface is a folded manifold, and flattening it while preserving adjacency is the requirement — *surface topology independent of display coordinates*.

---

## 4. Pipeline 3 — External input tapes

**The most demanded pipeline, and the simplest.** A recorded series the World reads; no Cells, no Layout, no collapse. Twenty-two demands across the nine reports.

| Tape | Labs |
| :--- | :--- |
| **Wind series** | 1, 4, 5 |
| **Rainfall / storm sequence** | 3, 12, 15 |
| **Wave climate** | 5 |
| **Discharge and sediment supply** | 6 |
| **Warming trajectory** | 8 |
| **Melt forcing** | 9 |
| **Large-scale meteorology** | 11 |
| **Drought and winter cold** | 16 |
| **Temperature, acidification, fishing pressure** | 17 |
| **Recruitment inflow** | 26 — *arrives from outside the World and dominates the outcome* |
| **Thermal schedule** | 29, 32 |
| **Applied load** | 31 |
| **Deposition flux** | 33 |
| **Charge/discharge schedule** | 34 — **a phase schedule, not a smooth tape** |
| **Gas composition** | 35 |
| **Traffic inflow demand** | 37 |
| **Task stream** | 39 |
| **Population and demand** | 41 |
| **Service load** | 45 |
| **Timetable** | 44 — **scheduled events at clock times, not tick-uniform** |

**Three tape shapes, not one.** Most are smooth series. Entry 34 is a **named phase schedule** with asymmetric transitions. Entry 44 is **clock-scheduled discrete events**. Those need different Reactor vocabulary, and the tape generator should not pretend they are the same thing.

---

## 5. Pipeline 4 — Reference cases

**Roughly forty datasets, and none of them enter a Run.** They are what a result is compared against. This is the cheapest pipeline and the largest, and recognizing that is the main practical relief in this inventory.

Sorted by how directly a Run's output can be compared:

### Same data type as a Run's stored history — direct frame-by-frame comparison

| Lab | Data |
| :--- | :--- |
| **24 Wound healing** | Scratch-assay time-lapse — *structurally identical to a stored Run* |
| **21 Excitable media** | Optical mapping movies of voltage across tissue |
| **35 Catalytic** | PEEM movies of surface patterns |
| **11 Convection** | Daily satellite imagery since 2000 |

### Quantitative statistics from controlled experiment

25 biofilm (plate photographs: fractal dimension, branch spacing, sector counts) · 10 snow (chamber growth at known temperature and supersaturation) · 6 river (flume braiding) · 27 cell sorting (hanging-drop aggregates) · 36 and 38 (instrumented corridor experiments with tracked participants) · 30 and 29 (electron backscatter orientation maps) · 33 (scanning probe and X-ray reflectivity roughness) · 34 (operando tomography, cycling statistics) · 23 (spheroid growth curves and layer thicknesses) · 28 (inspection coupons with pit depths and positions)

### Long-run observational series

1 wildfire (mapped perimeters) · 4 dune (satellite dune fields: spacing, orientation, migration) · 5 coastal (satellite shoreline series plus a century of aerial photography) · 8 permafrost (InSAR subsidence, lake extent, polygon succession) · 9 melt ponds (aerial photography of hundreds of thousands of ponds) · 12 vegetation (Landsat to the 1970s) · 14 invasion (annual range maps over a century) · 15 forest (plots remeasured for decades) · 16 pest (annual aerial mortality mapping) · 17 coral (photo-quadrat series) · 41 urban (historical land-use maps with an established goodness-of-fit practice) · **37 traffic (continuous public loop-detector data — the best in the catalog)** · **46 routing (twenty years of BGP archives)** · **54 worm (archived network telescope traces — the only real propagation evidence in Family H)** · 45 service (traces plus detailed public post-incident reports) · 56 supply chain (registry history)

### Not a dataset at all

**30 Grain growth** compares against **an exact relation**, not a measurement. It is the only entry in the catalog with law-level correctness available, and it needs no ingestion whatsoever to be useful.

---

## 6. Labs needing no ingestion

Eleven entries need nothing ingested, for three different reasons — and knowing which is which prevents building machinery nobody will use.

| Reason | Labs |
| :--- | :--- |
| **Rejected fit** — no build, no data | 43 water, 51 sensitive data, 53 patch, 60 parking lot |
| **Validation structurally unavailable** — nothing to ingest even in principle | 2 smouldering (subsurface), 7 karst outcomes, 26 immune (endpoint histology cannot check a time course), 40 degraded evacuation (the experiment is unethical), 50 agent memory (unmeasured) |
| **Boundary markers** — argument, not evidence | 57, 58, 59 |

---

## 7. The collapse, per Lab

The semantic ceiling makes ingestion **lossy by design.** The contract is provenance-shaped: source identity, the mapping including resolution, what was dropped, gaps and how they were handled. *An interpolated value presented as observed is a fabrication.*

The sharpest declared collapses in the catalog, which are the ones to build the contract against:

| Lab | The collapse | Cost |
| :--- | :--- | :--- |
| **1 Wildfire** | Four dead-fuel moisture timelag classes (1, 10, 100, 1000-hour) → **one scalar** | The difference between classes is often what decides whether a fire runs |
| **15 Forest gap** | Many coexisting species per patch → **one dominant occupant** | May be too coarse for the exact diversity question the Lab wants |
| **22 CSD** | Folded cortical manifold → flat lattice | Discards the geometry that produces propagation block |
| **49, 50** | Text semantics → **a contamination or distortion scalar** | Possibly destroys the mechanism; needs the sufficiency test |
| **46 Routing** | ~1M prefixes → a handful of tracked destinations | Studies a different scale than the operational reality |
| **17 Coral** | Moving grazers → a precomputed pressure field | Acceptable for the first Study; fails if grazer movement becomes the hypothesis |
| **13 Plankton** | Moving water → fixed patches | **Fatal** — this is why the Lab grades weak |

---

## 8. What to build first

**SYNTH before wild, and within wild, tapes before topology.**

1. **Tapes (pipeline 3)** — most demanded, structurally trivial, no collapse to argue about, unblocks a driver class across four families. Start with smooth series; add phase schedules and clock-scheduled events as separate shapes.
2. **Raster starting states (pipeline 2)** — the World's arrangement already matches the data's, so only resolution is in question.
3. **Reference-case reading (pipeline 4)** — not ingestion at all in the strict sense; it is comparison machinery, and it is where two-thirds of the named data lives.
4. **Public relational topology (pipeline 1)** — 45, 46, 56 only. All three are machine-readable, current, and free.
5. **Floor plans (pipeline 1)** — the easiest spatial topology case, and a good first test of a non-raster Layout.

**Do not build** enterprise-topology ingestion. Six Labs want it and none can have it; that path runs through `SYNTH-3`, not through a connector.

---

## 9. Open questions

- **Who owns shared ingestion machinery?** It is the fifth member of DEC-5's translation family and currently has no home.
- **Where does resolution choice get recorded?** For grid Worlds the data supplies values and the Lab chooses resolution — that choice is a modelling commitment and belongs on the Run, not in a config file.
- **Is a sufficiently expressive start recipe a mechanism in disguise?** DEC-23's third question, sharpened by the raster cases above.
- **Does a reference case need the same provenance contract as ingested data?** It never enters a Run, so the collapse contract does not apply — but a comparison claim depends on it just as strongly.
