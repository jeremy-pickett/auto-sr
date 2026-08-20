# Frontend

> **Release 2.2.1** · documented 2026-08-20 · **updated for 2.2.1.**
> Two feature families landed here. The run player gained a render-style picker
> implementing uplift 2.2's §8 — `activity` (REQ-13.17), `kind-stable` (REQ-13.18), a
> rebuilt `trails` (REQ-13.19) and a real `relief` (REQ-13.20) — covered in §3's new
> "Render styles" subsection, alongside a replaced kind palette (§2). And a System view
> was added (§11), with the dev proxy fixes it forced (§12). The Invent view, library
> browser, rule detail, catalog, and sign-in are unchanged and re-verified.
>
> Not built: the recurrent-structure detector (REQ-19.x) from §4–7 of the same uplift.
> Nothing in this document describes structure detection as existing, and the render
> styles here deliberately depend on none of it.

This is part six of a six-part deep-technical-documentation series on Autonomous Semantic Ruliology (ASR). It covers `frontend/` — a Vite + React 19 single-page app that is the only way a human ever looks at the library. It has no server-side rendering, no build-time data, and no state of its own beyond a hash route and a few `useState` hooks per view: everything it shows comes from the backend's `/rules`, `/runs`, `/catalog`, `/library`, `/profile`, `/comments`, and `/system` routes, fetched live.

The frontend has one job the rest of the series doesn't: it has to render **the pattern fingerprint's opposite** — a picture — without ever pretending that picture is the whole truth. REQ-9.8.1 (`documents/asr-requirements-v3.md`) says a run never stops just because the *picture* went quiet; the frontend's job is to make sure the human watching doesn't draw that conclusion either. That tension between what's on screen and what's actually still moving underneath it shows up repeatedly below — in the quiet-note banner, in the "your read on it" panel that treats the classifier's guess as a guess, and in the deliberate refusal to let the canvas play ahead of stored ticks.

## 1. App structure and routing

There is no router library. `frontend/src/App.jsx` hand-rolls a hash router in about a dozen lines:

```jsx
// frontend/src/App.jsx:15-35
function parseRoute() {
  const raw = window.location.hash.replace(/^#\/?/, '')
  const [path, query] = raw.split('?')
  const [head, id] = path.split('/')
  const params = new URLSearchParams(query || '')
  if (head === 'library') return { view: 'library' }
  if (head === 'mine') return { view: 'mine' }
  if (head === 'runs' && id) {
    return {
      view: 'run', id: Number(id),
      tick: params.has('tick') ? Number(params.get('tick')) : undefined,
      from: params.get('from'),
    }
  }
  if (head === 'rules' && id) return { view: 'rule', id: Number(id), from: params.get('from') }
  if (head === 'r' && id) return { view: 'rule', slug: id, from: params.get('from') }
  if (head === 'invent') return { view: 'invent' }
  if (head === 'catalog') return { view: 'catalog' }
  if (head === 'profile') return { view: 'profile' }
  return { view: 'landing' }
}
```

`App` keeps the parsed route in state and re-parses on `hashchange`:

```jsx
// frontend/src/App.jsx:37-45
export default function App() {
  const [route, setRoute] = useState(parseRoute)
  const { user } = useAuth()

  useEffect(() => {
    const onChange = () => setRoute(parseRoute())
    window.addEventListener('hashchange', onChange)
    return () => window.removeEventListener('hashchange', onChange)
  }, [])
```

and then does a flat conditional render — no route table, no lazy loading, no code-splitting boundary per view:

```jsx
// frontend/src/App.jsx:82-91
<main className="page">
  {route.view === 'landing' && <Landing />}
  {route.view === 'library' && <Library />}
  {route.view === 'mine' && <Library mine />}
  {route.view === 'run' && <RunView runId={route.id} initialTick={route.tick} />}
  {route.view === 'rule' && <RuleView ruleId={route.id} slug={route.slug} />}
  {route.view === 'invent' && <Invent />}
  {route.view === 'catalog' && <Catalog />}
  {route.view === 'profile' && <Profile />}
</main>
```

