// The observatory palette. Kind 0 reads as empty ground; kinds 1..7 are a
// bioluminescent/instrument-glow set — replaced 2026-08-20 (was a generic
// vivid categorical set with one jarring pure-saturation green) to match the
// "automaton is the light source" identity index.css already declares. Every
// kind clears >= 7.5:1 contrast on #0a0e14 (range 7.5-13.2:1), minimum
// pairwise YCbCr separation is 48.1 (up from the prior palette's ~36 floor).

export const KIND_COLORS = [
  '#0a0e14', // kind 0: empty ground (matches --ground exactly)
  '#38c8f0', // cyan glow (near the chrome accent, --cyan: #4cc9f0)
  '#ff7a59', // coral ember
  '#3ff0b0', // teal-aqua
  '#ffc247', // amber gold
  '#d97bff', // magenta-violet
  '#96a0ff', // periwinkle
  '#ff8fc4', // rose-pink
]

const rgb = (hex) => [
  parseInt(hex.slice(1, 3), 16),
  parseInt(hex.slice(3, 5), 16),
  parseInt(hex.slice(5, 7), 16),
]

export const KIND_RGB = KIND_COLORS.map(rgb)

// Some kinds are now bright enough that fixed white label text (the
// neighbor inspector's cell labels) would wash out against them —
// pick black or white per swatch by WCAG relative luminance instead.
function relativeLuminance([r, g, b]) {
  const lin = (c) => {
    c /= 255
    return c <= 0.03928 ? c / 12.92 : ((c + 0.055) / 1.055) ** 2.4
  }
  return 0.2126 * lin(r) + 0.7152 * lin(g) + 0.0722 * lin(b)
}
export function textOn(hex) {
  const idx = KIND_COLORS.indexOf(hex)
  const luminance = relativeLuminance(idx >= 0 ? KIND_RGB[idx] : rgb(hex))
  return luminance > 0.42 ? '#0a0e14' : '#f5f8fc'
}

// Default display mapping (REQ-13.2): kind drives color, age drives
// brightness — young cells glow, settled cells cool toward the ground.
// First floor (0.38) read as dull; the follow-up floor (0.6) still did,
// because most of a settled run's picture sits at the floor almost the
// whole time, and 60% of a saturated color next to the un-scaled 100%
// library thumbnail reads as a real gap side by side, not a subtle one.
// Raised again 2026-08-19 to close that gap to something barely
// perceptible rather than merely smaller — the glow-on-birth shape is
// unchanged, it's just a much narrower swing now (88-100% instead of
// 60-100%).
export function ageBrightness(age) {
  return 0.88 + 0.12 * Math.exp(-age / 30)
}

// Brightness when a 0..255 property (energy, memory) drives it instead.
export function levelBrightness(value) {
  return 0.72 + 0.28 * (value / 255)
}

export const SERIES = {
  variety: '#96a0ff',
  cells_changed: '#ff7a59',
  kind_quiet_for: '#3ff0b0',
}
