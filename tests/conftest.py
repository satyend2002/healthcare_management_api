# tests/conftest.py ............................................

import sys
from pathlib import Path

import pytest

sys.path.insert(
    0,
    str(Path(__file__).resolve().parents[1])
)

from app import app

@pytest.fixture
def client():
    app.config.update(
        TESTING=True,
        PROPAGATE_EXCEPTIONS=True,
        JWT_SECRET_KEY="test-secret-key"
    )

    with app.test_client() as client:
        yield client

@pytest.fixture
def access_token(client):
    response = client.post(
        "/api/v1/auth/login",
        json={
            "username": "admin",
            "password": "Admin@123"
        }
    )

    assert response.status_code == 200

    response_data = response.get_json()

    return response_data["access_token"]


@pytest.fixture
def auth_headers(access_token):
    return {
        "Authorization": f"Bearer {access_token}"
    }