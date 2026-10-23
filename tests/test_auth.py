from sqlalchemy import func, select

from app.core.security import InvalidTokenError
from app.models.user import User

FAKE_TOKEN = "x" * 30


def login(client, monkeypatch, sub="sub-1", email="a@example.com"):
    claims = {"sub": sub, "email": email, "name": "Test User"}
    monkeypatch.setattr("app.api.auth.verify_google_token", lambda token: claims)
    return client.post("/auth/google", json={"id_token": FAKE_TOKEN})


def auth_header(response):
    return {"Authorization": f"Bearer {response.json()['data']['access_token']}"}


def test_first_login_creates_user_and_me_works(client, monkeypatch):
    response = login(client, monkeypatch)
    assert response.status_code == 200
    me = client.get("/users/me", headers=auth_header(response))
    assert me.status_code == 200
    assert me.json()["data"]["email"] == "a@example.com"


def test_repeat_login_does_not_duplicate_user(client, monkeypatch, db_session):
    login(client, monkeypatch, sub="sub-1", email="old@example.com")
    login(client, monkeypatch, sub="sub-1", email="new@example.com")
    assert db_session.scalar(select(func.count()).select_from(User)) == 1


def test_each_user_sees_only_their_own_profile(client, monkeypatch):
    a = login(client, monkeypatch, sub="sub-a", email="a@example.com")
    b = login(client, monkeypatch, sub="sub-b", email="b@example.com")

    me_a = client.get("/users/me", headers=auth_header(a))
    me_b = client.get("/users/me", headers=auth_header(b))

    assert me_a.json()["data"]["email"] == "a@example.com"
    assert me_b.json()["data"]["email"] == "b@example.com"


def test_invalid_google_token_gives_401(client, monkeypatch):
    def reject(token):
        raise InvalidTokenError("bad")

    monkeypatch.setattr("app.api.auth.verify_google_token", reject)
    response = client.post("/auth/google", json={"id_token": FAKE_TOKEN})
    assert response.status_code == 401
    assert response.json()["success"] is False


def test_me_without_token_gives_401(client):
    response = client.get("/users/me")
    assert response.status_code == 401
    assert response.json() == {
        "success": False,
        "status_code": 401,
        "message": "Not authenticated",
    }


def test_me_with_garbage_token_gives_401(client):
    response = client.get("/users/me", headers={"Authorization": "Bearer garbage"})
    assert response.status_code == 401


def test_validation_error_uses_same_envelope(client):
    response = client.post("/auth/google", json={})
    assert response.status_code == 422
    body = response.json()
    assert body["success"] is False
    assert body["status_code"] == 422