from db.connection import get_connection
from utils.read_json import read_json

def seed():
    """
    1. Removes any data from previous runs
    2. Rebuild the table schemas
    3. Insert the test data
    """
    conn = get_connection()

    tables = ["venues", "users"]
    # Drop tables in order of dependencies
    for table in tables:
        drop_table(conn, table)

    create_users_table(conn)
    create_venues_table(conn)
    
    insert_users(conn)
    insert_venues(conn)

    conn.commit()
    conn.close()

def drop_table(conn, table_name):
    cursor = conn.cursor()

    cursor.execute(f"""
        DROP TABLE IF EXISTS {table_name};
    """)

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

def create_venues_table(conn):
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS venues(
            id SERIAL PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            address TEXT,
            capacity INT
        );
    """)

    cursor.close()


def insert_users(conn):
    cursor = conn.cursor()

    users = read_json("data/users.json")

    user_info = [
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
        user_info
    )

    cursor.close()

def insert_venues(conn):
    cursor = conn.cursor()

    venues = read_json("data/venues.json")

    venue_info = [
        (
            venue["name"],
            venue["address"],
            venue["capacity"]
        )
        for venue in venues
    ]
    cursor.executemany(
        """
        INSERT INTO venues (name, address, capacity)
        VALUES (%s, %s, %s)
        """,
        venue_info
    )

    cursor.close()

if __name__ == "__main__":
    seed()