import { useEffect, useState } from 'react'
import Landing from './views/Landing.jsx'
import Library from './views/Library.jsx'
import RunView from './views/RunView.jsx'
import RuleView from './views/RuleView.jsx'
import Catalog from './views/Catalog.jsx'
import Invent from './views/Invent.jsx'
import Profile from './views/Profile.jsx'
import { AuthControl } from './lib/AuthControl.jsx'
import { useAuth } from './lib/firebase'

// Tiny hash router: #/ (landing), #/library, #/mine, #/runs/3,
// #/runs/3?tick=150 (a permalink to a specific tick), #/rules/3,
// #/r/:slug (a titled rule's clean URL), #/invent, #/catalog
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
          {/* A rule/run reached from Mine carries ?from=mine (see
              RuleCard in Library.jsx) so it doesn't wrongly light up
              Library instead of the section you actually came from. */}
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
          <a href="#/invent" className={route.view === 'invent' ? 'active' : ''}>Invent</a>
          <a href="#/catalog" className={route.view === 'catalog' ? 'active' : ''}>Modifiers</a>
          {user && (
            <a href="#/profile" className={route.view === 'profile' ? 'active' : ''}>Profile</a>
          )}
        </nav>
        <span className="spacer" />
        <AuthControl />
      </header>

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

      <footer className="footer">
        <span>
          Inspired by Stephen Wolfram's work on cellular automata — not a
          reproduction of it, and claiming no coverage of any rule space.
        </span>
        <span>rules are invented by a machine; the library is the product</span>
        <a href="/library/feed.rss" target="_blank" rel="noopener noreferrer">RSS — watch the library grow</a>
      </footer>
    </>
  )
}
