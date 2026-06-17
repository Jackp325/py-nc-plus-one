from db.connection import get_connection
from utils.read_json import read_json

def seed():
    """
    1. Removes any data from previous runs
    2. Rebuild the table schemas
    3. Insert the test data
    """
    conn = get_connection()

    drop_users_table(conn)
    create_users_table(conn)
    insert_users(conn)

    conn.commit()
    conn.close()

def drop_users_table(conn):
    cursor = conn.cursor()

    cursor.execute("DROP TABLE IF EXISTS users;")

    cursor.close()

def create_users_table(conn):
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users(
            id SERIAL PRIMARY KEY,
            email VARCHAR(255) UNIQUE NOT NULL,
            password VARCHAR(255) NOT NULL,
            name VARCHAR(255) NOT NULL,
            created_at TIMESTAMPTZ DEFAULT NOW()
        );
    """)

    cursor.close()

def insert_users(conn):
    cursor = conn.cursor()

    users = read_json("data/users.json")

    user_records = [
        (
            user["name"],
            user["email"],
            user["password"]
        )
        for user in users
    ]
    cursor.executemany(
        """
        INSERT INTO users (name, email, password)
        VALUES (%s, %s, %s)
        """,
        user_records
    )

if __name__ == "__main__":
    seed()