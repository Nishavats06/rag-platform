import pytest

from app.core.security import InvalidTokenError, create_access_token, decode_access_token


def test_token_roundtrip():
    token = create_access_token(42)
    assert decode_access_token(token) == 42


def test_garbage_token_rejected():
    with pytest.raises(InvalidTokenError):
        decode_access_token("not-a-real-token")