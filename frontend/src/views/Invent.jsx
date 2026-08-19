import { useRef, useState } from 'react'
import { generateRule } from '../api'
import { RunThumbnail } from '../lib/RunThumbnail.jsx'
import { useAuth } from '../lib/firebase'

// The pipeline stages as the stream reports them (REQ-13.7): the user
// watches the machine think, including failures and the one repair.
const STAGES = [
  { key: 'stage_a', label: 'inventing', detail: 'Stage A proposes a rule in plain English' },
  { key: 'stage_b', label: 'implementing', detail: 'Stage B writes the Python' },
  { key: 'validating', label: 'validating', detail: 'structure · static checks · declaration · load · trial · reproducibility' },
  { key: 'running', label: 'running', detail: 'the canonical run, executed to completion' },
]

function stageStates(events) {
  // Fold the event log into a per-stage status: idle | active | done | failed.
  const state = Object.fromEntries(STAGES.map((s) => [s.key, 'idle']))
  let repaired = false
  for (const [name] of events) {
    if (name === 'stage_a_started') state.stage_a = 'active'
    if (name === 'stage_a_complete') state.stage_a = 'done'
    if (name === 'stage_b_started') state.stage_b = 'active'
    if (name === 'stage_b_complete') state.stage_b = 'done'
    if (name === 'validating') state.validating = 'active'
    if (name === 'validation_failed') state.validating = 'failed'
    if (name === 'repairing') { repaired = true; state.stage_b = 'active' }
    if (name === 'running') { state.validating = 'done'; state.running = 'active' }
    if (name === 'complete') {
      if (state.running === 'active') state.running = 'done'
    }
  }
  return { state, repaired }
}

