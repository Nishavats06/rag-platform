from app.schemas.common import ErrorResponse

UNAUTHORIZED_RESPONSE = {
    401: {"model": ErrorResponse, "description": "Missing, invalid or expired token"}
}