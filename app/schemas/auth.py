from pydantic import BaseModel, Field


class GoogleLoginRequest(BaseModel):
    id_token: str = Field(min_length=20, max_length=4096)


class TokenData(BaseModel):
    access_token: str
    token_type: str = "bearer"


class TokenResponse(BaseModel):
    success: bool = True
    message: str
    data: TokenData