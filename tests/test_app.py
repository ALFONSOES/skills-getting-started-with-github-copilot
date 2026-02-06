from fastapi.testclient import TestClient
from src.app import app
import urllib.parse

client = TestClient(app)


def test_get_activities():
    resp = client.get("/activities")
    assert resp.status_code == 200
    data = resp.json()
    assert isinstance(data, dict)
    # Ensure a known activity exists and has participants key
    assert "Equipo de Baloncesto" in data
    assert "participants" in data["Equipo de Baloncesto"]


def test_signup_and_remove_participant():
    activity = "Club de Ajedrez"
    email = "testuser@example.com"
    quoted = urllib.parse.quote(activity, safe="")

    # Sign up the test user
    resp = client.post(f"/activities/{quoted}/signup", params={"email": email})
    assert resp.status_code == 200
    body = resp.json()
    assert "Signed up" in body.get("message", "")

    # Confirm the participant was added
    resp2 = client.get("/activities")
    participants = resp2.json()[activity]["participants"]
    assert email in participants

    # Remove the participant
    resp3 = client.post(f"/activities/{quoted}/remove", params={"email": email})
    assert resp3.status_code == 200
    body3 = resp3.json()
    assert "Removed" in body3.get("message", "")

    # Confirm removal
    resp4 = client.get("/activities")
    participants2 = resp4.json()[activity]["participants"]
    assert email not in participants2
