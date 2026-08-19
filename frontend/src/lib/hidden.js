// Locally hidden rules — a personal decluttering filter for the
// library grid. Never sent to the backend, never touches recorded
// history (REQ-11.3 governs runs; this doesn't touch rules or runs
// at all). Persisted per browser in localStorage — fine for a
// single-user local app.
const KEY = 'asr.hiddenRuleIds'

function read() {
  try {
    const raw = localStorage.getItem(KEY)
    return new Set(raw ? JSON.parse(raw) : [])
  } catch {
    return new Set()
  }
}

function write(set) {
  localStorage.setItem(KEY, JSON.stringify([...set]))
}

export function getHiddenIds() {
  return read()
}

export function hideRule(id) {
  const set = read()
  set.add(id)
  write(set)
  return set
}

export function unhideRule(id) {
  const set = read()
  set.delete(id)
  write(set)
  return set
}
