from fastapi import APIRouter, HTTPException
from db.connection import get_connection
from db.queries.events import get_all_events, get_event_by_id

router = APIRouter(prefix="/api/events", tags=["events"])


@router.get("")
def list_events():
    conn = get_connection()
    rows = get_all_events(conn)
    conn.close()

    return {"events": rows}

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
            "id": row["id"],
            "title": row["title"],
            "description": row["description"],
            "starts_at": row["starts_at"],
            "ends_at": row["ends_at"],
            "location": row["location"],
            "address": row["address"],
            "capacity": row["capacity"],
            "created_at": row["created_at"]
        }

    return {"event": event}