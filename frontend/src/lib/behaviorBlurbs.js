// Short, plain-English tooltip text for a behavior chip. RunView.jsx's
// behaviorNote() says the same things at greater length for the panel
// under the canvas; this is the one-line version for hovering over a
// small badge anywhere else it shows up (library cards, rule detail
// run rows, the run player's own header chip).
export const BEHAVIOR_BLURBS = {
  settles: 'Froze solid — every piece of state this rule tracks, visible and hidden, stopped changing.',
  repeats: 'Settled into a cycle that repeats exactly, over and over.',
  noisy: 'Kept changing the whole way through, with no freeze and no repeating cycle detected.',
  structured: 'Settled into an organized, non-trivial pattern — neither frozen nor dissolved into noise.',
  unclassified: "The classifier couldn't confidently place this one in a bucket.",
}
