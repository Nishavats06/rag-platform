from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from sqlalchemy import text
from sqlalchemy.orm import Session

from app.core.database import get_db

router = APIRouter(prefix="/health", tags=["health"])


@router.get("/live")
def live():
    return {"success": True, "message": "alive", "data": {"status": "ok"}}


@router.get(
    "/ready",
    responses={503: {"description": "Database is not reachable"}},
)
def ready(db: Session = Depends(get_db)):
    try:
        db.execute(text("SELECT 1"))
    except Exception:
        return JSONResponse(
            status_code=503,
            content={
                "success": False,
                "status_code": 503,
                "message": "Database is not reachable",
            },
        )
    return {"success": True, "message": "ready", "data": {"database": "ok"}}