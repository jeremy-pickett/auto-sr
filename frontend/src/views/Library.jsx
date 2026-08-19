import { useEffect, useMemo, useRef, useState } from 'react'
import { listRules, getSummary, getGrids } from '../api'
import { plane } from '../lib/decode'
import { KIND_RGB } from '../lib/palette'

const BEHAVIORS = ['settles', 'repeats', 'noisy', 'structured', 'unclassified']

// Rendered final frames, kept for the session — a card's thumbnail is
// immutable history, so it never needs fetching twice.
const finalFrames = new Map()

// The rule's face: its canonical run's last tick, straight from the
// stored history in the player's own palette.
function LastTick({ run }) {
  const canvasRef = useRef(null)
  useEffect(() => {
    let alive = true
    const show = (frame) => {
      const canvas = canvasRef.current
      if (!canvas || !alive) return
      canvas.width = frame.width
      canvas.height = frame.height
      canvas.getContext('2d').drawImage(frame, 0, 0)
    }
    const cached = finalFrames.get(run.id)
    if (cached) {
      show(cached)
      return undefined
    }
    getGrids(run.id, run.ticks_run, run.ticks_run, ['kind']).then((decoded) => {
      const { width, height } = decoded
      const kinds = plane(decoded.properties.kind, 0, width, height)
      const frame = document.createElement('canvas')
      frame.width = width
      frame.height = height
      const ctx = frame.getContext('2d')
      const image = ctx.createImageData(width, height)
      for (let i = 0; i < kinds.length; i++) {
        const [r, g, b] = KIND_RGB[kinds[i] % KIND_RGB.length]
        image.data[i * 4] = r
        image.data[i * 4 + 1] = g
        image.data[i * 4 + 2] = b
        image.data[i * 4 + 3] = 255
      }
      ctx.putImageData(image, 0, 0)
      finalFrames.set(run.id, frame)
      show(frame)
    }, () => {})
    return () => { alive = false }
  }, [run.id, run.ticks_run])
  return <canvas ref={canvasRef} className="rule-thumb" title="how the canonical run ended" />
}

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
    // A playable rule opens its canonical run; a broken one opens its
    // details — the failure is part of the library too.
    window.location.hash = run ? `#/runs/${run.id}` : `#/rules/${rule.id}`
  }
  const details = (event) => {
    event.stopPropagation()
    window.location.hash = `#/rules/${rule.id}`
  }
  return (
    <div
      className="rule-card"
      onClick={open}
      style={run ? undefined : { opacity: 0.8 }}
    >
      <div className="row" style={{ justifyContent: 'space-between' }}>
        <span className="id">
          rule #{rule.id}{' '}
          <button className="linkish" onClick={details}>details</button>
        </span>
        <span className={`chip status-${rule.status}`}>
          <span className="dot" />
          {rule.status}
          {rule.failed_check ? `: ${rule.failed_check}` : ''}
        </span>
      </div>
      <div className="card-body">
        {run ? (
          <LastTick run={run} />
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
