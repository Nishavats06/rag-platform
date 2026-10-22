from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api import health
from app.core.config import settings

app = FastAPI(title=settings.app_name)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health.router)


# from fastapi import FastAPI

# app = FastAPI(title="Document Search & RAG Platform")


# @app.get("/health/live")
# def live():
#     return {"success": True, "message": "alive", "data": {"status": "ok"}}