from fastapi.testclient import TestClient

from app.main import app

EXPECTED_WITH_EXAMPLES = [
    "GoogleLoginRequest",
    "TokenData",
    "TokenResponse",
    "UserOut",
    "UserResponse",
    "ErrorResponse",
]


def get_schema() -> dict:
    return TestClient(app).get("/openapi.json").json()


def test_422_documented_with_error_envelope():
    schema = get_schema()
    operation = schema["paths"]["/auth/google"]["post"]
    ref = operation["responses"]["422"]["content"]["application/json"]["schema"]["$ref"]
    assert ref.endswith("/ErrorResponse")
    assert "HTTPValidationError" not in schema["components"]["schemas"]


def test_schemas_have_realistic_examples():
    schemas = get_schema()["components"]["schemas"]
    for name in EXPECTED_WITH_EXAMPLES:
        assert schemas[name].get("examples"), f"{name} has no example"