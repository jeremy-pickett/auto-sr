import { useEffect, useMemo, useState } from 'react'
import { listRules, getSummary } from '../api'
import { RunThumbnail } from '../lib/RunThumbnail.jsx'
import { getHiddenIds, hideRule, unhideRule } from '../lib/hidden'

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

function RuleCard({ rule, hidden, onToggleHidden }) {
  const run = rule.canonical_run
  const open = () => {
    // A playable rule opens its canonical run; a broken one opens its
    // details — the failure is part of the library too.
    window.location.hash = run ? `#/runs/${run.id}` : `#/rules/${rule.id}`
  }
  const details = (event) => {
    event.stopPropagation()
    window.location.hash = `#/rules/${rule.id}`
  }
  const toggleHidden = (event) => {
    event.stopPropagation()
    onToggleHidden(rule.id)
  }
  return (
    <div
      className={`rule-card ${hidden ? 'rule-card-hidden' : ''}`}
      onClick={open}
      style={run ? undefined : { opacity: 0.8 }}
    >
      <div className="row" style={{ justifyContent: 'space-between' }}>
        <span className="id">
          rule #{rule.id}{' '}
          <button className="linkish" onClick={details}>details</button>{' '}
          <button className="linkish" onClick={toggleHidden}>
            {hidden ? 'unhide' : 'hide'}
          </button>
        </span>
        <span className={`chip status-${rule.status}`}>
          <span className="dot" />
          {rule.status}
          {rule.failed_check ? `: ${rule.failed_check}` : ''}
        </span>
      </div>
      <div className="card-body">
        {run ? (
          <RunThumbnail run={run} className="rule-thumb" />
        ) : (
          <div className="rule-thumb never-ran" title="never ran">×</div>
        )}
        <div className="description">{rule.description || '(no description survived)'}</div>
      </div>
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
  const [page, setPage] = useState(1)
  const [hiddenIds, setHiddenIds] = useState(() => getHiddenIds())
  const [showHidden, setShowHidden] = useState(false)

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
      page,
    }).then(setData, setError)
  }, [filters, page])

  const toggleHidden = (id) => {
    setHiddenIds(hiddenIds.has(id) ? unhideRule(id) : hideRule(id))
  }

  // Concept choices come from what the current page of rules mentions.
  const concepts = useMemo(() => {
    const seen = new Set(filters.concept ? [filters.concept] : [])
    for (const rule of data?.rules ?? []) rule.concepts.forEach((c) => seen.add(c))
    return [...seen].sort()
  }, [data, filters.concept])

  const visibleRules = useMemo(
    () => (data?.rules ?? []).filter((rule) => showHidden || !hiddenIds.has(rule.id)),
    [data, hiddenIds, showHidden]
  )

  const set = (key) => (event) => {
    setPage(1)
    setFilters((old) => ({
      ...old,
      [key]: key === 'flagged' ? event.target.checked : event.target.value,
    }))
  }

  const lastPage = data ? Math.max(1, Math.ceil(data.total / data.page_size)) : 1

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
        <button className="primary" onClick={() => { window.location.hash = '#/invent' }}>
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
        <label>
          <input
            type="checkbox"
            checked={showHidden}
            onChange={(event) => setShowHidden(event.target.checked)}
          />
          show hidden{hiddenIds.size ? ` (${hiddenIds.size})` : ''}
        </label>
      </div>

      {error && <div className="error-note">could not load the library: {String(error)}</div>}
      {!error && !data && <div className="loading">loading the library…</div>}
      {data && visibleRules.length === 0 && (
        <div className="loading">
          {data.rules.length === 0 ? 'nothing matches these filters' : 'everything on this page is hidden'}
        </div>
      )}
      {data && visibleRules.length > 0 && (
        <div className="rule-grid">
          {visibleRules.map((rule) => (
            <RuleCard
              key={rule.id}
              rule={rule}
              hidden={hiddenIds.has(rule.id)}
              onToggleHidden={toggleHidden}
            />
          ))}
        </div>
      )}

      {data && data.total > data.page_size && (
        <div className="pager">
          <button disabled={page <= 1} onClick={() => setPage((p) => p - 1)}>‹ prev</button>
          <span className="pager-status">
            page {page} of {lastPage} · {data.total} rules
          </span>
          <button disabled={page >= lastPage} onClick={() => setPage((p) => p + 1)}>next ›</button>
        </div>
      )}
    </>
  )
}
