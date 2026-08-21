# DEC-9 — How much may the platform guess before asking?

*Formal name: Study planner autonomy. Cite this record as **DEC-9**.*

**Status:** open · **Who decides:** the project owner, on a proposal · **Kind:** deferred detail — the safety rail is set; the dial position isn't

> **In one sentence:** when someone asks a question in plain words, the platform figures out what experiment they mean — and we've decided it must read that back for confirmation before running anything; what's open is how much it fills in along the way.

---

## What this is about

Someone types: *"does the failure stop if I isolate this network?"* That is already an experiment — change one thing, see what changes — whether or not anyone calls it one. The platform's job is to recognize it, propose the setup, and put it in front of the asker.

The settled part is the read-back. Like a dispatcher repeating an address back to a caller, the platform states what it understood — question, what's held constant, what's varied, what would count as an answer — and **gets confirmation before anything runs.** That rail is law (STUDY-16): the platform never chooses an experiment and then reports the result as though it had been asked for.

The open part is the dial between the extremes. Fill in too little, and users must specify everything — the plain-language promise dies of paperwork. Fill in too much, and the machine has effectively chosen the experiment, with confirmation reduced to an OK-button people click without reading. The right position probably differs by how expensive the Study is and how much the inference had to invent.

## What this is blocking right now

- Nothing. Studies can be specified explicitly today; the confirmation rail is already in the requirements.
- This gets decided well when there are real users to watch, and badly in the abstract. It should wait for them.

---

## The precise version

*This is the wording other documents cite.*

How much SCR infers automatically from a semantic question before requiring human confirmation. Constrained by `../01-core/studies.md` STUDY-15 and STUDY-16: a proposed question, hypothesis, and comparison contract are shown for confirmation before Runs execute.

**A decision here owes:** the alternatives considered; the reasoning in plain language; what evidence would reopen it; the documents to be revised; and a status change recorded rather than assumed.

---

## Record history

**2026-08-21 — rewritten for readability.** Plain-question format; question, identifier, status, and constraints unchanged. Prior text is in version history.
