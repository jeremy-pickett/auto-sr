import { useEffect, useState } from 'react'
import Library from './views/Library.jsx'
import RunView from './views/RunView.jsx'
import Catalog from './views/Catalog.jsx'

// Tiny hash router: #/ (library), #/runs/3, #/catalog
function parseRoute() {
  const hash = window.location.hash.replace(/^#\/?/, '')
  const [head, id] = hash.split('/')
  if (head === 'runs' && id) return { view: 'run', id: Number(id) }
  if (head === 'catalog') return { view: 'catalog' }
  return { view: 'library' }
}

export default function App() {
  const [route, setRoute] = useState(parseRoute)

  useEffect(() => {
    const onChange = () => setRoute(parseRoute())
    window.addEventListener('hashchange', onChange)
    return () => window.removeEventListener('hashchange', onChange)
  }, [])

  return (
    <>
      <header className="topbar">
        <a href="#/" className="wordmark" style={{ textDecoration: 'none' }}>
          <span className="pip" />
          Autonomous Semantic Ruliology
        </a>
        <nav>
          <a href="#/" className={route.view !== 'catalog' ? 'active' : ''}>Library</a>
          <a href="#/catalog" className={route.view === 'catalog' ? 'active' : ''}>Modifiers</a>
        </nav>
        <span className="spacer" />
      </header>

      <main className="page">
        {route.view === 'library' && <Library />}
        {route.view === 'run' && <RunView runId={route.id} />}
        {route.view === 'catalog' && <Catalog />}
      </main>

      <footer className="footer">
        <span>
          Inspired by Stephen Wolfram's work on cellular automata — not a
          reproduction of it, and claiming no coverage of any rule space.
        </span>
        <span>rules are invented by a machine; the library is the product</span>
      </footer>
    </>
  )
}
