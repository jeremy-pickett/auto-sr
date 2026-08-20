// The rule's own generated text (description, reasoning) rendered as a
// single unbroken block reads as a wall of text no matter how good the
// writing is. This only changes presentation — same words, split into
// paragraphs on blank-line boundaries (falling back to one paragraph
// when there aren't any) and given real typographic rhythm via CSS.
// `quoted` marks the rule's own words specifically ("in its own words"),
// styled with a quote accent; reasoning and other prose stay plain.
export function Prose({ text, quoted = false }) {
  if (!text) return null
  const paragraphs = text.split(/\n\s*\n/).map((p) => p.trim()).filter(Boolean)
  return (
    <div className={`description prose ${quoted ? 'quoted' : ''}`}>
      {paragraphs.map((p, i) => <p key={i}>{p}</p>)}
    </div>
  )
}
