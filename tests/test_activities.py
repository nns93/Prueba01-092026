"""
Tests for GET /activities endpoint

AAA Pattern (Arrange-Act-Assert):
- Arrange: Set up TestClient via fixture
- Act: Call client.get("/activities")
- Assert: Verify status code, response structure, and data
"""

import pytest


class TestGetActivities:
    """Tests for the GET /activities endpoint"""
    
    def test_get_activities_returns_all_activities(self, client):
        """
        Test: GET /activities returns all activities
        
        Arrange: TestClient is set up via fixture
        Act: Make GET request to /activities
        Assert: Response status is 200 and contains all activities
        """
        # Arrange is handled by client fixture
        
        # Act
        response = client.get("/activities")
        
        # Assert
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, dict)
        assert len(data) > 0
        # Verify expected activities are present
        expected_activities = {
            "Chess Club",
            "Programming Class",
            "Gym Class",
            "Basketball Team",
            "Volleyball Club",
            "Art Studio",
            "Music Band",
            "Debate Team",
            "Science Club"
        }
        actual_activities = set(data.keys())
        assert expected_activities == actual_activities
    
    def test_get_activities_returns_correct_structure(self, client):
        """
        Test: GET /activities returns activities with correct structure
        
        Arrange: TestClient is set up via fixture
        Act: Make GET request to /activities
        Assert: Each activity has required fields (description, schedule, max_participants, participants)
        """
        # Arrange is handled by client fixture
        
        # Act
        response = client.get("/activities")
        data = response.json()
        
        # Assert
        required_fields = {"description", "schedule", "max_participants", "participants"}
        for activity_name, activity_data in data.items():
            assert isinstance(activity_name, str), f"Activity name should be string"
            assert isinstance(activity_data, dict), f"Activity data should be dict"
            assert required_fields.issubset(
                activity_data.keys()
            ), f"Activity '{activity_name}' missing required fields"
            
            # Verify field types
            assert isinstance(activity_data["description"], str)
            assert isinstance(activity_data["schedule"], str)
            assert isinstance(activity_data["max_participants"], int)
            assert isinstance(activity_data["participants"], list)
            assert all(
                isinstance(email, str) for email in activity_data["participants"]
            ), "All participants should be email strings"
    
    def test_get_activities_contains_participants(self, client):
        """
        Test: GET /activities returns activities with participant lists
        
        Arrange: TestClient is set up via fixture
        Act: Make GET request to /activities
        Assert: Activities have participants list (may be empty or populated)
        """
        # Arrange is handled by client fixture
        
        # Act
        response = client.get("/activities")
        data = response.json()
        
        # Assert
        activities_with_participants = [
            name for name, info in data.items()
            if len(info["participants"]) > 0
        ]
        # At least some activities should have participants pre-populated
        assert len(activities_with_participants) > 0, "Expected activities with existing participants"
