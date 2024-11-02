from flask import Blueprint, request, current_app
from flask_login import login_required, current_user
from flask_security import roles_required
from sqlalchemy import and_, or_, desc, func
from datetime import datetime, timedelta
import pytz

from ..models.models import (
    db, Project, Student, Instructor, ProjectStudentAssignment,
    Milestone, MilestoneSubmission
)
from ..utils.helpers import generate_response, handle_error, instructor_required

viva_bp = Blueprint('viva', __name__)

# Add Viva related models if not in models.py
class VivaSession(db.Model):
    __tablename__ = 'viva_sessions'
    
    session_id = db.Column(db.String(20), primary_key=True)
    milestone_id = db.Column(db.String(20), db.ForeignKey('milestones.milestone_id'), nullable=False)
    instructor_id = db.Column(db.String(20), db.ForeignKey('instructors.instructor_id'), nullable=False)
    date = db.Column(db.Date, nullable=False)
    start_time = db.Column(db.Time, nullable=False)
    end_time = db.Column(db.Time, nullable=False)
    status = db.Column(db.String(20), default='scheduled')  # scheduled, completed, cancelled
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    milestone = db.relationship('Milestone', backref='viva_sessions')
    instructor = db.relationship('Instructor', backref='viva_sessions')

class VivaSlot(db.Model):
    __tablename__ = 'viva_slots'
    
    slot_id = db.Column(db.String(20), primary_key=True)
    session_id = db.Column(db.String(20), db.ForeignKey('viva_sessions.session_id'), nullable=False)
    start_time = db.Column(db.DateTime, nullable=False)
    end_time = db.Column(db.DateTime, nullable=False)
    student_id = db.Column(db.String(20), db.ForeignKey('students.student_id'))
    status = db.Column(db.String(20), default='available')  # available, booked, completed
    
    # Relationships
    session = db.relationship('VivaSession', backref='slots')
    student = db.relationship('Student', backref='viva_slots')

@viva_bp.route('/sessions', methods=['POST'])
@login_required
@instructor_required
def create_viva_session():
    """Create a new viva session with slots"""
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['milestone_id', 'date', 'start_time', 'end_time', 'slot_duration']
        for field in required_fields:
            if field not in data:
                return generate_response(
                    message=f'Missing required field: {field}',
                    status=400
                )

        # Verify milestone ownership
        milestone = Milestone.query.get_or_404(data['milestone_id'])
        project = Project.query.get(milestone.project_id)
        if project.instructor_id != current_user.instructor.instructor_id:
            return generate_response(message='Unauthorized access', status=403)

        # Parse times
        date = datetime.strptime(data['date'], '%Y-%m-%d').date()
        start_time = datetime.strptime(data['start_time'], '%H:%M').time()
        end_time = datetime.strptime(data['end_time'], '%H:%M').time()
        slot_duration = int(data['slot_duration'])  # in minutes

        if start_time >= end_time:
            return generate_response(message='Invalid time range', status=400)

        # Create session
        session = VivaSession(
            milestone_id=milestone.milestone_id,
            instructor_id=current_user.instructor.instructor_id,
            date=date,
            start_time=start_time,
            end_time=end_time,
            status='scheduled'
        )
        db.session.add(session)
        db.session.flush()

        # Create slots
        current_time = datetime.combine(date, start_time)
        end_datetime = datetime.combine(date, end_time)
        slot_timedelta = timedelta(minutes=slot_duration)
        
        created_slots = []
        while current_time + slot_timedelta <= end_datetime:
            slot = VivaSlot(
                session_id=session.session_id,
                start_time=current_time,
                end_time=current_time + slot_timedelta,
                status='available'
            )
            db.session.add(slot)
            created_slots.append(slot)
            current_time += slot_timedelta

        db.session.commit()

        return generate_response(
            message='Viva session created successfully',
            data={
                'session_id': session.session_id,
                'slots_created': len(created_slots)
            }
        )
    except Exception as e:
        db.session.rollback()
        return handle_error(e)

