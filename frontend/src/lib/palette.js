// The observatory palette. Kind 0 reads as empty ground; kinds 1..7
// take the validated categorical slots — brightened 2026-08-19 for
// visibility against the dark ground (each now >= 7:1 contrast on
// #0a0e14, pairwise separation held constant vs. the prior palette).

export const KIND_COLORS = [
  '#182130', // kind 0: empty ground
  '#69a7f3', // blue
  '#ea7e52', // orange
  '#18dd98', // aqua
  '#ffab07', // yellow
  '#e77ca3', // magenta
  '#00c000', // green
  '#bdb6f6', // violet
]

const rgb = (hex) => [
  parseInt(hex.slice(1, 3), 16),
  parseInt(hex.slice(3, 5), 16),
  parseInt(hex.slice(5, 7), 16),
]

export const KIND_RGB = KIND_COLORS.map(rgb)

// Default display mapping (REQ-13.2): kind drives color, age drives
// brightness — young cells glow, settled cells cool toward the ground.
export function ageBrightness(age) {
  return 0.38 + 0.62 * Math.exp(-age / 30)
}

// Brightness when a 0..255 property (energy, memory) drives it instead.
export function levelBrightness(value) {
  return 0.3 + 0.7 * (value / 255)
}

export const SERIES = {
  variety: '#3987e5',
  cells_changed: '#d95926',
  kind_quiet_for: '#199e70',
}
