from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi

from app.schemas.common import ErrorResponse

HTTP_METHODS = {"get", "post", "put", "patch", "delete", "options", "head"}

VALIDATION_ERROR_RESPONSE = {
    "description": "Validation error",
    "content": {
        "application/json": {
            "schema": {"$ref": "#/components/schemas/ErrorResponse"},
            "example": {
                "success": False,
                "status_code": 422,
                "message": "id_token: String should have at least 20 characters",
            },
        }
    },
}


def install_custom_openapi(app: FastAPI) -> None:
    def custom_openapi():
        if app.openapi_schema:
            return app.openapi_schema

        schema = get_openapi(
            title=app.title,
            version=app.version,
            description=app.description,
            routes=app.routes,
        )
        components = schema.setdefault("components", {}).setdefault("schemas", {})

        if "ErrorResponse" not in components:
            error_schema = ErrorResponse.model_json_schema(
                ref_template="#/components/schemas/{model}"
            )
            error_schema.pop("$defs", None)
            components["ErrorResponse"] = error_schema

        for path_item in schema.get("paths", {}).values():
            for method, operation in path_item.items():
                if method not in HTTP_METHODS:
                    continue
                responses = operation.get("responses", {})
                if "422" in responses:
                    responses["422"] = VALIDATION_ERROR_RESPONSE

        components.pop("HTTPValidationError", None)
        components.pop("ValidationError", None)

        app.openapi_schema = schema
        return schema

    app.openapi = custom_openapi