@viva_bp.route('/sessions', methods=['GET'])
@login_required
def get_viva_sessions():
    """Get list of viva sessions"""
    try:
        # Get query parameters
        milestone_id = request.args.get('milestone_id')
        date = request.args.get('date')
        status = request.args.get('status')
        
        # Base query
        query = VivaSession.query

        # Apply filters
        if milestone_id:
            query = query.filter_by(milestone_id=milestone_id)
        if date:
            query = query.filter_by(date=datetime.strptime(date, '%Y-%m-%d').date())
        if status:
            query = query.filter_by(status=status)

        # Role-based filtering
        if current_user.has_role('student'):
            # Students see sessions for their projects
            project_ids = ProjectStudentAssignment.query\
                .filter_by(student_id=current_user.user_id)\
                .with_entities(ProjectStudentAssignment.project_id)\
                .all()
            milestone_ids = Milestone.query\
                .filter(Milestone.project_id.in_([p[0] for p in project_ids]))\
                .with_entities(Milestone.milestone_id)\
                .all()
            query = query.filter(VivaSession.milestone_id.in_([m[0] for m in milestone_ids]))
        elif current_user.has_role('instructor'):
            # Instructors see their sessions
            query = query.filter_by(instructor_id=current_user.instructor.instructor_id)

        sessions = query.order_by(VivaSession.date, VivaSession.start_time).all()

        return generate_response(data={
            'sessions': [{
                'session_id': session.session_id,
                'milestone_id': session.milestone_id,
                'date': session.date.isoformat(),
                'start_time': session.start_time.strftime('%H:%M'),
                'end_time': session.end_time.strftime('%H:%M'),
                'status': session.status,
                'instructor': {
                    'id': session.instructor.instructor_id,
                    'name': session.instructor.user.username
                },
                'slots': [{
                    'slot_id': slot.slot_id,
                    'start_time': slot.start_time.strftime('%H:%M'),
                    'end_time': slot.end_time.strftime('%H:%M'),
                    'status': slot.status,
                    'student': {
                        'id': slot.student.student_id,
                        'name': slot.student.user.username
                    } if slot.student else None
                } for slot in session.slots]
            } for session in sessions]
        })
    except Exception as e:
        return handle_error(e)

@viva_bp.route('/slots/available', methods=['GET'])
@login_required
def get_available_slots():
    """Get available viva slots"""
    try:
        milestone_id = request.args.get('milestone_id')
        date = request.args.get('date')

        if not milestone_id:
            return generate_response(message='Milestone ID is required', status=400)

        # Base query for available slots
        query = VivaSlot.query\
            .join(VivaSession)\
            .filter(VivaSlot.status == 'available')

        if milestone_id:
            query = query.filter(VivaSession.milestone_id == milestone_id)
        if date:
            query = query.filter(VivaSession.date == datetime.strptime(date, '%Y-%m-%d').date())

        # Only show future slots
        query = query.filter(VivaSlot.start_time > datetime.now())

        slots = query.order_by(VivaSlot.start_time).all()

        return generate_response(data={
            'slots': [{
                'slot_id': slot.slot_id,
                'session_id': slot.session_id,
                'start_time': slot.start_time.isoformat(),
                'end_time': slot.end_time.isoformat()
            } for slot in slots]
        })
    except Exception as e:
        return handle_error(e)

@viva_bp.route('/slots/<string:slot_id>/book', methods=['POST'])
@login_required
def book_slot(slot_id):
    """Book a viva slot"""
    try:
        slot = VivaSlot.query.get_or_404(slot_id)

        # Verify slot is available
        if slot.status != 'available':
            return generate_response(message='Slot is not available', status=400)

        # Verify student is part of the project
        milestone = slot.session.milestone
        assignment = ProjectStudentAssignment.query.filter_by(
            project_id=milestone.project_id,
            student_id=current_user.user_id
        ).first()
        if not assignment:
            return generate_response(message='Not authorized to book this slot', status=403)

        # Check if student already has a slot for this session
        existing_slot = VivaSlot.query\
            .filter_by(
                session_id=slot.session_id,
                student_id=current_user.user_id
            ).first()
        if existing_slot:
            return generate_response(message='Already booked a slot for this session', status=400)

        # Book the slot
        slot.student_id = current_user.user_id
        slot.status = 'booked'
        db.session.commit()

        # TODO: Send notification to instructor and student

        return generate_response(message='Slot booked successfully')
    except Exception as e:
        db.session.rollback()
        return handle_error(e)

