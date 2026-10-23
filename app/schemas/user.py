from datetime import datetime

from pydantic import BaseModel, ConfigDict


class UserOut(BaseModel):
    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "examples": [
                {
                    "id": 1,
                    "email": "ravi.sharma@example.com",
                    "name": "Ravi Sharma",
                    "created_at": "2026-01-15T10:30:00Z",
                }
            ]
        },
    )

    id: int
    email: str
    name: str | None
    created_at: datetime


class UserResponse(BaseModel):
    model_config = ConfigDict(
        json_schema_extra={
            "examples": [
                {
                    "success": True,
                    "message": "OK",
                    "data": {
                        "id": 1,
                        "email": "ravi.sharma@example.com",
                        "name": "Ravi Sharma",
                        "created_at": "2026-01-15T10:30:00Z",
                    },
                }
            ]
        }
    )

    success: bool = True
    message: str
    data: UserOut