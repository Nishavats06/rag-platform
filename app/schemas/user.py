from datetime import datetime

from pydantic import BaseModel, ConfigDict


class UserOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    email: str
    name: str | None
    created_at: datetime


class UserResponse(BaseModel):
    success: bool = True
    message: str
    data: UserOut