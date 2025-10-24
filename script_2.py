
# 2. app/__init__.py - Application Factory
app_init_content = '''"""
Application Factory for Flask Feedback Application.
Creates and configures the Flask app instance.
"""
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import os

# Initialize extensions
db = SQLAlchemy()
migrate = Migrate()

def create_app(config_name=None):
    """
    Application factory function.
    
    Args:
        config_name: Configuration to use ('development', 'testing', 'production')
    
    Returns:
        Flask application instance
    """
    app = Flask(__name__)
    
    # Load configuration
    if config_name is None:
        config_name = os.environ.get('FLASK_ENV', 'development')
    
    from config import config
    app.config.from_object(config[config_name])
    
    # Initialize extensions with app
    db.init_app(app)
    migrate.init_app(app, db)
    
    # Register blueprints
    from app.routes import main_bp
    app.register_blueprint(main_bp)
    
    # Create database tables
    with app.app_context():
        db.create_all()
    
    return app
'''

# 3. app/models.py - Database Models
models_content = '''"""
Database models for the Feedback Application.
"""
from app import db
from datetime import datetime

class Feedback(db.Model):
    """Feedback model for storing user feedback."""
    
    __tablename__ = 'feedback'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    feedback_text = db.Column(db.Text, nullable=False)
    rating = db.Column(db.Integer, nullable=True)  # 1-5 star rating
    submitted_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<Feedback {self.id}: {self.name}>'
    
    def to_dict(self):
        """Convert feedback to dictionary."""
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'feedback_text': self.feedback_text,
            'rating': self.rating,
            'submitted_at': self.submitted_at.strftime('%Y-%m-%d %H:%M:%S')
        }
    
    @staticmethod
    def validate_rating(rating):
        """Validate rating value."""
        if rating is not None:
            return 1 <= rating <= 5
        return True
'''

with open('app_init.py', 'w', encoding='utf-8') as f:
    f.write(app_init_content)

with open('models.py', 'w', encoding='utf-8') as f:
    f.write(models_content)

print("✓ app/__init__.py created")
print("✓ app/models.py created")
