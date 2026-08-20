# 33. Thin-Film Growth Lab

**Document class:** Lab Knowledge Brief · **Status:** draft
**Catalog:** SCR Lab Catalog v0.1 #33, Family E · **Standing:** ungraded
**Cites:** SCR-F v0.2 §11, §29, §30, §41; F-17
**Fit review (§30):** not performed

---

## The phenomenon

Deposit atoms onto a surface one at a time. Each lands somewhere, hops around for a while if it has enough thermal energy, and eventually sticks — usually next to an atom that is already there. Repeat a few billion times and you have a film.

Whether that film is smooth or rough, continuous or full of holes, and whether it grows layer by layer or as isolated islands that eventually merge, determines everything about its usefulness. Semiconductor devices, optical coatings, hard coatings, and barrier layers all depend on getting this right, and the difference between a good film and a useless one is set by the balance between how fast atoms arrive and how far they can move before they are buried.

There are three classical growth modes, distinguished by whether the arriving material wets the substrate: layer-by-layer, island, and layer-then-island. Which one occurs follows from surface energies.

## What the domain already knows

**This is the home domain of kinetic roughening theory, and that theory is one of statistical physics' cleanest successes.** A growing surface's roughness increases with time as a power law and saturates at a value set by system size, with both behaviours characterized by exponents. Family and Vicsek's scaling relation ties them together.

**And the exponents are universal.** Kardar, Parisi, and Zhang (1986) wrote down the continuum equation for a growing interface with lateral growth, and the **KPZ universality class** has known exponents — in one dimension, exactly 1/2 for roughness and 1/3 for growth *(these values I am confident of; the higher-dimensional values are numerical and I would verify)*. Ballistic deposition and the Eden model fall in this class. Deposition with surface relaxation falls into a different, linear class with different exponents.

This is the fact that dominates the Lab. **If a growth mechanism belongs to a known universality class, its scaling behaviour was determined before anyone ran it.** The exponents do not depend on the details of the rule — that is what universality means.

**Growth mode selection is a surface-energy argument**, classical and closed-form: compare substrate surface energy, film surface energy, and interface energy.

**Lattice models are the standard tool and always have been.** Solid-on-solid models, ballistic deposition, and kinetic Monte Carlo with explicit hopping barriers are how this field computes. SCR would be entering a domain built on cellular models.

## Where the shortcut holds, and where it breaks

**Reducible — and this is the largest reducible core in the catalog.** Roughness scaling exponents, given the universality class. Growth mode from surface energies. Island density scaling with deposition rate and temperature — a classical nucleation-theory result with known exponents. Saturation roughness for a given system size. Time to continuity, approximately.

**Irreducible.** What universality does not cover, and it is a real list:

- **Which universality class a given mechanism belongs to.** This is the sharp point. Universality tells you the exponents *once you know the class*, and determining the class for a novel mechanism is generally done by simulating it and measuring. That is irreducible in a precise and interesting way: the shortcut exists but only downstream of the thing you have to run.
- **Crossover behaviour.** Real systems show one scaling at short times and another later, and the crossover length and time are non-universal, mechanism-specific, and exactly what an experimentalist measures.
- **Island coalescence.** When separate islands touch and merge, the resulting grain boundaries and voids depend on the arrangement of nucleation sites. Film continuity — whether there are pinholes — is set here and is not a scaling question.
- **Ehrlich–Schwoebel effects and mound formation.** An extra barrier for atoms descending a step edge causes material to pile up rather than smooth out, producing mounds and unstable growth. Whether that instability wins is a competition between rates with a threshold.

**The lens, stated plainly.** Thin-film growth is the catalog's best illustration of a subtle and important point: **universality is a shortcut that makes most mechanisms equivalent, which is simultaneously a devastating limitation and a precise opportunity.**

Devastating, because the corpus's headline claim — that different mechanisms produce different behaviours worth cataloguing — is exactly false for scaling exponents. A hundred mechanisms in the KPZ class all give the same answer, and the corpus would be recording the same number a hundred times.

Precise, because the corpus's *actual* question becomes worth asking: **which local rules fall into which class, and where are the boundaries between classes?** That is a real, unresolved, ensemble-shaped question. Classifying mechanisms by universality class is a mapping exercise nobody has done systematically because it requires running many mechanisms, which is what this platform does.

## What a Cell would carry

A surface site: height (number of deposited layers), occupancy, and possibly species or a mobility state. This is the smallest useful state in the catalog alongside #30 — a solid-on-solid model needs one integer per column. §13.1 met trivially.

Layout is a grid and physically appropriate — crystalline surfaces really are lattices. The unusual comfort here is that **lattice discreteness is not an artifact**; atoms genuinely occupy discrete sites. This is one of only two or three Labs (with #10) where the grid is the physics rather than an approximation to it.

## Honest strength assessment

*My assessment, not a fit review (§30). It carries no standing and does not promote this entry.*

**Plausible, and more interesting to the platform than to the domain — but for a genuinely novel reason, not a consolation one.**

The domain case is weak in the usual way: mature theory, established lattice methods, exponents known. But the **universality framing gives this Lab a question that is specifically suited to a corpus and unsuited to a conventional research programme**, and I have not seen that argument made elsewhere in this catalog.

Mapping mechanism space to universality classes requires generating many mechanisms and running each to measure exponents. No individual investigator does that — it is not a paper. A corpus does it as a byproduct of existing. And the resulting map has real content: knowing that a proposed rule family is KPZ tells an experimentalist their measured exponent will not discriminate between their candidate mechanisms, which is a genuinely useful negative result.

**The upside worth being excited about.** The negative space argument is unusually strong here. "These eleven mechanism families all produced KPZ exponents; the measurement you are planning cannot distinguish them" is exactly the kind of pruning the position paper claims and this domain makes it concrete and checkable.

Data availability is excellent: scanning probe and X-ray reflectivity measurements of film roughness versus thickness are routine, published, and quantitative, and the exponents are directly comparable.

There is also a clean methodological benefit for the platform itself: this is a domain where **the same behaviour arises from many different mechanisms**, which is the exact opposite of the intent–outcome gap the position paper emphasizes. A corpus that only records surprising divergences would miss it. Having one Lab that stress-tests the indexing scheme's ability to represent *convergence* is worth having.

**The challenges, in order of severity.**

1. **Universality flattens mechanism differences** — the corpus's core value proposition partly fails here, and honestly stating that is required.
2. **Mature theory and established lattice methods.**
3. **Exponent measurement needs large systems and long runs** to separate scaling from crossover, which is computationally demanding.
4. **Small research audience** for the mapping question, though a real one.
5. **Deposition is an external driver**, a mild DEC-1 case.

## Non-claims

This Lab does not predict film properties for any real deposition process and produces nothing suitable for materials or manufacturing decisions (§41, §43).
