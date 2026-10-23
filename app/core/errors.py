from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException


def error_body(status_code: int, message: str) -> dict:
    return {"success": False, "status_code": status_code, "message": message}


def register_exception_handlers(app: FastAPI) -> None:
    @app.exception_handler(StarletteHTTPException)
    async def http_exception_handler(request: Request, exc: StarletteHTTPException):
        return JSONResponse(
            status_code=exc.status_code,
            content=error_body(exc.status_code, str(exc.detail)),
            headers=getattr(exc, "headers", None),
        )

    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(request: Request, exc: RequestValidationError):
        parts = []
        for err in exc.errors():
            field = ".".join(str(p) for p in err["loc"] if p != "body")
            parts.append(f"{field}: {err['msg']}" if field else err["msg"])
        return JSONResponse(status_code=422, content=error_body(422, "; ".join(parts)))