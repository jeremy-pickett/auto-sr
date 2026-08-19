import { useEffect, useMemo, useState } from 'react'
import { listRules, getSummary } from '../api'

const BEHAVIORS = ['settles', 'repeats', 'noisy', 'structured', 'unclassified']

function BehaviorChip({ run }) {
  if (!run || !run.guessed_behavior) return null
  const shown = run.user_behavior || run.guessed_behavior
  const low = run.guess_confidence === 'low' && !run.user_behavior
  return (
    <span className={`chip behavior-${shown} ${low ? 'confidence-low' : ''}`}>
      <span className="dot" />
      {shown}
      {run.user_behavior ? ' (yours)' : low ? ' (low confidence)' : ''}
    </span>
  )
}

function RuleCard({ rule }) {
  const run = rule.canonical_run
  const open = () => {
    if (run) window.location.hash = `#/runs/${run.id}`
  }
  return (
    <div
      className="rule-card"
      onClick={open}
      style={run ? undefined : { cursor: 'default', opacity: 0.75 }}
    >
      <div className="row" style={{ justifyContent: 'space-between' }}>
        <span className="id">rule #{rule.id}</span>
        <span className={`chip status-${rule.status}`}>
          <span className="dot" />
          {rule.status}
          {rule.failed_check ? `: ${rule.failed_check}` : ''}
        </span>
      </div>
      <div className="description">{rule.description || '(no description survived)'}</div>
      <div className="meta">
        <BehaviorChip run={run} />
        {run && <span className="chip">{run.stopped_because}</span>}
        {run && run.user_flagged && <span className="chip flag">⚑ flagged</span>}
        <span className="chip">
          {rule.kinds} kinds · {rule.neighbors} neighbors · reach {rule.reach}
        </span>
        {rule.modifiers.map((m) => (
          <span key={m} className="chip">{m}</span>
        ))}
        {rule.concepts.map((c) => (
          <span key={c} className="chip">{c}</span>
        ))}
      </div>
    </div>
  )
}

export default function Library() {
  const [data, setData] = useState(null)
  const [summary, setSummary] = useState(null)
  const [error, setError] = useState(null)
  const [filters, setFilters] = useState({ status: '', behavior: '', concept: '', flagged: false })

  useEffect(() => {
    getSummary().then(setSummary, () => {})
  }, [])

  useEffect(() => {
    setData(null)
    listRules({
      status: filters.status,
      behavior: filters.behavior,
      concept: filters.concept,
      flagged: filters.flagged || undefined,
    }).then(setData, setError)
  }, [filters])

  // Concept choices come from what the current page of rules mentions.
  const concepts = useMemo(() => {
    const seen = new Set(filters.concept ? [filters.concept] : [])
    for (const rule of data?.rules ?? []) rule.concepts.forEach((c) => seen.add(c))
    return [...seen].sort()
  }, [data, filters.concept])

  const set = (key) => (event) =>
    setFilters((old) => ({
      ...old,
      [key]: key === 'flagged' ? event.target.checked : event.target.value,
    }))

  return (
    <>
      <div className="library-head">
        <h1>The library</h1>
        {summary && (
          <span className="totals">
            {summary.totals.rules} rules · {summary.totals.broken} broken ·{' '}
            {Object.entries(summary.totals.behaviors)
              .map(([name, count]) => `${count} ${name}`)
              .join(' · ') || 'no classified runs yet'}
          </span>
        )}
        <span style={{ flex: 1 }} />
        <button className="primary" disabled title="arrives with the generation phase">
          ✦ Invent a rule
        </button>
      </div>

      <div className="filters">
        <label>
          status
          <select value={filters.status} onChange={set('status')}>
            <option value="">any</option>
            <option value="ok">ok</option>
            <option value="broken">broken</option>
          </select>
        </label>
        <label>
          behavior
          <select value={filters.behavior} onChange={set('behavior')}>
            <option value="">any</option>
            {BEHAVIORS.map((b) => (
              <option key={b} value={b}>{b}</option>
            ))}
          </select>
        </label>
        <label>
          concept
          <select value={filters.concept} onChange={set('concept')}>
            <option value="">any</option>
            {concepts.map((c) => (
              <option key={c} value={c}>{c}</option>
            ))}
          </select>
        </label>
        <label>
          <input type="checkbox" checked={filters.flagged} onChange={set('flagged')} />
          flagged only
        </label>
      </div>

      {error && <div className="error-note">could not load the library: {String(error)}</div>}
      {!error && !data && <div className="loading">loading the library…</div>}
      {data && data.rules.length === 0 && (
        <div className="loading">nothing matches these filters</div>
      )}
      {data && (
        <div className="rule-grid">
          {data.rules.map((rule) => (
            <RuleCard key={rule.id} rule={rule} />
          ))}
        </div>
      )}
    </>
  )
}
