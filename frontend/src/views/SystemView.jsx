import { useEffect, useState } from 'react'
import { getSystemStatus, getSystemSessions } from '../api'

const POLL_MS = 2000

// Which pipeline node a generation session's last-seen stage belongs to.
// validation_failed/repairing fold into Stage C -- a repair is still the
// harness working on the same implementation, not a new stage.
const STAGE_NODE = {
  stage_a_started: 0, stage_a_complete: 0,
  stage_b_started: 1, stage_b_complete: 1,
  validating: 2, validation_failed: 2, repairing: 2, running: 2,
}
const NODES = [
  { label: 'Stage A', sub: 'describe' },
  { label: 'Stage B', sub: 'implement' },
  { label: 'Stage C', sub: 'validate' },
  { label: 'Library', sub: 'stored' },
]

function formatBytes(n) {
  if (n == null) return '—'
  if (n < 1024 * 1024) return `${(n / 1024).toFixed(0)} KB`
  return `${(n / (1024 * 1024)).toFixed(1)} MB`
}

function formatUptime(seconds) {
  const h = Math.floor(seconds / 3600)
  const m = Math.floor((seconds % 3600) / 60)
  return h > 0 ? `${h}h ${m}m` : `${m}m`
}

function formatAgo(timestamp) {
  if (!timestamp) return '—'
  const s = Math.max(0, Math.round((Date.now() - new Date(timestamp)) / 1000))
  if (s < 60) return `${s}s ago`
  if (s < 3600) return `${Math.floor(s / 60)}m ago`
  return `${Math.floor(s / 3600)}h ago`
}

function outcomeLabel(session) {
  if (session.kind === 'http') return session.last_path ?? '—'
  if (!session.finished_at) return 'running'
  if (session.outcome === 'ok') return `stored as rule #${session.rule_id}`
  if (session.outcome === 'broken') return `rejected — ${session.error_text ?? 'failed validation'}`
  return 'generation failed'
}

// User-Agent strings are long; a short, still-identifiable prefix in the
// cell with the full string on hover beats either truncating badly or
// writing a whole UA parser for a debug table.
function shortUserAgent(ua) {
  if (!ua) return '—'
  return ua.length > 28 ? `${ua.slice(0, 28)}…` : ua
}

export default function SystemView() {
  const [status, setStatus] = useState(null)
  const [sessions, setSessions] = useState(null)
  const [page, setPage] = useState(1)
  const [error, setError] = useState(null)

  useEffect(() => {
    let cancelled = false
    const poll = () => {
      getSystemStatus().then((data) => { if (!cancelled) setStatus(data) }, setError)
      getSystemSessions({ page, page_size: 20 }).then((data) => { if (!cancelled) setSessions(data) }, setError)
    }
    poll()
    const interval = setInterval(poll, POLL_MS)
    return () => { cancelled = true; clearInterval(interval) }
  }, [page])

  if (error) return <div className="error-note">could not load the system page: {String(error)}</div>
  if (!status || !sessions) return <div className="loading">loading…</div>

  const inFlightByNode = new Map()
  for (const session of status.in_flight) {
    const node = STAGE_NODE[session.stage] ?? 2
    if (!inFlightByNode.has(node)) inFlightByNode.set(node, [])
    inFlightByNode.get(node).push(session)
  }
  const lastPage = Math.max(1, Math.ceil(sessions.total / sessions.page_size))

  return (
    <>
      <div className="library-head">
        <h1>System</h1>
        <span className="totals">
          {status.in_flight.length > 0
            ? `${status.in_flight.length} generation${status.in_flight.length === 1 ? '' : 's'} in flight`
            : 'idle'} · up {formatUptime(status.uptime_seconds)}
        </span>
      </div>

      <div className="panel">
        <h3>Pipeline</h3>
        <div className="pipeline-graph">
          {NODES.map((node, i) => (
            <div className="pipeline-stage" key={node.label}>
              <div className={`pipeline-node ${inFlightByNode.has(i) ? 'active' : ''}`} />
              <div className="pipeline-node-label">{node.label}</div>
              <div className="pipeline-node-sub">{node.sub}</div>
              {(inFlightByNode.get(i) ?? []).map((session) => (
                <div className="pipeline-node-gen mono" key={session.id}>{session.id}</div>
              ))}
              {i < NODES.length - 1 && <div className="pipeline-edge" />}
            </div>
          ))}
        </div>
      </div>

      <div className="hero-stats">
        <span><strong>{status.rules_total}</strong> rules</span>
        <span><strong>{status.runs_total}</strong> runs</span>
        <span><strong>{status.generations_last_hour}</strong> generations/hr</span>
        <span><strong>{status.errors_recent_24h}</strong> errors (24h)</span>
        <span><strong>{status.active_sessions}</strong> active now</span>
        <span><strong>{status.idle_sessions}</strong> idle</span>
        <span><strong>{formatBytes(status.db_size_bytes)}</strong> db size</span>
      </div>

      <div className="panel">
        <h3>Sessions</h3>
        <table className="catalog-table">
          <thead>
            <tr>
              <th>kind</th>
              <th>who</th>
              <th>ip</th>
              <th>user agent</th>
              <th>started</th>
              <th>last active</th>
              <th>requests</th>
              <th>last path</th>
            </tr>
          </thead>
          <tbody>
            {sessions.sessions.map((session) => (
              <tr key={`${session.kind}-${session.id}`}>
                <td>{session.kind}</td>
                <td>{session.signed_in ? 'user' : 'guest'}</td>
                <td className="mono">{session.ip_address ?? '—'}</td>
                <td className="mono" title={session.user_agent ?? ''}>{shortUserAgent(session.user_agent)}</td>
                <td className="mono">{new Date(session.started_at).toLocaleTimeString()}</td>
                <td className="mono">
                  {session.kind === 'gen' && !session.finished_at
                    ? 'running'
                    : formatAgo(session.kind === 'http' ? session.last_seen_at : session.finished_at)}
                </td>
                <td className="mono">{session.request_count ?? '—'}</td>
                <td className="blurb">{outcomeLabel(session)}</td>
              </tr>
            ))}
          </tbody>
        </table>
        {sessions.total > sessions.page_size && (
          <div className="pager">
            <button disabled={page <= 1} onClick={() => setPage((p) => p - 1)}>‹ prev</button>
            <span className="pager-status">page {page} of {lastPage} · {sessions.total} sessions</span>
            <button disabled={page >= lastPage} onClick={() => setPage((p) => p + 1)}>next ›</button>
          </div>
        )}
      </div>
    </>
  )
}
