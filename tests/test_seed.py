from db.seed import seed
from db.connection import get_connection


def test_seed_inserts_all_users():
    seed()

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM users;")

    count = cursor.fetchone()[0]

    assert count == 6

    cursor.close()
    conn.close()

def test_seed_user_ids_not_null():
    seed()

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT COUNT(*) FROM users
        WHERE id IS NULL;
    """)

    null_ids = cursor.fetchone()[0]

    assert null_ids == 0

    cursor.close()
    conn.close()

