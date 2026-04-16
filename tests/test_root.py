"""
Tests for the root endpoint (GET /).

Verifies redirect behavior to static index.html file.
"""

import pytest


def test_root_redirect(client):
    """GET / should redirect to /static/index.html"""
    response = client.get("/", follow_redirects=False)
    assert response.status_code in (307, 308)
    assert response.headers["location"] == "/static/index.html"


def test_root_redirect_has_location_header(client):
    """GET / response should include Location header"""
    response = client.get("/", follow_redirects=False)
    assert "location" in response.headers
    assert response.headers["location"] == "/static/index.html"
