import json
from datetime import datetime
from components.models import db, MilestoneSubmission

def test_submit_milestone(admin_setup_data):
    # Test valid submission
    token,client=admin_setup_data
    headers={'Authentication-Token': f'{token}'}
    valid_data = {
        "milestone_id": 1,
        "student_id": 101,
        "document_url": "http://example.com/document.pdf",
        "submission_date": "2024-11-24 10:00:00"
    }
    response = client.post(
        "/submitmilestone",
        
        data=json.dumps(valid_data),
        content_type="application/json",headers=headers
    )
    assert response.status_code == 201
    response_data = response.get_json()
    assert response_data["message"] == "Milestone submission successful"
    assert "submission_id" in response_data

    # Test missing required fields
    incomplete_data = {"milestone_id": 1, "student_id": 101}
    response = client.post(
        "/submitmilestone",
        data=json.dumps(incomplete_data),
        content_type="application/json",headers=headers)
    assert response.status_code == 400
    response_data = response.get_json()
    assert response_data["message"] == "Missing required fields "

  