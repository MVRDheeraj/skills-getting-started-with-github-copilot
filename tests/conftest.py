"""
Shared test fixtures for FastAPI backend tests.

Provides TestClient fixture and automatic state reset to prevent
cross-test contamination of in-memory activity data.
"""

import copy
import pytest
from fastapi.testclient import TestClient
from src.app import app, activities


@pytest.fixture
def client():
    """FastAPI TestClient fixture for endpoint testing."""
    return TestClient(app)


@pytest.fixture(autouse=True)
def reset_activities():
    """
    Auto-use fixture that snapshots and restores the in-memory activities
    dict before each test to prevent state bleed between tests.
    """
    # Snapshot original state
    original_activities = copy.deepcopy(activities)
    
    yield
    
    # Restore after test
    activities.clear()
    activities.update(original_activities)
