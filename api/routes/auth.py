from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from psycopg2.errors import UniqueViolation

from db.connection import get_connection
from db.queries.users import get_user_by_email, register_user
from utils.security import check_password, create_access_token

router = APIRouter(prefix="/api/auth", tags=["auth"])

class LoginRequest(BaseModel):
    email: str
    password: str

class RegisterUser(BaseModel):
    name: str
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

    return {"token": token}

@router.post("/register", status_code=201)
def register(payload:RegisterUser):
    conn = get_connection()
    try:
        row = register_user(conn, payload.name, payload.email, payload.password)
        conn.commit()
    except UniqueViolation:
        raise HTTPException(
            status_code=409,
            detail={"code": "CONFLICT", "message": "User already exists"},
        )
    finally:
        conn.close()

    return {"user": row}