import json
from components.models import ProjectStudentAssignment, db

def test_create_assignment(admin_setup_data):
    # Setup variables
    token,client=admin_setup_data
    headers={'Authentication-Token': f'{token}'}

    # Test valid assignment creation
    response = client.post(
        "/assignment",
        headers=headers,
        data=json.dumps({
            "project_id": 1,  # Assuming project_id=1 exists in the database
            "github_url": "https://github.com/user/project"
        }),
        content_type="application/json"
    )
    assert response.status_code == 201
    data = response.get_json()
    assert data["message"] == "Assignment created successfully"
    assert data["project_id"] == 1
    assert data["github_url"] == "https://github.com/user/project"

    # Test assignment already exists
    response = client.post(
        "/assignment",
        headers=headers,
        data=json.dumps({
            "project_id": 1,
            "github_url": "https://github.com/user/project"
        }),
        content_type="application/json"
    )
    assert response.status_code == 409
    assert response.get_json()["error"] == "Assignment already exists"

    # Test missing fields
    response = client.post(
        "/assignment",
        headers=headers,
        data=json.dumps({"github_url": "https://github.com/user/project"}),
        content_type="application/json"
    )
    assert response.status_code == 400
    assert response.get_json()["error"] == "project_id and github_url are required"

    # Test invalid data (e.g., missing project_id)
    response = client.post(
        "/assignment",
        headers=headers,
        data=json.dumps({"project_id": 1}),
        content_type="application/json"
    )
    assert response.status_code == 400
    assert response.get_json()["error"] == "project_id and github_url are required"

    # Cleanup database
    assignment = ProjectStudentAssignment.query.filter_by(project_id=1).first()
    if assignment:
        db.session.delete(assignment)
        db.session.commit()
