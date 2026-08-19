import { useEffect, useState } from 'react'
import { getRule, getRuleBySlug, rerunRule, setRuleTitle, addFavorite, removeFavorite } from '../api'
import { useDocumentTitle } from '../lib/useDocumentTitle'
import { useAuth } from '../lib/firebase'

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

export default function RuleView({ ruleId, slug }) {
  const { user } = useAuth()
  const [rule, setRule] = useState(null)
  const [error, setError] = useState(null)
  const [rerunning, setRerunning] = useState(false)
  const [editingTitle, setEditingTitle] = useState(false)
  const [titleDraft, setTitleDraft] = useState('')
  const [savingTitle, setSavingTitle] = useState(false)
  const [favBusy, setFavBusy] = useState(false)

  useEffect(() => {
    setRule(null)
    const load = slug ? getRuleBySlug(slug) : getRule(ruleId)
    load.then(setRule, setError)
  }, [ruleId, slug])

  useDocumentTitle(rule ? `${rule.title || `rule #${rule.id}`} — ASR` : null)

  const rerun = () => {
    setRerunning(true)
    rerunRule(rule.id).then(
      (fresh) => { window.location.hash = `#/runs/${fresh.id}` },
      (bad) => { setError(bad); setRerunning(false) },
    )
  }

  const canEditTitle = rule && (!rule.has_owner || rule.mine)

  const startEditingTitle = () => {
    setTitleDraft(rule.title || '')
    setEditingTitle(true)
  }
  const saveTitle = async () => {
    setSavingTitle(true)
    try {
      const fresh = await setRuleTitle(rule.id, titleDraft.trim() || null)
      setRule((old) => ({ ...old, ...fresh }))
      setEditingTitle(false)
    } catch (bad) {
      setError(bad)
    } finally {
      setSavingTitle(false)
    }
  }

  const toggleFavorite = async () => {
    setFavBusy(true)
    try {
      const result = rule.favorited ? await removeFavorite(rule.id) : await addFavorite(rule.id)
      setRule((old) => ({ ...old, favorited: result.favorited }))
    } catch (bad) {
      setError(bad)
    } finally {
      setFavBusy(false)
    }
  }

  if (error) return <div className="error-note">something went wrong: {String(error)}</div>
  if (!rule) return <div className="loading">loading the rule…</div>

  const provenance = rule.provenance
  const canonical = rule.runs.find((run) => run.is_canonical)

  return (
    <div className="rule-view">
      <div className="library-head">
        {editingTitle ? (
          <span className="row" style={{ gap: 6 }}>
            <input
              type="text" value={titleDraft} maxLength={120} autoFocus
              onChange={(e) => setTitleDraft(e.target.value)}
              placeholder="give this rule a name"
              style={{ width: 260 }}
            />
            <button className="primary" onClick={saveTitle} disabled={savingTitle}>save</button>
            <button onClick={() => setEditingTitle(false)} disabled={savingTitle}>cancel</button>
          </span>
        ) : (
          <span className="row" style={{ gap: 8 }}>
            <h1>{rule.title || `rule #${rule.id}`}</h1>
            {rule.title && <span className="sub mono">#{rule.id}</span>}
            {canEditTitle && (
              <button className="linkish" onClick={startEditingTitle} title="give this rule a display name">
                {rule.title ? 'rename' : '+ add a name'}
              </button>
            )}
          </span>
        )}
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
        {rule.favorite_count > 0 && <span className="sub">★ {rule.favorite_count} favorited this</span>}
        {user && (
          <button onClick={toggleFavorite} disabled={favBusy} title={rule.favorited ? 'remove from favorites' : 'favorite this rule'}>
            {rule.favorited ? '★ favorited' : '☆ favorite'}
          </button>
        )}
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