@viva_bp.route('/sessions/<string:session_id>', methods=['PUT'])
@login_required
@instructor_required
def update_session(session_id):
    """Update viva session details"""
    try:
        session = VivaSession.query.get_or_404(session_id)
        
        # Verify ownership
        if session.instructor_id != current_user.instructor.instructor_id:
            return generate_response(message='Unauthorized access', status=403)

        data = request.get_json()

        # Update session fields
        if 'status' in data:
            session.status = data['status']
        
        if 'date' in data:
            new_date = datetime.strptime(data['date'], '%Y-%m-%d').date()
            time_diff = new_date - session.date
            session.date = new_date
            
            # Update all slot times
            for slot in session.slots:
                slot.start_time += time_diff
                slot.end_time += time_diff

        db.session.commit()

        # TODO: Send notifications for schedule changes

        return generate_response(message='Session updated successfully')
    except Exception as e:
        db.session.rollback()
        return handle_error(e)

@viva_bp.route('/slots/<string:slot_id>/cancel', methods=['POST'])
@login_required
def cancel_slot_booking(slot_id):
    """Cancel a booked viva slot"""
    try:
        slot = VivaSlot.query.get_or_404(slot_id)

        # Verify ownership or instructor access
        if not current_user.has_role('admin') and \
           not current_user.has_role('instructor') and \
           slot.student_id != current_user.user_id:
            return generate_response(message='Unauthorized access', status=403)

        # Verify slot is booked
        if slot.status != 'booked':
            return generate_response(message='Slot is not booked', status=400)

        # Cancel booking
        slot.student_id = None
        slot.status = 'available'
        db.session.commit()

        # TODO: Send notification about cancellation

        return generate_response(message='Slot booking cancelled successfully')
    except Exception as e:
        db.session.rollback()
        return handle_error(e)

@viva_bp.route('/schedule/<string:student_id>', methods=['GET'])
@login_required
def get_student_schedule(student_id):
    """Get student's viva schedule"""
    try:
        # Verify access permissions
        if not current_user.has_role('admin') and \
           not current_user.has_role('instructor') and \
           current_user.user_id != student_id:
            return generate_response(message='Unauthorized access', status=403)

        # Get upcoming slots
        slots = VivaSlot.query\
            .filter_by(student_id=student_id)\
            .join(VivaSession)\
            .filter(VivaSession.status == 'scheduled')\
            .filter(VivaSlot.start_time > datetime.now())\
            .order_by(VivaSlot.start_time)\
            .all()

        return generate_response(data={
            'schedule': [{
                'slot_id': slot.slot_id,
                'session_id': slot.session_id,
                'milestone': {
                    'id': slot.session.milestone.milestone_id,
                    'title': slot.session.milestone.title
                },
                'date': slot.session.date.isoformat(),
                'start_time': slot.start_time.strftime('%H:%M'),
                'end_time': slot.end_time.strftime('%H:%M'),
                'instructor': {
                    'id': slot.session.instructor.instructor_id,
                    'name': slot.session.instructor.user.username
                }
            } for slot in slots]
        })
    except Exception as e:
        return handle_error(e)

# Error handlers
@viva_bp.errorhandler(404)
def not_found_error(error):
    return generate_response(message='Resource not found', status=404)

@viva_bp.errorhandler(403)
def forbidden_error(error):
    return generate_response(message='Forbidden', status=403)
