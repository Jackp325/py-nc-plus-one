import pytest
from db.seed import seed
from db.connection import get_connection


@pytest.fixture
def default_seed():
    seed()
    conn = get_connection()
    yield conn
    conn.close()


