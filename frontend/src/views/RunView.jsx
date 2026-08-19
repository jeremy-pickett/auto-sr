import { useCallback, useEffect, useMemo, useRef, useState } from 'react'
import { getCellHistory, getRule, getRun, getGrids, patchRun, rerunRule } from '../api'
import { plane } from '../lib/decode'
import { KIND_COLORS, KIND_RGB, ageBrightness, levelBrightness, SERIES, textOn } from '../lib/palette'

const CHUNK = 100 // ticks per grid request: small enough to land fast
const BEHAVIORS = ['settles', 'repeats', 'noisy', 'structured', 'unclassified']
const SPEEDS = [
  { label: 'slow', ticksPerSecond: 4 },
  { label: 'walk', ticksPerSecond: 10 },
  { label: 'play', ticksPerSecond: 30 },
  { label: 'sprint', ticksPerSecond: 60 },
]

// A short, plain-language gloss on what a guessed_behavior actually
// means for this specific run — the same spirit as the quiet-note
// below, just for the ordinary case instead of the surprising one.
function behaviorNote(behavior, run) {
  switch (behavior) {
    case 'repeats':
      return run.loop_length
        ? `Settled into a loop that repeats every ${run.loop_length} ticks — from here on you're watching the same cycle over and over.`
        : 'Settled into a cycle that repeats exactly.'
    case 'noisy':
      return "Kept changing the whole way through, with no freeze and no repeating cycle inside this run's tracked window. That can mean real chaos, or a cycle too long to have shown up yet."
    case 'structured':
      return 'Settled into an organized, non-trivial pattern — neither frozen solid nor dissolved into noise. This is the kind of result the library exists to find.'
    case 'settles':
      return 'Froze solid: every piece of state this rule tracks, visible and hidden, stopped changing — it can never move again from here.'
    case 'unclassified':
      return "The classifier couldn't confidently place this one in a bucket — worth a look with your own eyes."
    default:
      return null
  }
}

function Sparkline({ name, values, tick, settledAt, color }) {
  const peak = Math.max(1, ...values)
  const step = 100 / Math.max(1, values.length - 1)
  const points = values
    .map((v, i) => `${(i * step).toFixed(2)},${(26 - (v / peak) * 24).toFixed(2)}`)
    .join(' ')
  const tickX = tick * step
  return (
    <div className="spark">
      <div className="spark-head">
        <span>{name.replaceAll('_', ' ')}</span>
        <span className="value">{values[tick] ?? '—'}</span>
      </div>
      <svg viewBox="0 0 100 28" height="34" preserveAspectRatio="none">
        {settledAt != null && (
          <line
            x1={settledAt * step} y1="0" x2={settledAt * step} y2="28"
            stroke="var(--amber)" strokeWidth="0.6" strokeDasharray="2 2"
          />
        )}
        <polyline points={points} fill="none" stroke={color} strokeWidth="1" />
        <line x1={tickX} y1="0" x2={tickX} y2="28" stroke="var(--cyan)" strokeWidth="0.8" />
      </svg>
    </div>
  )
}

function CellInspector({ runId, picked, tick, kindPlane, width, height, props }) {
  const [history, setHistory] = useState(null)
  const stripRef = useRef(null)

  useEffect(() => {
    setHistory(null)
    if (picked) getCellHistory(runId, picked.y, picked.x, props).then((d) => setHistory(d.history), () => {})
  }, [runId, picked, props])

  // The strip: this cell's own kind across the whole run (REQ-13.4).
  useEffect(() => {
    const canvas = stripRef.current
    const kinds = history?.kind
    if (!canvas || !kinds) return
    canvas.width = kinds.length
    canvas.height = 1
    const ctx = canvas.getContext('2d')
    const image = ctx.createImageData(kinds.length, 1)
    kinds.forEach((k, i) => {
      const [r, g, b] = KIND_RGB[k % KIND_RGB.length]
      image.data.set([r, g, b, 255], i * 4)
    })
    ctx.putImageData(image, 0, 0)
  }, [history])

  if (!picked) {
    return <div className="hint">Pause and click a cell to inspect it. Read-only — history never changes.</div>
  }

  const neighbors = []
  if (kindPlane) {
    for (let dy = -1; dy <= 1; dy++) {
      for (let dx = -1; dx <= 1; dx++) {
        const y = (picked.y + dy + height) % height
        const x = (picked.x + dx + width) % width
        neighbors.push({ y, x, kind: kindPlane[y * width + x], me: dy === 0 && dx === 0 })
      }
    }
  }

  return (
    <>
      <div className="position">row {picked.y}, column {picked.x} · tick {tick}</div>
      <div className="neighbors">
        {neighbors.map((n, i) => (
          <div
            key={i}
            className={`n ${n.me ? 'me' : ''}`}
            style={{
              background: KIND_COLORS[n.kind % KIND_COLORS.length],
              color: textOn(KIND_COLORS[n.kind % KIND_COLORS.length]),
            }}
            title={`row ${n.y}, column ${n.x}`}
          >
            {n.kind}
          </div>
        ))}
      </div>
      {history && (
        <div className="kv" style={{ marginBottom: 8 }}>
          {Object.entries(history).map(([name, values]) => (
            <div key={name} style={{ display: 'contents' }}>
              <dt>{name.replaceAll('_', ' ')}</dt>
              <dd>{String(values[tick])}</dd>
            </div>
          ))}
        </div>
      )}
      <div className="strip-label">this cell across the whole run</div>
      <canvas ref={stripRef} />
    </>
  )
}

