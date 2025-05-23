from flask_security import Security, auth_required
from config import DevelopmentConfig
from components.extensions import db, bcrypt, cache, datastore
from components.models import User
from flask import Flask
from flask_login import LoginManager
from flask_cors import CORS

from components.authentication import auth_bp
from components.project import project_bp
from components.submission import student_submission_bp
from components.milestones import milestone_bp
from components.student import student_bp
from components.commit_history import commit_history_bp
from components.llm import llm_bp
from components.github_url import assignment_bp
from components.admin_stats import admin_dashboard_bp

def create_app():
    app = Flask(__name__)
    app.config.from_object(DevelopmentConfig)
    login_manager = LoginManager()
    login_manager.init_app(app)
    app.security = Security(app, datastore)
    db.init_app(app)
    bcrypt.init_app(app)
    
    app.register_blueprint(auth_bp)
    app.register_blueprint(project_bp)
    app.register_blueprint(student_submission_bp)
    app.register_blueprint(milestone_bp)
    app.register_blueprint(student_bp)
    app.register_blueprint(commit_history_bp)
    app.register_blueprint(llm_bp)
    app.register_blueprint(assignment_bp)
    app.register_blueprint(admin_dashboard_bp)
    
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))
    
    # CORS for separate servers
    
    CORS(app), 
     

    # Initialize Flask-Caching with Redis
    cache.init_app(app)

    # Initialize Redis client
    #redis_client = Redis(host='localhost', port=6379, db=0)
    
    return app

app = create_app()

@app.route('/')
def hello_world():
    return "Hello World"

if __name__ == '__main__':
    print("Running app")
    print(app.url_map)
    app.run(debug=True)