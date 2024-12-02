import pytest
import json
from io import BytesIO
from werkzeug.security import generate_password_hash
from models import db, User

# Test cases for student-related operations

def test_bulk_upload_students_success(admin_setup_data):
    """Test successful bulk upload of students."""
    token, client = admin_setup_data
    headers = {'Authentication-Token': f'{token}'}

    csv_content = (
        "student_id,email,username,password,department,batch\n"
        "S001,student1@example.com,student1,password123,Computer Science,2024\n"
        "S002,student2@example.com,student2,password123,Electrical,2024\n"
    )

    data = {
        'file': (BytesIO(csv_content.encode('utf-8')), 'students.csv')
    }

    response = client.post('/students/bulk-upload', headers=headers, data=data, content_type='multipart/form-data')

    assert response.status_code == 200
    assert response.get_json()["message"] == "Students uploaded successfully"

    # Verify data in the database
    student1 = User.query.filter_by(email='student1@example.com').first()
    assert student1 is not None
    assert student1.username == 'student1'

    student2 = User.query.filter_by(email='student2@example.com').first()
    assert student2 is not None
    assert student2.username == 'student2'


def test_bulk_upload_students_no_file(admin_setup_data):
    """Test bulk upload with no file provided."""
    token, client = admin_setup_data
    headers = {'Authentication-Token': f'{token}'}

    response = client.post('/students/bulk-upload', headers=headers, data={}, content_type='multipart/form-data')

    assert response.status_code == 400
    assert response.get_json()["error"] == "No file provided"


def test_bulk_upload_students_invalid_csv(admin_setup_data):
    """Test bulk upload with invalid CSV format."""
    token, client = admin_setup_data
    headers = {'Authentication-Token': f'{token}'}

    csv_content = "invalid,data\n"
    data = {
        'file': (BytesIO(csv_content.encode('utf-8')), 'students.csv')
    }

    response = client.post('/students/bulk-upload', headers=headers, data=data, content_type='multipart/form-data')

    assert response.status_code == 500
    assert "error" in response.get_json()


def test_delete_student_success(admin_setup_data):
    """Test successful deletion of a student."""
    token, client = admin_setup_data
    headers = {'Authentication-Token': f'{token}'}

    # Add mock data
    user = User(
        user_id=1,
        email='student_to_delete@example.com',
        username='student_delete',
        password=generate_password_hash('password123'),
        active=True,
        fs_uniquifier='unique_id_1'
    )
    db.session.add(user)
    db.session.commit()

    response = client.delete('/students/S001', headers=headers)
    assert response.status_code == 200
    assert response.get_json()["message"] == "Student deleted successfully"

    # Verify deletion in the database
    deleted_user = User.query.filter_by(email='student_to_delete@example.com').first()
    assert deleted_user is None


def test_delete_student_not_found(admin_setup_data):
    """Test deletion of a student that does not exist."""
    token, client = admin_setup_data
    headers = {'Authentication-Token': f'{token}'}

    response = client.delete('/students/S999', headers=headers)

    assert response.status_code == 404
    assert response.get_json()["error"] == "Student not found"
