from fastapi.testclient import TestClient
from main import app, create_access_token
import pytest


client = TestClient(app)

@pytest.fixture
def auth_headers():
    token = create_access_token(1)
    return {"Authorization": f"Bearer {token}"}

@pytest.fixture
def auth_headers_user_2():
    token = create_access_token(2)
    return {"Authorization": f"Bearer {token}"}

def test_get_all_events_returns_200_and_events():
    response = client.get("/api/events")

    assert response.status_code == 200

    body = response.json()

    assert "events" in body
    assert len(body["events"]) == 10
    assert body["events"][0]["title"] == "Leeds Tech Meetup – June Edition"


    
    
def test_get_event_by_id_returns_200_and_correct_event():
    response = client.get("/api/events/2")

    assert response.status_code == 200

    body = response.json()

    assert "event" in body
    assert body["event"]["id"] == 2
    assert body["event"]["title"] == "Intro to Machine Learning Workshop"

def test_get_event_by_id_returns_404_when_event_does_not_exist():
    response = client.get("/api/events/999")

    assert response.status_code == 404

def test_get_event_by_id_returns_400_when_id_is_not_a_number():
    response = client.get("/api/events/hello")

    assert response.status_code == 400    


def test_login_returns_token():
    response = client.post(
        "/api/auth/login",
        json={
            "email": "alice@example.com",
            "password": "password123",
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert "token" in data    

def test_login_returns_401_for_wrong_password():
    response = client.post(
        "/api/auth/login",
        json={
            "email": "alice@example.com",
            "password": "wrongpassword",
        },
    )

    assert response.status_code == 401


def test_login_returns_401_for_unknown_email():
    response = client.post(
        "/api/auth/login",
        json={
            "email": "notfound@example.com",
            "password": "password123",
        },
    )

    assert response.status_code == 401

def test_login_returns_400_when_email_is_missing():
    response = client.post(
        "/api/auth/login",
        json={
            "password": "password123",
        },
    )

    assert response.status_code == 400


def test_login_returns_400_when_password_is_missing():
    response = client.post(
        "/api/auth/login",
        json={
            "email": "alice@example.com",
        },
    )

    assert response.status_code == 400

def test_register_returns_201_and_user():
    response = client.post(
        "/api/auth/register",
        json={
            "name": "New User",
            "email": "newuser@example.com",
            "password": "password123",
        },
    )

    assert response.status_code == 201

    body = response.json()

    assert "user" in body
    assert body["user"]["name"] == "New User"
    assert body["user"]["email"] == "newuser@example.com"
    assert "password" not in body["user"]

def test_register_returns_409_when_email_already_exists():
    response = client.post(
        "/api/auth/register",
        json={
            "name": "Another Alice",
            "email": "alice@example.com",
            "password": "password123",
        },
    )

    assert response.status_code == 409

def test_register_returns_400_when_name_is_missing():
    response = client.post(
        "/api/auth/register",
        json={
            "email": "missingname@example.com",
            "password": "password123",
        },
    )

    assert response.status_code == 400


def test_register_returns_400_when_email_is_missing():
    response = client.post(
        "/api/auth/register",
        json={
            "name": "Missing Email",
            "password": "password123",
        },
    )

    assert response.status_code == 400


def test_register_returns_400_when_password_is_missing():
    response = client.post(
        "/api/auth/register",
        json={
            "name": "Missing Password",
            "email": "missingpassword@example.com",
        },
    )

    assert response.status_code == 400

def test_create_rsvp_returns_201(auth_headers):
    response = client.post("/api/events/1/rsvp", headers=auth_headers)

    assert response.status_code == 201

    data = response.json()

    assert "rsvp" in data
    assert data["rsvp"]["attendee_id"] == 1
    assert data["rsvp"]["event_id"] == 1

def test_create_rsvp_returns_401_when_token_is_missing():
    response = client.post("/api/events/1/rsvp")

    assert response.status_code == 401

def test_create_rsvp_returns_404_when_event_does_not_exist(auth_headers):
    response = client.post("/api/events/999/rsvp", headers=auth_headers)

    assert response.status_code == 404

def test_create_rsvp_returns_409_when_user_already_rsvped(auth_headers_user_2):
    response = client.post("/api/events/1/rsvp", headers=auth_headers_user_2)

    assert response.status_code == 409

def test_create_rsvp_returns_401_when_token_is_invalid():
    response = client.post(
        "/api/events/1/rsvp",
        headers={"Authorization": "Bearer not-a-real-token"},
    )

    assert response.status_code == 401

def test_delete_rsvp_returns_204_when_user_has_rsvped(auth_headers_user_2):
    response = client.delete("/api/events/1/rsvp/me", headers=auth_headers_user_2)

    assert response.status_code == 204
    assert response.content == b""


def test_delete_rsvp_returns_401_when_token_is_missing():
    response = client.delete("/api/events/1/rsvp/me")

    assert response.status_code == 401


def test_delete_rsvp_returns_401_when_token_is_invalid():
    response = client.delete(
        "/api/events/1/rsvp/me",
        headers={"Authorization": "Bearer not-a-real-token"},
    )

    assert response.status_code == 401

def test_delete_rsvp_returns_404_when_rsvp_does_not_exist(auth_headers):
    response = client.delete("/api/events/999/rsvp/me", headers=auth_headers)

    assert response.status_code == 404    

def test_create_event_returns_201_and_event(auth_headers):
    response = client.post(
        "/api/events",
        headers=auth_headers,
        json={
            "title": "Summer Rooftop Social",
            "description": "An evening of networking and good vibes.",
            "starts_at": "2026-08-15T18:00:00Z",
            "ends_at": "2026-08-15T21:00:00Z",
            "venue_id": 2,
        },
    )

    assert response.status_code == 201

    data = response.json()

    assert "event" in data
    assert data["event"]["title"] == "Summer Rooftop Social"
    assert data["event"]["description"] == "An evening of networking and good vibes."
    assert data["event"]["venue_id"] == 2
    assert data["event"]["organiser_id"] == 1
    assert "created_at" in data["event"]


def test_create_event_uses_token_user_as_organiser(auth_headers):
    response = client.post(
        "/api/events",
        headers=auth_headers,
        json={
            "title": "Organiser Check Event",
            "description": "Checking organiser comes from token.",
            "starts_at": "2026-09-15T18:00:00Z",
            "ends_at": "2026-09-15T21:00:00Z",
            "venue_id": 2,
            "organiser_id": 999,
        },
    )

    assert response.status_code == 201

    data = response.json()

    assert data["event"]["organiser_id"] == 1


def test_create_event_returns_401_when_token_is_missing():
    response = client.post(
        "/api/events",
        json={
            "title": "No Token Event",
            "description": "This should not be created.",
            "starts_at": "2026-08-15T18:00:00Z",
            "ends_at": "2026-08-15T21:00:00Z",
            "venue_id": 2,
        },
    )

    assert response.status_code == 401


def test_create_event_returns_401_when_token_is_invalid():
    response = client.post(
        "/api/events",
        headers={"Authorization": "Bearer not-a-real-token"},
        json={
            "title": "Invalid Token Event",
            "description": "This should not be created.",
            "starts_at": "2026-08-15T18:00:00Z",
            "ends_at": "2026-08-15T21:00:00Z",
            "venue_id": 2,
        },
    )

    assert response.status_code == 401


def test_create_event_returns_400_when_required_field_is_missing(auth_headers):
    response = client.post(
        "/api/events",
        headers=auth_headers,
        json={
            "title": "Missing Field Event",
            "description": "This is missing venue_id.",
            "starts_at": "2026-08-15T18:00:00Z",
            "ends_at": "2026-08-15T21:00:00Z",
        },
    )

    assert response.status_code == 400


def test_create_event_returns_400_when_date_format_is_invalid(auth_headers):
    response = client.post(
        "/api/events",
        headers=auth_headers,
        json={
            "title": "Bad Date Event",
            "description": "This has an invalid date.",
            "starts_at": "not-a-date",
            "ends_at": "2026-08-15T21:00:00Z",
            "venue_id": 2,
        },
    )

    assert response.status_code == 400

def test_patch_event_returns_200_and_updated_event(auth_headers):
    response = client.patch(
        "/api/events/1",
        headers=auth_headers,
        json={
            "description": "Updated description with live music.",
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert "event" in data
    assert data["event"]["id"] == 1
    assert data["event"]["description"] == "Updated description with live music."


def test_patch_event_keeps_omitted_fields_unchanged(auth_headers):
    response = client.patch(
        "/api/events/1",
        headers=auth_headers,
        json={
            "description": "Only the description changed.",
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["event"]["title"] == "Leeds Tech Meetup – June Edition"
    assert data["event"]["description"] == "Only the description changed."


def test_patch_event_returns_401_when_token_is_missing():
    response = client.patch(
        "/api/events/1",
        json={
            "description": "This should not update.",
        },
    )

    assert response.status_code == 401


def test_patch_event_returns_401_when_token_is_invalid():
    response = client.patch(
        "/api/events/1",
        headers={"Authorization": "Bearer not-a-real-token"},
        json={
            "description": "This should not update.",
        },
    )

    assert response.status_code == 401


def test_patch_event_returns_403_when_user_is_not_organiser(auth_headers_user_2):
    response = client.patch(
        "/api/events/1",
        headers=auth_headers_user_2,
        json={
            "description": "User 2 should not be able to update this.",
        },
    )

    assert response.status_code == 403


def test_patch_event_returns_404_when_event_does_not_exist(auth_headers):
    response = client.patch(
        "/api/events/999",
        headers=auth_headers,
        json={
            "description": "This event does not exist.",
        },
    )

    assert response.status_code == 404


def test_patch_event_returns_400_when_date_format_is_invalid(auth_headers):
    response = client.patch(
        "/api/events/1",
        headers=auth_headers,
        json={
            "starts_at": "not-a-date",
        },
    )

    assert response.status_code == 400


def test_patch_event_returns_400_when_ends_at_is_before_starts_at(auth_headers):
    response = client.patch(
        "/api/events/1",
        headers=auth_headers,
        json={
            "starts_at": "2026-08-15T21:00:00Z",
            "ends_at": "2026-08-15T18:00:00Z",
        },
    )

    assert response.status_code == 400

def test_get_event_attendees_returns_200_and_attendees(auth_headers):
    response = client.get("/api/events/1/attendees", headers=auth_headers)

    assert response.status_code == 200

    data = response.json()

    assert "attendees" in data
    assert len(data["attendees"]) > 0

    first_attendee = data["attendees"][0]

    assert "id" in first_attendee
    assert "name" in first_attendee
    assert "email" in first_attendee


def test_get_event_attendees_does_not_return_passwords(auth_headers):
    response = client.get("/api/events/1/attendees", headers=auth_headers)

    assert response.status_code == 200

    data = response.json()

    for attendee in data["attendees"]:
        assert "password" not in attendee


def test_get_event_attendees_returns_401_when_token_is_missing():
    response = client.get("/api/events/1/attendees")

    assert response.status_code == 401


def test_get_event_attendees_returns_401_when_token_is_invalid():
    response = client.get(
        "/api/events/1/attendees",
        headers={"Authorization": "Bearer not-a-real-token"},
    )

    assert response.status_code == 401


def test_get_event_attendees_returns_403_when_user_is_not_organiser(auth_headers_user_2):
    response = client.get("/api/events/1/attendees", headers=auth_headers_user_2)

    assert response.status_code == 403


def test_get_event_attendees_returns_404_when_event_does_not_exist(auth_headers):
    response = client.get("/api/events/999/attendees", headers=auth_headers)

    assert response.status_code == 404

def test_get_my_events_returns_200_and_events(auth_headers):
    response = client.get("/api/user/me/events", headers=auth_headers)

    assert response.status_code == 200

    data = response.json()

    assert "events" in data
    assert len(data["events"]) > 0

    first_event = data["events"][0]

    assert "id" in first_event
    assert "title" in first_event
    assert "starts_at" in first_event
    assert "rsvp_date" in first_event
    assert "event_rank" in first_event
    assert "total_rsvps" in first_event


def test_get_my_events_returns_event_rank_and_total_rsvps(auth_headers):
    response = client.get("/api/user/me/events", headers=auth_headers)

    assert response.status_code == 200

    data = response.json()

    events = data["events"]

    assert events[0]["event_rank"] == 1

    for event in events:
        assert event["total_rsvps"] == len(events)


def test_get_my_events_returns_401_when_token_is_missing():
    response = client.get("/api/user/me/events")

    assert response.status_code == 401


def test_get_my_events_returns_401_when_token_is_invalid():
    response = client.get(
        "/api/user/me/events",
        headers={"Authorization": "Bearer not-a-real-token"},
    )

    assert response.status_code == 401