# Identity and access

**Document class:** Level 3 — Requirements · **Status:** draft
**Path:** `02-platform/identity-and-access.md`
**Identifier namespace:** `IDENT-` — reserved to this document. Identifiers are permanent and never reused.
**Cites:** SCR-F v0.2 §22, §31, §33 · `../01-core/corpus.md`, `../03-quality/human-review.md`, `../01-core/search.md`
**Standing constraint (§33):** Platform Services support the conceptual platform and must not define its scientific assumptions accidentally.

> Identity's first job here is not keeping people out. It is **attribution**: a platform whose evidence includes who corrected what, who decided what, and which machine wrote what, needs to know who everyone is before it needs to stop anyone.

---

## 1. Attribution before permission

**IDENT-1.** Every act that enters the permanent record carries its actor: who supplied a correction and why (CORPUS-10), who adopted a document, who promoted a Lab, who designated a Run evidence-grade (DEC-2), who decided an open decision (REVIEW-1). "The system" is not an actor; an unattributed act of that kind is a defect.

**IDENT-2.** Machines are actors too, identified with the same seriousness: which model, which version, which settings wrote or repaired a mechanism (GEN-15). Human and machine attribution use one framework — the provenance model already adopted for the Corpus treats "who is responsible" as a first-class concept for both (CORPUS-6).

**IDENT-3.** Attribution is never retroactively editable. A recorded actor on a recorded act is part of the evidence.

---

## 2. Access, in the current phase

**IDENT-4.** The platform's current posture — single user, optional sign-in, everything readable — is documented as **temporary**, adequate for the same reason the earlier system's execution posture was: one trusted person, one host. The moment a second person arrives, every read and write surface needs a deliberate answer, and the gate for that is DEC-16's mechanism plus this document's ownership question below.

**IDENT-5.** Authorization, when it arrives, is a platform service and never a scientific assumption (§33): nothing about what an experiment *is* may depend on who may see it.

---

## 3. The ownership question — flagged, not answered

The Corpus is described everywhere as **one durable body of evidence** — that framing does real work: coverage claims, search honesty, the accumulated-library argument all lean on it. None of the founding documents says *whose* evidence it is. That was invisible with one user, and stops being invisible the moment a Lab models a real organisation's incident data, or two users disagree about what may be shared.

**IDENT-6.** Until the ownership question is registered and decided, no partitioning of the Corpus is built. Partitioning changes the meaning of every coverage statement — and a Search that silently sees only *your* slice while speaking as if it saw everything violates SEARCH-8 in the worst available way: absence of evidence would quietly mean absence of *permission*.

**IDENT-7.** When partitioning is decided, every coverage, search, and Study statement must say what body of evidence it speaks for. The one-Corpus language in the founding documents becomes conditional the same day, by amendment, not by drift.

This is one of the three registry candidates (`../04-decisions/README.md`); registering it is the owner's call.
