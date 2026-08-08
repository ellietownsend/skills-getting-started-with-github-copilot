from fastapi.testclient import TestClient

from src.app import app


client = TestClient(app)


def test_unregister_participant_removes_their_email_from_activity():
    email = "delete-me@example.com"

    signup_response = client.post(
        f"/activities/Chess Club/signup?email={email}"
    )
    assert signup_response.status_code == 200

    delete_response = client.delete(f"/activities/Chess Club/participants/{email}")
    assert delete_response.status_code == 200

    activities_response = client.get("/activities")
    assert activities_response.status_code == 200
    data = activities_response.json()["Chess Club"]
    assert email not in data["participants"]