export default function Invent() {
  const { user } = useAuth()
  const [events, setEvents] = useState([])
  const [working, setWorking] = useState(false)
  const [failure, setFailure] = useState(null)
  const [visibility, setVisibility] = useState('public')
  const [spark, setSpark] = useState('')
  const [title, setTitle] = useState('')
  const startedRef = useRef(false)

  const start = async () => {
    if (startedRef.current) return
    startedRef.current = true
    setWorking(true)
    setEvents([])
    setFailure(null)
    try {
      await generateRule(
        (name, data) => setEvents((log) => [...log, [name, data]]),
        { visibility, spark: spark.trim(), title: title.trim() }
      )
    } catch (error) {
      setFailure(String(error))
    } finally {
      setWorking(false)
      startedRef.current = false
    }
  }

  const { state, repaired } = stageStates(events)
  const byName = Object.fromEntries(events)
  const proposal = byName.stage_a_complete
  const progress = byName.tick_progress
  const complete = byName.complete
  const failures = events.filter(([name]) => name === 'validation_failed')

  return (
    <div className="invent">
      <div className="invent-head">
        <h1>Invent a rule</h1>
        <p className="sub">
          The machine reads the coverage map — never your flags, never your
          reruns — proposes one rule, implements it, and every outcome lands
          in the library. Failure is data too.
        </p>
        <div className="row" style={{ gap: 16, marginBottom: 12, flexWrap: 'wrap' }}>
          <label className="row" style={{ color: 'var(--muted)', fontSize: 12, gap: 6 }}>
            name
            <input
              type="text"
              value={title}
              onChange={(e) => setTitle(e.target.value)}
              disabled={working}
              maxLength={120}
              placeholder="give it a name — optional, you can add one later too"
              style={{ width: 260 }}
            />
          </label>
        </div>
        {user && (
          <div className="row" style={{ gap: 16, marginBottom: 12, flexWrap: 'wrap' }}>
            <label className="row" style={{ color: 'var(--muted)', fontSize: 12, gap: 6 }}>
              visibility
              <select value={visibility} onChange={(e) => setVisibility(e.target.value)} disabled={working}>
                <option value="public">public — joins the global library</option>
                <option value="private">private — only in your library</option>
              </select>
            </label>
            <label className="row" style={{ color: 'var(--muted)', fontSize: 12, gap: 6 }}>
              spark
              <input
                type="text"
                value={spark}
                onChange={(e) => setSpark(e.target.value)}
                disabled={working}
                maxLength={64}
                placeholder="a hint for what it invents — optional, 64 characters"
                style={{ width: 260 }}
              />
            </label>
          </div>
        )}
        <button className="primary" onClick={start} disabled={working}>
          {working ? 'thinking…' : events.length ? '✦ Invent another' : '✦ Invent a rule'}
        </button>
      </div>

      {(working || events.length > 0) && (
        <ol className="pipeline">
          {STAGES.map((stage) => (
            <li key={stage.key} className={`stage-${state[stage.key]}`}>
              <span className="lamp" />
              <div>
                <div className="stage-label">
                  {stage.label}
                  {stage.key === 'stage_b' && repaired ? ' (repair attempt)' : ''}
                </div>
                <div className="stage-detail">
                  {stage.key === 'running' && progress
                    ? `tick ${progress.tick} / ${progress.max_ticks}`
                    : stage.detail}
                </div>
              </div>
            </li>
          ))}
        </ol>
      )}

      {proposal && (
        <div className="panel proposal">
          <h3>the proposal</h3>
          <div className="description">{proposal.description}</div>
          <div className="meta row" style={{ marginTop: 10 }}>
            <span className="chip">{proposal.kinds} kinds</span>
            <span className="chip">{proposal.neighbors}</span>
            <span className="chip">reach {proposal.reach}</span>
            <span className="chip">shape {proposal.shape}</span>
            {proposal.modifiers.map((m) => <span key={m} className="chip">{m}</span>)}
            {proposal.concepts.map((c) => <span key={c} className="chip">{c}</span>)}
          </div>
        </div>
      )}

      {failures.map(([, data], index) => (
        <div key={index} className="error-note">
          {index === 0 ? 'validation failed' : 'the repair also failed'} — {data.check}: {data.error}
        </div>
      ))}

      {repaired && working && !complete && failures.length === 1 && (
        <div className="repair-status">
          <span className="repair-spinner" />
          attempting the one permitted repair…
        </div>
      )}

      {failure && <div className="error-note">the stream broke: {failure}</div>}

      {complete && complete.status === 'ok' && (
        <div className="panel done-note">
          <h3>{title.trim() ? title.trim() : 'it works'}</h3>
          <div className="done-result">
            <RunThumbnail
              run={{ id: complete.run_id, ticks_run: complete.ticks_run }}
              className="rule-thumb-lg"
            />
            <div>
              {repaired && <p className="repair-outcome ok">✓ needed one repair attempt — the fix held.</p>}
              <p>
                Ran {complete.ticks_run} ticks and stopped: {complete.stopped_because}.
                Guessed behavior: <strong>{complete.behavior}</strong> ({complete.confidence}{' '}
                confidence).
              </p>
              <p>
                <a className="chip" href={`#/runs/${complete.run_id}`}>▶ watch the run</a>{' '}
                <a className="chip" href={`#/rules/${complete.rule_id}`}>rule #{complete.rule_id} details</a>
              </p>
            </div>
          </div>
        </div>
      )}
      {complete && complete.status === 'broken' && (
        <div className="panel done-note">
          <h3>broken — and kept</h3>
          <p>
            {repaired
              ? <>The repair attempt did not save it ({complete.failed_check}).</>
              : <>It broke at the {complete.failed_check} stage before any repair
                  was attempted — the one repair only covers validation
                  failures, not a crash during the canonical run.</>}
            {' '}The rule, its description, and the failure stay in the
            library as generator-quality data.
          </p>
          <p>
            <a className="chip" href={`#/rules/${complete.rule_id}`}>rule #{complete.rule_id} details</a>
          </p>
        </div>
      )}
      {complete && (complete.status === 'generation_failed' || complete.status === 'error') && (
        <div className="error-note">
          the generation failed before producing a rule: {complete.error}
        </div>
      )}
    </div>
  )
}
