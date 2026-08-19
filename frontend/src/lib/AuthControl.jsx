import { useState } from 'react'
import { useAuth, signInEmail, signUpEmail, signOutUser } from './firebase'

// The topbar's sign-in surface: a trigger when signed out, opening a
// small email+password form (sign-in/create-account toggle — Email/
// Password needs an explicit account, there's no magic link in scope
// yet); an email + sign-out control when signed in.
export function AuthControl() {
  const { user, loading } = useAuth()
  const [open, setOpen] = useState(false)
  const [mode, setMode] = useState('signin') // signin | signup
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [error, setError] = useState(null)
  const [busy, setBusy] = useState(false)

  if (loading) return null

  if (user) {
    return (
      <div className="auth-control row">
        <span className="auth-email" title={user.uid}>{user.email}</span>
        <button className="linkish" onClick={signOutUser}>sign out</button>
      </div>
    )
  }

  const submit = async (event) => {
    event.preventDefault()
    setBusy(true)
    setError(null)
    try {
      await (mode === 'signin' ? signInEmail(email, password) : signUpEmail(email, password))
      setOpen(false)
      setEmail('')
      setPassword('')
    } catch (failed) {
      setError(failed.message.replace(/^Firebase: /, ''))
    } finally {
      setBusy(false)
    }
  }

  if (!open) {
    return <button onClick={() => setOpen(true)}>sign in</button>
  }

  return (
    <form className="auth-form" onSubmit={submit}>
      <input
        type="email"
        placeholder="email"
        value={email}
        onChange={(e) => setEmail(e.target.value)}
        required
      />
      <input
        type="password"
        placeholder="password"
        value={password}
        onChange={(e) => setPassword(e.target.value)}
        required
      />
      <button type="submit" className="primary" disabled={busy}>
        {mode === 'signin' ? 'sign in' : 'create account'}
      </button>
      <button type="button" className="linkish" onClick={() => setMode(mode === 'signin' ? 'signup' : 'signin')}>
        {mode === 'signin' ? 'need an account?' : 'have an account?'}
      </button>
      <button type="button" className="linkish" onClick={() => setOpen(false)}>cancel</button>
      {error && <span className="auth-error">{error}</span>}
    </form>
  )
}
