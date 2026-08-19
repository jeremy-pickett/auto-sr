import { decodeGrids } from './lib/decode'
import { getIdToken } from './lib/firebase'

async function asJson(response) {
  if (!response.ok) {
    const text = await response.text()
    throw new Error(`${response.status}: ${text}`)
  }
  return response.json()
}

// Every request goes through this — attaches Authorization when
// signed in, adds nothing when not. Anonymous requests stay byte-
// identical to what they were before auth existed: no header at all.
async function authorizedFetch(path, options = {}) {
  const token = await getIdToken()
  const headers = new Headers(options.headers || {})
  if (token) headers.set('Authorization', `Bearer ${token}`)
  return fetch(path, { ...options, headers })
}

export const listRules = (params = {}) => {
  const query = new URLSearchParams(
    Object.entries(params).filter(([, value]) => value !== undefined && value !== '')
  )
  return authorizedFetch(`/rules?${query}`).then(asJson)
}

export const getRule = (id) => authorizedFetch(`/rules/${id}`).then(asJson)

export const rerunRule = (id, seed) =>
  authorizedFetch(`/rules/${id}/runs`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(seed == null ? {} : { seed }),
  }).then(asJson)

export const getRun = (id) => authorizedFetch(`/runs/${id}`).then(asJson)

export async function getGrids(runId, from, to, props) {
  const response = await authorizedFetch(`/runs/${runId}/grids?from=${from}&to=${to}&props=${props.join(',')}`)
  if (!response.ok) throw new Error(`${response.status}: ${await response.text()}`)
  return decodeGrids(await response.arrayBuffer())
}

export const getCellHistory = (runId, y, x, props) =>
  authorizedFetch(`/runs/${runId}/cell/${y}/${x}?props=${props.join(',')}`).then(asJson)

export const patchRun = (id, corrections) =>
  authorizedFetch(`/runs/${id}`, {
    method: 'PATCH',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(corrections),
  }).then(asJson)

// The generation stream (REQ-11.4). The endpoint is a POST that
// responds text/event-stream, so this must be a streaming fetch() with
// a ReadableStream reader — EventSource cannot POST (REQ-11.4.1).
// A body is sent only to request private (visibility defaults to
// public either way) — keeps the ordinary request exactly the bare,
// bodyless POST it's always been.
export async function generateRule(onEvent, { visibility } = {}) {
  const response = await authorizedFetch('/rules/generate', {
    method: 'POST',
    ...(visibility === 'private'
      ? { headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ visibility }) }
      : {}),
  })
  if (!response.ok) throw new Error(`${response.status}: ${await response.text()}`)
  const reader = response.body.getReader()
  const decoder = new TextDecoder()
  let buffered = ''
  for (;;) {
    const { done, value } = await reader.read()
    if (done) break
    buffered += decoder.decode(value, { stream: true })
    let split
    while ((split = buffered.indexOf('\n\n')) >= 0) {
      const frame = buffered.slice(0, split)
      buffered = buffered.slice(split + 2)
      const name = frame.match(/^event: (.+)$/m)?.[1]
      const data = frame.match(/^data: (.+)$/m)?.[1]
      if (name) onEvent(name, data ? JSON.parse(data) : {})
    }
  }
}

export const getCatalog = () => authorizedFetch('/catalog/modifiers').then(asJson)

export const getSummary = () => authorizedFetch('/library/summary').then(asJson)
