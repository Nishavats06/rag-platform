
from typing import Annotated

from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from sqlalchemy import text
from sqlalchemy.orm import Session

from app.api.responses import SERVICE_UNAVAILABLE_RESPONSE
from app.core.database import get_db
from app.core.errors import error_body
from app.schemas.health import LiveData, LiveResponse, ReadyData, ReadyResponse

router = APIRouter(prefix="/health", tags=["health"])


@router.get("/live", response_model=LiveResponse)
def live():
    return LiveResponse(message="alive", data=LiveData(status="ok"))


@router.get(
    "/ready",
    response_model=ReadyResponse,
    responses={**SERVICE_UNAVAILABLE_RESPONSE},
)
def ready(db: Annotated[Session, Depends(get_db)]):
    try:
        db.execute(text("SELECT 1"))
    except Exception:
        return JSONResponse(
            status_code=503,
            content=error_body(503, "Database is not reachable"),
        )
    return ReadyResponse(message="ready", data=ReadyData(database="ok"))