export default function RunView({ runId }) {
  const [run, setRun] = useState(null)
  const [rule, setRule] = useState(null)
  const [error, setError] = useState(null)
  const [tick, setTick] = useState(0)
  const [playing, setPlaying] = useState(false)
  const [speed, setSpeed] = useState(2)
  const [mapping, setMapping] = useState(null) // {color, brightness}
  const [picked, setPicked] = useState(null)
  const [showSource, setShowSource] = useState(false)
  const [smooth, setSmooth] = useState(true)
  const [chunks, setChunks] = useState(() => new Map())
  const [isFullscreen, setIsFullscreen] = useState(false)

  const stageRef = useRef(null)
  const canvasRef = useRef(null)
  const pendingRef = useRef(new Set())
  const chunksRef = useRef(chunks)
  chunksRef.current = chunks
  const runRef = useRef(run)
  runRef.current = run
  const tickRef = useRef(tick)
  tickRef.current = tick
  // Each tick is rendered once into a small offscreen canvas; playback
  // crossfades neighboring frames with GPU-composited drawImage calls,
  // so smooth motion costs almost nothing.
  const framesRef = useRef(new Map())
  const drawBlendRef = useRef(null)
  const smoothRef = useRef(smooth)
  smoothRef.current = smooth

  useEffect(() => {
    setRun(null); setRule(null); setTick(0); setPlaying(false); setPicked(null)
    setChunks(new Map()); pendingRef.current = new Set()
    getRun(runId)
      .then((r) => { setRun(r); return getRule(r.rule_id) })
      .then(setRule, setError)
  }, [runId])

  useEffect(() => {
    const onChange = () => setIsFullscreen(document.fullscreenElement === stageRef.current)
    document.addEventListener('fullscreenchange', onChange)
    return () => document.removeEventListener('fullscreenchange', onChange)
  }, [])

  const toggleFullscreen = () => {
    if (document.fullscreenElement) document.exitFullscreen()
    else stageRef.current?.requestFullscreen?.()
  }

  // Display mapping precedence (REQ-13.2): the user's choice, then the
  // rule's suggestion, then kind for color and age for brightness.
  const display = useMemo(() => {
    const suggested = rule?.suggested_display ?? {}
    return {
      color: mapping?.color ?? suggested.color ?? 'kind',
      brightness: mapping?.brightness ?? suggested.brightness ?? 'age',
    }
  }, [rule, mapping])

  const gridProps = useMemo(() => {
    const wanted = new Set(['kind', display.color])
    if (display.brightness !== 'none') wanted.add(display.brightness)
    return [...wanted]
  }, [display])
  const propsKey = gridProps.join(',')

  const ensureChunk = useCallback((index) => {
    if (!run || index * CHUNK > run.ticks_run) return
    const key = `${propsKey}|${index}`
    if (pendingRef.current.has(key)) return // requested already, in flight or done
    pendingRef.current.add(key)
    getGrids(runId, index * CHUNK, Math.min((index + 1) * CHUNK - 1, run.ticks_run), gridProps)
      .then((decoded) => setChunks((now) => new Map(now).set(key, decoded)), setError)
  }, [run, runId, propsKey, gridProps])

  const chunkIndex = Math.floor(tick / CHUNK)
  const chunk = chunks.get(`${propsKey}|${chunkIndex}`)

  useEffect(() => {
    ensureChunk(chunkIndex)
    // Fetch the next stretch before playback reaches it.
    if (tick - chunkIndex * CHUNK > CHUNK * 0.6) ensureChunk(chunkIndex + 1)
  }, [ensureChunk, chunkIndex, tick])

  // Playback clock. Playback reads stored ticks only (REQ-13.3), and
  // never runs ahead of them: if the next stretch of grids has not
  // arrived yet, the clock holds on the last tick it can draw instead
  // of racing blind to the end.
  useEffect(() => {
    if (!playing || !run) return
    const arrived = (t) =>
      chunksRef.current.has(`${propsKey}|${Math.floor(t / CHUNK)}`)
    let frame
    let last = performance.now()
    let carried = 0
    const step = (now) => {
      carried += ((now - last) / 1000) * SPEEDS[speed].ticksPerSecond
      last = now
      if (carried >= 1) {
        const advance = Math.floor(carried)
        carried -= advance
        setTick((t) => {
          let next = Math.min(t + advance, run.ticks_run)
          while (next > t && !arrived(next)) next -= 1
          if (next === run.ticks_run) setPlaying(false)
          return next
        })
        // Held ticks are dropped, not banked — when the download
        // catches up, playback resumes smoothly instead of leaping.
        if (carried > 1) carried = 0
      }
      // Between ticks, crossfade toward the upcoming frame ("tween"),
      // so motion reads as continuous instead of a slideshow.
      if (drawBlendRef.current) {
        const fraction = smoothRef.current ? Math.min(carried, 1) : 0
        drawBlendRef.current(tickRef.current, fraction)
      }
      frame = requestAnimationFrame(step)
    }
    frame = requestAnimationFrame(step)
    return () => cancelAnimationFrame(frame)
  }, [playing, speed, run, propsKey])

  // One tick rendered to a cached offscreen canvas.
  const paintFrame = useCallback((t) => {
    const frames = framesRef.current
    const cached = frames.get(t)
    if (cached) return cached
    const runNow = runRef.current
    if (!runNow) return null
    const inChunk = chunksRef.current.get(`${propsKey}|${Math.floor(t / CHUNK)}`)
    if (!inChunk) return null
    const { width, height } = runNow
    const within = t - inChunk.firstTick
    const colors = plane(inChunk.properties[display.color], within, width, height)
    const bright =
      display.brightness !== 'none' && inChunk.properties[display.brightness]
        ? plane(inChunk.properties[display.brightness], within, width, height)
        : null
    const off = document.createElement('canvas')
    off.width = width
    off.height = height
    const ctx = off.getContext('2d')
    const image = ctx.createImageData(width, height)
    const data = image.data
    for (let i = 0; i < colors.length; i++) {
      const value = colors[i]
      let [r, g, b] = KIND_RGB[value % KIND_RGB.length]
      // Kind 0 is the empty ground; it never glows or dims.
      const isGround = display.color === 'kind' && value === 0
      if (bright && !isGround) {
        const level =
          display.brightness === 'age' ? ageBrightness(bright[i]) : levelBrightness(bright[i])
        r *= level; g *= level; b *= level
      }
      data[i * 4] = r; data[i * 4 + 1] = g; data[i * 4 + 2] = b; data[i * 4 + 3] = 255
    }
    ctx.putImageData(image, 0, 0)
    frames.set(t, off)
    while (frames.size > 6) frames.delete(frames.keys().next().value)
    return off
  }, [propsKey, display])

  // Draw tick t, optionally crossfaded `frac` of the way to t+1.
  const drawBlend = useCallback((t, frac) => {
    const canvas = canvasRef.current
    const runNow = runRef.current
    if (!canvas || !runNow) return
    const current = paintFrame(t)
    if (!current) return
    const ctx = canvas.getContext('2d')
    ctx.imageSmoothingEnabled = false
    ctx.globalAlpha = 1
    ctx.drawImage(current, 0, 0)
    if (frac > 0 && t < runNow.ticks_run) {
      const upcoming = paintFrame(t + 1)
      if (upcoming) {
        ctx.globalAlpha = frac
        ctx.drawImage(upcoming, 0, 0)
        ctx.globalAlpha = 1
      }
    }
  }, [paintFrame])

  // Rendered frames depend on the display mapping; start fresh when it
  // changes (or on a new run).
  useEffect(() => {
    framesRef.current = new Map()
  }, [display, propsKey, runId])

  drawBlendRef.current = drawBlend

  // Crisp draw while paused or scrubbing; the playback loop owns the
  // canvas while playing.
  useEffect(() => {
    if (playing) return
    drawBlend(tick, 0)
  }, [run, chunk, tick, display, playing, drawBlend])

  const pickCell = (event) => {
    if (!run || playing) return
    const rect = event.currentTarget.getBoundingClientRect()
    const x = Math.floor(((event.clientX - rect.left) / rect.width) * run.width)
    const y = Math.floor(((event.clientY - rect.top) / rect.height) * run.height)
    setPicked((old) => (old && old.y === y && old.x === x ? null : { y, x }))
  }

  const correct = (fields) =>
    patchRun(runId, fields).then(setRun, setError)

  const rerun = () =>
    rerunRule(rule.id).then((fresh) => { window.location.hash = `#/runs/${fresh.id}` }, setError)

  if (error) return <div className="error-note">something went wrong: {String(error)}</div>
  if (!run || !rule) return <div className="loading">loading the run…</div>

  const shownBehavior = run.user_behavior || run.guessed_behavior
  const displayChoices = ['kind', ...rule.uses]
  const brightnessChoices = ['age', 'none', 'changed_last_tick', ...rule.uses]
  const stillActive = [...rule.uses, ...rule.modifiers]
  const quietlyRanOut = run.stopped_because === 'ran_out' && run.pattern_settled_at != null
  const note = behaviorNote(shownBehavior, run)

  return (
    <div className="run-layout">
      <section className="stage" ref={stageRef}>
        <div className="stage-head">
          <div>
            <div className="title">rule #{rule.id} · run #{run.id} {run.is_canonical ? '· canonical' : ''}</div>
            <div className="sub">
              seed {run.start_seed} · {run.width}×{run.height} · {run.ticks_run + 1} ticks stored ·
              stopped: {run.stopped_because}
              {run.loop_length ? ` (repeats every ${run.loop_length})` : ''}
            </div>
          </div>
          <div className="row">
            <span className={`chip behavior-${shownBehavior} ${run.guess_confidence === 'low' && !run.user_behavior ? 'confidence-low' : ''}`}>
              <span className="dot" />{shownBehavior}
            </span>
            {run.user_flagged && <span className="chip flag">⚑ flagged</span>}
          </div>
        </div>

        {note && <div className="behavior-note">{note}</div>}

        <div className="grid-shell">
          <canvas
            ref={canvasRef}
            className="grid-canvas"
            width={run.width}
            height={run.height}
            onClick={pickCell}
          />
          {!picked && !playing && (
            <div className="inspect-hint">click a cell to inspect it</div>
          )}
          {picked && !playing && (
            <div
              className="pick-ring"
              style={{
                left: `${(picked.x / run.width) * 100}%`,
                top: `${(picked.y / run.height) * 100}%`,
                width: `${100 / run.width}%`,
                height: `${100 / run.height}%`,
              }}
            />
          )}
        </div>

        <div className="transport">
          <button onClick={() => { setPicked(null); setPlaying((p) => !p) }} title={playing ? 'pause' : 'play'}>
            {playing ? '⏸' : '▶'}
          </button>
          <button onClick={() => { setPlaying(false); setTick((t) => Math.max(0, t - 1)) }} title="one tick back">⏮</button>
          <button onClick={() => { setPlaying(false); setTick((t) => Math.min(run.ticks_run, t + 1)) }} title="one tick forward">⏭</button>
          <input
            type="range"
            min="0"
            max={run.ticks_run}
            value={tick}
            onChange={(e) => { setPlaying(false); setTick(Number(e.target.value)) }}
          />
          <span
            className="tick-readout"
            title="an ellipsis means grids are still downloading"
          >
            {chunk &&
            (!playing ||
              tick >= run.ticks_run ||
              chunks.has(`${propsKey}|${Math.floor((tick + 1) / CHUNK)}`))
              ? ''
              : '… '}
            tick {tick} / {run.ticks_run}
          </span>
          <select value={speed} onChange={(e) => setSpeed(Number(e.target.value))}>
            {SPEEDS.map((s, i) => (
              <option key={s.label} value={i}>{s.label} · {s.ticksPerSecond}/s</option>
            ))}
          </select>
          <label
            className="row"
            style={{ color: 'var(--muted)', fontSize: 12, gap: 5 }}
            title="crossfade between ticks instead of stepping"
          >
            <input
              type="checkbox"
              checked={smooth}
              onChange={(e) => setSmooth(e.target.checked)}
            />
            smooth
          </label>
          <button onClick={toggleFullscreen} title={isFullscreen ? 'exit fullscreen' : 'fullscreen'}>
            {isFullscreen ? '⤢' : '⛶'}
          </button>
        </div>

        <div className="row" style={{ width: '100%' }}>
          <label className="row" style={{ color: 'var(--muted)', fontSize: 12 }}>
            color by
            <select value={display.color} onChange={(e) => setMapping({ ...display, color: e.target.value })}>
              {displayChoices.map((p) => <option key={p} value={p}>{p.replaceAll('_', ' ')}</option>)}
            </select>
          </label>
          <label className="row" style={{ color: 'var(--muted)', fontSize: 12 }}>
            brightness by
            <select value={display.brightness} onChange={(e) => setMapping({ ...display, brightness: e.target.value })}>
              {brightnessChoices.map((p) => <option key={p} value={p}>{p.replaceAll('_', ' ')}</option>)}
            </select>
          </label>
          <span style={{ flex: 1 }} />
          <div className="kind-legend">
            {Array.from({ length: rule.kinds }, (_, k) => (
              <span key={k} className="entry">
                <span className="swatch" style={{ background: KIND_COLORS[k % KIND_COLORS.length] }} />
                {k === 0 ? 'kind 0 (empty)' : `kind ${k}`}
              </span>
            ))}
          </div>
        </div>

        {quietlyRanOut && (
          <div className="quiet-note">
            Looks finished, but it wasn't provably finished. The colors you can
            see froze at tick {run.pattern_settled_at} — but this rule also
            carries invisible bookkeeping
            {stillActive.length > 0 ? ` (${stillActive.join(', ')})` : ' (turn schedules or pending random draws)'}
            {' '}that kept changing under the still picture, and a change there
            could have woken the picture back up later. A run only stops early
            when its entire state, hidden parts included, exactly repeats — so
            this one was watched to its full {run.ticks_run}-tick budget. It
            never woke.
          </div>
        )}
      </section>

      <aside className="side">
        <div className="panel">
          <h3>the rule, in its own words</h3>
          <div className="description">{rule.description}</div>
          <div className="meta row" style={{ marginTop: 10 }}>
            {rule.concepts.map((c) => <span key={c} className="chip">{c}</span>)}
          </div>
        </div>

        <div className="panel">
          <h3>facts</h3>
          <dl className="kv">
            <dt>kinds</dt><dd>{rule.kinds}</dd>
            <dt>neighbors</dt><dd>{rule.neighbors}</dd>
            <dt>reach</dt><dd>{rule.reach}</dd>
            <dt>extra properties</dt><dd>{rule.uses.join(', ') || 'none'}</dd>
            <dt>modifiers</dt><dd>{rule.modifiers.join(', ') || 'none'}</dd>
            <dt>picture settled at</dt><dd>{run.pattern_settled_at ?? 'never'}</dd>
            <dt>engine revision</dt><dd>{rule.provenance.engine_version}</dd>
          </dl>
        </div>

        <div className="panel">
          <h3>the numbers</h3>
          {['variety', 'cells_changed', 'kind_quiet_for'].map((name) => (
            <Sparkline
              key={name}
              name={name}
              values={run.numbers[name]}
              tick={tick}
              settledAt={run.pattern_settled_at}
              color={SERIES[name]}
            />
          ))}
        </div>

        <div className="panel inspector">
          <h3>cell inspector</h3>
          <CellInspector
            runId={runId}
            picked={playing ? null : picked}
            tick={tick}
            kindPlane={chunk ? plane(chunk.properties.kind, tick - chunk.firstTick, run.width, run.height) : null}
            width={run.width}
            height={run.height}
            props={['kind', 'age', ...rule.uses]}
          />
        </div>

        <div className="panel">
          <h3>your read on it</h3>
          <div className="corrections">
            <label style={{ color: 'var(--muted)', fontSize: 12 }}>
              behavior{' '}
              <select
                value={run.user_behavior ?? ''}
                onChange={(e) => correct({ user_behavior: e.target.value || null })}
              >
                <option value="">keep the guess ({run.guessed_behavior ?? 'none'})</option>
                {BEHAVIORS.map((b) => <option key={b} value={b}>{b}</option>)}
              </select>
            </label>
            <button
              className={`flag-btn ${run.user_flagged ? 'on' : ''}`}
              onClick={() => correct({ user_flagged: !run.user_flagged })}
            >
              ⚑ {run.user_flagged ? 'flagged' : 'flag as interesting'}
            </button>
            <button onClick={rerun}>run again, new seed</button>
          </div>
        </div>

        <div className="panel">
          <h3>
            <button style={{ all: 'unset', cursor: 'pointer', font: 'inherit', color: 'inherit', letterSpacing: 'inherit' }}
              onClick={() => setShowSource((s) => !s)}>
              source {showSource ? '▾' : '▸'}
            </button>
          </h3>
          {showSource && <pre className="source-view">{rule.source_code}</pre>}
        </div>
      </aside>
    </div>
  )
}
