from app.schemas.common import ErrorResponse

UNAUTHORIZED_RESPONSE = {
    401: {"model": ErrorResponse, "description": "Missing, invalid or expired token"}
}
SERVICE_UNAVAILABLE_RESPONSE = {
    503: {
        "model": ErrorResponse,
        "description": "Database is not reachable",
        "content": {
            "application/json": {
                "example": {
                    "success": False,
                    "status_code": 503,
                    "message": "Database is not reachable",
                }
            }
        },
    }
}