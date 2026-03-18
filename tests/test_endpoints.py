"""Integration tests for FastAPI endpoints."""

def test_get_root_redirects_to_index(client):
    """Test that GET / redirects to static index.html."""
    response = client.get("/")
    assert response.status_code == 200
    # FastAPI redirects to static files, so we check the response
    assert "text/html" in response.headers.get("content-type", "")


def test_get_activities_returns_all_activities(client):
    """Test GET /activities returns all activities."""
    response = client.get("/activities")
    assert response.status_code == 200

    data = response.json()
    assert isinstance(data, dict)
    assert len(data) == 9  # Should have 9 activities

    # Check that expected activities are present
    expected_activities = [
        "Chess Club", "Programming Class", "Gym Class", "Basketball Team",
        "Tennis Club", "Debate Club", "Science Olympiad", "Drama Club", "Art Studio"
    ]

    for activity in expected_activities:
        assert activity in data
        assert "description" in data[activity]
        assert "schedule" in data[activity]
        assert "max_participants" in data[activity]
        assert "participants" in data[activity]
        assert isinstance(data[activity]["participants"], list)


def test_post_signup_success(client):
    """Test successful signup for an activity."""
    response = client.post("/activities/Chess Club/signup?email=test@mergington.edu")
    assert response.status_code == 200

    data = response.json()
    assert "message" in data
    assert "Signed up" in data["message"]


def test_post_signup_activity_not_found(client):
    """Test signup for non-existent activity returns 404."""
    response = client.post("/activities/Nonexistent Activity/signup?email=test@mergington.edu")
    assert response.status_code == 404

    data = response.json()
    assert "detail" in data
    assert "not found" in data["detail"].lower()


def test_delete_unregister_success(client):
    """Test successful unregistration from an activity."""
    # First sign up
    client.post("/activities/Programming Class/signup?email=test@mergington.edu")

    # Then unregister
    response = client.delete("/activities/Programming Class/unregister?email=test@mergington.edu")
    assert response.status_code == 200

    data = response.json()
    assert "message" in data
    assert "unregistered" in data["message"].lower()


def test_delete_unregister_activity_not_found(client):
    """Test unregister from non-existent activity returns 404."""
    response = client.delete("/activities/Nonexistent Activity/unregister?email=test@mergington.edu")
    assert response.status_code == 404

    data = response.json()
    assert "detail" in data
    assert "not found" in data["detail"].lower()


def test_delete_unregister_not_signed_up(client):
    """Test unregister when student is not signed up returns 400."""
    response = client.delete("/activities/Chess Club/unregister?email=notsignedup@mergington.edu")
    assert response.status_code == 400

    data = response.json()
    assert "detail" in data
    assert "not signed up" in data["detail"].lower()