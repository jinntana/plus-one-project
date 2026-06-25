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