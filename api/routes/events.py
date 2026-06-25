from fastapi import APIRouter
from db.connection import get_connection
from db.queries.events import get_all_events

router = APIRouter(prefix="/api/events", tags=["events"])


@router.get("")
def list_events():
    conn = get_connection()
    rows = get_all_events(conn)
    conn.close()
    events = [
        {
            "id": r[0],
            "title": r[1],
            "starts_at": r[2],
            "ends_at": r[3],
            "location": r[4]
        }
        for r in rows
    ]
    return {"events": events}