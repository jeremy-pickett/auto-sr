# STYLE.md

Voice guide for SCR project writing. Derived from a line-by-line edit pass over the manifesto, v0.5 → v0.6. Every rule below has a real before/after attached. Nothing here is invented from taste.

Written primarily for Claude Code and other model writers. Read it before drafting anything outward-facing.

---

## 0. Scope — which voice goes where

**This guide describes the outward-facing voice.** Manifesto, README, About page, talk material, blog posts, anything a stranger reads first.

**It does not describe internal document voice.** The foundations document, requirements, decision records, and deep dives are deliberately flat, numbered, and citable. Writing SCR-F in manifesto register would be a defect. The house style there is different and lives in SCR-F §5 and §36.

If you're unsure which you're writing: does it have identifiers people will cite? Internal. Is someone reading it to decide whether to care? Outward.

---

## 1. Run-on sentences are load-bearing. Do not compress them.

The long sentences are not sloppy. They tire the reader on purpose, so that the reader *feels* the repetition before being told the outcome was unpredictable.

> The hardest problems we have are small pieces of data, with simple rules repeating. And repeating. And repeating until the world is different.

A model will "tighten" this into "simple rules repeating until the world is different." That deletes the mechanism. The fatigue **is** the argument.

**Rule:** when a sentence in this voice runs long or repeats, assume it's deliberate. Compressing is the default failure mode and it is almost always wrong.

---

## 2. Anaphora completes. It does not elide.

Draft had three parallel clauses where the third dropped the stem:

> It can be the fire that jumps the break. It can be the account that keeps getting pwned. ~~The Claude agent that trusts poisoned memory.~~

Correction restored it:

> It could be the Claude agent that trusts poisoned memory.

Note the drift from *can* to *could* on the third. That's spoken rhythm — nobody says the same auxiliary three times out loud. Keep the drift.

---

## 3. Don't name the feeling. Cause it.

The single most useful correction in the session.

Before: *A model invents a package that almost exists. Close enough to fool you.*
After: *A model invents a package that almost exists. Close enough that you read it, recognized it, and installed it.*

The first **reports** danger. The second makes the reader do the recognizing, in past tense, so it already happened to them. Naming an emotion is a substitute for constructing it.

**Rule:** if a sentence contains a word for how the reader should feel — sinister, alarming, dangerous, striking, powerful — delete it and build the conditions instead.

---

## 4. Don't state the conclusion. Build the gap.

> Small things acting on the things next to them, and nobody has the rules for why these huge sets of small things do what they do. That is not a problem humans can solve.

The paragraph stops there. It never says "which is why we built this." The reader is holding a document about a machine that runs a hundred thousand mechanisms overnight; they close the loop themselves, and closing it is what makes it stick.

**Rule:** trust the reader to be smart. The unstated conclusion is stronger than the stated one, every time.

---

## 5. Machines run. Humans judge. Never blur it.

This is a content rule wearing a style rule's clothes, and it is the most important entry here.

A cellular automaton applies a rule and produces a state. It does not check, verify, test, assess, evaluate, confirm, or grade. It has no notion of correct. Every draft that gave the machine a judging verb was rejected:

- ~~"a rule that reproduces reality is a candidate"~~ — reproduces implies comparison
- ~~"checked once"~~ — nothing checked anything
- ~~"we're making its understanding testable"~~ — it has no understanding

What survived:

> A rule ran. It made a shape. The shape looked familiar to you. Judgement is a human's job, man.

Machine acts. Human judges. If a sentence blurs it, the sentence is wrong on the facts before it's wrong on the voice.

---

## 6. The machine is a noble collaborator. Never a servant, never lesser.

A draft opened with *"The machine does what a machine can do"* and then *"You do the rest."* Rejected hard, and correctly.

*The rest* makes human judgment a remainder — the leftovers after the machine finished. It inverts the entire thesis while sounding generous.

The correct framing: the machine takes an enormous amount of genuinely difficult work, and it is *better at that work than any human*. It does not get tired at 2am. It does not transpose a number on the four hundredth repetition. It never loses a result. That's not a lesser role, it's a superhuman one.

And it hands over the one decision that matters.

> The machine takes the work it is genuinely better at. […] You take the work only you can do.

