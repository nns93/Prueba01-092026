"""
Tests for POST /activities/{activity_name}/signup endpoint

AAA Pattern (Arrange-Act-Assert):
- Arrange: Set up test data (activity name, email) via fixtures
- Act: Make POST request to signup endpoint
- Assert: Verify status code, response message, and side effects (participant added/not added)
"""

import pytest


class TestSignupForActivity:
    """Tests for the POST /activities/{activity_name}/signup endpoint"""
    
    def test_successful_signup(self, client, reset_activities, sample_activity, sample_email):
        """
        Test: Student can successfully sign up for an activity
        
        Arrange: Sample activity and email are ready
        Act: POST request to signup endpoint with valid activity and email
        Assert: Status 200, response contains success message, participant added to activity
        """
        # Arrange
        activity_name = sample_activity
        email = sample_email
        
        # Act
        response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )
        
        # Assert
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert email in data["message"]
        assert activity_name in data["message"]
        
        # Verify participant was added to activity
        from src.app import activities
        assert email in activities[activity_name]["participants"]
    
    def test_signup_to_nonexistent_activity(self, client, reset_activities, sample_email):
        """
        Test: Signup to non-existent activity returns 404
        
        Arrange: Invalid activity name prepared
        Act: POST request to signup with non-existent activity
        Assert: Status 404, error detail message present
        """
        # Arrange
        activity_name = "Nonexistent Activity"
        email = sample_email
        
        # Act
        response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )
        
        # Assert
        assert response.status_code == 404
        data = response.json()
        assert "detail" in data
        assert "not found" in data["detail"].lower()
    
    def test_duplicate_signup_returns_400(
        self, client, reset_activities, sample_activity_with_participant
    ):
        """
        Test: Duplicate signup (already signed up) returns 400
        
        Arrange: Activity has a participant already (via fixture)
        Act: Try to POST same participant to same activity again
        Assert: Status 400, error detail about already signed up
        """
        # Arrange
        activity_name = sample_activity_with_participant["activity_name"]
        email = sample_activity_with_participant["participant_email"]
        
        # Act
        response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )
        
        # Assert
        assert response.status_code == 400
        data = response.json()
        assert "detail" in data
        assert "already" in data["detail"].lower()
    
    def test_signup_response_format(self, client, reset_activities, sample_activity, sample_email):
        """
        Test: Signup response has correct format
        
        Arrange: Valid signup parameters ready
        Act: Make successful signup POST request
        Assert: Response is JSON dict with "message" key containing activity and email
        """
        # Arrange
        activity_name = sample_activity
        email = sample_email
        
        # Act
        response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )
        
        # Assert
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, dict)
        assert "message" in data
        assert isinstance(data["message"], str)
    
    def test_multiple_participants_can_signup(self, client, reset_activities, sample_activity):
        """
        Test: Multiple different students can sign up for the same activity
        
        Arrange: Multiple unique emails prepared
        Act: Sign up two different students to same activity
        Assert: Both students successfully added to activity participants list
        """
        # Arrange
        activity_name = sample_activity
        email1 = "student1@mergington.edu"
        email2 = "student2@mergington.edu"
        
        # Act - First signup
        response1 = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email1}
        )
        
        # Act - Second signup
        response2 = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email2}
        )
        
        # Assert
        assert response1.status_code == 200
        assert response2.status_code == 200
        
        from src.app import activities
        participants = activities[activity_name]["participants"]
        assert email1 in participants
        assert email2 in participants
