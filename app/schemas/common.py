from pydantic import BaseModel


class ErrorResponse(BaseModel):
    success: bool = False
    status_code: int
    message: str