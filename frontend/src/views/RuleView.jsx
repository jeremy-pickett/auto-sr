import { useEffect, useState } from 'react'
import { getRule, rerunRule } from '../api'

function Fold({ title, text }) {
  const [open, setOpen] = useState(false)
  if (!text) return null
  return (
    <div className="fold">
      <button className="fold-toggle" onClick={() => setOpen((o) => !o)}>
        {open ? '▾' : '▸'} {title}
      </button>
      {open && <pre className="source-view">{text}</pre>}
    </div>
  )
}

export default function RuleView({ ruleId }) {
  const [rule, setRule] = useState(null)
  const [error, setError] = useState(null)
  const [rerunning, setRerunning] = useState(false)

  useEffect(() => {
    setRule(null)
    getRule(ruleId).then(setRule, setError)
  }, [ruleId])

  const rerun = () => {
    setRerunning(true)
    rerunRule(ruleId).then(
      (fresh) => { window.location.hash = `#/runs/${fresh.id}` },
      (bad) => { setError(bad); setRerunning(false) },
    )
  }

  if (error) return <div className="error-note">something went wrong: {String(error)}</div>
  if (!rule) return <div className="loading">loading the rule…</div>

  const provenance = rule.provenance
  const canonical = rule.runs.find((run) => run.is_canonical)

  return (
    <div className="rule-view">
      <div className="library-head">
        <h1>rule #{rule.id}</h1>
        <span className={`chip status-${rule.status}`}>
          <span className="dot" />
          {rule.status}{rule.failed_check ? `: ${rule.failed_check}` : ''}
        </span>
        {rule.mode === 'variation' && (
          <span className="chip">
            variation of <a href={`#/rules/${rule.parent_rule_id}`}>#{rule.parent_rule_id}</a>
          </span>
        )}
        <span style={{ flex: 1 }} />
        {rule.status === 'ok' && (
          <button onClick={rerun} disabled={rerunning}>
            {rerunning ? 'running…' : 'run again, new seed'}
          </button>
        )}
      </div>

      <div className="rule-columns">
        <div>
          <div className="panel">
            <h3>the rule, in its own words</h3>
            <div className="description">{rule.description}</div>
            {rule.change_note && (
              <p className="sub">the change: {rule.change_note}</p>
            )}
            {rule.spark && (
              <p className="sub">✦ spark: "{rule.spark}"</p>
            )}
          </div>

          {rule.reasoning && (
            <div className="panel">
              <h3>why the machine tried it</h3>
              <div className="description">{rule.reasoning}</div>
            </div>
          )}

          {rule.error_text && (
            <div className="panel">
              <h3>what broke</h3>
              <pre className="source-view">{rule.error_text}</pre>
            </div>
          )}

          <div className="panel">
            <h3>source</h3>
            <pre className="source-view">{rule.source_code}</pre>
          </div>
        </div>

        <div>
          <div className="panel">
            <h3>facts</h3>
            <dl className="kv">
              <dt>kinds</dt><dd>{rule.kinds}</dd>
              <dt>neighbors</dt><dd>{rule.neighbors}</dd>
              <dt>reach</dt><dd>{rule.reach}</dd>
              <dt>extra properties</dt><dd>{rule.uses.join(', ') || 'none'}</dd>
              <dt>reads</dt><dd>{rule.reads.join(', ') || 'none'}</dd>
              <dt>modifiers</dt><dd>{rule.modifiers.join(', ') || 'none'}</dd>
              <dt>shape asked / observed</dt>
              <dd>{rule.requested_shape} / {rule.observed_shape ?? '—'}</dd>
              <dt>concepts</dt><dd>{rule.concepts.join(', ')}</dd>
            </dl>
          </div>

          <div className="panel">
            <h3>runs</h3>
            {rule.runs.length === 0 && <div className="hint">never ran</div>}
            {rule.runs.map((run) => (
              <div key={run.id} className="run-row">
                <a href={`#/runs/${run.id}`}>run #{run.id}</a>
                <span className={`chip behavior-${run.user_behavior || run.guessed_behavior}`}>
                  <span className="dot" />{run.user_behavior || run.guessed_behavior}
                </span>
                <span className="mono sub">
                  seed {run.start_seed} · {run.ticks_run} ticks · {run.stopped_because}
                  {run.is_canonical ? ' · canonical' : ''}
                  {run.user_flagged ? ' · ⚑' : ''}
                </span>
              </div>
            ))}
            {canonical && (
              <div className="hint" style={{ marginTop: 8 }}>
                only the canonical run counts toward the coverage map — reruns
                are analysis, never generation input
              </div>
            )}
          </div>

          <div className="panel">
            <h3>provenance</h3>
            <dl className="kv">
              <dt>model</dt><dd>{provenance.model_id ?? '—'}</dd>
              <dt>engine revision</dt>
              <dd className="mono">{(provenance.engine_version || '').slice(0, 12)}</dd>
              <dt>prompt set</dt>
              <dd className="mono">{(provenance.prompt_set_hash || '—').slice(0, 12)}</dd>
              <dt>modifier catalog</dt>
              <dd className="mono">{(provenance.modifier_catalog_hash || '—').slice(0, 12)}</dd>
              <dt>helper version</dt><dd>{provenance.helper_version ?? '—'}</dd>
            </dl>
            <Fold title="Stage A prompt, exactly as rendered" text={provenance.stage_a_rendered} />
            <Fold title="Stage A raw response" text={provenance.stage_a_raw} />
            <Fold title="Stage B prompt, exactly as rendered" text={provenance.stage_b_rendered} />
            <Fold title="Stage B raw response" text={provenance.stage_b_raw} />
            <Fold title="repair prompt" text={provenance.repair_rendered} />
            <Fold title="repair raw response" text={provenance.repair_raw} />
          </div>
        </div>
      </div>
    </div>
  )
}
