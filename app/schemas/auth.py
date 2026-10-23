from pydantic import BaseModel, ConfigDict, Field


class GoogleLoginRequest(BaseModel):
    model_config = ConfigDict(
        json_schema_extra={
            "examples": [
                {
                    "id_token": "eyJhbGciOiJSUzI1NiIsImtpZCI6ImFiYzEyMyIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMTA1MjMxNDc4OTAxMjM0NTY3ODkifQ.c2lnbmF0dXJl"
                }
            ]
        }
    )

    id_token: str = Field(min_length=20, max_length=4096)


class TokenData(BaseModel):
    model_config = ConfigDict(
        json_schema_extra={
            "examples": [
                {
                    "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxIiwiZXhwIjoxNzg4MDAwMDAwfQ.c2lnbmF0dXJl",
                    "token_type": "bearer",
                }
            ]
        }
    )

    access_token: str
    token_type: str = "bearer"


class TokenResponse(BaseModel):
    model_config = ConfigDict(
        json_schema_extra={
            "examples": [
                {
                    "success": True,
                    "message": "Login successful",
                    "data": {
                        "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxIiwiZXhwIjoxNzg4MDAwMDAwfQ.c2lnbmF0dXJl",
                        "token_type": "bearer",
                    },
                }
            ]
        }
    )

    success: bool = True
    message: str
    data: TokenData