from fastapi.testclient import TestClient
from urllib.parse import quote

from src.app import app

client = TestClient(app)


def test_get_activities():
    res = client.get("/activities")
    assert res.status_code == 200
    data = res.json()
    assert isinstance(data, dict)
    assert "Basketball Team" in data


def test_signup_and_delete_participant():
    activity = "Basketball Team"
    email = "tester@example.com"
    enc_activity = quote(activity, safe="")

    # sign up
    res = client.post(f"/activities/{enc_activity}/signup", params={"email": email})
    assert res.status_code == 200
    assert "Signed up" in res.json().get("message", "")

    # verify participant present
    res = client.get("/activities")
    assert email in res.json()[activity]["participants"]

    # duplicate signup fails
    res = client.post(f"/activities/{enc_activity}/signup", params={"email": email})
    assert res.status_code == 400

    # remove participant
    res = client.delete(f"/activities/{enc_activity}/participants", params={"email": email})
    assert res.status_code == 200
    assert "Removed" in res.json().get("message", "")

    # verify removed
    res = client.get("/activities")
    assert email not in res.json()[activity]["participants"]

    # deleting again fails
    res = client.delete(f"/activities/{enc_activity}/participants", params={"email": email})
    assert res.status_code == 400


def test_signup_nonexistent_activity():
    res = client.post("/activities/Nonexistent/signup", params={"email": "a@b.c"})
    assert res.status_code == 404