The URL shapes that fall out of `parseRoute` are all documented in the comment directly above it (`App.jsx:12-14`): `#/` (landing), `#/library`, `#/mine`, `#/runs/3` and `#/runs/3?tick=150` (a permalink to one exact tick — see §3), `#/rules/3` and `#/r/:slug` (a rule's numeric ID or its human-readable slug reach the same `RuleView`), `#/invent`, `#/catalog`, `#/profile`, and — added in 2.2.1 — `#/system` (§11). `Mine` and `Profile` are two of the nav links that only render when `useAuth()` reports a signed-in `user` (`App.jsx:64-76`) — the personal library and the display-name page have no meaning for an anonymous visitor.

`#/system` is deliberately *not* one of those: it renders in the nav unconditionally (`App.jsx:76`), for signed-in and anonymous visitors alike. That matches the backend, where `/system/*` has no access check at all (document 5, §11), and both halves carry the same caveat — it is the posture of a single-user app, and the first thing to revisit if this one ever has strangers on it.

`Library` itself is one component reused for both the global and personal views — `mine` is a boolean prop, not a separate implementation:

```jsx
// frontend/src/App.jsx:84-85
{route.view === 'library' && <Library />}
{route.view === 'mine' && <Library mine />}
```

Inside `Library`, that prop changes which query parameter goes to the backend (`mine: mine || undefined` in the `listRules` call, `Library.jsx:149`) and swaps the "sign in to see your personal library" placeholder in for the grid when the visitor is signed out (`Library.jsx:136, 206-208`).

## 2. The dark-observatory UI design language

The whole visual system lives in one file, `frontend/src/index.css`, opening with a comment that states the intent plainly:

```css
/* frontend/src/index.css:1-5 */
/* ============================================================
   Autonomous Semantic Ruliology — the dark observatory.
   One deliberate mode: near-black ground, the automaton is the
   light source, instrument-panel chrome around it.
   ============================================================ */
```

"One deliberate mode" is literal — there is no light theme, no `prefers-color-scheme` branch, no toggle. The design commits to a single dark visual world and the CSS custom properties reflect that:

```css
/* frontend/src/index.css:7-39 */
:root {
  /* ground & surfaces */
  --ground: #0a0e14;
  --panel: #10151e;
  --panel-2: #151c28;
  --panel-3: #1a2332;
  --line: #202a3a;
  --line-2: #2b3850;

  /* ink */
  --ink: #e9eef6;
  --ink-2: #a7b4c6;
  --muted: #64738a;

  /* accents */
  --cyan: #4cc9f0;
  --cyan-dim: #2a7d9b;
  --amber: #ffb86b;

  /* series (validated against the ground) */
  --series-variety: #96a0ff;
  --series-changed: #ff7a59;
  --series-quiet: #3ff0b0;

  /* status */
  --ok: #0ca30c;
  --broken: #e66767;

  --radius: 10px;
  --radius-sm: 6px;
  --font-sans: 'Inter Variable', system-ui, -apple-system, 'Segoe UI', sans-serif;
  --font-mono: 'JetBrains Mono Variable', ui-monospace, 'SF Mono', Menlo, monospace;
}
```

(The three `--series-*` values were restated in 2.2.1 to match the new kind palette described in §3; they mirror `SERIES` in `palette.js`. Everything else in this block is unchanged.)

The metaphor is worked through consistently rather than being a color scheme slapped on top of generic components:

- **Ground and panels are layered, not flat.** `--ground` (`#0a0e14`) is the page; `--panel` through `--panel-3` step up in lightness for cards, the transport bar, and hover states, so the UI reads as instrument surfaces sitting above a dark floor rather than a single gray box.
- **The page background is a radial gradient, not a solid fill** — a soft glow positioned off-canvas top-right, like ambient light from an instrument rather than a lit room:

  ```css
  /* frontend/src/index.css:43-53 */
  html, body {
    margin: 0;
    min-height: 100vh;
    background:
      radial-gradient(1200px 600px at 70% -10%, #101a2b 0%, transparent 60%),
      var(--ground);
    color: var(--ink);
    font-family: var(--font-sans);
    font-size: 14px;
    line-height: 1.5;
  }
  ```

- **Cyan is the one accent that means "system," amber is reserved for "flagged by a human."** The wordmark's pip glows cyan (`.wordmark .pip { background: var(--cyan); box-shadow: 0 0 10px var(--cyan), 0 0 24px rgba(76, 201, 240, 0.5); }`, `index.css:121-125`); the active nav link turns cyan; buttons glow cyan on hover. Amber shows up only for `user_flagged` runs, the quiet-note banner, and the pick-ring around an inspected cell — all cases where a human, not the system, called something out.
- **Typography is instrument-panel, not editorial.** The wordmark and panel headers (`.panel h3`) are small, uppercase, and letter-spaced — `letter-spacing: 0.14em` / `0.16em`, `font-size: 11-12px` — reading like labels on a physical console rather than prose headings (`index.css:111-120`, `452-459`).
- **Status is color-coded chips, everywhere, consistently.** One `.chip` base class (`index.css:181-193`) is specialized per meaning — `behavior-structured`, `behavior-settles`, `behavior-repeats`, `behavior-noisy`, `status-ok`, `status-broken`, `flag`, `private` (`index.css:194-202`) — so a rule's classification, a run's status, and a "flagged" marker all look like the same kind of object no matter which view they appear in.
- **Cards float, they don't sit flat.** `.rule-card` uses a subtle top-to-bottom gradient (`linear-gradient(180deg, var(--panel), #0d121b)`) and lifts on hover with both a `translateY` and a cyan-tinted glow:

  ```css
  /* frontend/src/index.css:234-249 */
  .rule-card {
    background: linear-gradient(180deg, var(--panel), #0d121b);
    border: 1px solid var(--line);
    border-radius: var(--radius);
    padding: 16px 16px 14px;
    display: flex;
    flex-direction: column;
    gap: 10px;
    cursor: pointer;
    transition: border-color 140ms ease, transform 140ms ease, box-shadow 140ms ease;
  }
  .rule-card:hover {
    border-color: var(--cyan-dim);
    transform: translateY(-2px);
    box-shadow: 0 10px 30px rgba(0, 0, 0, 0.45), 0 0 24px rgba(76, 201, 240, 0.07);
  }
  ```

- **The grid canvas itself gets the same glow treatment as the chrome around it** — `filter: drop-shadow(0 0 22px rgba(76, 201, 240, 0.10))` on `.grid-canvas` (`index.css:343-352`), intensifying on hover — reinforcing "the automaton is the light source" from the file's opening comment.
- **The landing page's hero literally runs a computation as its background image.** `.hero-automaton` is a live canvas (see `Landing.jsx`, §9 discussion of the wider design below) masked with a gradient so it "glows behind the words, then yields to them" (`index.css:746-749`).

The font pairing is Inter Variable for interface text and JetBrains Mono Variable for anything numeric or code-like — tick counters, seeds, hashes, source panels — both loaded as local variable-font packages (`@fontsource-variable/inter`, `@fontsource-variable/jetbrains-mono` in `package.json:13-14`) rather than a CDN, so the app has no external font dependency at runtime.

## 3. The run player

`RunView` (`frontend/src/views/RunView.jsx`) is the largest view in the app and the one place all four backend concerns — binary framing, snapshot/delta reconstruction, the computational-vs-pattern fingerprint distinction, and display mapping — surface in the UI at once.

### Wire format and decoding

The full framing spec lives in the storage/API docs (REQ-11.5.1); the frontend's job is just to decode it. `frontend/src/lib/decode.js` is the entire client-side contract with that format:

```js
// frontend/src/lib/decode.js:1-30
// Decoder for the grid wire format (REQ-11.5.1):
//   bytes 0..3   uint32 little-endian: byte length of the JSON header
//   bytes 4..N   UTF-8 JSON header
//   bytes N..    payload region: C-order array blocks at stated offsets

const VIEWS = {
  uint8: Uint8Array,
  uint16: Uint16Array,
  int32: Int32Array,
  float32: Float32Array,
  bool: Uint8Array,
}

export function decodeGrids(buffer) {
  const headLength = new DataView(buffer).getUint32(0, true)
  const header = JSON.parse(new TextDecoder().decode(new Uint8Array(buffer, 4, headLength)))
  const payloadStart = 4 + headLength
  const [firstTick, lastTick] = header.ticks
  const [height, width] = header.shape
  const tickCount = lastTick - firstTick + 1
  const properties = {}
  for (const prop of header.properties) {
    const View = VIEWS[prop.dtype]
    if (!View) throw new Error(`unknown dtype ${prop.dtype}`)
    // Slice so each stack owns aligned memory regardless of offset.
    const bytes = buffer.slice(payloadStart + prop.offset, payloadStart + prop.offset + prop.length)
    properties[prop.name] = new View(bytes)
  }
  return { firstTick, lastTick, tickCount, width, height, properties }
}

// One tick's plane from a decoded stack.
export function plane(stack, tickIndex, width, height) {
  const size = width * height
  return stack.subarray(tickIndex * size, (tickIndex + 1) * size)
}
```

The little-endian `uint32` header length, then a JSON header, then a raw payload region addressed by byte offsets, is exactly the shape REQ-11.5.1 specifies. `decodeGrids` never copies the payload wholesale into JS numbers; it wraps typed-array views (`Uint8Array`, `Uint16Array`, `Int32Array`, `Float32Array`, and `bool` reusing `Uint8Array`) directly over slices of the response `ArrayBuffer`, one per requested property. `plane()` then slices out a single tick's `width × height` block from a property's stacked buffer — this is what turns "the whole chunk's `kind` property" into "tick 47's kind grid" for painting.

`api.js` calls this decoder immediately after fetching:

```js
// frontend/src/api.js:52-56
export async function getGrids(runId, from, to, props) {
  const response = await authorizedFetch(`/runs/${runId}/grids?from=${from}&to=${to}&props=${props.join(',')}`)
  if (!response.ok) throw new Error(`${response.status}: ${await response.text()}`)
  return decodeGrids(await response.arrayBuffer())
}
```

### Fetching in chunks, with prefetch

`RunView` never fetches the whole run. It requests fixed-size tick ranges (`CHUNK = 100`, `RunView.jsx:11`) keyed by a string of the requested properties plus the chunk index, and tracks in-flight requests so the same chunk is never requested twice:

```jsx
// frontend/src/views/RunView.jsx:262-278
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
```

Which properties get fetched at all is driven by the **display mapping** — the `color` and `brightness` choices, defaulting per REQ-13.2's stated precedence (user override → the rule's `SUGGESTED_DISPLAY` → `kind`/`age`):

```jsx
// frontend/src/views/RunView.jsx:245-260
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
```

