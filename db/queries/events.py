def get_all_events(conn):
    cursor = conn.cursor()
    cursor.execute("""
    SELECT 
        events.id,
        events.title,
        events.starts_at,
        events.ends_at,
        venues.name || ', ' || venues.address AS location
    FROM events
    LEFT JOIN venues ON events.venue_id = venues.id
    ORDER BY starts_at;
    """)
    rows = cursor.fetchall()
    cursor.close()
    return rows

def get_event_by_id(conn, event_id):
    cursor = conn.cursor()
    cursor.execute("""
    SELECT 
        events.id,
        events.title,
        events.description,
        events.starts_at,
        events.ends_at,
        venues.name AS location,
        venues.address,
        venues.capacity,
        events.created_at
    FROM events
    LEFT JOIN venues ON events.venue_id = venues.id
    WHERE events.id = %s;
    """, (event_id,))
    event = cursor.fetchone()
    cursor.close()
    return event
    