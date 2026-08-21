# DEC-6 — What happens to the old library?

*Formal name: 2.x corpus migration. Cite this record as **DEC-6**.*

**Status:** partially decided · **Who decides:** the project owner · **Kind:** partially decided — the destination is settled, the moving arrangements are not

> **In one sentence:** everything the earlier system produced comes with us — that's decided; what's open is how the old records get new labels, and what happens to old measurements when our measuring tools improve.

---

## What this is about

The earlier version of this platform built a library: mechanisms, experiment histories, failures, the lot. Two things about it are already decided:

1. **It comes forward as founding evidence.** Not archived, not orphaned, not a separate lineage.
2. **Nothing in it gets rewritten. Ever.** Old histories are immutable evidence, same as new ones.

The unresolved part is familiar to anyone who has lived through a records-system change. When a hospital moves to a new charting system, the old charts come along — but old lab results were measured under old reference ranges, on old equipment. You don't re-interpret them silently as if they were measured today. You carry them forward *labelled as what they are*, and you decide deliberately which old readings are worth re-running under the new methods.

Same three questions here:

1. **Naming** — old records had old identifiers; how do they map into the new scheme without breaking anything that referenced them?
2. **Comparability** — an old experiment ran under old machinery; when may it be compared with a new one, and how is the difference flagged?
3. **Re-measuring** — our measurement tools (Readers) are versioned and improve; which old measurements get recomputed under new tools, and which are preserved as historical readings? The rule for that already exists: when both exist, keep both, each labelled with the version that produced it.

## What would make this easy to decide

Mostly, this one just needs doing rather than agonizing — it's the most mechanical record in the registry. One genuine judgment call inside it:

> **The old library is small now (tens of Runs) and a large scale-up is planned. Migrate before the scale-up, and the job is an afternoon; after, it's a project.**

The timing is the decision.

## What this is blocking right now

- Nothing today. It becomes urgent the moment the scale-up starts.
- `../01-core/corpus.md` §6 holds the constraints (CORPUS-12 to CORPUS-14).

---

## The precise version

*This is the wording other documents cite.*

**Decided (SCR-F §22.1):** the 2.x library is carried forward into the 3.x Corpus as founding evidence. **Constrained by §7:** migration never rewrites 2.x histories. **Open:** identifier mapping into 3.x namespaces, cross-version comparability, and which derived data is recomputed under 3.x Readers versus preserved as historical readings (CORPUS-14 governs the keep-both rule where recomputation happens).

**A decision here owes:** the alternatives considered; the reasoning in plain language; what evidence would reopen it; the documents to be revised; and a status change recorded rather than assumed.

---

## Record history

**2026-08-21 — rewritten for readability.** Plain-question format; question, identifier, status, and constraints unchanged. Prior text is in version history.
