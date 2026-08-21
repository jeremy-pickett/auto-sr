# DEC-10 — How does a measurement admit its doubts?

*Formal name: Reader trust presentation. Cite this record as **DEC-10**.*

**Status:** open · **Who decides:** the project owner, on a proposal · **Kind:** deferred detail — the obligations are law; the presentation is design work

> **In one sentence:** every measurement this platform shows must carry its own uncertainty and its known failure cases, in the same place as the number — what's open is what that looks like on screen.

---

## What this is about

A lab report never hands you a bare number. Values come flagged high or low, and when something went wrong with the sample, the flag says so right there — *result unreliable, repeat advised* — on the same page, not in a manual nobody opens.

Our measurements (Readers) owe the same. The obligations are already requirements:

- every assertion names the tool and version that produced it;
- important claims can be traced back to the exact evidence;
- uncertainty and known failure cases appear **with the result**, in ordinary language — because a measurement displayed without its doubts reads as a fact.

There's one more piece, and it's the unusual one: a Reader here records *where it worked and where it didn't*, and that coverage is presented as a **map, not a grade**. A measurement that succeeds on six of ten experiments hasn't scored 60% — it has found the boundary of the territory where that behaviour is even measurable, and the four failures are findings.

## What's open

Purely the presentation: how flags, versions, trace-back, and the coverage map appear in the interface without burying the result under its own caveats. This is design work, best done against real screens with real data.

## What this is blocking right now

- Nothing. The requirements are set (READER-11 to READER-15); this record closes when the interface is being built.

---

## The precise version

*This is the wording other documents cite.*

How Readers expose uncertainty and known failure cases in ordinary UI language. Constrained by `../01-core/readers.md` READER-13 through READER-15 (attribution, trace-back, uncertainty co-presented) and READER-11/READER-12 (coverage recorded and reported as a map, not a quality score).

**A decision here owes:** the alternatives considered; the reasoning in plain language; what evidence would reopen it; the documents to be revised; and a status change recorded rather than assumed.

---

## Record history

**2026-08-21 — rewritten for readability.** Plain-question format; question, identifier, status, and constraints unchanged. Prior text is in version history.
