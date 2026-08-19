import { useEffect, useRef } from 'react'
import { getGrids } from '../api'
import { plane } from './decode'
import { KIND_RGB } from './palette'

// Rendered final frames, kept for the session — a run's last tick is
// immutable history, so it never needs fetching twice.
const finalFrames = new Map()

// The rule's face: its run's last tick, straight from the stored
// history in the player's own palette. `className` controls size —
// callers set it (e.g. `.rule-thumb` for the library grid, a larger
// one for the invent done-note).
export function RunThumbnail({ run, className }) {
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
  return <canvas ref={canvasRef} className={className} title="how the run ended" />
}
