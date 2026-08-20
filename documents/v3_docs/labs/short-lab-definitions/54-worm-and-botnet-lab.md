# 54. Worm and Botnet Lab

**Document class:** Lab Knowledge Brief · **Status:** draft
**Catalog:** SCR Lab Catalog v0.1 #54, Family H · **Standing:** ungraded
**Cites:** SCR-F v0.2 §11, §15, §29, §30, §41; F-17, F-20
**Fit review (§30):** not performed

---

## The phenomenon

Self-propagating code finds vulnerable hosts, compromises them, and uses each new host to find more. With no human in the loop, growth is exponential until the vulnerable population is exhausted or the network itself becomes the limit.

The historical events are the reference points. Code Red in 2001 infected on the order of three hundred and fifty thousand hosts in a day. Slammer in 2003 was a single UDP packet requiring no connection handshake and infected most of its vulnerable population **in about ten minutes**, at which point it was limited not by the exploit but by the bandwidth it had saturated. Later, worm-propagated ransomware in 2017 combined self-propagation with destructive payloads and caused losses in the billions.

Botnets are the persistent version: compromised hosts retained under central or peer-to-peer command, growing and decaying continuously against defender takedowns.

## What the domain already knows

**This domain has an analytic model and it fits the data well — which is unusual and decisive.**

Staniford, Paxson, and Weaver's 2002 analysis showed that a random-scanning worm's spread follows the logistic curve of classical epidemiology, and fitted it to Code Red's observed infection counts with good agreement *(attribution from memory, verify)*. The same paper introduced faster designs — hit-list scanning to bootstrap the epidemic, permutation scanning to reduce redundant work, and the flash worm concept — and estimated how quickly a well-engineered worm could saturate its population. Those estimates were, uncomfortably, borne out by Slammer a few months later.

**The refinements are also analytic.** Local-preference and topological scanning are handled by epidemic models on structured graphs. Bandwidth-limited saturation, which is what actually stopped Slammer, is a resource constraint with a straightforward form. Epidemic thresholds on scale-free contact networks — the result that the threshold vanishes as the degree distribution's tail heavies — is a known analytic result *(Pastor-Satorras and Vespignani, 2001)*.

**Measurement infrastructure exists.** Network telescopes — large blocks of unused address space that record unsolicited traffic — captured the historical events directly, and the traces are archived and studied. This is genuine, quantitative, timestamped reference data for a real self-propagating event.

**The threat has substantially changed.** Internet-scale scanning worms of the classic kind are largely a historical phenomenon: network address translation, firewalls, faster patching, and cloud hosting removed the flat reachable address space they depended on. Contemporary propagation is mostly internal to enterprises or targets embedded devices.

## Where the shortcut holds, and where it breaks

**Reducible — and the reducible core here is the largest in Family H.**

Random-scanning worm growth: logistic curve, closed form, fitted to real events with good agreement. Time to saturation from scan rate and vulnerable population. Epidemic threshold on a given contact structure. Bandwidth saturation limits. Botnet population equilibrium under constant infection and takedown rates: a birth-death process with a closed-form steady state.

**A Lab that models worm spread and produces an S-curve has reproduced a 2002 result.**

**Irreducible.** What remains, honestly:

- **Topological propagation on real structures.** When a worm spreads along the graph of who-connects-to-whom rather than by random scanning, the outcome depends on the specific topology, and enterprise topologies are heterogeneous and clustered in ways no random graph captures.
- **Interaction with defence.** Takedowns, sinkholing, and patching race the propagation. As in #52, a race between timed processes with delayed observation has no closed form.
- **Segmented environments.** Modern propagation happens inside networks with partial segmentation, which makes it a percolation question on a specific structure rather than a well-mixed epidemic. Whether a worm crosses a boundary is arrangement-dependent.
- **Multi-mechanism propagation.** Contemporary self-propagating malware uses several methods with different reachability, and their union on a specific environment is not the sum of their independent behaviours.

**The lens, stated plainly.** This Lab is the catalog's clearest case of a domain where **the analytic shortcut genuinely works for the historical phenomenon** — and where the phenomenon has since moved somewhere the shortcut fits worse.

Classic internet-wide scanning was well-mixed, which is why epidemiology described it so well. Contemporary propagation is inside structured, segmented, heterogeneous enterprise networks, which is exactly where well-mixed assumptions fail. The opening, if there is one, is entirely in that shift — and it makes this Lab a specialization of #47's reachability problem rather than an independent domain.

## What a Cell would carry

A host: vulnerable, infected, patched, or immune; scan rate; reachability class; and detection state. Bounded scalars; §13.1 met trivially — this is close to an SIR state machine.

**Layout is a Network World.** For the historical case the "network" is a flat address space, which is nearly a well-mixed population and barely a topology at all. For the contemporary case it is a segmented enterprise network, which is #47's and #55's World.

That is worth stating plainly: **this Lab and #47 and #55 share a World**, and the difference between them is the mechanism running on it — autonomous propagation, directed movement, or containment evaluation. If SCR builds Family H, they should be built as one World with three mechanisms rather than three Labs.

## Honest strength assessment

*My assessment, not a fit review (§30). It carries no standing and does not promote this entry.*

**Weak to plausible, and I would place it fifth in Family H — behind #48, #47, #52, and #55.**

The catalog's own framing is the right instinct: *"historically the domain that made everyone reach for epidemic models, and the place to test whether those models mislead."* But testing whether epidemic models mislead is a methodological exercise, not a domain contribution — and for the classic worms the answer is that they did not mislead much, which is why the 2002 paper is still cited.

The independent case is thin. The historical phenomenon is analytically covered and largely extinct. The contemporary phenomenon is enterprise lateral propagation, which belongs to #47.

**The upside worth being excited about — and there are two genuinely good things here.**

First, and best: **this is the only Lab in Family H with real, quantitative, timestamped reference data for the actual phenomenon.** Network telescope traces of Code Red and Slammer are archived and public. Every other security Lab in this catalog faces the objection that its topology is unverifiable and its outcomes unmeasurable. This one can check a generated mechanism's infection curve against a measured one from a real event. If Family H needs a **calibration anchor** — the thing wildfire is for Family A — it is this Lab, and it is the only candidate.

That is a strong argument for building it despite the weak domain case: not for what it says about worms, but because it is the only place Family H can demonstrate that its evidence chain works at all.

Second, the **well-mixed-to-structured transition** is a real methodological question: at what degree of segmentation does the epidemic approximation stop describing propagation, and how does that threshold depend on the segmentation pattern? That is answerable, publishable, and directly relevant to whether the security industry's habitual epidemic framing is still appropriate.

**The challenges, in order of severity.**

1. **The classic case is analytically solved** and fitted to real data twenty years ago.
2. **The phenomenon has moved**, and where it moved to is #47's territory.
3. **Direct dual-use content.** Worm design efficiency is exactly what the 2002 paper's most-cited section discusses. This Lab must stay on defence and containment questions and must not generate or optimize propagation strategies. F-20 and §18.4 apply with unusual directness, and this is the entry in the catalog where that constraint bites hardest.
4. **Overlap with #47, #52, and #55** is substantial enough to question independence.
5. **Modern reference data is scarce** — the good traces are two decades old.

## Non-claims

This Lab does not model any real network or malware, does not assess exposure or resilience for any organization, does not produce or evaluate propagation techniques, and produces nothing suitable for security decisions. It is ungraded and may fail its fit review (§30, §41, §43).
