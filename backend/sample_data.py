from app import app, db
from components.extensions import datastore, bcrypt
from components.models import Project, ProjectStudentAssignment, ProjectInstructorAssignment, Milestone, MilestoneSubmission, ChatHistory
from datetime import date, timedelta

with app.app_context():
    db.drop_all()
    db.create_all()

    # Creating Roles
    datastore.find_or_create_role(name="Admin", description="Admins have control over everything")
    datastore.find_or_create_role(name="Instructor", description="Instructors can create and manage projects")
    datastore.find_or_create_role(name="Student", description="Students can apply for projects")
    db.session.commit()

    # Create Users for each role using datastore
    admins = [
        {"username": f"Admin", "email": f"admin@gmail.com", "password": f"Admin@12"} 
    ]
    instructors = [
        {"username": f"Instructor{i}", "email": f"instructor{i}@gmail.com", "password": f"Instructor@12{i}"} for i in range(1, 6)
    ]
    students = [
        {"username": f"Student{i}", "email": f"student{i}@gmail.com", "password": f"Student@12{i}"} for i in range(1, 6)
    ]

    for admin in admins:
        datastore.create_user(username=admin["username"], email=admin["email"], password=bcrypt.generate_password_hash(admin["password"]), roles=["Admin"])

    for instructor in instructors:
        datastore.create_user(username=instructor["username"], email=instructor["email"], password=bcrypt.generate_password_hash(instructor["password"]), roles=["Instructor"])

    for student in students:
        datastore.create_user(username=student["username"], email=student["email"], password=bcrypt.generate_password_hash(student["password"]), roles=["Student"])

    db.session.commit()

    # Add projects
    projects = [
        Project(
            project_id=i,
            title=f"Project {i}",
            description=f"Description for project {i}",
        )
        for i in range(1, 6)
    ]
    db.session.add_all(projects)
    db.session.commit()

    # Assign projects to students
    project_student_assignments = []
    for i in range(1, 6):
        # Get the student ID for each student
        student_id = datastore.find_user(email=f"student{i}@gmail.com").user_id
        
        # Assign the student to the project with the same ID
        project_student_assignments.append(
            ProjectStudentAssignment(
                project_id=i,  # Match student index `i` with project ID `i`
                student_id=student_id,
                github_url=f"https://github.com/student{i}/project{i}"  # Each student has a project with the same ID
            )
        )

    # Add all assignments to the database session
    db.session.add_all(project_student_assignments)
    db.session.commit()


    # Assign projects to instructors
    project_instructor_assignments = []
    for i in range(1, 6):
        instructor_id = datastore.find_user(email=f"instructor{i}@gmail.com").user_id
        for j in range(1, 6):
            project_instructor_assignments.append(
                ProjectInstructorAssignment(
                    project_id=j,
                    instructor_id=instructor_id
                )
            )
    db.session.add_all(project_instructor_assignments)
    db.session.commit()

    # Add milestones
    milestones = []
    for i in range(1, 6):
        for j in range(1, 6):
            milestones.append(
                Milestone(
                    milestone_id=i * 10 + j,
                    project_id=i,
                    title=f"Milestone {j} for Project {i}",
                    description=f"Description of milestone {j} for project {i}",
                    start_date=date(2024, 1, 1) + timedelta(days=j * 5),
                    end_date=date(2024, 1, 10) + timedelta(days=j * 5),
                    weightage=10 * j,
                    document_url=f"https://example.com/project{i}/milestone{j}"
                )
            )
    db.session.add_all(milestones)
    db.session.commit()

    # Add milestone submissions
    milestone_submissions = []
    for i in range(1, 6):
        for j in range(1, 6):
            milestone_id = i * 10 + j
            student_id = datastore.find_user(email=f"student{i}@gmail.com").user_id
            milestone_submissions.append(
                MilestoneSubmission(
                    milestone_id=milestone_id,
                    student_id=student_id,
                    submission_date=date(2024, 2, 1) + timedelta(days=j),
                    evaluation_status="approved" if j % 2 == 0 else "pending",
                    evaluation_date=date(2024, 2, 10) + timedelta(days=j) if j % 2 == 0 else None,
                    document_url=f"https://example.com/student{i}/submission{j}"
                )
            )
    db.session.add_all(milestone_submissions)
    db.session.commit()

    # Add chat history
    chat_histories = []
    for i in range(1, 6):
        instructor_id = datastore.find_user(email=f"instructor{i}@gmail.com").user_id
        for j in range(1, 6):
            chat_histories.append(
                ChatHistory(
                    project_id=j,
                    instructor_id=instructor_id,
                    message_text=f"Message {j} for Project {j} by Instructor {i}",
                )
            )
    db.session.add_all(chat_histories)
    db.session.commit()

print("Database seeded with sufficient data points!")
