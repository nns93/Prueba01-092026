"""
Tests for DELETE /activities/{activity_name}/participants/{email} endpoint

AAA Pattern (Arrange-Act-Assert):
- Arrange: Set up test data (activity with participant) via fixtures
- Act: Make DELETE request to unregister endpoint
- Assert: Verify status code, response message, and side effects (participant removed/not removed)
"""

import pytest


class TestUnregisterFromActivity:
    """Tests for the DELETE /activities/{activity_name}/participants/{email} endpoint"""
    
    def test_successful_unregistration(self, client, reset_activities, sample_activity_with_participant):
        """
        Test: Student can successfully unregister from an activity
        
        Arrange: Activity has a participant (via fixture)
        Act: DELETE request to unregister that participant
        Assert: Status 200, response contains success message, participant removed from activity
        """
        # Arrange
        activity_name = sample_activity_with_participant["activity_name"]
        email = sample_activity_with_participant["participant_email"]
        
        # Verify participant is in activity before deletion
        from src.app import activities
        assert email in activities[activity_name]["participants"]
        
        # Act
        response = client.delete(
            f"/activities/{activity_name}/participants/{email}"
        )
        
        # Assert
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert email in data["message"]
        assert activity_name in data["message"]
        
        # Verify participant was removed from activity
        assert email not in activities[activity_name]["participants"]
    
    def test_unregister_from_nonexistent_activity(self, client, reset_activities, sample_email):
        """
        Test: Unregister from non-existent activity returns 404
        
        Arrange: Invalid activity name prepared
        Act: DELETE request with non-existent activity
        Assert: Status 404, error detail message present
        """
        # Arrange
        activity_name = "Nonexistent Activity"
        email = sample_email
        
        # Act
        response = client.delete(
            f"/activities/{activity_name}/participants/{email}"
        )
        
        # Assert
        assert response.status_code == 404
        data = response.json()
        assert "detail" in data
        assert "not found" in data["detail"].lower()
    
    def test_unregister_nonexistent_participant_returns_400(
        self, client, reset_activities, sample_activity, sample_email
    ):
        """
        Test: Unregister participant who is not signed up returns 400
        
        Arrange: Email is not in activity participants list
        Act: DELETE request for non-existent participant
        Assert: Status 400, error detail about not signed up
        """
        # Arrange
        activity_name = sample_activity
        email = sample_email
        
        from src.app import activities
        # Verify email is not in the activity
        assert email not in activities[activity_name]["participants"]
        
        # Act
        response = client.delete(
            f"/activities/{activity_name}/participants/{email}"
        )
        
        # Assert
        assert response.status_code == 400
        data = response.json()
        assert "detail" in data
        assert "not signed up" in data["detail"].lower()
    
    def test_unregister_response_format(
        self, client, reset_activities, sample_activity_with_participant
    ):
        """
        Test: Unregister response has correct format
        
        Arrange: Activity with participant ready
        Act: Make successful unregister DELETE request
        Assert: Response is JSON dict with "message" key
        """
        # Arrange
        activity_name = sample_activity_with_participant["activity_name"]
        email = sample_activity_with_participant["participant_email"]
        
        # Act
        response = client.delete(
            f"/activities/{activity_name}/participants/{email}"
        )
        
        # Assert
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, dict)
        assert "message" in data
        assert isinstance(data["message"], str)
    
    def test_cannot_unregister_twice(
        self, client, reset_activities, sample_activity_with_participant
    ):
        """
        Test: Cannot unregister same participant twice from same activity
        
        Arrange: Activity has a participant
        Act: DELETE same participant twice
        Assert: First DELETE succeeds (200), second DELETE fails (400)
        """
        # Arrange
        activity_name = sample_activity_with_participant["activity_name"]
        email = sample_activity_with_participant["participant_email"]
        
        # Act - First unregister
        response1 = client.delete(
            f"/activities/{activity_name}/participants/{email}"
        )
        
        # Act - Second unregister (should fail)
        response2 = client.delete(
            f"/activities/{activity_name}/participants/{email}"
        )
        
        # Assert
        assert response1.status_code == 200
        assert response2.status_code == 400
        data = response2.json()
        assert "detail" in data
        assert "not signed up" in data["detail"].lower()
    
    def test_unregister_only_removes_specific_participant(
        self, client, reset_activities, sample_activity
    ):
        """
        Test: Unregistering one participant doesn't affect others
        
        Arrange: Two participants in same activity
        Act: Unregister first participant
        Assert: First participant removed, second participant still in activity
        """
        # Arrange
        activity_name = sample_activity
        email1 = "student1@mergington.edu"
        email2 = "student2@mergington.edu"
        
        from src.app import activities
        # Add both participants
        activities[activity_name]["participants"].extend([email1, email2])
        assert email1 in activities[activity_name]["participants"]
        assert email2 in activities[activity_name]["participants"]
        
        # Act - Unregister first participant
        response = client.delete(
            f"/activities/{activity_name}/participants/{email1}"
        )
        
        # Assert
        assert response.status_code == 200
        assert email1 not in activities[activity_name]["participants"]
        assert email2 in activities[activity_name]["participants"]
