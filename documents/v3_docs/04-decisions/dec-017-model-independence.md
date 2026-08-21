# DEC-17 — What changes when we change the AI?

*Formal name: model independence. Cite this record as **DEC-17**.*

**Status:** open · **Who decides:** the project owner, on a proposal · **Kind:** deferred detail — the record-keeping that makes it answerable is already law

> **In one sentence:** the AI that writes our rules will be swapped, upgraded, and multiplied over this platform's life — and the evidence must always show which machine wrote what, because different machines make different mistakes.

---

## What this is about

A transcription service gets replaced; the new one is better overall but makes *different* errors than the old one. Any office that has lived through that knows the two survival rules: record which system produced which document, and expect the error patterns to shift under you.

Same here. Rules are written by an AI model. Models get upgraded, swapped between providers, and eventually mixed — one writing, another repairing. Each has its own habits and its own characteristic failures, and our library is supposed to be *generator-quality data*: it should be able to answer "did the upgrade make the mechanisms better or worse?" That question is only answerable if the bookkeeping was right from the start.

The bookkeeping is already law: every generation records the machine's identity and settings, the **exact rendered text sent to it** (stored, never reconstructed from templates that may have changed since), and its raw responses. And the record must always distinguish *this machine's output naturally varies* from *we failed to record what we asked it* — an honest limitation versus a platform defect.

## What's open

The seams: which parts of the Generation pipeline are provider-neutral versus provider-specific; whether prompts are per-model or shared; how a model change is surfaced in the library ("mechanisms before / after the upgrade"); and what happens to in-flight work during a swap.

## What this is blocking right now

- Nothing — a single model, fully recorded, satisfies every current requirement.
- Due when the second model arrives. The bookkeeping that makes the transition safe is already in force.

---

## The precise version

*This is the wording other documents cite.*

Which parts of Generation are provider-neutral, and how model changes appear in provenance. Constrained by `../01-core/generation.md` GEN-15 through GEN-17 (identity, settings, rendered inputs stored not reconstructed, raw outputs; the varies-versus-unrecorded distinction) and `../01-core/corpus.md` CORPUS-5.

**A decision here owes:** the alternatives considered; the reasoning in plain language; what evidence would reopen it; the documents to be revised; and a status change recorded rather than assumed.

---

## Record history

**2026-08-21 — rewritten for readability.** Plain-question format; question, identifier, status, and constraints unchanged. Prior text is in version history.
