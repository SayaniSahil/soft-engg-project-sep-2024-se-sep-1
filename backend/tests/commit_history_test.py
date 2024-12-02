import pytest
from unittest.mock import patch, MagicMock




@pytest.fixture
def mock_github_token(monkeypatch):
    monkeypatch.setenv("GITHUB_TOKEN", "mock_github_token")

@pytest.fixture
def mock_project_assignment():
    mock_assignment = MagicMock()
    mock_assignment.github_url = "https://github.com/user/repo"
    return mock_assignment

# Mock database query


def test_commit_history_success(admin_setup_data):
    token,client=admin_setup_data
    headers={'Authentication-Token': f'{token}'}

    response = client.get("/commit_history/1/3",headers=headers)

    assert response.status_code == 200
    json_data = response.get_json()

    assert json_data["student_id"] == 3
    assert json_data["project_id"] == 1
# 



# Test case: Student not enrolled in project

def test_student_not_enrolled(admin_setup_data):
    token,client=admin_setup_data
    headers={'Authentication-Token': f'{token}'}
    response = client.get("/commit_history/1/2")

    assert response.status_code == 404
    assert response.get_json() == {"error": "Student is not enrolled in this project"}

# Test case: No GitHub URL for student

def test_no_github_url(admin_setup_data):
    token,client=admin_setup_data
    headers={'Authentication-Token': f'{token}'}

    response = client.get("/commit_history/1/1")

    assert response.status_code == 400
    assert response.get_json() == {"error": "GitHub URL not available for this student"}

# Test case: GitHub API failure

def test_github_api_failure(admin_setup_data):
    token,client=admin_setup_data
    headers={'Authentication-Token': f'{token}'}

def test_missing_github_token(admin_setup_data , monkeypatch):
    token,client=admin_setup_data
    headers={'Authentication-Token': f'{token}'}
    monkeypatch.delenv("GITHUB_TOKEN", raising=False)
    

    response = client.get("/commit_history/1/3")

    assert response.status_code == 500
    assert response.get_json() == {"error": "Failed to fetch commit history"}
