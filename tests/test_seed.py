from datetime import datetime as dt

def test_seed_inserts_all_users(default_seed):
    cursor = default_seed.cursor()

    cursor.execute("SELECT COUNT(*) FROM users;")

    count = cursor.fetchone()[0]

    assert count == 6

    cursor.close()

def test_seed_user_ids_data_matches(default_seed):
    cursor = default_seed.cursor()

    cursor.execute("""
        SELECT name, email, password FROM users
        WHERE email = %s;
    """, ('bob@example.com',))

    user = cursor.fetchone()

    assert user == (
        "Bob Nguyen", "bob@example.com", "password123"
    )

    cursor.close()

def test_seed_inserts_all_venues(default_seed):
    cursor = default_seed.cursor()

    cursor.execute("SELECT COUNT(*) FROM venues;")

    count = cursor.fetchone()[0]

    assert count == 5

    cursor.close()

def test_seed_venues_data_matches(default_seed):
    cursor = default_seed.cursor()

    cursor.execute("""
        SELECT name, address, capacity FROM venues
        WHERE name = %s;
    """, ("Manchester Central Library",))

    venue = cursor.fetchone()

    assert venue == (
        "Manchester Central Library",
        "St Peter's Square, Manchester, M2 5PD", 
        80
    )

    cursor.close()

def test_seed_inserts_all_events(default_seed):
    cursor = default_seed.cursor()

    cursor.execute("SELECT COUNT(*) FROM events;")

    count = cursor.fetchone()[0]

    assert count == 10

    cursor.close()

def test_seed_events_data_matches(default_seed):
    cursor = default_seed.cursor()

    cursor.execute("""
        SELECT starts_at FROM events
        WHERE title = %s;
    """,("Brighton Python Meetup",))

    event_start = cursor.fetchone()

    assert event_start == (dt.fromisoformat("2026-07-10T18:00:00+01:00"),)

    cursor.close()

def test_seed_inserts_all_rsvps(default_seed):
    cursor = default_seed.cursor()

    cursor.execute("SELECT COUNT(*) FROM rsvps;")

    count = cursor.fetchone()[0]

    assert count == 28

    cursor.close()

def test_seed_rsvps_data_matches(default_seed):
    cursor = default_seed.cursor()

    cursor.execute("""
        SELECT COUNT(*) FROM rsvps
        WHERE attendee_id = %s AND event_id = %s;
    """, (3, 4))

    count = cursor.fetchone()[0]

    assert count == 1

    cursor.close()