Switching what colors or brightens the grid changes `propsKey`, which invalidates the chunk cache and re-fetches — the frontend never asks the backend for properties it isn't currently rendering.

### Playback: reads stored ticks only, never runs ahead

REQ-13.3 says playback reads stored ticks and never re-runs the rule; RunView enforces "never get ahead of what's actually downloaded" as an explicit invariant in its animation-frame loop:

```jsx
// frontend/src/views/RunView.jsx:284-321
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
      const ceiling = loopEnabled ? Math.min(loopEnd ?? run.ticks_run, run.ticks_run) : run.ticks_run
      setTick((t) => {
        let next = Math.min(t + advance, ceiling)
        while (next > t && !arrived(next)) next -= 1
        if (next === ceiling) {
          if (loopEnabled) next = Math.min(loopStart, ceiling)
          else setPlaying(false)
        }
        return next
      })
      // Held ticks are dropped, not banked — when the download
      // catches up, playback resumes smoothly instead of leaping.
      if (carried > 1) carried = 0
    }
    ...
```

Four speeds are offered — `slow`/`walk`/`play`/`sprint` at 4/10/30/60 ticks per second (`RunView.jsx:27-32`) — `play` at 30/s matching REQ-13.1's "200×200 at 30fps playback" target. The `while (next > t && !arrived(next)) next -= 1` line is the actual holdback mechanism: it walks backward from the desired tick until it finds one whose chunk has already arrived, so the displayed tick can lag behind the clock but never point at ungenerated data.

### Canvas rendering: offscreen frame cache with crossfade

Each tick is painted once into a small offscreen canvas and cached; playback composites between the current and next cached frame with `globalAlpha`, rather than repainting `ImageData` pixel-by-pixel every animation frame:

```jsx
// frontend/src/views/RunView.jsx:345-465 (abridged to the default path;
// the style branches are the subject of the next subsection)
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
  /* ... activity/kind_stable read the previous tick here ... */
  const off = document.createElement('canvas')
  off.width = width
  off.height = height
  const ctx = off.getContext('2d')
  const image = ctx.createImageData(width, height)
  const data = image.data
  const relief = renderStyle === 'relief'
  const factor = display.brightness === 'age' ? ageBrightness : levelBrightness
  for (let i = 0; i < colors.length; i++) {
    let r, g, b
    if (renderStyle === 'activity') {
      /* ... */
    } else if (renderStyle === 'kind_stable') {
      /* ... */
    } else {
      const value = colors[i]
      const c = KIND_RGB[value % KIND_RGB.length]
      r = c[0]; g = c[1]; b = c[2]
      // Kind 0 is the empty ground; it never glows or dims.
      const isGround = display.color === 'kind' && value === 0
      if (bright && !isGround) {
        const level = factor(bright[i])
        r *= level; g *= level; b *= level
        if (relief) { /* ... gradient shading ... */ }
      }
    }
    data[i * 4] = r; data[i * 4 + 1] = g; data[i * 4 + 2] = b; data[i * 4 + 3] = 255
  }
  ctx.putImageData(image, 0, 0)
  frames.set(t, off)
  const keep = renderStyle === 'trails' ? TRAIL_WINDOW_TICKS + 4 : 6
  while (frames.size > keep) frames.delete(frames.keys().next().value)
  return off
}, [propsKey, display, renderStyle])

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
  /* ... trails compositing and the glow canvas follow ... */
}, [paintFrame, renderStyle])
```

The frame cache is normally capped at six entries — enough to smooth a crossfade window without holding an unbounded number of decoded canvases. In 2.2.1 that cap became conditional, because `trails` composites a long window of past frames and would otherwise evict them faster than it could use them (`const keep = renderStyle === 'trails' ? TRAIL_WINDOW_TICKS + 4 : 6`, `RunView.jsx:457`).

