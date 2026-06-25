from fastapi.testclient import TestClient
from main import app


client = TestClient(app)


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