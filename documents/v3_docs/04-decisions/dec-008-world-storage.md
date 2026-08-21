# DEC-8 — One filing system for two shapes of world?

*Formal name: World storage. Cite this record as **DEC-8**.*

**Status:** open · **Who decides:** the project owner, on a proposal · **Kind:** deferred detail — one hard constraint is already registered; the rest is engineering that building will inform

> **In one sentence:** some experimental worlds are shaped like maps and some are shaped like org charts, and a filing system built for one quietly cripples the other.

---

## What this is about

A grid world — terrain, ice, tissue — files naturally like a map: every patch has coordinates, every patch has the same neighbours-count, storage is a neat rectangle.

A relationship world — accounts and permissions, machines and connections — files like an org chart. And org charts don't fit rectangles: you can't file an org chart by street address, and you can't assume everyone has the same number of connections.

The trap is specific and known. The earlier system got real speed from map-shaped storage, and the temptation is to reuse it everywhere by giving every participant a fixed number of connection slots. But real networks aren't like that: **a few participants are hubs with enormous connection counts, while most have a handful** — think of the identity provider every account touches, the shared server every workstation reaches, the one group everyone belongs to. Slots sized for the hubs waste nearly all their space; slots sized for the typical participant can't hold the hubs. Either way, the org-chart worlds become second-class citizens of a map-shaped filing system — while appearing supported.

That one constraint is already law in the core documents: **storage may not assume everyone has roughly the same number of connections unless the world family guarantees it.**

## What's open

The actual representation — how both shapes are stored efficiently without forcing one into the other's mold. This is engineering, it has known good starting points (store each connection as its own entry: from, to, kind), and real Lab data will teach us more than debate will.

## What this is blocking right now

- `../02-platform/storage.md` cannot be written to production quality without this and DEC-2.
- Nothing conceptual — the constraint that matters is registered (WORLD-15).

---

## The precise version

*This is the wording other documents cite.*

What common representation handles spatial and relational Worlds without forcing one into the other's shape. Constrained by `../01-core/worlds.md` WORLD-15: a World's representation may not assume near-uniform connection counts unless the World family guarantees it — connection counts in real networks commonly follow a power-law distribution with high-degree hubs (Barabási and Albert, 1999 — cited there).

**A decision here owes:** the alternatives considered; the reasoning in plain language; what evidence would reopen it; the documents to be revised; and a status change recorded rather than assumed.

---

## Record history

**2026-08-21 — rewritten for readability.** Plain-question format; question, identifier, status, and constraints unchanged. Prior text is in version history.