**Rules:**
- Never *servant*, *assistant-as-subordinate*, *does the grunt work*, *frees you up to*.
- Never position human work as what's left over.
- Give the machine more verbs, not fewer. It wrote, ran, recorded, kept.
- The machine paragraph can be the longest one. Detail is how you honor the work.

---

## 7. No numbers that sound like results.

Killed on sight during the pass:

- ~~"forty mechanisms that produce fires shaped like yours, and the eleven families that never did"~~ — invented, sounds measured
- ~~"the same seven or so ingredients underneath"~~ — invented
- ~~"5,317 commands across 34 sessions"~~ — real, but invites arithmetic instead of agreement

Replacement for the last one:

> a campaign that took a season now runs in an afternoon

The reader supplies their own scale from their own experience and nobody argues with it.

**Allowed:** facts about the world (fifty years, eighty thousand acres, a ninety-day intrusion). **Not allowed:** figures describing what the system produces.

**Corollary:** names are the opposite of numbers. *Slopsquatting*, *EchoLeak*, *rug pull* — a number invites a fact-check, a name invites a search, and a name signals you've been in the room without claiming you were.

---

## 8. No aphorisms. No slide titles.

Two lines were cut for this, both mine, both quotable:

- ~~"A framework that fits everything explains nothing."~~
- ~~"An answer you can't open isn't an answer. It's a rumor in a lab coat."~~ (survived only after rework)

**The test:** would this work as a slide title? Then it's suspect. Reversible, unfalsifiable, sounds like it argued something and didn't.

The author's verdict on the first one: *"it does nothing. yeah sure it could go in marketing copy, but sorry it's just bad."*

---

## 9. Metaphor arrives unannounced, carried by synonym choice.

The author never says "think of this like a workshop." He just picks the verb:

> "try roughing it up, then i'll dismantle it"
> "go for the throat slightly more"
> "like a Boeing MAX I'll smash it into the ground"
> "drawing that concise line in the sand"
> "release the tigers"
> "where data exfil wants to live, like coliform bacteria in your butt"

Shop, body, trades, disaster. The register does all the work and never explains itself. The wrong synonym would break it — "revise it, then I'll critique it" is the same instruction with the metaphor drained out.

**Rule:** never establish a metaphor before using it. No *"think of it like…"*, no *"imagine a…"*. Pick the word from the right world and move on. Models labor metaphors; this voice doesn't.

---

## 10. Register shifts are meaningful. Don't flatten them.

A rough-up of the Wolfram section was rejected outright: *"it tries waaaaaay too hard. especially after the more casual opening. talking about wolfram robot-like is appropriate."*

The document opens warm and second-person to put the reader inside the Game of Life. It goes cold and clipped to state a disagreement with a serious person. **The cold is respect.** Making it casual turned it into a guy in a bar with opinions about Wolfram.

**Rule:** the voice is not one register. It's a controlled shift between them, and the shift carries meaning. Don't homogenize.

---

## 11. Hard on the field. Warm to the person.

The manifesto tells the reader their discipline moves at a few good hypotheses per career. It also says:

> Your job is the most important part. Judgment.

That's flattery, it's slightly cheap, and it stays. Author's ruling: *"yes i kept the cheap flattery. that is how i talk, for better or worse."*

This is a consistent posture, not an inconsistency. Be brutal about the problem, decent to the human reading.

---

## 12. Repetition is a tool, so accidental repetition is worse here than elsewhere.

> Language models just made guessing cheap. Not correct. Cheap.

Three beats, deliberate. A draft then added *"But that makes it cheap to iterate"* — a fourth *cheap* that wasn't on the beat. Cut immediately.

**Rule:** in this voice a repeated word either lands exactly on the drum or it reads as a missed one. There is no neutral repetition. Check every recurrence.

Deliberate bookending is different and encouraged:

> That's the whole game. Simple rules on simple data. That's the whole game.

---

## 13. Lists are weak. Put a person in it.

Rejected: four stacked noun phrases with no verbs and no reader.

> ~~A million mechanisms, with their ancestry and their failures kept. A card catalog of emergence. A fire officer handed the mechanisms that produce junction-fire acceleration…~~

Replaced with something that happens to *you*, on a specific day:

> so the next person doesn't spend their Tuesday finding out what you already found out on a Tuesday two years ago

