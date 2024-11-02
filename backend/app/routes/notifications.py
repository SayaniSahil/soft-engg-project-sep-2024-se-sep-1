from flask import Blueprint, request, current_app
from flask_login import login_required, current_user
from flask_security import roles_required
from sqlalchemy import and_, or_, desc
from datetime import datetime, timedelta
import enum

from ..models.models import db
from ..utils.helpers import generate_response, handle_error

notification_bp = Blueprint('notifications', __name__)

# Add Notification Models if not in models.py
class NotificationType(enum.Enum):
    MILESTONE = 'milestone'
    SUBMISSION = 'submission'
    FEEDBACK = 'feedback'
    VIVA = 'viva'
    GITHUB = 'github'
    GENERAL = 'general'

class NotificationPriority(enum.Enum):
    LOW = 'low'
    MEDIUM = 'medium'
    HIGH = 'high'

class Notification(db.Model):
    __tablename__ = 'notifications'
    
    notification_id = db.Column(db.String(20), primary_key=True)
    recipient_id = db.Column(db.String(20), db.ForeignKey('users.user_id'), nullable=False)
    sender_id = db.Column(db.String(20), db.ForeignKey('users.user_id'))
    type = db.Column(db.Enum(NotificationType), nullable=False)
    priority = db.Column(db.Enum(NotificationPriority), default=NotificationPriority.MEDIUM)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)
    link = db.Column(db.String(500))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    read_at = db.Column(db.DateTime)
    expires_at = db.Column(db.DateTime)
    
    # Relationships
    recipient = db.relationship('User', foreign_keys=[recipient_id], backref='notifications_received')
    sender = db.relationship('User', foreign_keys=[sender_id], backref='notifications_sent')

class NotificationPreference(db.Model):
    __tablename__ = 'notification_preferences'
    
    user_id = db.Column(db.String(20), db.ForeignKey('users.user_id'), primary_key=True)
    notification_type = db.Column(db.Enum(NotificationType), primary_key=True)
    email_enabled = db.Column(db.Boolean, default=True)
    push_enabled = db.Column(db.Boolean, default=True)
    in_app_enabled = db.Column(db.Boolean, default=True)

@notification_bp.route('/', methods=['POST'])
@login_required
def create_notification():
    """Create a new notification"""
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['recipient_id', 'type', 'title', 'content']
        for field in required_fields:
            if field not in data:
                return generate_response(
                    message=f'Missing required field: {field}',
                    status=400
                )

        # Verify recipient exists and check notification preferences
        preferences = NotificationPreference.query.filter_by(
            user_id=data['recipient_id'],
            notification_type=data['type']
        ).first()

        if preferences and not preferences.in_app_enabled:
            return generate_response(message='Notifications disabled by recipient', status=400)

        # Create notification
        notification = Notification(
            recipient_id=data['recipient_id'],
            sender_id=current_user.user_id,
            type=data['type'],
            priority=data.get('priority', NotificationPriority.MEDIUM),
            title=data['title'],
            content=data['content'],
            link=data.get('link'),
            expires_at=datetime.utcnow() + timedelta(days=30)  # Default 30 days expiry
        )
        db.session.add(notification)
        db.session.commit()

        # TODO: Handle email and push notifications based on preferences
        if preferences and preferences.email_enabled:
            # Send email notification
            pass

        if preferences and preferences.push_enabled:
            # Send push notification
            pass

        return generate_response(
            message='Notification created successfully',
            data={'notification_id': notification.notification_id}
        )
    except Exception as e:
        db.session.rollback()
        return handle_error(e)

@notification_bp.route('/', methods=['GET'])
@login_required
def get_notifications():
    """Get user's notifications"""
    try:
        # Get query parameters
        notification_type = request.args.get('type')
        read_status = request.args.get('read_status')
        priority = request.args.get('priority')
        page = int(request.args.get('page', 1))
        per_page = int(request.args.get('per_page', 20))

        # Base query
        query = Notification.query.filter_by(recipient_id=current_user.user_id)

        # Apply filters
        if notification_type:
            query = query.filter_by(type=notification_type)
        if read_status:
            if read_status.lower() == 'read':
                query = query.filter(Notification.read_at.isnot(None))
            elif read_status.lower() == 'unread':
                query = query.filter(Notification.read_at.is_(None))
        if priority:
            query = query.filter_by(priority=priority)

        # Filter expired notifications
        query = query.filter(or_(
            Notification.expires_at.is_(None),
            Notification.expires_at > datetime.utcnow()
        ))

        # Order by creation date
        query = query.order_by(desc(Notification.created_at))

        # Pagination
        paginated_notifications = query.paginate(
            page=page,
            per_page=per_page,
            error_out=False
        )

        return generate_response(data={
            'notifications': [{
                'notification_id': notif.notification_id,
                'type': notif.type.value,
                'priority': notif.priority.value,
                'title': notif.title,
                'content': notif.content,
                'link': notif.link,
                'created_at': notif.created_at.isoformat(),
                'read_at': notif.read_at.isoformat() if notif.read_at else None,
                'sender': {
                    'id': notif.sender_id,
                    'name': notif.sender.username if notif.sender else None
                }
            } for notif in paginated_notifications.items],
            'total': paginated_notifications.total,
            'pages': paginated_notifications.pages,
            'current_page': page
        })
    except Exception as e:
        return handle_error(e)

