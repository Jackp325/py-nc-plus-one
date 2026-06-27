from db.connection import get_connection
from utils.read_json import read_json
from utils.security import hash_password

def seed():
    conn = get_connection()

    tables = [
        "rsvps",
        "events", 
        "venues", 
        "users"
    ]
    # Drop tables in reverse order of dependencies
    for table in tables:
        drop_table(conn, table)

    create_users_table(conn)
    create_venues_table(conn)
    create_events_table(conn)
    create_rsvps_table(conn)
    
    insert_users(conn)
    insert_venues(conn)
    insert_events(conn)
    insert_rsvps(conn)

    conn.commit()
    conn.close()

def drop_table(conn, table_name):
    cursor = conn.cursor()

    cursor.execute(f"""
        DROP TABLE IF EXISTS {table_name};
    """)
    # Internal coding, no risks of SQL injection
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

def create_events_table(conn):
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS events(
            id SERIAL PRIMARY KEY,
            title VARCHAR(255) NOT NULL,
            description VARCHAR(255),
            starts_at TIMESTAMPTZ NOT NULL,
            ends_at TIMESTAMPTZ NOT NULL,
            organiser_id INT REFERENCES users(id),
            venue_id INT REFERENCES venues(id),
            created_at TIMESTAMPTZ DEFAULT NOW()
        );
    """)

    cursor.close()

def create_rsvps_table(conn):
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS rsvps(
            id SERIAL PRIMARY KEY,
            attendee_id INT REFERENCES users(id),
            event_id INT REFERENCES events(id),
            created_at TIMESTAMPTZ DEFAULT NOW()
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
            hash_password(user["password"])
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

def insert_events(conn):
    cursor = conn.cursor()

    events = read_json("data/events.json")

    event_info = [
        (
            event["title"],
            event["description"],
            event["starts_at"],
            event["ends_at"],
            event["organiser_id"],
            event["venue_id"]
        )
        for event in events
    ]
    cursor.executemany(
        """
        INSERT INTO events (
            title, 
            description, 
            starts_at,
            ends_at,
            organiser_id,
            venue_id
        )
        VALUES (%s, %s, %s, %s, %s, %s)
        """,
        event_info
    )

    cursor.close()

def insert_rsvps(conn):
    cursor = conn.cursor()

    rsvps = read_json("data/rsvps.json")

    rsvp_info = [
        (
            rsvp["attendee_id"],
            rsvp["event_id"],
        )
        for rsvp in rsvps
    ]
    cursor.executemany(
        """
        INSERT INTO rsvps (attendee_id, event_id)
        VALUES (%s, %s)
        """,
        rsvp_info
    )

    cursor.close()


if __name__ == "__main__":
    seed()