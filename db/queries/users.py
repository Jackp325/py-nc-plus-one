from psycopg2.extras import RealDictCursor

def get_user_by_email(conn, email):
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