Color comes from `KIND_COLORS`/`KIND_RGB` in `frontend/src/lib/palette.js`, and brightness from one of two curves: `ageBrightness` (a narrow 88–100% glow that decays with age, retuned twice per the file's comments to avoid reading as "dull") or `levelBrightness` (a linear 72–100% ramp for an arbitrary 0–255 property).

**The palette was replaced in 2.2.1.** The eight kind colors are now a bioluminescent/instrument-glow set rather than the generic vivid categorical set that preceded them, and the file's header comment records both the reason and the measurements:

```js
// frontend/src/lib/palette.js:1-6
// The observatory palette. Kind 0 reads as empty ground; kinds 1..7 are a
// bioluminescent/instrument-glow set — replaced 2026-08-20 (was a generic
// vivid categorical set with one jarring pure-saturation green) to match the
// "automaton is the light source" identity index.css already declares. Every
// kind clears >= 7.5:1 contrast on #0a0e14 (range 7.5-13.2:1), minimum
// pairwise YCbCr separation is 48.1 (up from the prior palette's ~36 floor).
```

Two changes matter beyond aesthetics. Kind 0 moved from `#182130` to `#0a0e14` — exactly `--ground`, the page background — so empty ground is now genuinely absent rather than a slightly-lighter tile; it still "never glows or dims." And minimum pairwise separation went *up* to 48.1 from roughly 36, meaning the new palette is measurably easier to tell apart kind-by-kind, not merely better looking. The `SERIES` colors for the sparkline charts were restated in the same vocabulary (`palette.js:62-66`).

The "smooth" checkbox toggles whether the crossfade fraction is computed at all — when off, `drawBlend` is always called with `frac = 0` and playback steps discretely tick to tick instead of tweening (`smoothRef.current ? Math.min(carried, 1) : 0`, `RunView.jsx:314`).

### Render styles (new in 2.2.1)

The run player has a second selector next to the speed picker (`RunView.jsx:739-751`) offering six styles: `flat`, `glow`, `activity`, `kind-stable`, `trails`, `relief`. This implements §8 of the visualization uplift (`documents/requirements/frontend-vis-uplift-2.2.1.md`), and the governing requirement is REQ-13.16: **every one of these is display only.** None affects any fingerprint, the classifier, stopping, storage, or the coverage map. REQ-13.20.2 adds that the choice is never persisted to the run — it is UI state, and a run does not have a render style the way it has a width.

They are also strictly *layered on top of* the existing color/brightness mapping (REQ-13.2), not new entries in it. The comment on the state hook says so explicitly (`RunView.jsx:194-200`), and the distinction is what keeps the picker from becoming a third axis of display precedence.

`glow` predates this uplift and is not covered by any REQ; it was kept as-is.

**`activity` (REQ-13.17)** lights a cell where `kind` changed on this exact tick and leaves everything else at ground. It answers "where is computation happening," which the default view answers only by implication. Its cost is the reason the uplift called it nearly free: the comparison needs the previous tick's `kind` plane, which is almost always sitting in an already-fetched chunk. The lookup reaches across a chunk boundary at worst and **never triggers a fetch** (`RunView.jsx:371-390`) — if the previous chunk is not cached, the comparison is simply skipped for that frame.

**`kind-stable` (REQ-13.18)** is the inverse and the most interesting of the six. A cell glows where `kind` held constant *but the mapped brightness property changed underneath it*, and everything else is dimmed to 10%. A grid that reads as completely frozen in the default view lights up like a city in this one.

This is the clearest visual expression the app has of REQ-9.7's central distinction — pattern state versus computational state — and it is the continuous, per-cell form of the "picture went quiet" banner described later in this section. The uplift rates it the highest value-to-cost item in the document precisely because it needs no detector and no new storage: everything it shows is already in reconstructed history.

The backend test that pins the data contract these two views read is `test_slow_burn_kind_is_stable_while_memory_stays_active_before_the_flip` (`backend/tests/test_run.py:89-104`, citing REQ-15.12.1). Before `slow_burn`'s flip, every cell's `kind` is identical tick to tick while `memory` changes on *every* tick — so the same fixture reads as entirely dark under `activity` and entirely lit under `kind-stable`, then swaps. The canvas rendering itself has no test harness; that test covers the reconstructible data underneath it, which is the honest boundary.

**`trails` (REQ-13.19)** composites the last 40 ticks into one frame with geometrically decaying alpha (`TRAIL_WINDOW_TICKS = 40`, `TRAIL_BASE_ALPHA = 0.5`, `TRAIL_DECAY = 0.9`, `RunView.jsx:19-21`). The compositing detail worth reading is the blend mode (`RunView.jsx:489-503`): every pixel in a painted frame is fully opaque, kind 0 included, so drawing older frames normally would *blot out* the current one rather than ghosting behind it. The loop sets `globalCompositeOperation = 'lighter'` — additive — so an older frame can only brighten a past-active cell into a fading ghost, never erase what the current tick drew. It stops early when a contribution drops below 0.005 alpha or when a frame isn't cached (a scrub jump landing past what has been painted).

REQ-13.19.2 requires that trails never be the default and always be labeled, because a trails frame is not a tick and a viewer who doesn't know that is reading a smear as a state. The implementation satisfies this with an on-canvas badge (`RunView.jsx:678-682`) reading `trails — last 40 ticks blended, not tick N alone`.

**`relief` (REQ-13.20)** treats the mapped brightness property as a height field, derives a surface normal from the local gradient, and shades it with a fixed light direction (`RunView.jsx:429-449`) — replacing a cruder single-neighbor emboss. The uplift marks it optional and lowest-value, and it carries a caveat the UI must respect: only the legibility trick is borrowed from surface rendering, **nothing here is three-dimensional**, and the interface must not imply otherwise.

Two implementation notes cut across the set. Relief bakes its shading into cached pixels, so the frame cache is invalidated when the style changes, not only when the display mapping or run does (`RunView.jsx:519-521`). And `activity`/`kind-stable` automatically get the glow canvas that `glow` uses (`RunView.jsx:511`) — since their flagged cells are boosted near-white against a near-black field, blurring the whole frame blooms only the cells that were flagged, which is the "bigger and more obvious" half that dimmed cells don't receive.

### Canvas zoom

Zoom is a pure CSS transform on the grid's wrapping `<div>`, not a re-render at higher resolution:

```jsx
// frontend/src/views/RunView.jsx:524-533
<div className="grid-zoom-viewport">
  <div className="grid-shell" style={{ transform: `scale(${zoom})`, transformOrigin: 'center' }}>
    <canvas
      ref={canvasRef}
      className={`grid-canvas ${roundCells ? 'round-cells' : ''}`}
      width={run.width}
      height={run.height}
      onClick={pickCell}
      style={{ '--cell-cols': run.width, '--cell-rows': run.height }}
    />
```

The zoom range is 1×–8×, stepped by ×1.5 per click (`setZoom((z) => Math.min(8, z * 1.5))`, `RunView.jsx:553`), and panning is native browser scroll rather than custom drag code — `.grid-zoom-viewport` sets `overflow: auto` and a `max-height` cap so the scaled content simply overflows into scrollbars:

```css
/* frontend/src/index.css:317-328 */
/* Zoom (documents/new-features-2.md item 12): a CSS scale on the
   shell, with the viewport around it handling pan via plain browser
   scrollbars once the scaled content overflows it -- no custom drag
   code needed. max-height caps how tall the scrollable area gets so
   zooming in doesn't blow out the rest of the page layout. */
.grid-zoom-viewport {
  width: 100%;
  max-height: calc(100vh - 250px);
  overflow: auto;
  display: flex;
  justify-content: center;
}
```

A second CSS-only feature sits alongside zoom: "round cells." Rather than a different renderer, it masks the already-rendered square-pixel canvas with a repeating SVG circle pattern sized to exactly one cell per tile, so the underlying pixel data — still one square texel per cell, which is what keeps 40,000-cell playback cheap — is untouched; only the compositor's mask changes (`index.css:353-369`).

### Cell inspection and history

REQ-13.4 requires that, while paused, clicking a cell shows its property values, its neighbors' values, and its own history strip across the whole run, strictly read-only. `pickCell` in `RunView.jsx:399-405` refuses to register a pick while `playing` is true; `CellInspector` (`RunView.jsx:83-155`) fetches per-cell history from `getCellHistory` (`GET /runs/{id}/cell/{y}/{x}`) and paints a one-pixel-tall canvas strip, one column per tick, colored by that cell's own `kind` history — a compact "this cell's whole life" sparkline distinct from the run-wide numeric sparklines in the side panel.

### Loop, fullscreen, and the "picture went quiet" honesty banner

A loop toggle lets playback wrap a `[loopStart, loopEnd]` tick range instead of stopping at the end, with a "use the settled period" shortcut that seeds the range from `run.loop_length` when the run's classifier detected an exact repeat (`suggestLoopRange`, `RunView.jsx:228-232`). Fullscreen uses the standard Fullscreen API (`stageRef.current?.requestFullscreen?.()`) and CSS `:fullscreen` variants that swap in the page's own background gradient so the stage isn't sitting on flat black once it owns the whole viewport (`index.css:301-310`).

The most spec-driven piece of the player is the quiet-but-alive banner, which exists specifically to satisfy REQ-13.11 ("Where a run ended `ran_out` with a high `kind_quiet_for`, the UI says the pattern stopped moving while the underlying state kept changing"):

```jsx
// frontend/src/views/RunView.jsx:680-692
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
```

This is a direct UI expression of the *pattern fingerprint vs. computational fingerprint* distinction CLAUDE.md calls "the subtlest part" of the state model: the picture (pattern fingerprint) can look done while `weight`/`stubbornness`/scheduler-phase/RNG state (computational fingerprint) is still moving, and REQ-9.8.1 forbids stopping on the former alone. The banner only fires when `run.stopped_because === 'ran_out'` and `run.pattern_settled_at != null` (`quietlyRanOut`, `RunView.jsx:494`) — i.e., exactly the case the spec calls out.

A calmer, always-present sibling — `behaviorNote()` (`RunView.jsx:37-54`) — gives a one-paragraph plain-language gloss on whatever `guessed_behavior` (or the user's override) actually is, rendered in a `.behavior-note` panel regardless of whether anything surprising happened; the quiet-note above is reserved for the specifically surprising case.

## 4. The Invent view and the generation stream

`POST /rules/generate` streams `text/event-stream` from a POST body, which per REQ-11.4.1 rules out the native `EventSource` object (it can only issue GET). `api.js`'s `generateRule` therefore hand-parses SSE framing out of a streaming `fetch()` response:

```js
// frontend/src/api.js:68-102
// The generation stream (REQ-11.4). The endpoint is a POST that
// responds text/event-stream, so this must be a streaming fetch() with
// a ReadableStream reader — EventSource cannot POST (REQ-11.4.1).
// A body is sent only when there's something to say (private, or a
// spark) — keeps the ordinary request exactly the bare, bodyless POST
// it's always been.
export async function generateRule(onEvent, { visibility, spark, title } = {}) {
  const body = {}
  if (visibility === 'private') body.visibility = visibility
  if (spark) body.spark = spark
  if (title) body.title = title
  const response = await authorizedFetch('/rules/generate', {
    method: 'POST',
    ...(Object.keys(body).length
      ? { headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(body) }
      : {}),
  })
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
```

This is a minimal, purpose-built SSE parser: it buffers decoded text, splits on the blank-line frame delimiter (`\n\n`), and regex-extracts the `event:` and `data:` lines from each frame, calling `onEvent(name, parsedData)` for each complete one. It never depends on any SSE library and never falls back to polling — matching the architecture note that this satisfies REQ-13.7 "without a job queue."

`Invent.jsx` consumes this by pushing every event onto a log and folding that log into per-stage UI state on each render, rather than tracking stage state imperatively:

```jsx
// frontend/src/views/Invent.jsx:8-33
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
```

`start()` wires the reader into React state with a `startedRef` guard against double-submission (`Invent.jsx:43-62`):

```jsx
// frontend/src/views/Invent.jsx:45-62
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
```

Every distinct backend event (`stage_a_started`, `stage_a_complete`, `stage_b_started`, `stage_b_complete`, `validating`, `validation_failed`, `repairing`, `running`, `tick_progress`, `complete` — the exact list REQ-11.4 specifies) turns into UI: a four-item `<ol className="pipeline">` of stage "lamps" that go idle → active (with a CSS `lamp-breathe` pulse animation, `index.css:607-621`) → done or failed; the Stage A proposal rendered into its own panel the moment `stage_a_complete` arrives (`Invent.jsx:143-156`); a running tick counter sourced from `tick_progress` payloads (`stage.key === 'running' && progress ? \`tick ${progress.tick} / ${progress.max_ticks}\` : stage.detail`, `Invent.jsx:133-135`); every `validation_failed` event rendered as its own error line, with the second one specifically labeled "the repair also failed" (`Invent.jsx:158-161`, matching the "one repair attempt" contract from CLAUDE.md); and finally a `complete` event branching into three distinct outcome panels — `ok` (thumbnail of the final frame, ticks run, stop reason, guessed behavior, links to the run and rule), `broken` (kept in the library regardless, with an explanation of whether the one permitted repair was even attempted), and `generation_failed`/`error` (no rule was produced at all) — at `Invent.jsx:173-217`.

One UI detail worth flagging as policy made visible: the view's own subhead states the no-signal rule in plain language —

```jsx
// frontend/src/views/Invent.jsx:75-79
<p className="sub">
  The machine reads the coverage map — never your flags, never your
  reruns — proposes one rule, implements it, and every outcome lands
  in the library. Failure is data too.
</p>
```

— directly reflecting REQ-8.5/REQ-8.6 (user signals never enter Stage A context; only canonical runs count toward coverage), and the "run again, new seed" tooltips in both `RunView.jsx:776` and `RuleView.jsx:131` repeat the same guarantee for reruns specifically.

## 5. Library browser and pagination

`Library.jsx` fetches through `listRules`, which builds a query string from whatever filters are set, dropping any `undefined`/empty ones so the request stays minimal:

```js
// frontend/src/api.js:22-27
export const listRules = (params = {}) => {
  const query = new URLSearchParams(
    Object.entries(params).filter(([, value]) => value !== undefined && value !== '')
  )
  return authorizedFetch(`/rules?${query}`).then(asJson)
}
```

The call site passes through every filter the UI exposes plus the current page:

```jsx
// frontend/src/views/Library.jsx:142-152
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
```

`mine: mine || undefined` is the entire mechanism that turns the shared `Library` component into the personal library — when the `#/mine` route renders `<Library mine />`, that one query parameter is what tells the backend to scope to the signed-in user's own rules instead of the public set. Filters offered in the UI: `status` (any/ok/broken), `behavior` (any of the five classifier outcomes), `concept` (populated dynamically from whatever concepts appear on the currently loaded page — `concepts` is a `useMemo` over `data?.rules`, `Library.jsx:166-170`, not a separate catalog fetch), `flagged only`, `favorited only` (only shown when signed in), and a client-only `show hidden` toggle backed by `localStorage` (see §9). Sort is one of `newest`, `most_liked`, `most_discussed`, `most_looped` (`Library.jsx:257-263`).

Pagination is entirely server-driven. `list_rules` on the backend (`backend/asr/api/routes.py:187-189`) defaults `page_size` to 24 and caps it at 200 (`page_size: int = Query(24, ge=1, le=200)`); the frontend never overrides that default — it just reads `data.page_size` and `data.total` back to compute the last page and render a prev/next pager:

```jsx
// frontend/src/views/Library.jsx:290-298
{data && data.total > data.page_size && (
  <div className="pager">
    <button disabled={page <= 1} onClick={() => setPage((p) => p - 1)}>‹ prev</button>
    <span className="pager-status">
      page {page} of {lastPage} · {data.total} rules
    </span>
    <button disabled={page >= lastPage} onClick={() => setPage((p) => p + 1)}>next ›</button>
  </div>
)}
```

with `lastPage` computed client-side as `Math.max(1, Math.ceil(data.total / data.page_size))` (`Library.jsx:185`). Changing any filter or the sort order resets `page` back to 1 (every `set(key)` handler and the sort `<select>`'s `onChange` both call `setPage(1)` before updating the filter, `Library.jsx:177-183, 257`), so a filter change never leaves the view stranded on an out-of-range page.

Each `RuleCard` renders a `RunThumbnail` of the canonical run's last frame (see §9) alongside behavior/status/modifier/concept chips, and clicking a card navigates to the canonical run's player (or the rule's detail page if it never produced a playable run, `RuleCard.open`, `Library.jsx:32-36`). A `?from=mine` query parameter is appended to every link a `RuleCard` produces when `mine` is true — this exists purely to fix the nav-highlight bug covered in §9.

## 6. Rule detail with provenance

`RuleView.jsx` renders `#/rules/:id` or `#/r/:slug` (both resolve through the same component; `slug` routes call `getRuleBySlug`, id routes call `getRule`, `RuleView.jsx:35`). Layout is a two-column grid (`rule-columns`, `index.css:647-655`) — description/reasoning/error/source on the left, facts/runs/provenance on the right.

"Provenance," concretely, is a `panel` rendering hashes, the model ID, and every fully-rendered prompt and raw model response the pipeline stored for that rule, each collapsed behind a fold so the page isn't dominated by prompt text by default:

```jsx
// frontend/src/views/RuleView.jsx:226-244
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
```

`Fold` (`RuleView.jsx:9-20`) is a tiny disclosure component — a button toggling a `<pre className="source-view">` block — reused for each of the six possible prompt/response pairs (Stage A prompt and response, Stage B prompt and response, and the one permitted repair's prompt and response, which is `null` and renders nothing via `Fold`'s early `if (!text) return null` when no repair was attempted). This directly surfaces CLAUDE.md's "prompt templates live in version control as files, and fully rendered prompts are stored per rule" guarantee — the UI is a plain window onto exactly what was stored, not a reconstruction.

Elsewhere on the page: `rule.description` and, for a repaired or edited variation, `rule.change_note` and `rule.spark` (`RuleView.jsx:142-149`); `rule.reasoning` in its own panel when present ("why the machine tried it," `RuleView.jsx:151-156`); `rule.error_text` verbatim for a broken rule ("what broke," `RuleView.jsx:158-163`); the full `rule.source_code` (`RuleView.jsx:165-168`); a `facts` panel listing `kinds`, `neighbors`, `reach`, `uses`, `reads`, `modifiers` (each with a tooltip from the modifier catalog, discussed in §7), requested-vs-observed shape, and concepts (`RuleView.jsx:174-197`); and a `runs` panel listing every run of the rule with its behavior chip, seed, tick count, and stop reason, closing with an explicit reminder that "only the canonical run counts toward the coverage map — reruns are analysis, never generation input" (`RuleView.jsx:218-223`) — the UI restating REQ-8.6 in plain language at the exact point a user might otherwise assume a rerun matters.

Title editing is gated by ownership: `canEditTitle = rule && (!rule.has_owner || rule.mine)` (`RuleView.jsx:49`) — an unowned (anonymous/public-by-default) rule is editable by anyone, an owned one only by its owner — and saves through `setRuleTitle` (`PATCH /rules/{id}`).

## 7. The modifier catalog

`Catalog.jsx` renders `GET /catalog/modifiers` as a plain read-only table — REQ-13.9 specifies exactly that ("Modifier catalog view, read-only in v1"):

```jsx
// frontend/src/views/Catalog.jsx:16-51
<div className="library-head">
  <h1>Modifier catalog</h1>
  <span className="totals">
    per-cell dials the harness applies on the rule's behalf — read-only in v1
  </span>
</div>
<div className="panel">
  <table className="catalog-table">
    <thead>
      <tr>
        <th>name</th>
        <th>what it does</th>
        <th>values</th>
        <th>no-effect value</th>
        <th>assigned</th>
        <th>offered</th>
      </tr>
    </thead>
    <tbody>
      {modifiers.map((m) => (
        <tr key={m.name}>
          <td>{m.name}</td>
          <td className="blurb">{m.blurb}</td>
          <td className="mono">{m.type_spec}</td>
          <td className="mono">{m.default_value}</td>
          <td>{m.assign_when === 'birth' ? 'when a cell is born' : 'at the start'}</td>
          <td className="mono">{m.availability}</td>
        </tr>
      ))}
    </tbody>
  </table>
</div>
```

The column labeled **"no-effect value"** is where REQ-5.1's identity-default rule becomes a visible UI promise: every modifier (`weight`, `stubbornness`, `rate`, and whatever else the catalog holds) is required to have a `default_value` at which it changes nothing, and the table names that value explicitly rather than just listing a default. This is the same guarantee CLAUDE.md states as a hard rule ("Modifier defaults must be identity values — no effect at all") and REQ-15.2 backs with a bit-identical test per modifier — the frontend's contribution is simply making that identity value legible next to the modifier's name instead of leaving it implicit.

The catalog is also consumed elsewhere as tooltip data rather than only on its own page. `frontend/src/lib/modifierCatalog.js` fetches and caches the same `/catalog/modifiers` response once per page load and exposes it as a name→blurb lookup:

```js
// frontend/src/lib/modifierCatalog.js:1-31
// The modifier catalog barely changes and is small (REQ-13.9's
// read-only table already fetches it whole) -- fetched once per page
// load and shared, rather than every chip that wants a blurb making
// its own request.
let cached = null

function fetchBlurbs() {
  if (!cached) {
    cached = getCatalog().then(
      (data) => Object.fromEntries(data.modifiers.map((m) => [m.name, m.blurb])),
      () => ({}),
    )
  }
  return cached
}

// Plain-English tooltip text for a modifier chip, keyed by name --
// null until the catalog has loaded, then a lookup (missing names,
// e.g. from an older catalog hash, just get no tooltip).
export function useModifierBlurbs() {
  const [blurbs, setBlurbs] = useState(null)
  useEffect(() => {
    let alive = true
    fetchBlurbs().then((b) => { if (alive) setBlurbs(b) })
    return () => { alive = false }
  }, [])
  return blurbs
}
```

`useModifierBlurbs()` is called from `Library.jsx`, `RuleView.jsx`, and `RunView.jsx` so that every modifier chip anywhere in the app carries the same plain-language `title` tooltip, sourced once and shared — a small but deliberate consistency choice matching REQ-0.1's plain-language mandate.

## 8. Firebase Email/Password sign-in

`frontend/src/lib/firebase.js` initializes one Firebase app instance from Vite env vars and exposes a `useAuth()` hook wrapping `onAuthStateChanged` — no React Context, since (per the file's own comment) each `useAuth()` caller sets up its own listener against the same singleton `auth` object and they all update in lockstep:

```js
// frontend/src/lib/firebase.js:1-39
import { useEffect, useState } from 'react'
import { initializeApp } from 'firebase/app'
import {
  getAuth,
  onAuthStateChanged,
  createUserWithEmailAndPassword,
  signInWithEmailAndPassword,
  signOut,
} from 'firebase/auth'

const firebaseConfig = {
  apiKey: import.meta.env.VITE_FIREBASE_API_KEY,
  authDomain: import.meta.env.VITE_FIREBASE_AUTH_DOMAIN,
  projectId: import.meta.env.VITE_FIREBASE_PROJECT_ID,
  storageBucket: import.meta.env.VITE_FIREBASE_STORAGE_BUCKET,
  messagingSenderId: import.meta.env.VITE_FIREBASE_MESSAGING_SENDER_ID,
  appId: import.meta.env.VITE_FIREBASE_APP_ID,
}

const app = initializeApp(firebaseConfig)
export const auth = getAuth(app)

// One singleton auth instance; each component's useAuth() call sets
// up its own listener against it and they all update in lockstep — no
// Context needed for the handful of consumers this app has.
export function useAuth() {
  const [user, setUser] = useState(auth.currentUser)
  const [loading, setLoading] = useState(auth.currentUser === null)
  useEffect(() => onAuthStateChanged(auth, (u) => { setUser(u); setLoading(false) }), [])
  return { user, loading }
}

export const signInEmail = (email, password) => signInWithEmailAndPassword(auth, email, password)
export const signUpEmail = (email, password) => createUserWithEmailAndPassword(auth, email, password)
export const signOutUser = () => signOut(auth)

// The SDK handles caching/refresh internally, so this is safe to call
// on every request rather than bookkeeping a cached token ourselves.
export const getIdToken = () => (auth.currentUser ? auth.currentUser.getIdToken() : Promise.resolve(null))
```

Only Email/Password is wired up — CLAUDE.md's stated reason is that OAuth's redirect flow needs a real domain and TLS, which this single-user local deployment deliberately doesn't have yet. `AuthControl.jsx` is the topbar's sign-in surface: a bare "sign in" button when signed out, expanding into a small form that toggles between sign-in and create-account modes, and collapsing to an email address plus "sign out" once authenticated:

```jsx
// frontend/src/lib/AuthControl.jsx:19-26
if (user) {
  return (
    <div className="auth-control row">
      <span className="auth-email" title={user.uid}>{user.email}</span>
      <button className="linkish" onClick={signOutUser}>sign out</button>
    </div>
  )
}
```

Every API call goes through a single `authorizedFetch` wrapper in `api.js` that attaches a bearer token when signed in and adds nothing at all when anonymous:

```js
// frontend/src/api.js:12-20
// Every request goes through this — attaches Authorization when
// signed in, adds nothing when not. Anonymous requests stay byte-
// identical to what they were before auth existed: no header at all.
async function authorizedFetch(path, options = {}) {
  const token = await getIdToken()
  const headers = new Headers(options.headers || {})
  if (token) headers.set('Authorization', `Bearer ${token}`)
  return fetch(path, { ...options, headers })
}
```

Auth state is what gates the personal library. `App.jsx` only renders the `Mine` and `Profile` nav links when `user` is truthy (`App.jsx:64-76`); `Library` itself checks `mine && !authLoading && !user` to show a "sign in to see your personal library" placeholder instead of an empty grid or an error (`signedOut`, `Library.jsx:136, 206-208`), and deliberately waits out `authLoading` before firing its `listRules` request (`if (mine && authLoading) return // wait for auth state before asking`, `Library.jsx:140`) so a signed-in user's first paint of `#/mine` doesn't flash "sign in" before the auth listener has resolved.

## 9. Recent feature work — three case studies

### Real clipboard copy

The run player's "copy tick link" button (`copyTickLink`, `RunView.jsx:415-425`) calls a shared helper, `frontend/src/lib/clipboard.js`, rather than `navigator.clipboard.writeText` directly. The comment explains exactly what naive approach it replaces:

```js
// frontend/src/lib/clipboard.js:1-30
// navigator.clipboard.writeText silently rejects in a lot of ordinary
// situations -- an insecure context, a permissions policy that denies
// clipboard-write, an iframe without the right allow list -- and the
// old copy-link button swallowed that rejection, so all it visibly did
// was change the URL bar. This tries the modern API first and falls
// back to the old execCommand('copy') trick (a hidden, off-screen
// textarea, selected and copied synchronously) before giving up.
export async function copyText(text) {
  try {
    await navigator.clipboard.writeText(text)
    return true
  } catch {
    // fall through to the legacy path below
  }
  try {
    const area = document.createElement('textarea')
    area.value = text
    area.style.position = 'fixed'
    area.style.top = '-1000px'
    area.style.left = '-1000px'
    document.body.appendChild(area)
    area.focus()
    area.select()
    const ok = document.execCommand('copy')
    document.body.removeChild(area)
    return ok
  } catch {
    return false
  }
}
```

The old approach was: call `navigator.clipboard.writeText`, and — because nothing awaited or checked its result — the button appeared to succeed (the URL bar hash changed) even when the clipboard write silently failed, which the comment says happens "in a lot of ordinary situations." `copyText` is "real" in the sense that it (a) awaits the modern Clipboard API and treats a rejection as a real failure rather than an unhandled promise, (b) falls back to the legacy `execCommand('copy')` trick — creating an off-screen `<textarea>`, focusing and selecting it, and issuing a synchronous copy command — when the modern API isn't available or is denied, and (c) returns a genuine boolean the caller can act on. `copyTickLink` only shows the "✓ copied" state when `copyText` actually returns `true`:

```jsx
// frontend/src/views/RunView.jsx:415-425
const copyTickLink = async () => {
  const url = `${window.location.origin}${window.location.pathname}#/runs/${runId}?tick=${tick}`
  window.location.hash = `/runs/${runId}?tick=${tick}`
  if (await copyText(url)) {
    setLinkCopied(true)
    setTimeout(() => setLinkCopied(false), 1500)
  }
  // If both copy paths fail (clipboard permission denied, no
  // execCommand support), the URL bar itself still reflects the
  // link — but the button no longer silently claims success.
}
```

### Robust downloads

Two independent things make `RunView`'s downloads (the PNG frame export and the full JSON run export) "robust." First, a shared `downloadBlobUrl` helper solves a real cross-browser correctness bug rather than just wrapping `element.click()`:

```jsx
// frontend/src/views/RunView.jsx:14-26
// Some browsers (older Safari in particular) never fire the download
// if the triggering <a> isn't attached to the document when .click()
// runs -- it silently no-ops instead of erroring, which reads exactly
// like "the button doesn't do anything." Attaching then detaching
// fixes it everywhere without changing behavior where it already worked.
function downloadBlobUrl(url, filename) {
  const a = document.createElement('a')
  a.href = url
  a.download = filename
  document.body.appendChild(a)
  a.click()
  document.body.removeChild(a)
}
```

An `<a download>` created but never inserted into the DOM is, on some browsers, a no-op click — exactly the "the button doesn't do anything" failure mode the comment names. Attaching the element before `.click()` and removing it immediately after fixes that universally.

Second, the full-run JSON export wraps its `fetch` in error handling that surfaces failures in the UI instead of letting them vanish into a rejected promise, and only creates/revokes the object URL inside a `try/finally` so a failed fetch never leaves a dangling blob URL or a stuck "fetching…" button:

```jsx
// frontend/src/views/RunView.jsx:468-483
// The lazy-loaded "enormous thing": every tick, uncapped, as a
// downloaded JSON file — not fetched until asked for.
const exportFull = async () => {
  setExporting(true)
  setExportError(null)
  try {
    const blob = await exportRun(runId, ['kind', ...rule.uses])
    const url = URL.createObjectURL(blob)
    downloadBlobUrl(url, `run-${runId}-export.json`)
    URL.revokeObjectURL(url)
  } catch (err) {
    setExportError(String(err))
  } finally {
    setExporting(false)
  }
}
```

`exportRun` in `api.js` (`api.js:109-113`) deliberately returns a `Blob` rather than parsing the response as JSON — the comment there notes a full run export "can be tens of MB and the browser has no reason to hold it as a JS object" — so the export path never materializes a giant parsed structure in memory just to immediately hand it back off as a file.

### The Mine-vs-Library nav highlight fix

The bug (named directly in the commit log: "Fix: viewing a rule from Mine wrongly lit up the Library nav tab") was that opening a rule or run reached via `#/mine` would highlight the `Library` tab in the top nav instead of `Mine`, because `RuleView`/`RunView` don't know or care which library they were opened from — there is only one `#/rules/:id` and one `#/runs/:id` route regardless of origin.

The fix threads a `?from=mine` query parameter through every link a `RuleCard` produces when it's being rendered inside the personal library:

```jsx
// frontend/src/views/Library.jsx:24-36
function RuleCard({ rule, hidden, onToggleHidden, signedIn, onFavoriteChange, mine, modifierBlurbs }) {
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
```

`parseRoute()` already captured `params.get('from')` into the route object for both `run` and `rule` views (`App.jsx:26, 29-30`); the nav bar's active-class logic then checks that flag instead of only the route name:

```jsx
// frontend/src/App.jsx:54-71
<a
  href="#/library"
  className={route.view === 'library' || (['run', 'rule'].includes(route.view) && route.from !== 'mine') ? 'active' : ''}
>
  Library
</a>
{user && (
  <a
    href="#/mine"
    className={route.view === 'mine' || (['run', 'rule'].includes(route.view) && route.from === 'mine') ? 'active' : ''}
  >
    Mine
  </a>
)}
```

So a `run`/`rule` view lights up `Library` unless its route carries `from === 'mine'`, in which case it lights up `Mine` instead — and the global `Library` (rendered without the `mine` prop) never sets `fromMine` at all, so every link it produces is bare and continues to light up `Library` exactly as before the fix.

### RSS feed and pagination default (context)

Two smaller items from the same commit round out the picture of the frontend/backend seam. The footer links to a plain RSS 2.0 feed of newly invented public rules — `<a href="/library/feed.rss" target="_blank" rel="noopener noreferrer">RSS — watch the library grow</a>` (`App.jsx:99`) — served by the backend at `GET /library/feed.rss` (`backend/asr/api/routes.py:726-749`, capped at the 30 most recent public rules, `MOST_RSS_ITEMS = 30`); the frontend does nothing more than link to it, since RSS is consumed by an external reader, not rendered in-app. And the `page_size: int = Query(24, ge=1, le=200)` default discussed in §5 (`backend/asr/api/routes.py:189`) is what the frontend's pager silently inherits — there is no frontend-side page-size control or override.

## 10. The System view (new in 2.2.1)

`frontend/src/views/SystemView.jsx` (167 lines) renders `#/system` from the two routes in document 5, §11. It is the app's only polling view: a single `useEffect` fetches both endpoints every two seconds (`POLL_MS = 2000`, `SystemView.jsx:4`), with a `cancelled` flag guarding against a late response landing after unmount and the interval cleared on teardown (`SystemView.jsx:63-72`).

### The pipeline map

The page's centerpiece is a four-node process map — Stage A (describe) → Stage B (implement) → Stage C (validate) → Library (stored) — with any in-flight generation shown pulsing on the node it currently occupies. The mapping from event name to node is a plain lookup table (`SystemView.jsx:9-19`):

```jsx
// Which pipeline node a generation session's last-seen stage belongs to.
// validation_failed/repairing fold into Stage C -- a repair is still the
// harness working on the same implementation, not a new stage.
const STAGE_NODE = {
  stage_a_started: 0, stage_a_complete: 0,
  stage_b_started: 1, stage_b_complete: 1,
  validating: 2, validation_failed: 2, repairing: 2, running: 2,
}
```

Two modelling decisions are embedded there. `validation_failed` and `repairing` fold into Stage C rather than getting nodes of their own, on the grounds that a repair attempt is still the harness working on the same implementation — which matches how the pipeline itself treats the one permitted repair (document 4). And `running` — the canonical run — also folds into Stage C, since from the pipeline's perspective the trial execution is part of validating that the rule works. An unrecognized stage falls back to node 2 (`STAGE_NODE[session.stage] ?? 2`, `SystemView.jsx:79`) rather than disappearing from the map.

The pulse itself is CSS, not JavaScript: `.pipeline-node.active` runs a `pipeline-pulse` keyframe animation (`index.css`), so an in-flight generation animates without the two-second poll driving any per-frame work.

### The session table

Below the map, the merged session list renders with columns for kind, who, IP, User-Agent, started, last active, request count, and last path. Three small presentation decisions are worth noting because each avoids a worse alternative:

- **`who` is `user` or `guest`,** never an identifier — the frontend never receives `owner_uid` at all, because the backend already reduced it to a boolean (document 5, §11).
- **User-Agent strings are truncated to 28 characters with the full value on hover** (`shortUserAgent`, `SystemView.jsx:52-55`). The comment gives the reasoning: a short identifiable prefix with the whole string in a `title` beats either truncating badly or "writing a whole UA parser for a debug table."
- **`outcomeLabel` (`SystemView.jsx:41-47`) resolves the two session kinds to one column.** An HTTP session shows its last path; a generation shows `running`, `stored as rule #N`, `rejected — <error>`, or `generation failed` — which is `generation_sessions.outcome`'s three values plus the in-flight case, rendered in plain language per REQ-0.1.

An `in_flight` count also drives the header line, which reads either `N generations in flight` (correctly singular at one) or `idle`, followed by process uptime.

---

## 11. Build and dev tooling

`npm run dev` (`package.json:7`) starts the Vite dev server. Vite's proxy config forwards the path prefixes the frontend talks to on the FastAPI backend, so `fetch('/rules?...')` et al. resolve against `localhost:8000` in dev without any CORS configuration or absolute URLs baked into `api.js`. **All three of the settings below were changed in 2.2.1, each fixing a real failure:**

```js
// frontend/vite.config.js:1-28
import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

const backend = 'http://localhost:8000'

// xfwd: true makes the proxy add X-Forwarded-For (and X-Forwarded-Port)
// with the real browser's address -- without it, every request the
// backend sees comes from this proxy's own outbound connection, i.e.
// 127.0.0.1 for everyone, which is what api/app.py's session tracking
// was silently recording until this was added.
const proxied = { target: backend, xfwd: true }

// https://vite.dev/config/
export default defineConfig({
  plugins: [react()],
  server: {
    host: true,
    proxy: {
      '/rules': proxied,
      '/runs': proxied,
      '/catalog': proxied,
      '/library': proxied,
      '/system': proxied,
      '/profile': proxied,
      '/comments': proxied,
    },
  },
})
```

**The missing prefixes were a silent bug, and the shape of it is worth remembering.** `/profile` and `/comments` had backend routes and frontend code calling them, but no proxy entry — so in dev those requests fell through to the Vite dev server itself, which knows nothing about them. Sign-in profile edits and comment edit/delete were broken in development only, in a way that looked like frontend bugs. `CLAUDE.md` now carries the standing warning this produced: watch for the gap again whenever a new top-level route is added to the backend. `/system` was added to the same list when the system page landed.

**`host: true`** binds the dev server to `0.0.0.0` instead of Vite's loopback-only default. This droplet is reached by external IP, and a loopback bind is simply unreachable from outside — a dev server that is "running fine" and completely inaccessible. The diagnostic recorded in `CLAUDE.md` is to check `ss -tlnp | grep 5173` for a loopback-only bind before suspecting anything else.

**`xfwd: true`** is the frontend half of the client-IP fix documented in document 5, §10. Without it the backend's session tracking recorded `127.0.0.1` for every visitor, since the proxy makes its own outbound connection; with it, `X-Forwarded-For` carries the real address for `_client_ip` to prefer.

Note that `/rules/generate`'s streaming response and `/runs/{id}/grids`'s binary payload both pass through this same proxy unmodified — Vite's proxy is a raw pass-through, so neither the SSE framing nor the binary grid framing needs special-casing in dev versus a production deployment where the frontend build is served separately from the API.

`npm run build` (`package.json:8`) runs `vite build` — a standard static production build with no server-side rendering step; `dist/` (present in the repo tree as a build artifact) contains a single bundled JS entry, a single CSS file, and `index.html`.

`npm run lint` (`package.json:9`) runs `oxlint`, configured minimally in `.oxlintrc.json`:

```json
// frontend/.oxlintrc.json
{
  "$schema": "./node_modules/oxlint/configuration_schema.json",
  "plugins": ["react", "oxc"],
  "rules": {
    "react/rules-of-hooks": "error",
    "react/only-export-components": ["warn", { "allowConstantExport": true }]
  }
}
```

Two rules are configured explicitly: `react/rules-of-hooks` as a hard error (catching conditional or out-of-order hook calls — meaningful given how much of this codebase leans on `useState`/`useEffect`/`useMemo`/`useCallback` combinations, especially in `RunView.jsx`), and `react/only-export-components` as a warning permitting constant exports alongside components (needed because files like `lib/AuthControl.jsx` and `lib/Comments.jsx` export both a component and, in other files, plain constants/hooks from the same module). Everything else oxlint offers runs at its plugin defaults.

Dependencies are intentionally small: React 19, the `firebase` modular SDK, and two self-hosted variable-font packages (`@fontsource-variable/inter`, `@fontsource-variable/jetbrains-mono`) are the only runtime dependencies (`package.json:12-18`); there is no state-management library, no router library, no UI component library, and no CSS framework — every visual and behavioral pattern documented above is hand-written specifically for this app.
