import pytest
from requests import Session

@pytest.fixture(scope='session')
def admin_setup_data():
    client = Session()
    # Login Admin
    response = client.post('http://localhost:5000/login_user', json={
        'email': 'admin@gmail.com',
        'password': 'Admin@12'
    })
    response_data = response.json()
    assert response.status_code == 200
    token = response_data['token']
    yield token, client

@pytest.fixture(scope='session')
def instructor_setup_data():
    client = Session()
    # Login Instructor
    response = client.post('http://localhost:5000/login_user', json={
        'email': 'instructor@gmail.com',
        'password': 'Instructor@12'
    })
    response_data = response.json()
    assert response.status_code == 200
    token = response_data['token']
    yield token, client

@pytest.fixture(scope='session')
def student_setup_data():
    client = Session()
    # Login Student
    response = client.post('http://localhost:5000/login_user', json={
        'email': 'student@gmail.com',
        'password': 'Student@12'
    })
    response_data = response.json()
    assert response.status_code == 200
    token = response_data['token']
    yield token, client

# This is how you get the token for the admin, instructor, and student
# For further use directly call client.get, client.post, client.put, client.delete
# do not create a new session for each request
def test(admin_setup_data):
    token, client = admin_setup_data
    response = client.get('http://localhost:5000/projects', headers={'Authentication-Token': f'{token}'})
    assert response.status_code == 200, f"Unexpected status code: {response.status_code}"
    # Check if the response is as expected, a valid json response
    assert response.headers.get('Content-Type') == 'application/json', "Response is not JSON"
    print(response.json())

# This should fail because the token is invalid. Create exhasutive tests for the other roles
def test_1(admin_setup_data):
    token, client = admin_setup_data
    response = client.get('http://localhost:5000/projects', headers={'Authentication-Token': f'invalid{token}'})
    assert response.status_code == 200, f"Unexpected status code: {response.status_code}"
    # Check if the response is as expected, a valid json response
    assert response.headers.get('Content-Type') != 'application/json', "Response is not JSON" # This should be true