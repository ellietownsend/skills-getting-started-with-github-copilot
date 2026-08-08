from fastapi.testclient import TestClient

from src.app import app


client = TestClient(app)


def test_get_activities_returns_activity_catalog():
    # Arrange
    expected_activity_names = {"Chess Club", "Programming Class", "Gym Class"}

    # Act
    response = client.get("/activities")

    # Assert
    assert response.status_code == 200
    data = response.json()
    assert expected_activity_names.issubset(data.keys())


def test_unregister_participant_removes_their_email_from_activity():
    # Arrange
    email = "delete-me-aaa@example.com"

    # Act
    signup_response = client.post(f"/activities/Chess Club/signup?email={email}")
    delete_response = client.delete(f"/activities/Chess Club/participants/{email}")
    activities_response = client.get("/activities")

    # Assert
    assert signup_response.status_code == 200
    assert delete_response.status_code == 200
    assert activities_response.status_code == 200

    data = activities_response.json()["Chess Club"]
    assert email not in data["participants"]


def test_signup_rejects_duplicate_participant():
    # Arrange
    email = "duplicate-me-aaa@example.com"

    # Act
    first_signup_response = client.post(f"/activities/Programming Class/signup?email={email}")
    second_signup_response = client.post(f"/activities/Programming Class/signup?email={email}")

    # Assert
    assert first_signup_response.status_code == 200
    assert second_signup_response.status_code == 400
    assert second_signup_response.json()["detail"] == "Student already signed up for this activity"
