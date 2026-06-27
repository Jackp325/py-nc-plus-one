from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from db.connection import get_connection
from db.queries.users import get_user_by_email
from utils.security import check_password, create_access_token

router = APIRouter(prefix="/api/auth", tags=["auth"])

class LoginRequest(BaseModel):
    email: str
    password: str

@router.post("/login")
def login(payload:LoginRequest):
    conn = get_connection()
    row = get_user_by_email(conn, payload.email)
    conn.close()
    if row is None or not check_password(payload.password, row["hashed_password"]):
        raise HTTPException(
            status_code=401,
            detail={"code": "UNAUTHORIZED", "message": "Invalid email or password"},
        )
    token = create_access_token(row["id"])

    return {"access_token": token, "token_type": "bearer"}