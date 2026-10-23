from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api.responses import UNAUTHORIZED_RESPONSE
from app.core.database import get_db
from app.core.security import InvalidTokenError, create_access_token, verify_google_token
from app.schemas.auth import GoogleLoginRequest, TokenData, TokenResponse
from app.services.user_service import get_or_create_user

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post(
    "/google",
    response_model=TokenResponse,
    responses={**UNAUTHORIZED_RESPONSE},
)
def google_login(body: GoogleLoginRequest, db: Annotated[Session, Depends(get_db)]):
    try:
        claims = verify_google_token(body.id_token)
    except InvalidTokenError:
        raise HTTPException(401, "Invalid or expired Google token") from None
    if not claims.get("email"):
        raise HTTPException(401, "Google account has no email")

    user = get_or_create_user(db, claims)
    token = create_access_token(user.id)
    return TokenResponse(message="Login successful", data=TokenData(access_token=token))