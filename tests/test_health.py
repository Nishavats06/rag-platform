from app.core.database import get_db
from app.main import app


def test_live_returns_ok(client):
    response = client.get("/health/live")
    assert response.status_code == 200
    body = response.json()
    assert body["success"] is True
    assert body["data"]["status"] == "ok"


def test_ready_returns_ok_when_database_is_up(client):
    response = client.get("/health/ready")
    assert response.status_code == 200
    assert response.json()["data"]["database"] == "ok"


def test_ready_returns_503_in_error_envelope_when_database_is_down(client):
    class BrokenSession:
        def execute(self, *args, **kwargs):
            raise RuntimeError("database down")

    def broken_db():
        yield BrokenSession()

    app.dependency_overrides[get_db] = broken_db
    response = client.get("/health/ready")
    assert response.status_code == 503
    assert response.json() == {
        "success": False,
        "status_code": 503,
        "message": "Database is not reachable",
    }