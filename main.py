import bcrypt
import jwt
from datetime import datetime, timedelta, timezone
import os
from fastapi import FastAPI, Depends, HTTPException, Response
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel
from db.connection import get_connection
from dotenv import load_dotenv


load_dotenv()

JWT_SECRET = os.getenv("JWT_SECRET")
JWT_ALGORITHM = os.getenv("JWT_ALGORITHM")
JWT_EXPIRY_MINUTES = int(os.getenv("JWT_EXPIRY_MINUTES"))


class CredentialsRequest(BaseModel):
    email: str | None = None
    password: str | None = None


class RegisterRequest(BaseModel):
    name: str | None = None
    email: str | None = None
    password: str | None = None


class CreateEventRequest(BaseModel):
    title: str | None = None
    description: str | None = None
    starts_at: str | None = None
    ends_at: str | None = None
    venue_id: int | None = None

class PatchEventRequest(BaseModel):
    title: str | None = None
    description: str | None = None
    starts_at: str | None = None
    ends_at: str | None = None
    venue_id: int | None = None    


def hash_password(plain: str) -> str:
    return bcrypt.hashpw(plain.encode(), bcrypt.gensalt()).decode()


def verify_password(plain: str, hashed: str) -> bool:
    return bcrypt.checkpw(plain.encode(), hashed.encode())


def create_access_token(user_id: int) -> str:
    expire = datetime.now(timezone.utc) + timedelta(minutes=JWT_EXPIRY_MINUTES)
    payload = {"sub": str(user_id), "exp": expire}
    return jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)


def validate_iso_date(date_value: str):
    try:
        return datetime.fromisoformat(date_value.replace("Z", "+00:00"))
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid date format")


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")


def get_current_user_id(token: str = Depends(oauth2_scheme)) -> int:
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        return int(payload["sub"])

    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired")

    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Could not validate token")


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


@app.post("/api/events", status_code=201)
def create_event(payload: CreateEventRequest, user_id: int = Depends(get_current_user_id)):
    if (
        payload.title is None
        or payload.description is None
        or payload.starts_at is None
        or payload.ends_at is None
        or payload.venue_id is None
    ):
        raise HTTPException(status_code=400, detail="Missing required fields")

    validate_iso_date(payload.starts_at)
    validate_iso_date(payload.ends_at)

    conn = get_connection()

    with conn.cursor() as cursor:
        cursor.execute(
            """
            INSERT INTO events (title, description, starts_at, ends_at, organiser_id, venue_id)
            VALUES (%s, %s, %s, %s, %s, %s)
            RETURNING id, title, description, starts_at, ends_at, organiser_id, venue_id, created_at
            """,
            (
                payload.title,
                payload.description,
                payload.starts_at,
                payload.ends_at,
                user_id,
                payload.venue_id,
            ),
        )

        row = cursor.fetchone()

    conn.commit()
    conn.close()

    event = {
        "id": row[0],
        "title": row[1],
        "description": row[2],
        "starts_at": row[3],
        "ends_at": row[4],
        "organiser_id": row[5],
        "venue_id": row[6],
        "created_at": row[7],
    }

    return {"event": event}

@app.patch("/api/events/{event_id}")
def update_event(event_id: int, payload: PatchEventRequest, user_id: int = Depends(get_current_user_id)):
    conn = get_connection()

    with conn.cursor() as cursor:
        cursor.execute(
            """
            SELECT id, title, description, starts_at, ends_at, organiser_id, venue_id, created_at
            FROM events
            WHERE id = %s
            """,
            (event_id,),
        )

        row = cursor.fetchone()

        if row is None:
            conn.close()
            raise HTTPException(status_code=404, detail="Event not found")

        if row[5] != user_id:
            conn.close()
            raise HTTPException(status_code=403, detail="You are not the organiser of this event")

        new_title = payload.title if payload.title is not None else row[1]
        new_description = payload.description if payload.description is not None else row[2]
        new_starts_at = payload.starts_at if payload.starts_at is not None else row[3].isoformat()
        new_ends_at = payload.ends_at if payload.ends_at is not None else row[4].isoformat()
        new_venue_id = payload.venue_id if payload.venue_id is not None else row[6]

        starts_at_date = validate_iso_date(new_starts_at)
        ends_at_date = validate_iso_date(new_ends_at)

        if ends_at_date <= starts_at_date:
            conn.close()
            raise HTTPException(status_code=400, detail="ends_at must be after starts_at")

        cursor.execute(
            """
            UPDATE events
            SET title = %s,
                description = %s,
                starts_at = %s,
                ends_at = %s,
                venue_id = %s
            WHERE id = %s
            RETURNING id, title, description, starts_at, ends_at, organiser_id, venue_id, created_at
            """,
            (
                new_title,
                new_description,
                new_starts_at,
                new_ends_at,
                new_venue_id,
                event_id,
            ),
        )

        updated_row = cursor.fetchone()

    conn.commit()
    conn.close()

    event = {
        "id": updated_row[0],
        "title": updated_row[1],
        "description": updated_row[2],
        "starts_at": updated_row[3],
        "ends_at": updated_row[4],
        "organiser_id": updated_row[5],
        "venue_id": updated_row[6],
        "created_at": updated_row[7],
    }

    return {"event": event}

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


@app.post("/api/events/{event_id}/rsvp", status_code=201)
def create_rsvp(event_id: int, user_id: int = Depends(get_current_user_id)):
    conn = get_connection()

    with conn.cursor() as cursor:
        cursor.execute(
            """
            SELECT id
            FROM events
            WHERE id = %s
            """,
            (event_id,),
        )

        event = cursor.fetchone()

        if event is None:
            conn.close()
            raise HTTPException(status_code=404, detail="Event not found")

        cursor.execute(
            """
            SELECT id
            FROM rsvps
            WHERE attendee_id = %s
            AND event_id = %s
            """,
            (user_id, event_id),
        )

        existing_rsvp = cursor.fetchone()

        if existing_rsvp is not None:
            conn.close()
            raise HTTPException(status_code=409, detail="User has already RSVPed to this event")

        cursor.execute(
            """
            INSERT INTO rsvps (attendee_id, event_id)
            VALUES (%s, %s)
            RETURNING id, attendee_id, event_id, created_at
            """,
            (user_id, event_id),
        )

        row = cursor.fetchone()

    conn.commit()
    conn.close()

    rsvp = {
        "id": row[0],
        "attendee_id": row[1],
        "event_id": row[2],
        "created_at": row[3],
    }

    return {"rsvp": rsvp}


@app.delete("/api/events/{event_id}/rsvp/me", status_code=204)
def delete_my_rsvp(event_id: int, user_id: int = Depends(get_current_user_id)):
    conn = get_connection()

    with conn.cursor() as cursor:
        cursor.execute(
            """
            SELECT id
            FROM rsvps
            WHERE attendee_id = %s
            AND event_id = %s
            """,
            (user_id, event_id),
        )

        rsvp = cursor.fetchone()

        if rsvp is None:
            conn.close()
            raise HTTPException(status_code=404, detail="RSVP not found")

        cursor.execute(
            """
            DELETE FROM rsvps
            WHERE attendee_id = %s
            AND event_id = %s
            """,
            (user_id, event_id),
        )

    conn.commit()
    conn.close()

    return Response(status_code=204)


@app.get("/api/health")
def get_health():
    return {"status": "ok"}