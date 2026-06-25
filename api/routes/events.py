from fastapi import APIRouter, HTTPException
from db.connection import get_connection
from db.queries.events import get_all_events, get_event_by_id

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

@router.get("/{id}")
def get_event(id: int):
    conn = get_connection()
    row = get_event_by_id(conn, id)
    conn.close()
    if row is None:
        raise HTTPException(
            status_code=404,
            detail={"code": "NOT_FOUND", "message": "event not found"},
        )
    event = {
            "id": row[0],
            "title": row[1],
            "description": row[2],
            "starts_at": row[3],
            "ends_at": row[4],
            "location": row[5],
            "address": row[6],
            "capacity": row[7],
            "created_at": row[8]
        }

    return {"event": event}