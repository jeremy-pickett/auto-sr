// The observatory palette. Kind 0 reads as empty ground; kinds 1..7
// take the validated categorical slots — brightened again 2026-08-19
// (each now >= 7.5:1 contrast on #0a0e14; pairwise separation is
// down from the first brightening pass but still comfortably clear,
// min ~36 in a YCbCr distance check).

export const KIND_COLORS = [
  '#182130', // kind 0: empty ground
  '#95c2fa', // blue
  '#f49e7b', // orange
  '#38f0b0', // aqua
  '#ffbc3a', // yellow
  '#f2a4c0', // magenta
  '#00f300', // green
  '#e5e2fd', // violet
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
// The floor was 0.38 (settled cells at 38% brightness), which with the
// brightened palette read as dull once most of a run had aged past a
// few dozen ticks — the common case for anything that settles or
// loops. Raised 2026-08-19 so the floor is still visibly dimmer than
// a fresh cell but doesn't wash the picture out by default.
export function ageBrightness(age) {
  return 0.6 + 0.4 * Math.exp(-age / 30)
}

// Brightness when a 0..255 property (energy, memory) drives it instead.
export function levelBrightness(value) {
  return 0.5 + 0.5 * (value / 255)
}

export const SERIES = {
  variety: '#3987e5',
  cells_changed: '#d95926',
  kind_quiet_for: '#199e70',
}
