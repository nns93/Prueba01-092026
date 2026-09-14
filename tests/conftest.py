"""
pytest configuration and shared fixtures for FastAPI tests

This module provides:
- TestClient fixture for making HTTP requests to the FastAPI app
- Sample activities data fixture for Arrange phase of tests
- Helper fixtures for common test scenarios
"""

import pytest
from fastapi.testclient import TestClient
from src.app import app, activities


@pytest.fixture
def client():
    """
    Fixture: Provides a TestClient for making HTTP requests
    
    Used in Arrange phase to set up the test client.
    """
    return TestClient(app)


@pytest.fixture
def reset_activities():
    """
    Fixture: Saves and resets activities data before/after each test
    
    Ensures test isolation by restoring original activities dict.
    Use this fixture in any test that modifies the activities dict.
    
    Usage:
        def test_something(client, reset_activities):
            # Activities dict is clean for this test
            ...
    """
    original_activities = activities.copy()
    
    # Clear existing participants but keep activity structure
    for activity_name in activities:
        activities[activity_name]["participants"] = []
    
    yield
    
    # Restore original state after test
    activities.clear()
    activities.update(original_activities)


@pytest.fixture
def sample_email():
    """Fixture: Provides a sample test email for signup tests"""
    return "test_student@mergington.edu"


@pytest.fixture
def sample_activity():
    """Fixture: Provides a sample activity name from the activities dict"""
    return "Chess Club"


@pytest.fixture
def sample_activity_with_participant(reset_activities):
    """
    Fixture: Sets up an activity with a participant for testing
    
    Arrange phase: Adds a participant to Chess Club activity
    """
    activity_name = "Chess Club"
    participant_email = "existing_student@mergington.edu"
    activities[activity_name]["participants"].append(participant_email)
    
    return {
        "activity_name": activity_name,
        "participant_email": participant_email
    }
