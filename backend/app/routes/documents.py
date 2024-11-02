from flask import Blueprint, request, send_file, current_app
from flask_login import login_required, current_user
from flask_security import roles_required
from werkzeug.utils import secure_filename
from sqlalchemy import and_, or_, desc
from datetime import datetime
import os
import mimetypes
import hashlib
from pathlib import Path

from ..models.models import (
    db, Document, Project, ProjectStudentAssignment, 
    MilestoneSubmission, Student
)
from ..utils.helpers import generate_response, handle_error, instructor_required

document_bp = Blueprint('documents', __name__)

# Configure upload settings
ALLOWED_EXTENSIONS = {'pdf', 'doc', 'docx', 'txt', 'zip', 'rar', 'py', 'java', 'cpp', 'h', 'c'}
MAX_FILE_SIZE = 50 * 1024 * 1024  # 50MB

def allowed_file(filename):
    """Check if file extension is allowed"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def generate_file_path(file, student_id=None):
    """Generate unique file path for uploaded document"""
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    filename = secure_filename(file.filename)
    hash_str = hashlib.md5(f"{timestamp}_{filename}".encode()).hexdigest()[:8]
    
    base_path = current_app.config['UPLOAD_FOLDER']
    if student_id:
        base_path = os.path.join(base_path, student_id)
    
    Path(base_path).mkdir(parents=True, exist_ok=True)
    return os.path.join(base_path, f"{hash_str}_{filename}")

@document_bp.route('/upload', methods=['POST'])
@login_required
def upload_document():
    """Upload a document"""
    try:
        if 'file' not in request.files:
            return generate_response(message='No file provided', status=400)
        
        file = request.files['file']
        if file.filename == '':
            return generate_response(message='No file selected', status=400)
            
        if not allowed_file(file.filename):
            return generate_response(
                message=f'File type not allowed. Allowed types: {", ".join(ALLOWED_EXTENSIONS)}',
                status=400
            )

        # Check file size
        file.seek(0, os.SEEK_END)
        file_size = file.tell()
        file.seek(0)
        
        if file_size > MAX_FILE_SIZE:
            return generate_response(
                message=f'File size exceeds maximum limit of {MAX_FILE_SIZE/1024/1024}MB',
                status=400
            )

        project_id = request.form.get('project_id')
        if not project_id:
            return generate_response(message='Project ID is required', status=400)

        # Verify project access
        if current_user.has_role('student'):
            assignment = ProjectStudentAssignment.query.filter_by(
                project_id=project_id,
                student_id=current_user.user_id
            ).first()
            if not assignment:
                return generate_response(message='Access denied', status=403)

        # Save file
        file_path = generate_file_path(
            file, 
            student_id=current_user.user_id if current_user.has_role('student') else None
        )
        file.save(file_path)

        # Create document record
        document = Document(
            project_id=project_id,
            uploaded_by=current_user.user_id,
            document_type=request.form.get('document_type', 'other'),
            file_path=file_path,
            file_size=file_size,
            mime_type=mimetypes.guess_type(file.filename)[0]
        )
        db.session.add(document)
        db.session.commit()

        return generate_response(
            message='Document uploaded successfully',
            data={'document_id': document.document_id}
        )
    except Exception as e:
        return handle_error(e)

@document_bp.route('/', methods=['GET'])
@login_required
def get_documents():
    """Get list of documents with filtering options"""
    try:
        # Get query parameters
        project_id = request.args.get('project_id')
        document_type = request.args.get('document_type')
        uploaded_by = request.args.get('uploaded_by')
        page = int(request.args.get('page', 1))
        per_page = int(request.args.get('per_page', 10))

        # Base query
        query = Document.query

        # Apply filters
        if project_id:
            query = query.filter_by(project_id=project_id)
        if document_type:
            query = query.filter_by(document_type=document_type)
        if uploaded_by:
            query = query.filter_by(uploaded_by=uploaded_by)

        # Apply role-based filters
        if current_user.has_role('student'):
            # Students see only their documents and project documents
            project_ids = ProjectStudentAssignment.query\
                .filter_by(student_id=current_user.user_id)\
                .with_entities(ProjectStudentAssignment.project_id)\
                .all()
            project_ids = [p[0] for p in project_ids]
            
            query = query.filter(or_(
                Document.uploaded_by == current_user.user_id,
                and_(
                    Document.project_id.in_(project_ids),
                    Document.document_type != 'private'
                )
            ))

        # Order by upload date
        query = query.order_by(desc(Document.upload_timestamp))

        # Pagination
        paginated_docs = query.paginate(
            page=page,
            per_page=per_page,
            error_out=False
        )

        return generate_response(data={
            'documents': [{
                'document_id': doc.document_id,
                'project_id': doc.project_id,
                'document_type': doc.document_type,
                'uploaded_by': doc.uploaded_by,
                'upload_timestamp': doc.upload_timestamp.isoformat(),
                'file_size': doc.file_size,
                'mime_type': doc.mime_type
            } for doc in paginated_docs.items],
            'total': paginated_docs.total,
            'pages': paginated_docs.pages,
            'current_page': page
        })
    except Exception as e:
        return handle_error(e)

@document_bp.route('/<string:document_id>', methods=['GET'])
@login_required
def get_document(document_id):
    """Download a document"""
    try:
        document = Document.query.get_or_404(document_id)

        # Verify access permissions
        if current_user.has_role('student'):
            if document.uploaded_by != current_user.user_id:
                assignment = ProjectStudentAssignment.query.filter_by(
                    project_id=document.project_id,
                    student_id=current_user.user_id
                ).first()
                if not assignment or document.document_type == 'private':
                    return generate_response(message='Access denied', status=403)

        if not os.path.exists(document.file_path):
            return generate_response(message='File not found', status=404)

        return send_file(
            document.file_path,
            as_attachment=True,
            download_name=os.path.basename(document.file_path).split('_', 1)[1]
        )
    except Exception as e:
        return handle_error(e)

@document_bp.route('/analyze', methods=['POST'])
@login_required
def analyze_document():
    """Analyze document using AI"""
    try:
        data = request.get_json()
        document_id = data.get('document_id')
        analysis_type = data.get('analysis_type')

        if not document_id or not analysis_type:
            return generate_response(
                message='Document ID and analysis type are required',
                status=400
            )

        document = Document.query.get_or_404(document_id)

        # Verify access permissions
        if current_user.has_role('student') and document.uploaded_by != current_user.user_id:
            return generate_response(message='Access denied', status=403)

        # TODO: Implement different types of analysis
        analysis_results = None
        if analysis_type == 'code_quality':
            # Implement code quality analysis
            pass
        elif analysis_type == 'documentation_quality':
            # Implement documentation quality analysis
            pass
        elif analysis_type == 'plagiarism':
            # Implement plagiarism detection
            pass
        else:
            return generate_response(message='Invalid analysis type', status=400)

        return generate_response(
            message='Analysis completed',
            data={'results': analysis_results}
        )
    except Exception as e:
        return handle_error(e)

@document_bp.route('/<string:document_id>', methods=['DELETE'])
@login_required
def delete_document(document_id):
    """Delete a document"""
    try:
        document = Document.query.get_or_404(document_id)

        # Verify ownership
        if not current_user.has_role('admin') and document.uploaded_by != current_user.user_id:
            return generate_response(message='Access denied', status=403)

        # Delete file
        if os.path.exists(document.file_path):
            os.remove(document.file_path)

        # Delete record
        db.session.delete(document)
        db.session.commit()

        return generate_response(message='Document deleted successfully')
    except Exception as e:
        db.session.rollback()
        return handle_error(e)

@document_bp.route('/project/<string:project_id>/summary', methods=['GET'])
@login_required
def project_documents_summary(project_id):
    """Get summary of project documents"""
    try:
        # Verify project access
        if current_user.has_role('student'):
            assignment = ProjectStudentAssignment.query.filter_by(
                project_id=project_id,
                student_id=current_user.user_id
            ).first()
            if not assignment:
                return generate_response(message='Access denied', status=403)

        # Get document statistics
        stats = db.session.query(
            Document.document_type,
            db.func.count(Document.document_id),
            db.func.sum(Document.file_size)
        ).filter_by(project_id=project_id)\
        .group_by(Document.document_type)\
        .all()

        # Get recent uploads
        recent_uploads = Document.query\
            .filter_by(project_id=project_id)\
            .order_by(desc(Document.upload_timestamp))\
            .limit(5)\
            .all()

        return generate_response(data={
            'statistics': {
                doc_type: {
                    'count': count,
                    'total_size': size
                } for doc_type, count, size in stats
            },
            'recent_uploads': [{
                'document_id': doc.document_id,
                'document_type': doc.document_type,
                'uploaded_by': doc.uploaded_by,
                'upload_timestamp': doc.upload_timestamp.isoformat()
            } for doc in recent_uploads]
        })
    except Exception as e:
        return handle_error(e)

# Error handlers
@document_bp.errorhandler(404)
def not_found_error(error):
    return generate_response(message='Document not found', status=404)

@document_bp.errorhandler(403)
def forbidden_error(error):
    return generate_response(message='Forbidden', status=403)
