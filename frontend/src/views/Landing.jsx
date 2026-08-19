import { useEffect, useRef, useState } from 'react'
import { getSummary } from '../api'

// The hero runs a real one-dimensional automaton (rule 30 — the
// classic one) live in the browser: one lit cell, three-neighbor
// lookups, rows marching down the screen. The landing page opens on
// an actual computation, not a screenshot of one.
function LiveAutomaton() {
  const ref = useRef(null)

  useEffect(() => {
    const canvas = ref.current
    const width = 320
    const height = 150
    canvas.width = width
    canvas.height = height
    const ctx = canvas.getContext('2d')
    ctx.fillStyle = '#0a0e14'
    ctx.fillRect(0, 0, width, height)

    let cells = new Uint8Array(width)
    cells[width >> 1] = 1
    let y = 0

    const stampRow = () => {
      const row = ctx.createImageData(width, 1)
      for (let x = 0; x < width; x++) {
        const on = cells[x] === 1
        row.data[x * 4] = on ? 76 : 10
        row.data[x * 4 + 1] = on ? 201 : 14
        row.data[x * 4 + 2] = on ? 240 : 20
        row.data[x * 4 + 3] = 255
      }
      if (y < height) {
        ctx.putImageData(row, 0, y)
        y += 1
      } else {
        ctx.drawImage(canvas, 0, 1, width, height - 1, 0, 0, width, height - 1)
        ctx.putImageData(row, 0, height - 1)
      }
      const next = new Uint8Array(width)
      for (let x = 0; x < width; x++) {
        // edges wrap left to right
        const left = cells[(x + width - 1) % width]
        const right = cells[(x + 1) % width]
        next[x] = left ^ (cells[x] | right)
      }
      cells = next
    }

    if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) {
      for (let i = 0; i < height; i++) stampRow()
      return undefined
    }
    let raf
    let last = 0
    const loop = (t) => {
      if (t - last > 33) {
        stampRow()
        last = t
      }
      raf = requestAnimationFrame(loop)
    }
    raf = requestAnimationFrame(loop)
    return () => cancelAnimationFrame(raf)
  }, [])

  return <canvas ref={ref} className="hero-automaton" aria-hidden="true" />
}

function Stats() {
  const [totals, setTotals] = useState(null)
  useEffect(() => {
    getSummary().then((s) => setTotals(s.totals), () => {})
  }, [])
  if (!totals || !totals.rules) return null
  const classified = Object.values(totals.behaviors || {}).reduce((a, b) => a + b, 0)
  return (
    <div className="hero-stats">
      <span><strong>{totals.rules}</strong> rules invented so far</span>
      <span><strong>{classified}</strong> run to completion and shelved</span>
      <span><strong>{totals.broken}</strong> kept even though they broke</span>
    </div>
  )
}

export default function Landing() {
  return (
    <div className="landing">
      <section className="hero">
        <LiveAutomaton />
        <div className="hero-copy">
          <p className="eyebrow">an autonomous laboratory</p>
          <h1>
            A machine invents the rules.
            <br />
            Running them is the only way to find out.
          </h1>
          <p className="lead">
            This is a laboratory where an AI dreams up rules for tiny grid
            worlds — a few kinds of cell, a few sentences of instruction — and
            a harness runs every one to see what actually happens. Some
            settle. Some fall into loops. Some erupt into patterns nobody
            designed. All of them are kept.
          </p>
          <div className="hero-actions">
            <a href="#/library"><button className="primary">Enter the library</button></a>
            <a href="#/invent"><button>Watch a rule being invented</button></a>
          </div>
          <Stats />
        </div>
      </section>

      <section className="landing-section">
        <h2>What is computation, anyway?</h2>
        <div className="two-col">
          <div>
            <p>
              Strip away the machinery and computation is just this: state a
              rule, follow it, and see what happens. The rule running live
              above this paragraph fits in one sentence — each cell looks at
              itself and its two neighbors, then a tiny table says whether it
              lights up next.
            </p>
            <p>
              The surprise — one of the strangest facts anyone has noticed —
              is that rules this simple can produce behavior as complicated
              as anything in nature. You cannot tell by reading the rule.
              There is no formula that jumps ahead to the answer. The only
              way to know what a rule does is to run it and watch.
            </p>
          </div>
          <blockquote className="telescope">
            <p>
              “It's kind of like you get to take the computer like a
              telescope, turn it at the sky and see what you see.”
            </p>
            <footer>
              — Stephen Wolfram, whose <em>ruliology</em> — his word for the
              study of simple rules and their consequences — inspired this
              project. From{' '}
              <a href="https://www.youtube.com/watch?v=5_O-kSzWdu4" target="_blank" rel="noopener noreferrer">
                the interview
              </a>{' '}
              that started it.
            </footer>
          </blockquote>
        </div>
      </section>

      <section className="landing-section">
        <h2>What happens here</h2>
        <div className="step-cards">
          <div className="step-card">
            <span className="step-num">1</span>
            <h3>The machine invents</h3>
            <p>
              A language model studies a map of what the library already
              holds, finds an empty corner, and describes a brand-new rule in
              plain English. Then it writes the code to match its own
              description.
            </p>
          </div>
          <div className="step-card">
            <span className="step-num">2</span>
            <h3>The harness runs it</h3>
            <p>
              Every rule is checked, run to completion, and recorded tick by
              tick — same seed, same result, forever. The harness decides
              when a world has truly frozen or fallen into a loop. A quiet
              picture is never enough to stop a run.
            </p>
          </div>
          <div className="step-card">
            <span className="step-num">3</span>
            <h3>Everything is kept</h3>
            <p>
              Brilliant, boring, or broken — every attempt goes on the shelf
              with its full history: what the machine intended, what it
              wrote, and what actually happened. The failures teach the next
              invention. The library is the product.
            </p>
          </div>
        </div>
      </section>

      <section className="landing-section">
        <h2>What you're in for</h2>
        <div className="honest-note">
          <p>
            Fair warning: most of what a machine invents is gray soup or
            instant death. Every so often, something crawls, or breathes, or
            builds. The duds stay on the shelf next to the gems, because
            that's what exploring actually looks like — and because a machine
            that never sees its failures keeps making them.
          </p>
          <p>
            So browse the library like a telescope log, not a highlight reel.
            The interesting question is never “is this one pretty?” It's
            “nobody has ever watched this rule run before — what does it do?”
          </p>
        </div>
      </section>

      <p className="attribution">
        This project is inspired by Stephen Wolfram's work on simple programs
        and cellular automata. It is not affiliated with or endorsed by him
        or Wolfram Research, reproduces none of his work, and claims no
        coverage of any rule space — it simply points the telescope and keeps
        an honest log.
      </p>
    </div>
  )
}
