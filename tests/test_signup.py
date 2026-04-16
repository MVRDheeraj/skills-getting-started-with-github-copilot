"""
Tests for the signup endpoint (POST /activities/{activity_name}/signup).

Verifies success cases, error conditions, and participant list mutation.
"""

import pytest


def test_signup_success(client):
    """Successful signup should return 200 with confirmation message"""
    response = client.post(
        "/activities/Chess%20Club/signup?email=test@example.com"
    )
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert "test@example.com" in data["message"]
    assert "Chess Club" in data["message"]


def test_signup_adds_participant(client):
    """Signup should add email to activity's participants list"""
    email = "newstudent@mergington.edu"
    activity_name = "Chess Club"
    
    # Get initial state
    response = client.get("/activities")
    initial_data = response.json()
    initial_count = len(initial_data[activity_name]["participants"])
    
    # Sign up
    response = client.post(f"/activities/{activity_name}/signup?email={email}")
    assert response.status_code == 200
    
    # Verify participant was added
    response = client.get("/activities")
    updated_data = response.json()
    assert email in updated_data[activity_name]["participants"]
    assert len(updated_data[activity_name]["participants"]) == initial_count + 1


def test_signup_activity_not_found(client):
    """Signup to non-existent activity should return 404"""
    response = client.post(
        "/activities/NonExistentActivity/signup?email=test@example.com"
    )
    assert response.status_code == 404
    data = response.json()
    assert "Activity not found" in data.get("detail", "")


def test_signup_duplicate_returns_400(client):
    """Signing up twice with same email should return 400"""
    email = "duplicate@example.com"
    activity_name = "Chess Club"
    
    # First signup
    response = client.post(
        f"/activities/{activity_name}/signup?email={email}"
    )
    assert response.status_code == 200
    
    # Second signup with same email
    response = client.post(
        f"/activities/{activity_name}/signup?email={email}"
    )
    assert response.status_code == 400
    data = response.json()
    assert "already signed up" in data.get("detail", "").lower()


def test_signup_missing_email_fails(client):
    """Signup without email parameter should fail validation"""
    response = client.post("/activities/Chess%20Club/signup")
    assert response.status_code in (400, 422)


def test_signup_with_special_characters_in_email(client):
    """Signup should handle email with special characters"""
    from urllib.parse import quote
    email = "user+tag@example.com"
    activity_name = "Programming Class"
    
    response = client.post(
        f"/activities/{activity_name}/signup?email={quote(email)}"
    )
    assert response.status_code == 200
    
    # Verify it was stored
    response = client.get("/activities")
    data = response.json()
    assert email in data[activity_name]["participants"]
