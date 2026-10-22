from fastapi import FastAPI

from app.api import health
from app.core.config import settings

app = FastAPI(title=settings.app_name)

app.include_router(health.router)


# from fastapi import FastAPI

# app = FastAPI(title="Document Search & RAG Platform")


# @app.get("/health/live")
# def live():
#     return {"success": True, "message": "alive", "data": {"status": "ok"}}