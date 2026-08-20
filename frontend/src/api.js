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

export const getRuleBySlug = (slug) => authorizedFetch(`/rules/by-slug/${slug}`).then(asJson)

export const setRuleTitle = (id, title) =>
  authorizedFetch(`/rules/${id}`, {
    method: 'PATCH',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ title }),
  }).then(asJson)

export const addFavorite = (id) => authorizedFetch(`/rules/${id}/favorite`, { method: 'POST' }).then(asJson)
export const removeFavorite = (id) => authorizedFetch(`/rules/${id}/favorite`, { method: 'DELETE' }).then(asJson)

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
// A body is sent only when there's something to say (private, or a
// spark) — keeps the ordinary request exactly the bare, bodyless POST
// it's always been.
export async function generateRule(onEvent, { visibility, spark, title } = {}) {
  const body = {}
  if (visibility === 'private') body.visibility = visibility
  if (spark) body.spark = spark
  if (title) body.title = title
  const response = await authorizedFetch('/rules/generate', {
    method: 'POST',
    ...(Object.keys(body).length
      ? { headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(body) }
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

// The lazy-loaded "enormous thing": every tick of a run, uncapped,
// as plain JSON — not the packed binary framing used for playback.
// Returns a Blob rather than parsing it, since a full run can be tens
// of MB and the browser has no reason to hold it as a JS object; the
// caller just hands it off as a download.
export async function exportRun(runId, props) {
  const response = await authorizedFetch(`/runs/${runId}/export?props=${props.join(',')}`)
  if (!response.ok) throw new Error(`${response.status}: ${await response.text()}`)
  return response.blob()
}

export const getComments = (ruleId) => authorizedFetch(`/rules/${ruleId}/comments`).then(asJson)

export const createComment = (ruleId, body) =>
  authorizedFetch(`/rules/${ruleId}/comments`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ body }),
  }).then(asJson)

export const editComment = (id, body) =>
  authorizedFetch(`/comments/${id}`, {
    method: 'PATCH',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ body }),
  }).then(asJson)

export const deleteComment = (id) => authorizedFetch(`/comments/${id}`, { method: 'DELETE' }).then(asJson)

export const getCatalog = () => authorizedFetch('/catalog/modifiers').then(asJson)

export const getSummary = () => authorizedFetch('/library/summary').then(asJson)

export const getProfile = () => authorizedFetch('/profile').then(asJson)

export const setDisplayName = (displayName) =>
  authorizedFetch('/profile', {
    method: 'PUT',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ display_name: displayName }),
  }).then(asJson)
