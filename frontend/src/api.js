import { decodeGrids } from './lib/decode'

async function asJson(response) {
  if (!response.ok) {
    const text = await response.text()
    throw new Error(`${response.status}: ${text}`)
  }
  return response.json()
}

export const listRules = (params = {}) => {
  const query = new URLSearchParams(
    Object.entries(params).filter(([, value]) => value !== undefined && value !== '')
  )
  return fetch(`/rules?${query}`).then(asJson)
}

export const getRule = (id) => fetch(`/rules/${id}`).then(asJson)

export const rerunRule = (id, seed) =>
  fetch(`/rules/${id}/runs`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(seed == null ? {} : { seed }),
  }).then(asJson)

export const getRun = (id) => fetch(`/runs/${id}`).then(asJson)

export async function getGrids(runId, from, to, props) {
  const response = await fetch(`/runs/${runId}/grids?from=${from}&to=${to}&props=${props.join(',')}`)
  if (!response.ok) throw new Error(`${response.status}: ${await response.text()}`)
  return decodeGrids(await response.arrayBuffer())
}

export const getCellHistory = (runId, y, x, props) =>
  fetch(`/runs/${runId}/cell/${y}/${x}?props=${props.join(',')}`).then(asJson)

export const patchRun = (id, corrections) =>
  fetch(`/runs/${id}`, {
    method: 'PATCH',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(corrections),
  }).then(asJson)

// The generation stream (REQ-11.4). The endpoint is a POST that
// responds text/event-stream, so this must be a streaming fetch() with
// a ReadableStream reader — EventSource cannot POST (REQ-11.4.1).
export async function generateRule(onEvent) {
  const response = await fetch('/rules/generate', { method: 'POST' })
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

export const getCatalog = () => fetch('/catalog/modifiers').then(asJson)

export const getSummary = () => fetch('/library/summary').then(asJson)
