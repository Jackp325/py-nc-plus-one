import pytest
from fastapi.testclient import TestClient

from db.seed import seed
from db.connection import get_connection
from main import app

@pytest.fixture
def client():
    return TestClient(app)

@pytest.fixture(scope="session")
def default_seed():
    seed()
    conn = get_connection()
    yield conn
    conn.close()

@pytest.fixture
def sample_user(default_seed, client):
    payload = {
        "name": "Jane Doe",
        "email": "j.doe@gmail.com",
        "password": "doedoe123"
    }
    response = client.post("/api/auth/register", json=payload)
    user = response.json()["user"]
    user_id = user["id"]
    yield response
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM users WHERE id = %s", (user_id,))
    conn.commit()
    cursor.close()
    conn.close()