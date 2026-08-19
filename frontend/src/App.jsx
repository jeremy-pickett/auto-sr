import { useEffect, useState } from 'react'
import Landing from './views/Landing.jsx'
import Library from './views/Library.jsx'
import RunView from './views/RunView.jsx'
import RuleView from './views/RuleView.jsx'
import Catalog from './views/Catalog.jsx'
import Invent from './views/Invent.jsx'
import { AuthControl } from './lib/AuthControl.jsx'
import { useAuth } from './lib/firebase'

// Tiny hash router: #/ (landing), #/library, #/mine, #/runs/3,
// #/rules/3, #/invent, #/catalog
function parseRoute() {
  const hash = window.location.hash.replace(/^#\/?/, '')
  const [head, id] = hash.split('/')
  if (head === 'library') return { view: 'library' }
  if (head === 'mine') return { view: 'mine' }
  if (head === 'runs' && id) return { view: 'run', id: Number(id) }
  if (head === 'rules' && id) return { view: 'rule', id: Number(id) }
  if (head === 'invent') return { view: 'invent' }
  if (head === 'catalog') return { view: 'catalog' }
  return { view: 'landing' }
}

export default function App() {
  const [route, setRoute] = useState(parseRoute)
  const { user } = useAuth()

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
          <a href="#/library" className={['library', 'run', 'rule'].includes(route.view) ? 'active' : ''}>Library</a>
          {user && <a href="#/mine" className={route.view === 'mine' ? 'active' : ''}>Mine</a>}
          <a href="#/invent" className={route.view === 'invent' ? 'active' : ''}>Invent</a>
          <a href="#/catalog" className={route.view === 'catalog' ? 'active' : ''}>Modifiers</a>
        </nav>
        <span className="spacer" />
        <AuthControl />
      </header>

      <main className="page">
        {route.view === 'landing' && <Landing />}
        {route.view === 'library' && <Library />}
        {route.view === 'mine' && <Library mine />}
        {route.view === 'run' && <RunView runId={route.id} />}
        {route.view === 'rule' && <RuleView ruleId={route.id} />}
        {route.view === 'invent' && <Invent />}
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
