import { useEffect, useState } from 'react'
import { getComments, createComment, editComment, deleteComment } from '../api'
import { useAuth } from './firebase'

const MAX_LENGTH = 1000

function timeAgo(iso) {
  const seconds = Math.max(0, (Date.now() - new Date(iso).getTime()) / 1000)
  if (seconds < 60) return 'just now'
  if (seconds < 3600) return `${Math.floor(seconds / 60)}m ago`
  if (seconds < 86400) return `${Math.floor(seconds / 3600)}h ago`
  return `${Math.floor(seconds / 86400)}d ago`
}

function CommentRow({ comment, onChanged }) {
  const [editing, setEditing] = useState(false)
  const [draft, setDraft] = useState(comment.body)
  const [busy, setBusy] = useState(false)
  const [error, setError] = useState(null)

  const save = async () => {
    setBusy(true)
    setError(null)
    try {
      const fresh = await editComment(comment.id, draft)
      onChanged(fresh)
      setEditing(false)
    } catch (bad) {
      setError(String(bad))
    } finally {
      setBusy(false)
    }
  }

  const remove = async () => {
    setBusy(true)
    try {
      await deleteComment(comment.id)
      onChanged(null, comment.id)
    } catch (bad) {
      setError(String(bad))
      setBusy(false)
    }
  }

  return (
    <div className="comment-row">
      <div className="comment-head">
        <span className="comment-author">{comment.author}</span>
        <span className="sub">
          {timeAgo(comment.created_at)}{comment.edited_at ? ' · edited' : ''}
        </span>
        {comment.mine && !editing && (
          <span className="row" style={{ gap: 6, marginLeft: 'auto' }}>
            <button className="linkish" onClick={() => setEditing(true)}>edit</button>
            <button className="linkish" onClick={remove} disabled={busy}>delete</button>
          </span>
        )}
      </div>
      {editing ? (
        <div className="comment-edit">
          <textarea value={draft} maxLength={MAX_LENGTH} onChange={(e) => setDraft(e.target.value)} rows={3} />
          <div className="row" style={{ gap: 6 }}>
            <button className="primary" onClick={save} disabled={busy || !draft.trim()}>save</button>
            <button onClick={() => { setEditing(false); setDraft(comment.body) }} disabled={busy}>cancel</button>
          </div>
        </div>
      ) : (
        <div className="comment-body">{comment.body}</div>
      )}
      {error && <div className="error-note">{error}</div>}
    </div>
  )
}

export function Comments({ ruleId }) {
  const { user } = useAuth()
  const [comments, setComments] = useState(null)
  const [error, setError] = useState(null)
  const [draft, setDraft] = useState('')
  const [posting, setPosting] = useState(false)

  useEffect(() => {
    setComments(null)
    getComments(ruleId).then((d) => setComments(d.comments), setError)
  }, [ruleId])

  const onChanged = (fresh, deletedId) => {
    setComments((old) => {
      if (deletedId != null) return old.filter((c) => c.id !== deletedId)
      return old.map((c) => (c.id === fresh.id ? fresh : c))
    })
  }

  const post = async () => {
    setPosting(true)
    setError(null)
    try {
      const fresh = await createComment(ruleId, draft)
      setComments((old) => [...(old || []), fresh])
      setDraft('')
    } catch (bad) {
      setError(String(bad))
    } finally {
      setPosting(false)
    }
  }

  return (
    <div className="panel">
      <h3>comments{comments ? ` (${comments.length})` : ''}</h3>
      {error && <div className="error-note">{error}</div>}
      {!comments && !error && <div className="loading">loading comments…</div>}
      {comments && comments.length === 0 && <div className="hint">no comments yet</div>}
      {comments && comments.map((c) => (
        <CommentRow key={c.id} comment={c} onChanged={onChanged} />
      ))}
      {user ? (
        <div className="comment-new">
          <textarea
            value={draft}
            maxLength={MAX_LENGTH}
            onChange={(e) => setDraft(e.target.value)}
            placeholder="what do you make of this one?"
            rows={2}
          />
          <div className="row" style={{ justifyContent: 'space-between' }}>
            <span className="sub">{draft.length}/{MAX_LENGTH} · shown as {user ? 'a generated name, not your email' : ''}</span>
            <button className="primary" onClick={post} disabled={posting || !draft.trim()}>
              {posting ? 'posting…' : 'comment'}
            </button>
          </div>
        </div>
      ) : (
        <div className="hint">sign in to comment</div>
      )}
    </div>
  )
}
