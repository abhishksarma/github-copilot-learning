from urllib.parse import quote

from src import app as app_module


def test_get_activities_returns_all_activities(client):
    # Arrange: client fixture provided

    # Act
    response = client.get("/activities")

    # Assert
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert "Chess Club" in data


def test_signup_adds_participant(client):
    # Arrange
    activity = "Chess Club"
    email = "testuser@example.com"
    before = list(app_module.activities[activity]["participants"])[:]

    # Act
    response = client.post(f"/activities/{quote(activity)}/signup", params={"email": email})

    # Assert
    assert response.status_code == 200
    assert email in app_module.activities[activity]["participants"]
    assert len(app_module.activities[activity]["participants"]) == len(before) + 1


def test_unregister_removes_participant(client):
    # Arrange
    activity = "Chess Club"
    email = "michael@mergington.edu"
    assert email in app_module.activities[activity]["participants"]

    # Act
    response = client.post(f"/activities/{quote(activity)}/unregister", params={"email": email})

    # Assert
    assert response.status_code == 200
    assert email not in app_module.activities[activity]["participants"]


def test_signup_nonexistent_activity_returns_404(client):
    # Arrange
    bad_activity = "NoSuchActivity"

    # Act
    response = client.post(f"/activities/{quote(bad_activity)}/signup", params={"email": "x@example.com"})

    # Assert
    assert response.status_code == 404


def test_unregister_non_member_returns_404(client):
    # Arrange
    activity = "Chess Club"
    nonmember = "nonmember@example.com"

    # Act
    response = client.post(f"/activities/{quote(activity)}/unregister", params={"email": nonmember})

    # Assert
    assert response.status_code == 404