@notification_bp.route('/unread/count', methods=['GET'])
@login_required
def get_unread_count():
    """Get count of unread notifications"""
    try:
        count = Notification.query.filter_by(
            recipient_id=current_user.user_id,
            read_at=None
        ).filter(or_(
            Notification.expires_at.is_(None),
            Notification.expires_at > datetime.utcnow()
        )).count()

        return generate_response(data={'unread_count': count})
    except Exception as e:
        return handle_error(e)

@notification_bp.route('/<string:notification_id>/read', methods=['PUT'])
@login_required
def mark_as_read(notification_id):
    """Mark notification as read"""
    try:
        notification = Notification.query.get_or_404(notification_id)
        
        # Verify ownership
        if notification.recipient_id != current_user.user_id:
            return generate_response(message='Unauthorized access', status=403)

        notification.read_at = datetime.utcnow()
        db.session.commit()

        return generate_response(message='Notification marked as read')
    except Exception as e:
        db.session.rollback()
        return handle_error(e)

@notification_bp.route('/read/all', methods=['PUT'])
@login_required
def mark_all_as_read():
    """Mark all notifications as read"""
    try:
        Notification.query.filter_by(
            recipient_id=current_user.user_id,
            read_at=None
        ).update({
            'read_at': datetime.utcnow()
        })
        db.session.commit()

        return generate_response(message='All notifications marked as read')
    except Exception as e:
        db.session.rollback()
        return handle_error(e)

@notification_bp.route('/preferences', methods=['GET'])
@login_required
def get_preferences():
    """Get notification preferences"""
    try:
        preferences = NotificationPreference.query.filter_by(
            user_id=current_user.user_id
        ).all()

        return generate_response(data={
            'preferences': [{
                'notification_type': pref.notification_type.value,
                'email_enabled': pref.email_enabled,
                'push_enabled': pref.push_enabled,
                'in_app_enabled': pref.in_app_enabled
            } for pref in preferences]
        })
    except Exception as e:
        return handle_error(e)

@notification_bp.route('/preferences', methods=['PUT'])
@login_required
def update_preferences():
    """Update notification preferences"""
    try:
        data = request.get_json()
        preferences = data.get('preferences', [])

        for pref in preferences:
            notification_type = pref.get('notification_type')
            if not notification_type:
                continue

            preference = NotificationPreference.query.filter_by(
                user_id=current_user.user_id,
                notification_type=notification_type
            ).first()

            if not preference:
                preference = NotificationPreference(
                    user_id=current_user.user_id,
                    notification_type=notification_type
                )
                db.session.add(preference)

            if 'email_enabled' in pref:
                preference.email_enabled = pref['email_enabled']
            if 'push_enabled' in pref:
                preference.push_enabled = pref['push_enabled']
            if 'in_app_enabled' in pref:
                preference.in_app_enabled = pref['in_app_enabled']

        db.session.commit()
        return generate_response(message='Preferences updated successfully')
    except Exception as e:
        db.session.rollback()
        return handle_error(e)

@notification_bp.route('/<string:notification_id>', methods=['DELETE'])
@login_required
def delete_notification(notification_id):
    """Delete a notification"""
    try:
        notification = Notification.query.get_or_404(notification_id)
        
        # Verify ownership
        if notification.recipient_id != current_user.user_id:
            return generate_response(message='Unauthorized access', status=403)

        db.session.delete(notification)
        db.session.commit()

        return generate_response(message='Notification deleted successfully')
    except Exception as e:
        db.session.rollback()
        return handle_error(e)

# Utility function to create system notifications
def create_system_notification(recipient_id, title, content, notification_type, priority=NotificationPriority.MEDIUM, link=None):
    """Create a system notification"""
    try:
        notification = Notification(
            recipient_id=recipient_id,
            type=notification_type,
            priority=priority,
            title=title,
            content=content,
            link=link,
            expires_at=datetime.utcnow() + timedelta(days=30)
        )
        db.session.add(notification)
        db.session.commit()
        return notification
    except Exception as e:
        db.session.rollback()
        raise e

# Error handlers
@notification_bp.errorhandler(404)
def not_found_error(error):
    return generate_response(message='Notification not found', status=404)

@notification_bp.errorhandler(403)
def forbidden_error(error):
    return generate_response(message='Forbidden', status=403)
