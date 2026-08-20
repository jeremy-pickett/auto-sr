import { useEffect, useState } from 'react'
import { getCatalog } from '../api'

// The modifier catalog barely changes and is small (REQ-13.9's
// read-only table already fetches it whole) -- fetched once per page
// load and shared, rather than every chip that wants a blurb making
// its own request.
let cached = null

function fetchBlurbs() {
  if (!cached) {
    cached = getCatalog().then(
      (data) => Object.fromEntries(data.modifiers.map((m) => [m.name, m.blurb])),
      () => ({}),
    )
  }
  return cached
}

// Plain-English tooltip text for a modifier chip, keyed by name --
// null until the catalog has loaded, then a lookup (missing names,
// e.g. from an older catalog hash, just get no tooltip).
export function useModifierBlurbs() {
  const [blurbs, setBlurbs] = useState(null)
  useEffect(() => {
    let alive = true
    fetchBlurbs().then((b) => { if (alive) setBlurbs(b) })
    return () => { alive = false }
  }, [])
  return blurbs
}
