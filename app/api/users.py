from typing import Annotated

from fastapi import APIRouter, Depends

from app.api.deps import get_current_user
from app.api.responses import UNAUTHORIZED_RESPONSE
from app.models.user import User
from app.schemas.user import UserOut, UserResponse

router = APIRouter(prefix="/users", tags=["users"])


@router.get("/me", response_model=UserResponse, responses={**UNAUTHORIZED_RESPONSE})
def read_me(current_user: Annotated[User, Depends(get_current_user)]):
    return UserResponse(message="OK", data=UserOut.model_validate(current_user))