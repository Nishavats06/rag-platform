from datetime import UTC, datetime, timedelta

import jwt
from google.auth.transport import requests as google_requests
from google.oauth2 import id_token

from app.core.config import settings


class InvalidTokenError(Exception):
    """Raised when a token (Google ID token or our own JWT) cannot be verified."""


def verify_google_token(token: str) -> dict:
    try:
        claims = id_token.verify_oauth2_token(
            token,
            google_requests.Request(),
            settings.google_client_id,
        )
    except ValueError as exc:
        raise InvalidTokenError("Invalid or expired Google token") from exc

    if not claims.get("sub"):
        raise InvalidTokenError("Token has no subject")

    return claims


def create_access_token(user_id: int) -> str:
    expire = datetime.now(UTC) + timedelta(minutes=settings.access_token_expire_minutes)
    payload = {"sub": str(user_id), "exp": expire}
    return jwt.encode(payload, settings.jwt_secret_key, algorithm=settings.jwt_algorithm)


def decode_access_token(token: str) -> int:
    try:
        payload = jwt.decode(
            token,
            settings.jwt_secret_key,
            algorithms=[settings.jwt_algorithm],
            options={"require": ["exp", "sub"]},
        )
        return int(payload["sub"])
    except (jwt.PyJWTError, KeyError, ValueError) as exc:
        raise InvalidTokenError("Invalid or expired token") from exc