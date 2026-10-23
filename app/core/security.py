from google.auth.transport import requests as google_requests
from google.oauth2 import id_token

from app.core.config import settings


class InvalidTokenError(Exception):
    """Raised when a Google ID token cannot be verified."""


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