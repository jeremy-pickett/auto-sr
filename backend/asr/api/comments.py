"""Comments on rules (documents/new-features-v1.md). Scoped
deliberately: create, edit-own, delete-own, and a simple rate limit --
NOT a report/moderation queue, since no admin or moderator role exists
anywhere in this app for one to feed. Logged in documents/
feature-run-log.md before this was written.

Author display is a deliberately generated pseudonym, never the
signed-in user's email -- the same privacy reasoning that ruled out
"author attribution" on rules applies here: publishing a login email
next to public commentary is not a call this pass makes unilaterally.
The pseudonym is a deterministic function of the Firebase uid, so the
same person's comments consistently show the same name without ever
exposing what that name is derived from. A user can override it with
a self-chosen display name via asr/api/profile.py; that override, not
the email, is the only other thing ever shown here.
"""

import hashlib
import time

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field

from asr.api.auth import get_current_user
from asr.api.profile import get_display_name
from asr.api.routes import _rule_hidden_from, get_db
from asr.storage import db

router = APIRouter()

COMMENT_MAX_LENGTH = 1000

_ADJECTIVES = (
    "cyan", "amber", "quiet", "restless", "settled", "noisy", "structured",
    "wraparound", "toroidal", "recursive", "fractal", "parity", "drifting",
)
_NOUNS = (
    "observer", "spark", "cell", "lattice", "automaton", "watcher",
    "signal", "pattern", "horizon", "loop", "seed", "kernel",
)


def pseudonym(uid: str) -> str:
    digest = hashlib.blake2b(uid.encode(), digest_size=4).digest()
    n = int.from_bytes(digest, "big")
    adjective = _ADJECTIVES[n % len(_ADJECTIVES)]
    noun = _NOUNS[(n // len(_ADJECTIVES)) % len(_NOUNS)]
    return f"{adjective}-{noun}-{n % 1000:03d}"


# In-memory, per-process -- fine for this single-node app, would need
# a shared store (e.g. the database itself) if this ever runs as
# multiple worker processes. 5 comments per rolling 60 seconds.
_RATE_LIMIT = 5
_RATE_WINDOW_SECONDS = 60
_recent_comments: dict[str, list[float]] = {}


def _check_rate_limit(uid: str) -> None:
    now = time.monotonic()
    history = [t for t in _recent_comments.get(uid, []) if now - t < _RATE_WINDOW_SECONDS]
    if len(history) >= _RATE_LIMIT:
        raise HTTPException(429, f"at most {_RATE_LIMIT} comments per minute -- slow down")
    history.append(now)
    _recent_comments[uid] = history


def clean_comment(text: str) -> str:
    """Unlike spark (single-line, 64 chars), comments are ordinary
    multi-line prose -- newlines are kept, only non-printable/control
    and bidi-override characters are stripped (same reasoning as
    clean_spark: a comment shouldn't be able to visually lie about its
    own contents), and blank-line runs are collapsed so a wall of
    empty lines can't be used to bury other comments off-screen.
    """
    lines = [
        "".join(c for c in line if c.isprintable())
        for line in text.replace("\r\n", "\n").split("\n")
    ]
    cleaned = "\n".join(lines).strip()
    while "\n\n\n" in cleaned:
        cleaned = cleaned.replace("\n\n\n", "\n\n")
    return cleaned


class CommentBody(BaseModel):
    body: str = Field(min_length=1, max_length=COMMENT_MAX_LENGTH)


def _comment_row(conn, row, user) -> dict:
    return {
        "id": row["id"],
        "rule_id": row["rule_id"],
        "author": get_display_name(conn, row["user_uid"]) or pseudonym(row["user_uid"]),
        "body": row["body"],
        "created_at": row["created_at"],
        "edited_at": row["edited_at"],
        "mine": bool(user) and user["uid"] == row["user_uid"],
    }


@router.get("/rules/{rule_id}/comments")
def list_comments(rule_id: int, user: dict | None = Depends(get_current_user), conn=Depends(get_db)):
    row = conn.execute("SELECT visibility, owner_uid FROM rules WHERE id = ?", (rule_id,)).fetchone()
    if row is None or _rule_hidden_from(row["visibility"], row["owner_uid"], user):
        raise HTTPException(404, "no such rule")
    rows = conn.execute(
        "SELECT * FROM comments WHERE rule_id = ? ORDER BY id", (rule_id,)
    ).fetchall()
    return {"comments": [_comment_row(conn, r, user) for r in rows]}


@router.post("/rules/{rule_id}/comments")
def create_comment(
    rule_id: int, body: CommentBody,
    user: dict | None = Depends(get_current_user), conn=Depends(get_db),
):
    if user is None:
        raise HTTPException(401, "sign in to comment")
    row = conn.execute("SELECT visibility, owner_uid FROM rules WHERE id = ?", (rule_id,)).fetchone()
    if row is None or _rule_hidden_from(row["visibility"], row["owner_uid"], user):
        raise HTTPException(404, "no such rule")
    cleaned = clean_comment(body.body)
    if not cleaned:
        raise HTTPException(400, "comment is empty")
    _check_rate_limit(user["uid"])
    cursor = conn.execute(
        "INSERT INTO comments(rule_id, user_uid, body, created_at) VALUES(?,?,?,?)",
        (rule_id, user["uid"], cleaned, db.now()),
    )
    conn.commit()
    fresh = conn.execute("SELECT * FROM comments WHERE id = ?", (cursor.lastrowid,)).fetchone()
    return _comment_row(conn, fresh, user)


@router.patch("/comments/{comment_id}")
def edit_comment(
    comment_id: int, body: CommentBody,
    user: dict | None = Depends(get_current_user), conn=Depends(get_db),
):
    if user is None:
        raise HTTPException(401, "sign in to edit a comment")
    row = conn.execute("SELECT * FROM comments WHERE id = ?", (comment_id,)).fetchone()
    if row is None:
        raise HTTPException(404, "no such comment")
    if row["user_uid"] != user["uid"]:
        raise HTTPException(403, "you can only edit your own comments")
    cleaned = clean_comment(body.body)
    if not cleaned:
        raise HTTPException(400, "comment is empty")
    conn.execute(
        "UPDATE comments SET body = ?, edited_at = ? WHERE id = ?",
        (cleaned, db.now(), comment_id),
    )
    conn.commit()
    fresh = conn.execute("SELECT * FROM comments WHERE id = ?", (comment_id,)).fetchone()
    return _comment_row(conn, fresh, user)


@router.delete("/comments/{comment_id}")
def delete_comment(
    comment_id: int, user: dict | None = Depends(get_current_user), conn=Depends(get_db),
):
    if user is None:
        raise HTTPException(401, "sign in to delete a comment")
    row = conn.execute("SELECT * FROM comments WHERE id = ?", (comment_id,)).fetchone()
    if row is None:
        return {"deleted": True}  # already gone; deleting is idempotent
    if row["user_uid"] != user["uid"]:
        raise HTTPException(403, "you can only delete your own comments")
    conn.execute("DELETE FROM comments WHERE id = ?", (comment_id,))
    conn.commit()
    return {"deleted": True}
