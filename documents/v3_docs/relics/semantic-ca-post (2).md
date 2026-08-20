I will always be a computer scientist and infosec guy. Couldn't sleep last night, ended up listening to an interview with Stephen Wolfram about cellular automata — grids of cells that do things through pure computation.

A chessboard has 64 squares and a handful of rules, but there's no shortcut to knowing how a game turns out — you have to play it. That's Wolfram's point about computation: for a lot of simple rule systems, running them is the only way to find out what they do.

Cellular automata push that to an extreme: a few cell states, a few sentences of rule, run over a grid thousands of times — and sometimes structure erupts that nobody put there on purpose.

My variant, semantic cellular automata, takes a language-first approach: the rule starts as a plain-English description, then becomes running code, and nobody knows in advance if it'll be boring, stable, or break interesting.

Live on a bare droplet, zero guardrails: http://159.89.80.215:5173/#/ — expect it to fall over 🫠🤣🙃

---

## Longer version (for technical audiences)

A chessboard has 64 squares and a handful of rules, but there's no shortcut to knowing how a game turns out — you have to play it. Wolfram's point about computation is the general case of that: for a lot of simple rule systems there's no closed-form answer for what they'll do. Running the rule is the only way to find out, no matter how much compute you throw at predicting it instead.

Cellular automata are the cleanest demonstration. A few cell states, a few sentences of rule, iterated over a grid — and sometimes what comes out is structure nobody designed in. Rule 30 is the canonical example: trivial to state, complex enough to use as a random number generator.

My variant, semantic cellular automata, pushes rule-authorship onto a language-first pipeline instead of a human. Stage one reads a coverage map of what's already in the library — not scores, not flags, just what's been tried — and proposes a new rule in plain English, aimed at an unexplored corner. Stage two turns that description into running code. Neither stage knows in advance whether the result will be interesting.

Every proposed rule goes through validation (structural checks, does it load, does it run deterministically from a fixed seed) and gets run to completion by a harness — same seed, same result, every time. The harness decides when a world has actually frozen or fallen into a loop; a static-looking frame isn't enough on its own to stop a run.

The library keeps everything: gray soup, instant death, stable structure, and the rare thing that breaks in a way worth keeping. 50 rules invented so far, 48 ran clean and got shelved, 2 broke and stayed. Failures aren't discarded — they feed the next invention pass, so the corpus is closer to a telescope log than a highlight reel. The interesting question was never "is this one pretty," it's "nobody's run this rule before, what does it do."

To be direct about scope: this is inspired by Wolfram's work on cellular automata, not a reproduction of it, not affiliated with or endorsed by Wolfram Research, and makes no claim to covering any meaningful fraction of rule space. It's a small, deliberately unguarded experiment in letting a language-first system author and run rules it can't fully predict the outcome of.

Live (and fragile) here: http://159.89.80.215:5173/#/ 🫠🤣🙃
