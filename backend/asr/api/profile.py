"""A signed-in user's one editable bit of public identity: an optional
display name that overrides their comment pseudonym everywhere it's
shown (documents/new-features-2.md, items 5 and 11 -- "i like the
anonymous name for comments, and we need to start building a profile
mechanism where people can change bits like that").

Deliberately narrow. This is not a profile page with a bio, an
avatar, or a history -- nothing asked for that, and there's no reason
to invent more surface than "a place to change the name." The only
identity Firebase gives this app is a login email, and publishing
that was already ruled out (documents/feature-run-log.md's "author
attribution" and comment-pseudonym decisions) -- this endpoint never
reads or returns it, and clearing the display name just falls back to
the same deterministic pseudonym everyone already gets.
"""

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field

from asr.api.auth import get_current_user
from asr.api.routes import get_db

router = APIRouter()

DISPLAY_NAME_MAX_LENGTH = 40


def clean_display_name(text: str) -> str:
    cleaned = "".join(c for c in text if c.isprintable()).strip()
    return " ".join(cleaned.split())  # collapse internal whitespace runs


class ProfileBody(BaseModel):
    display_name: str = Field(max_length=DISPLAY_NAME_MAX_LENGTH)


def get_display_name(conn, uid: str) -> str | None:
    """None means "no override set" -- caller falls back to the
    pseudonym. Used by comments.py so the two stay in sync without a
    circular import.
    """
    row = conn.execute(
        "SELECT display_name FROM user_profiles WHERE uid = ?", (uid,)
    ).fetchone()
    return row["display_name"] if row and row["display_name"] else None


@router.get("/profile")
def get_profile(user: dict | None = Depends(get_current_user), conn=Depends(get_db)):
    if user is None:
        raise HTTPException(401, "sign in to view your profile")
    return {"display_name": get_display_name(conn, user["uid"])}


@router.put("/profile")
def set_profile(
    body: ProfileBody,
    user: dict | None = Depends(get_current_user), conn=Depends(get_db),
):
    if user is None:
        raise HTTPException(401, "sign in to edit your profile")
    cleaned = clean_display_name(body.display_name)
    conn.execute(
        """INSERT INTO user_profiles(uid, display_name) VALUES(?, ?)
           ON CONFLICT(uid) DO UPDATE SET display_name = excluded.display_name""",
        (user["uid"], cleaned or None),
    )
    conn.commit()
    return {"display_name": cleaned or None}
