from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.models.user import User


def get_or_create_user(db: Session, claims: dict) -> User:
    sub = claims["sub"]
    user = db.scalar(select(User).where(User.google_sub == sub))
    if user:
        return user

    user = User(google_sub=sub, email=claims["email"], name=claims.get("name"))
    db.add(user)
    try:
        db.commit()
    except IntegrityError:
        # do requests ek saath pehli baar aayi: doosri ko unique index ne roka
        db.rollback()
        user = db.scalar(select(User).where(User.google_sub == sub))
        if user is None:
            raise
        return user
    db.refresh(user)
    return user