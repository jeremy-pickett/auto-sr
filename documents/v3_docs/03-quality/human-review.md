# Human review

**Document class:** Level 3 — Requirements · **Status:** draft
**Path:** `03-quality/human-review.md`
**Identifier namespace:** `REVIEW-` — reserved to this document. Identifiers are permanent and never reused.
**Cites:** SCR-F v0.2 §4, §16.5, §31, §36.3, §36.5, §36.6, §43; F-4 · `../00-start-here/human-and-machine.md`, `../01-core/corpus.md`

> Most of this platform's documentation and most of its mechanisms will be machine-written. Review is what stands between that and a system that agrees with itself.

---

## 1. What only a person can do

**REVIEW-1.** These acts are performed by a person and are never delegated, automated, or inferred from an absence of objection:

- **adopting** a document, moving it from draft to relied-upon;
- **deciding** an open decision;
- **promoting** a Lab's status;
- **declaring** a mechanism useful, or a finding worth acting on;
- **accepting** that evidence justifies a real-world action.

**REVIEW-2.** A machine-written document enters the tree as a draft and cannot promote itself. Nothing downstream may rely on it until a person adopts it.

**REVIEW-3.** Silence is not adoption, and time passing is not adoption. A draft that nobody objected to for six months is a draft.

---

## 2. Reviewing what a machine wrote about its own work

**REVIEW-4.** Every machine-produced account of machine-produced work is **interpretation**: repair explanations (GEN-14), generated summaries, narration, and any confidence statement not traceable to a computation.

**REVIEW-5.** Reviewing such an account means checking it against the evidence it describes, not reading it for plausibility. Plausibility is what the machinery is best at and is therefore worthless as a signal.

**REVIEW-6.** Where an account cannot be checked against evidence, the review records that it could not be checked. It does not record approval.

---

## 3. Reviewing a machine-written document

A tree of this size drifts at the root, one reasonably-interpreted ambiguity at a time. Review is where that gets caught, and it takes specific questions rather than general attention.

**REVIEW-7.** A review of a document in this tree checks at least:

| Check | Failure it catches |
|---|---|
| Does it cite the sections and identifiers it depends on? | claims with no traceable basis |
| Did it **flag** ambiguity rather than resolve it? | an undecided question inherited as settled fact |
| Did it refuse questions the Decision Registry owns? | a fork answered locally, invisibly |
| Is subject vocabulary absent from core documents? | the leak that propagates into every later document |
| Is every citation real, and verified? | the most damaging single failure available to a machine writer |
| Does it name a technology above Level 3? | a replaceable choice made permanent by placement |
| Does it distinguish evidence from interpretation? | authority attaching to something that has not earned it |

**REVIEW-8.** Citations are spot-checked against their sources during review, not accepted because they are well-formed. A fabricated reference is confident, specific, and indistinguishable from diligence without looking.

**REVIEW-9.** A reviewer who resolves an open decision while reviewing has answered a question the tree deliberately left open. The correct action is to critique the framing and record the finding.

---

## 4. Corrections

**REVIEW-10.** A correction records the original machine proposal or interpretation, the correction, the reason where given, what changed as a result, who supplied it, and what later work depends on it (CORPUS-10).

**REVIEW-11.** A correction never rewrites what it corrects. Disagreement stays visible and attributed (CORPUS-11).

**REVIEW-12.** A person's correction is not automatically right. It is evidence of expert disagreement, recorded as such, and it can itself be disputed later. What the platform guarantees is that both positions survive with their reasons, not that the human one wins.

---

## 5. Amendment

**REVIEW-13.** Where any document, Run, Study, or Lab review demonstrates that a higher document is wrong, the discovery is filed as a proposed amendment with the evidence attached. It is not fixed locally by the document that found it.

**REVIEW-14.** An adopted amendment revs the amended document's version, records the change in its revision history, and leaves the superseded text readable.

**REVIEW-15.** Identifiers are permanent and never reused. A retired requirement is marked retired, with the amendment that retired it, and is not deleted.

**REVIEW-16.** An amendment record states: what it was, what it is now, why, who raised it, what did not change, and what remains outstanding.

> Being wrong is recoverable. Being silently reinterpreted is not.

---

## 6. Conflict between adopted documents

**REVIEW-17.** A conflict between two adopted documents is a **defect in the tree**. It is recorded as one and resolved by amendment.

**REVIEW-18.** No downstream writer resolves such a conflict by choosing a side, and no reader is expected to work out which document was meant. Where a conflict is known and not yet resolved, both documents carry a note pointing at the other.

---

## 7. What review is for

**REVIEW-19.** Review moves human attention toward judgement and away from mechanical checking. Where a check can be made mechanical — a citation format, a namespace collision, a missing identifier, a technology name above Level 3 — it is made mechanical, so that review time is spent on the parts that need a person.

**REVIEW-20.** The parts that need a person are the ones this document opened with: whether the abstraction is defensible, whether the question was worth asking, whether the evidence supports the claim, and whether anyone should act on it.
