import { useEffect, useState } from 'react'
import { getCatalog } from '../api'

// Read-only modifier catalog (REQ-13.9).
export default function Catalog() {
  const [modifiers, setModifiers] = useState(null)
  const [error, setError] = useState(null)

  useEffect(() => {
    getCatalog().then((data) => setModifiers(data.modifiers), setError)
  }, [])

  if (error) return <div className="error-note">could not load the catalog: {String(error)}</div>
  if (!modifiers) return <div className="loading">loading the catalog…</div>

  return (
    <>
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
    </>
  )
}
