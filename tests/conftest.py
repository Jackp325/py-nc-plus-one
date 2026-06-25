import pytest
from fastapi.testclient import TestClient

from db.seed import seed
from db.connection import get_connection
from main import app

@pytest.fixture
def client():
    return TestClient(app)

@pytest.fixture
def default_seed():
    seed()
    conn = get_connection()
    yield conn
    conn.close()


