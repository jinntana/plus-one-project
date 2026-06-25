import bcrypt
import jwt
from datetime import datetime, timedelta, timezone

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from db.connection import get_connection
from db.credentials import JWT_SECRET, JWT_ALGORITHM, JWT_EXPIRY_MINUTES


class CredentialsRequest(BaseModel):
    email: str | None = None
    password: str | None = None


class RegisterRequest(BaseModel):
    name: str | None = None
    email: str | None = None
    password: str | None = None


def hash_password(plain: str) -> str:
    return bcrypt.hashpw(plain.encode(), bcrypt.gensalt()).decode()


def verify_password(plain: str, hashed: str) -> bool:
    return bcrypt.checkpw(plain.encode(), hashed.encode())


def create_access_token(user_id: int) -> str:
    expire = datetime.now(timezone.utc) + timedelta(minutes=JWT_EXPIRY_MINUTES)
    payload = {"sub": str(user_id), "exp": expire}
    return jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)


app = FastAPI()


@app.get("/api/events")
def get_all_events():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT
            events.id,
            events.title,
            events.starts_at,
            events.ends_at,
            venues.name AS location
        FROM events
        JOIN venues
        ON events.venue_id = venues.id
        ORDER BY events.starts_at ASC
        """
    )

    rows = cursor.fetchall()
    cursor.close()
    conn.close()

    events = []

    for row in rows:
        events.append(
            {
                "id": row[0],
                "title": row[1],
                "starts_at": row[2],
                "ends_at": row[3],
                "location": row[4],
            }
        )

    return {"events": events}


@app.get("/api/events/{event_id}")
def get_event_by_id(event_id: str):
    if not event_id.isdigit():
        raise HTTPException(status_code=400, detail="Invalid event id")

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
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
        JOIN venues
        ON events.venue_id = venues.id
        WHERE events.id = %s
        """,
        (event_id,),
    )

    row = cursor.fetchone()
    cursor.close()
    conn.close()

    if row is None:
        raise HTTPException(status_code=404, detail="Event not found")

    event = {
        "id": row[0],
        "title": row[1],
        "description": row[2],
        "starts_at": row[3],
        "ends_at": row[4],
        "location": row[5],
        "address": row[6],
        "capacity": row[7],
        "created_at": row[8],
    }

    return {"event": event}



@app.post("/api/auth/login")
def login_user(payload: CredentialsRequest):
    if payload.email is None or payload.password is None:
        raise HTTPException(status_code=400, detail="Email and password are required")

    conn = get_connection()

    with conn.cursor() as cursor:
        cursor.execute(
            """
            SELECT id, password
            FROM users
            WHERE email = %s
            """,
            (payload.email,),
        )

        row = cursor.fetchone()

    conn.close()

    if row is None or not verify_password(payload.password, row[1]):
        raise HTTPException(status_code=401, detail="Invalid email or password")

    token = create_access_token(row[0])
    return {"token": token}



@app.post("/api/auth/register", status_code=201)
def register_user(payload: RegisterRequest):
    if payload.name is None or payload.email is None or payload.password is None:
        raise HTTPException(status_code=400, detail="Name, email and password are required")

    conn = get_connection()

    with conn.cursor() as cursor:
        cursor.execute(
            """
            SELECT id
            FROM users
            WHERE email = %s
            """,
            (payload.email,),
        )

        existing_user = cursor.fetchone()

        if existing_user is not None:
            conn.close()
            raise HTTPException(status_code=409, detail="Email already registered")

        hashed_password = hash_password(payload.password)

        cursor.execute(
            """
            INSERT INTO users (name, email, password)
            VALUES (%s, %s, %s)
            RETURNING id, name, email, created_at
            """,
            (payload.name, payload.email, hashed_password),
        )

        row = cursor.fetchone()

    conn.commit()
    conn.close()

    user = {
        "id": row[0],
        "name": row[1],
        "email": row[2],
        "created_at": row[3],
    }

    return {"user": user}    