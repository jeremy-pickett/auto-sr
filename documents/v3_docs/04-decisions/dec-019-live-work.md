# DEC-19 — Watching live versus the permanent record

*Formal name: live work. Cite this record as **DEC-19**.*

**Status:** open · **Who decides:** the project owner, on a proposal · **Kind:** deferred detail — the one dangerous failure is already fenced off

> **In one sentence:** today nothing is watched while it runs — experiments finish, then you review the finished record; if we ever add live viewing, provisional glimpses must be visibly provisional, because an unmarked provisional observation becomes evidence by default and nobody notices the moment it happens.

---

## What this is about

Emergency medicine runs on this distinction daily. A preliminary imaging read gets acted on — that's what it's for — but it is *labelled preliminary*, and everyone treats it accordingly until the final read is in. The label is not bureaucracy. It is the thing that prevents a quick first look from quietly becoming the official finding.

Our current model sidesteps the problem entirely, on purpose: **an experiment completes before anyone views it.** Playback is reading a finished, permanent record. That's what makes stepping backward free, makes every viewer see the same thing, and lets measurements invented years later run against old evidence.

Some future Labs may genuinely need live views — watching a long experiment progress rather than waiting. The founding document allows for it, with one requirement already law: **a provisional observation is marked provisional at the moment it is made.** Not retroactively. Not by convention. In the record.

## What's open

Everything else about live viewing, none of it urgent: what a live stream contains, how provisional observations are stored (or discarded once the final record exists), and how the interface visually separates *watching it happen* from *reviewing what happened*.

## What this is blocking right now

- Nothing. No current Lab needs live viewing; the completed-before-playback model is fully specified and serves everything on the roadmap.

---

## The precise version

*This is the wording other documents cite.*

If future Labs need live streams, how provisional live observations are separated from finalized immutable Runs. Constrained by `../01-core/runs.md` RUN-21 and RUN-22 (a Run completes before it is viewed; any streamed observation is marked provisional at the moment it is made) and SCR-F §19's distinction between a live execution stream and the finalized immutable Run.

**A decision here owes:** the alternatives considered; the reasoning in plain language; what evidence would reopen it; the documents to be revised; and a status change recorded rather than assumed.

---

## Record history

**2026-08-21 — rewritten for readability.** Plain-question format; question, identifier, status, and constraints unchanged. Prior text is in version history.
