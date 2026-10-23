from typing import Annotated

from fastapi import Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import InvalidTokenError, decode_access_token
from app.models.user import User

bearer_scheme = HTTPBearer(auto_error=False)
_AUTH_HEADERS = {"WWW-Authenticate": "Bearer"}


def get_current_user(
    credentials: Annotated[HTTPAuthorizationCredentials | None, Depends(bearer_scheme)],
    db: Annotated[Session, Depends(get_db)],
) -> User:
    if credentials is None:
        raise HTTPException(401, "Not authenticated", headers=_AUTH_HEADERS)
    try:
        user_id = decode_access_token(credentials.credentials)
    except InvalidTokenError:
        raise HTTPException(401, "Invalid or expired token", headers=_AUTH_HEADERS) from None
    user = db.get(User, user_id)
    if user is None:
        raise HTTPException(401, "User no longer exists", headers=_AUTH_HEADERS)
    return user