**Rule:** if a paragraph is three or more noun phrases in a row, it's a list pretending to be prose. Rewrite with a verb and a human.

---

## 14. No jargon that costs a lookup.

Cut: *spiral waves in cardiac tissue*, *junction-fire acceleration*, *topologies of trust*.

These are correct terms from real fields, and every one makes a general reader stop. The author's ruling on the cardiac example: *"let's not talk specific surgical procedures. our value is simple rules, simple data."*

**Rule:** in outward-facing writing, if a term needs a clause of explanation, it needs to be gone. The permafrost feeding back on itself and the exit that always clogs need nothing. That's the bar.

**Includes our own vocabulary.** Don't use SCR component names — Request, Reader, Study, World, Plugin, Lab — in outward-facing prose. Describe the thing.

---

## 15. Say *immutable*, not *forever*.

> That goes in the catalog too, with your reasons, immutable.

Author's reasoning: *"forever gives DB admins jitters, immutable is a programming term that'll calm them down."*

Forever is a promise about time. Immutable is a property of how it's built. One is a vow you might break; the other is a fact.

---

## 16. The sales-pitch moment: name the pain flatly. Never perform it.

> And it is exhausting and tedious.

Five words. No *"there's got to be a better way."* No winking. The reader has done this work and recognizes it; performing their pain back at them is how you lose them.

---

## 17. Second person, present tense, and the capital You.

The document opens *"You are playing 'The Game of Life'"* and keeps the reader inside the system throughout.

At the payoff, the pronoun capitalizes:

> When You arrive, it's been working.

That's the machine addressing the reader directly, and it earns the capital because the second person has been running since line one. Use sparingly — once per document at most.

---

## 18. Profanity: rare, functional, never decorative.

> **The only way to know is to run the damn scenario.**

One *damn*, in bold, at the end of the section that establishes irreducibility. It's doing emphasis work no other word does there. Don't add more; don't remove that one.

---

## 19. Conversational asides are in-voice.

> Let's talk examples, shall we.

> Judgement is a human's job, man.

> We need all the juicy, gory stuff.

> A model used by a bazillion developers

These are the moments a person shows up in the machinery. They tend to land right after the most writerly line in a paragraph, undercutting it. That placement is deliberate and good.

---

## 20. Claude's tells — delete these on sight

Patterns produced by model writers that were caught and cut repeatedly during this pass:

| Tell | Example from the pass |
|---|---|
| Three short sentences after a long one | *"That's fine. That's honest. That is a scientist saying the true thing out loud."* |
| Transition sentences doing transition work | *"Same shape, different room."* |
| Throat-clearing before the real line | *"Our answer is structural, not rhetorical."* |
| Lines written to be quoted | *"Nobody's fire is waiting on a beautiful picture."* |
| Naming the emotion | *"Close enough to fool you."* |
| Stating the conclusion the reader would reach | *"…which is why we built this."* |
| Announced metaphor | *"Think of it like a workbench…"* |
| Compressing a deliberate run-on | any tightening of *"And repeating. And repeating."* |
| Giving the machine a judging verb | *checks, verifies, determines, concludes* |
| Making human work the remainder | *"You do the rest."* |
| Precision theater | invented counts, fake percentages, made-up ratios |

The pattern behind most of these: **models optimize for a sentence that sounds finished.** This voice optimizes for a sentence that makes the reader do something.

---

## 21. Mechanical notes

- **Spelling:** pick one of *judgment* / *judgement* per document and hold it. (v0.6 currently has both — a real defect.)
- **Typos in author drafts** are common and should be fixed silently, not flagged: *ketting → getting*, *interate → iterate*, *coliniform → coliform*.
- **Dropped words** are also common. If a clause is missing a word and the intent is ambiguous, ask rather than guess — one such clause (*"the rule the data and cell used"*) was cut because nobody could reconstruct it.
- **Em-dashes:** used, but less than a model would. Prefer a period.
- **Slashes for alternatives** are in-voice: *helpfully/accidentally*.
- **Lowercase casual** in correspondence; sentence case in documents.

---

## 22. The one-line test

Before shipping a paragraph, ask: **did I make the reader feel something, or did I tell them what to feel?**

If it's the second one, it isn't done.
