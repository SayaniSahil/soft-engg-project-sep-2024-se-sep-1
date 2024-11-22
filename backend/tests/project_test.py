from datetime import datetime
import json
from components.models import Project, db

project_id = None

def test_create_project(admin_setup_data):
    global project_id
    token,client=admin_setup_data
    headers={'Authentication-Token': f'{token}'}
    # Valid project creation
    response = client.post(
        "/projects",
        headers=headers,
        data=json.dumps({
            "title": "Test Project",
            "description": "Test Description"
        }),
        content_type="application/json"
    )
    assert response.status_code == 201
    data = response.get_json()
    assert data["message"] == "Project created successfully"
    assert data["project"]["title"] == "Test Project"
    project_id = data["project"]["project_id"]
    assert project_id != None

    # Missing fields
    response = client.post(
        "/projects",
        headers=headers,
        data=json.dumps({"title": ""}),
        content_type="application/json"
    )
    assert response.status_code == 400
    assert response.get_json()["message"] == "Title and description are required"


def test_get_projects(admin_setup_data):

    token,client=admin_setup_data
    headers={'Authentication-Token': f'{token}'}

    response = client.get("/projects", headers=headers)
    assert response.status_code == 200
    data = response.get_json()


def test_get_project(admin_setup_data):
    global project_id
    token,client=admin_setup_data
    headers={'Authentication-Token': f'{token}'}

    response = client.get(f"/projects/{project_id}", headers=headers)
    assert response.status_code == 200
    data = response.get_json()
    assert data["title"] == "Test Project"

    # Invalid project ID
    response = client.get("/projects/999", headers=headers)
    assert response.status_code == 404


def test_update_project(admin_setup_data):
    global project_id
    token,client=admin_setup_data
    headers={'Authentication-Token': f'{token}'}

    response = client.put(
        f"/projects/{project_id}",
        headers=headers,
        data=json.dumps({"title": "New Title"}),
        content_type="application/json"
    )
    assert response.status_code == 200
    data = response.get_json()
    assert data["project"]["title"] == "New Title"

    # Missing fields
    response = client.put(
        f"/projects/{project_id}",
        headers=headers,
        data=json.dumps({}),
        content_type="application/json"
    )
    assert response.status_code == 400
    assert response.get_json()["error"] == "Title and description are required"


def test_delete_project(admin_setup_data):
    global project_id
    token,client=admin_setup_data
    headers={'Authentication-Token': f'{token}'}

    response = client.delete(f"/projects/{project_id}", headers=headers)
    assert response.status_code == 200
    assert response.get_json()["message"] == "Project deleted successfully"

    response = client.get(f"/projects/{project_id}", headers=headers)
    # Verify deletion
    assert response.status_code == 404

    # Invalid project ID
    response = client.delete("/projects/999", headers=headers)
    assert response.status_code == 404
