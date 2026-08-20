import { useEffect, useState } from 'react'
import { getProfile, setDisplayName } from '../api'
import { useAuth } from '../lib/firebase'

// The one editable bit of public identity a signed-in user has: a
// display name that overrides their comment pseudonym everywhere it
// shows up. Deliberately just this one field -- see asr/api/profile.py
// for why there isn't more here.
export default function Profile() {
  const { user, loading: authLoading } = useAuth()
  const [profile, setProfile] = useState(null)
  const [draft, setDraft] = useState('')
  const [error, setError] = useState(null)
  const [saving, setSaving] = useState(false)
  const [saved, setSaved] = useState(false)

  useEffect(() => {
    if (!user) return
    getProfile().then((p) => { setProfile(p); setDraft(p.display_name || '') }, setError)
  }, [user])

  if (authLoading) return <div className="loading">loading…</div>
  if (!user) return <div className="error-note">sign in to view your profile</div>
  if (error) return <div className="error-note">something went wrong: {String(error)}</div>
  if (!profile) return <div className="loading">loading your profile…</div>

  const save = () => {
    setSaving(true)
    setError(null)
    setSaved(false)
    setDisplayName(draft).then((p) => {
      setProfile(p)
      setSaving(false)
      setSaved(true)
      setTimeout(() => setSaved(false), 1500)
    }, (err) => { setError(err); setSaving(false) })
  }

  return (
    <>
      <div className="library-head">
        <h1>Profile</h1>
        <span className="totals">the only thing to set is a display name for comments</span>
      </div>
      <div className="panel">
        <p className="hint">
          By default your comments show a pseudonym generated from your account
          (never your email). Set a display name here to use that instead —
          it shows up on every comment you've made or make from now on. Leave
          it blank to go back to the pseudonym.
        </p>
        <div className="row" style={{ marginTop: 12 }}>
          <input
            type="text"
            value={draft}
            onChange={(e) => setDraft(e.target.value)}
            placeholder={profile.display_name ? '' : 'pseudonym (no override set)'}
            maxLength={40}
          />
          <button onClick={save} disabled={saving}>{saving ? 'saving…' : 'save'}</button>
          {saved && <span className="hint">saved</span>}
        </div>
        {error && <div className="error-note" style={{ marginTop: 8 }}>{String(error)}</div>}
      </div>
    </>
  )
}
