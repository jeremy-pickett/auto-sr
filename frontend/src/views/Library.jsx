import { useEffect, useMemo, useState } from 'react'
import { listRules, getSummary, addFavorite, removeFavorite } from '../api'
import { RunThumbnail } from '../lib/RunThumbnail.jsx'
import { getHiddenIds, hideRule, unhideRule } from '../lib/hidden'
import { useAuth } from '../lib/firebase'

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

function RuleCard({ rule, hidden, onToggleHidden, signedIn, onFavoriteChange, mine }) {
  const run = rule.canonical_run
  const [favBusy, setFavBusy] = useState(false)
  // Carries "you got here from Mine" through to the nav bar, so it
  // doesn't wrongly light up "Library" for a rule/run you reached from
  // your personal library — see App.jsx's active-tab logic.
  const fromMine = mine ? '?from=mine' : ''
  const detailHref = (rule.slug ? `#/r/${rule.slug}` : `#/rules/${rule.id}`) + fromMine
  const open = () => {
    // A playable rule opens its canonical run; a broken one opens its
    // details — the failure is part of the library too.
    window.location.hash = run ? `#/runs/${run.id}${fromMine}` : detailHref
  }
  const details = (event) => {
    event.stopPropagation()
    window.location.hash = detailHref
  }
  const toggleHidden = (event) => {
    event.stopPropagation()
    onToggleHidden(rule.id)
  }
  const toggleFavorite = async (event) => {
    event.stopPropagation()
    setFavBusy(true)
    try {
      const result = rule.favorited ? await removeFavorite(rule.id) : await addFavorite(rule.id)
      onFavoriteChange(rule.id, result.favorited)
    } finally {
      setFavBusy(false)
    }
  }
  return (
    <div
      className={`rule-card ${hidden ? 'rule-card-hidden' : ''}`}
      onClick={open}
      style={run ? undefined : { opacity: 0.8 }}
    >
      <div className="row" style={{ justifyContent: 'space-between' }}>
        <span>
          {rule.title ? (
            <>
              <span className="rule-title">{rule.title}</span>{' '}
              <span className="id">#{rule.id}</span>
            </>
          ) : (
            <span className="id">rule #{rule.id}</span>
          )}
          {' '}
          <button className="linkish" onClick={details}>details</button>{' '}
          <button className="linkish" onClick={toggleHidden}>
            {hidden ? 'unhide' : 'hide'}
          </button>
        </span>
        <span className="row" style={{ gap: 6 }}>
          {signedIn ? (
            <button className="linkish" onClick={toggleFavorite} disabled={favBusy} title="favorite">
              {rule.favorited ? '★' : '☆'} {rule.favorite_count || ''}
            </button>
          ) : (
            rule.favorite_count > 0 && <span className="sub">★ {rule.favorite_count}</span>
          )}
          {rule.comment_count > 0 && <span className="sub">💬 {rule.comment_count}</span>}
          {rule.visibility === 'private' && <span className="chip private">🔒 private</span>}
          <span className={`chip status-${rule.status}`}>
            <span className="dot" />
            {rule.status}
            {rule.failed_check ? `: ${rule.failed_check}` : ''}
          </span>
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

export default function Library({ mine = false } = {}) {
  const { user, loading: authLoading } = useAuth()
  const [data, setData] = useState(null)
  const [summary, setSummary] = useState(null)
  const [error, setError] = useState(null)
  const [filters, setFilters] = useState({ status: '', behavior: '', concept: '', flagged: false, favorited: false })
  const [sort, setSort] = useState('newest')
  const [page, setPage] = useState(1)
  const [hiddenIds, setHiddenIds] = useState(() => getHiddenIds())
  const [showHidden, setShowHidden] = useState(false)

  useEffect(() => {
    if (!mine) getSummary().then(setSummary, () => {})
  }, [mine])

  const signedOut = mine && !authLoading && !user

  useEffect(() => {
    if (signedOut) { setData(null); return }
    if (mine && authLoading) return // wait for auth state before asking
    setData(null)
    listRules({
      status: filters.status,
      behavior: filters.behavior,
      concept: filters.concept,
      flagged: filters.flagged || undefined,
      favorited: filters.favorited || undefined,
      sort,
      mine: mine || undefined,
      page,
    }).then(setData, setError)
  }, [filters, sort, page, mine, authLoading, signedOut])

  const toggleHidden = (id) => {
    setHiddenIds(hiddenIds.has(id) ? unhideRule(id) : hideRule(id))
  }

  const onFavoriteChange = (id, favorited) => {
    setData((old) => ({
      ...old,
      rules: old.rules.map((r) => (r.id === id ? { ...r, favorited } : r)),
    }))
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
      [key]: key === 'flagged' || key === 'favorited' ? event.target.checked : event.target.value,
    }))
  }

  const lastPage = data ? Math.max(1, Math.ceil(data.total / data.page_size)) : 1

  return (
    <>
      <div className="library-head">
        <h1>{mine ? 'Your library' : 'The library'}</h1>
        {!mine && summary && (
          <span className="totals">
            {summary.totals.rules} rules · {summary.totals.broken} broken ·{' '}
            {Object.entries(summary.totals.behaviors)
              .map(([name, count]) => `${count} ${name}`)
              .join(' · ') || 'no classified runs yet'}
          </span>
        )}
        {mine && data && <span className="totals">{data.total} rules, public and private</span>}
        <span style={{ flex: 1 }} />
        <button className="primary" onClick={() => { window.location.hash = '#/invent' }}>
          ✦ Invent a rule
        </button>
      </div>

      {signedOut ? (
        <div className="loading">sign in to see your personal library</div>
      ) : (
        <>
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
            {user && (
              <label>
                <input type="checkbox" checked={filters.favorited} onChange={set('favorited')} />
                favorited only
              </label>
            )}
            <label>
              <input
                type="checkbox"
                checked={showHidden}
                onChange={(event) => setShowHidden(event.target.checked)}
              />
              show hidden{hiddenIds.size ? ` (${hiddenIds.size})` : ''}
            </label>
            <label>
              sort
              <select value={sort} onChange={(e) => { setPage(1); setSort(e.target.value) }}>
                <option value="newest">newest</option>
                <option value="most_liked">most favorited</option>
                <option value="most_discussed">most discussed</option>
                <option value="most_looped">longest loop</option>
              </select>
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
                  signedIn={!!user}
                  onFavoriteChange={onFavoriteChange}
                  mine={mine}
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
      )}
    </>
  )
}
