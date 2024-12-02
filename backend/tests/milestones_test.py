from datetime import datetime, timedelta
import json

milestone_id = None

def test_milestone_completion_rate(admin_setup_data, test_project):
    """Test milestone completion rate calculation"""
    global milestone_id
    token, client = admin_setup_data
    headers = {'Authentication-Token': f'{token}'}

    # Create milestone
    response = client.post(
        "/instructor/milestones",
        headers=headers,
        data=json.dumps({
            'title': 'Test Milestone',
            'description': 'Test Description',
            'start_date': datetime.now().strftime('%Y-%m-%d'),
            'end_date': (datetime.now() + timedelta(days=7)).strftime('%Y-%m-%d'),
            'project_id': test_project.project_id,
            'weightage': 20.0
        }),
        content_type="application/json"
    )
    assert response.status_code == 201
    milestone_id = response.get_json()['data']['milestone_id']

    # Add submissions
    for i in range(3):
        client.post(
            "/submitmilestone",
            headers=headers,
            data=json.dumps({
                'milestone_id': milestone_id,
                'student_id': i + 1,
                'document_url': 'test.pdf'
            }),
            content_type="application/json"
        )

    # Get milestone statistics
    response = client.get(
        f'/statistics/projects/{test_project.project_id}/milestone-statistics',
        headers=headers
    )
    assert response.status_code == 200
    data = response.get_json()
    assert len(data) == 1
    assert data[0]['completion_rate'] == 60  # 3 out of 5 students completed


def test_submission_tracking(admin_setup_data, test_project):
    """Test milestone submission creation and tracking"""
    token, client = admin_setup_data
    headers = {'Authentication-Token': f'{token}'}

    # Create a new submission
    response = client.post(
        "/submitmilestone",
        headers=headers,
        data=json.dumps({
            'milestone_id': milestone_id,
            'student_id': 5,
            'document_url': 'test.pdf'
        }),
        content_type="application/json"
    )
    assert response.status_code == 201
    submission_data = response.get_json()
    assert 'submission_id' in submission_data
from datetime import datetime, timedelta
import json

milestone_id = None

def test_create_milestone_success(admin_setup_data, test_project):
    """Test successful milestone creation"""
    global milestone_id
    token, client = admin_setup_data
    headers = {'Authentication-Token': f'{token}'}

    response = client.post(
        "/instructor/milestones",
        headers=headers,
        data=json.dumps({
            'title': 'Test Milestone',
            'description': 'Description',
            'start_date': datetime.now().strftime('%Y-%m-%d'),
            'end_date': (datetime.now() + timedelta(days=7)).strftime('%Y-%m-%d'),
            'project_id': test_project.project_id,
            'weightage': 20.0
        }),
        content_type="application/json"
    )
    assert response.status_code == 201
    data = response.get_json()
    assert data['status'] == 'success'
    milestone_id = data['data']['milestone_id']


def test_create_milestone_invalid_dates(admin_setup_data, test_project):
    """Test milestone creation with invalid date range"""
    token, client = admin_setup_data
    headers = {'Authentication-Token': f'{token}'}

    response = client.post(
        "/instructor/milestones",
        headers=headers,
        data=json.dumps({
            'title': 'Invalid Dates Milestone',
            'description': 'Description',
            'start_date': (datetime.now() + timedelta(days=7)).strftime('%Y-%m-%d'),
            'end_date': datetime.now().strftime('%Y-%m-%d'),
            'project_id': test_project.project_id
        }),
        content_type="application/json"
    )
    assert response.status_code == 400


def test_update_milestone_success(admin_setup_data):
    """Test successful milestone update"""
    token, client = admin_setup_data
    headers = {'Authentication-Token': f'{token}'}

    response = client.put(
        f"/instructor/milestones/{milestone_id}",
        headers=headers,
        data=json.dumps({
            'title': 'Updated Milestone Title',
            'description': 'Updated Milestone Description'
        }),
        content_type="application/json"
    )
    assert response.status_code == 200
    data = response.get_json()
    assert data['data']['title'] == 'Updated Milestone Title'


def test_delete_milestone_success(admin_setup_data):
    """Test successful milestone deletion"""
    global milestone_id
    token, client = admin_setup_data
    headers = {'Authentication-Token': f'{token}'}

    response = client.delete(f"/instructor/milestones/{milestone_id}", headers=headers)
    assert response.status_code == 200
    assert response.get_json()['message'] == "Milestone deleted successfully"
