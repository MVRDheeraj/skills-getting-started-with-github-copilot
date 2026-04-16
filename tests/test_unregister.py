"""
Tests for the unregister endpoint (DELETE /activities/{activity_name}/participants).

Verifies success cases, error conditions, and participant list mutation.
"""

import pytest


def test_unregister_success(client):
    """Successful unregister should return 200 with confirmation message"""
    # First sign up
    email = "todelete@example.com"
    activity_name = "Chess Club"
    client.post(f"/activities/{activity_name}/signup?email={email}")
    
    # Then unregister
    response = client.delete(
        f"/activities/{activity_name}/participants?email={email}"
    )
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert "Unregistered" in data["message"] or "unregistered" in data["message"].lower()


def test_unregister_removes_participant(client):
    """Unregister should remove email from activity's participants list"""
    email = "todelete2@example.com"
    activity_name = "Programming Class"
    
    # Sign up first
    response = client.post(f"/activities/{activity_name}/signup?email={email}")
    assert response.status_code == 200
    
    # Verify participant is in list
    response = client.get("/activities")
    data = response.json()
    assert email in data[activity_name]["participants"]
    initial_count = len(data[activity_name]["participants"])
    
    # Unregister
    response = client.delete(
        f"/activities/{activity_name}/participants?email={email}"
    )
    assert response.status_code == 200
    
    # Verify participant was removed
    response = client.get("/activities")
    data = response.json()
    assert email not in data[activity_name]["participants"]
    assert len(data[activity_name]["participants"]) == initial_count - 1


def test_unregister_activity_not_found(client):
    """Unregister from non-existent activity should return 404"""
    response = client.delete(
        "/activities/NonExistentActivity/participants?email=test@example.com"
    )
    assert response.status_code == 404
    data = response.json()
    assert "Activity not found" in data.get("detail", "")


def test_unregister_student_not_in_activity(client):
    """Unregister student not in activity should return 404"""
    response = client.delete(
        "/activities/Chess%20Club/participants?email=notregistered@example.com"
    )
    assert response.status_code == 404
    data = response.json()
    assert "not found" in data.get("detail", "").lower()


def test_unregister_missing_email_fails(client):
    """Unregister without email parameter should fail validation"""
    response = client.delete("/activities/Chess%20Club/participants")
    assert response.status_code in (400, 422)


def test_unregister_does_not_affect_other_activities(client):
    """Unregister from one activity should not affect others"""
    email = "multiactivity@example.com"
    activity1 = "Chess Club"
    activity2 = "Programming Class"
    
    # Sign up for both
    client.post(f"/activities/{activity1}/signup?email={email}")
    client.post(f"/activities/{activity2}/signup?email={email}")
    
    # Unregister from one
    response = client.delete(
        f"/activities/{activity1}/participants?email={email}"
    )
    assert response.status_code == 200
    
    # Verify removed from activity1 but still in activity2
    response = client.get("/activities")
    data = response.json()
    assert email not in data[activity1]["participants"]
    assert email in data[activity2]["participants"]
