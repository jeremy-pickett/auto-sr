# Foundations and Platform Architecture (SCR-F)

**Document class:** Level 1 — Foundations · **Status:** in review
**Path:** `00-start-here/foundations-and-platform-architecture.md`
**Cited as:** `SCR-F v0.2 §n`; condensed rules as `F-1` … `F-22`

> **Pointer, not a copy.** The canonical text of SCR-F v0.2 currently lives at
> `../../SCR_Foundations_and_Platform_Architecture_v0_2.md`. It has deliberately not been moved or
> duplicated here: a second copy of the root document is exactly the drift path §36 exists to
> close, and moving the original is a change no one has asked for yet.

## What SCR-F owes before it moves here

Three things, in order of consequence.

**1. Remove the technology dependence.** §2 states the readability requirement correctly and then
names a programming language in the next sentence. §17 and the §36.7 glossary go further and define
the Plugin *as* an artifact of that language; the naming has since spread through the document, and
into the title of the open decision covering the Plugin's contract surface. A Level 1 document that
names a language has made a Level 3 decision by accident and made it permanent by placing it too
high — and it puts an expiry date on a Corpus that is supposed to outlive its software. The
requirement that survives is the property, not the product. The argument is in `what-is-scr.md`;
the exact proposed change is recorded in `glossary.md`; the general rule is in `language-rules.md`.

**2. Render cleanly as Markdown.** The current file contains no code fences at all, so §35's
conceptual flow diagram and §37's documentation tree both render as a run of unrelated paragraphs.
It also carries 45 headings with escaped-number export artifacts (`## **13\. Cell**`). The root
document of a two-hundred-document tree has to render.

**3. Be adopted (§36.3).** Status is *in review*. Adoption is a human act, and until it happens
downstream documents may cite SCR-F but may not rely on it.

Once all three hold, the canonical file moves here and the copy at the repository's `documents/`
root is left as history rather than as a live second copy.

## Where the four documents in this directory stand

`what-is-scr.md`, `human-and-machine.md`, `language-rules.md`, and `glossary.md` are written to the
**corrected** form of the readability requirement — the property, with no language named. They
exist to set the direction the rest of the tree follows, so writing them to a form known to be
wrong would propagate the defect into everything downstream.

Foundations outranks them on conceptual meaning (§36.4). Until SCR-F revs, the two texts disagree in
the open, and `glossary.md` holds the record of the disagreement. That is the amendment procedure
working as designed (§36.5), not a downstream document choosing a side.

## What lives here permanently

The document itself. Its revision record, its Decision Registry index (§40, expanded into
`../04-decisions/`), and its canonical glossary (§36.7, hosted in `glossary.md`).
