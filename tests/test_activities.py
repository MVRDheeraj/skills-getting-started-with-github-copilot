"""
Tests for the activities listing endpoint (GET /activities).

Verifies response structure, required fields, and baseline payload.
"""

import pytest


def test_get_activities_returns_200(client):
    """GET /activities should return 200 OK"""
    response = client.get("/activities")
    assert response.status_code == 200


def test_get_activities_returns_dict(client):
    """GET /activities should return a dictionary"""
    response = client.get("/activities")
    data = response.json()
    assert isinstance(data, dict)
    assert len(data) > 0


def test_get_activities_has_required_fields(client):
    """Each activity should have required fields"""
    response = client.get("/activities")
    data = response.json()
    
    required_fields = {"description", "schedule", "max_participants", "participants"}
    
    for activity_name, activity_details in data.items():
        assert isinstance(activity_name, str)
        assert isinstance(activity_details, dict)
        for field in required_fields:
            assert field in activity_details, f"Missing field '{field}' in activity '{activity_name}'"


def test_get_activities_participants_is_list(client):
    """The 'participants' field should be a list"""
    response = client.get("/activities")
    data = response.json()
    
    for activity_name, activity_details in data.items():
        assert isinstance(activity_details["participants"], list)


def test_get_activities_returns_non_empty_initial_state(client):
    """GET /activities should return activities in initial state"""
    response = client.get("/activities")
    data = response.json()
    
    # Verify known activities exist in initial state
    assert "Chess Club" in data
    assert "Programming Class" in data
    assert "Gym Class" in data
