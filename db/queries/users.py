from psycopg2.extras import RealDictCursor

from utils.security import hash_password

def get_user_by_email(conn, email: str):
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    cursor.execute("""
    SELECT
        id,
        email,
        password AS hashed_password
    FROM users
    WHERE email = %s;
    """, (email,))
    row = cursor.fetchone()
    cursor.close()
    return row

def register_user(conn, name: str, email: str, plain_password: str):
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    password = hash_password(plain_password)
    cursor.execute(
        """
        INSERT INTO users (name, email, password)
        VALUES (%s, %s, %s)
        RETURNING id, name, email, created_at
        """,
        (name, email, password),
    )
    row = cursor.fetchone()
    cursor.close()
    return row