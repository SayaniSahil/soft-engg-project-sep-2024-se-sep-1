from flask import Flask
from flask_security import Security, SQLAlchemyUserDatastore
from flask_cors import CORS
from flask_login import LoginManager
from .models.models import db, User, Role
from flask_caching import Cache

def create_app():
    app = Flask(__name__)
    
    # Configuration
    app.config.from_object('config.Config')
    
    # Initialize extensions
    db.init_app(app)
    CORS(app)
    cache = Cache(app)
    
    # Setup Flask-Security
    user_datastore = SQLAlchemyUserDatastore(db, User, Role)
    security = Security(app, user_datastore)
    
    # Setup Flask-Login
    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(user_id)

    # Register blueprints
    from .routes.auth import auth_bp
    from .routes.students import student_bp
    from .routes.projects import project_bp
    from .routes.milestones import milestone_bp
    from .routes.github import github_bp
    from .routes.documents import document_bp
    from .routes.viva import viva_bp
    from .routes.notifications import notification_bp

    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(student_bp, url_prefix='/api/students')
    app.register_blueprint(project_bp, url_prefix='/api/projects')
    app.register_blueprint(milestone_bp, url_prefix='/api/milestones')
    app.register_blueprint(github_bp, url_prefix='/api/github')
    app.register_blueprint(document_bp, url_prefix='/api/documents')
    app.register_blueprint(viva_bp, url_prefix='/api/viva')
    app.register_blueprint(notification_bp, url_prefix='/api/notifications')

    # Create database tables
    with app.app_context():
        db.create_all()
        
    return app