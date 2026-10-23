from pydantic import BaseModel, ConfigDict


class ErrorResponse(BaseModel):
    model_config = ConfigDict(
        json_schema_extra={
            "examples": [
                {
                    "success": False,
                    "status_code": 401,
                    "message": "Not authenticated",
                }
            ]
        }
    )

    success: bool = False
    status_code: int
    message: str