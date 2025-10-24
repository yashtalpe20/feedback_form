
# Create additional helpful files

# .env.example for reference
env_example = '''# Flask Environment Configuration
# Copy this file to .env and update with your values

# Flask Configuration
FLASK_ENV=development
SECRET_KEY=your-secret-key-here-change-in-production

# Database Configuration
# For SQLite (Development)
DATABASE_URL=sqlite:///feedback_dev.db

# For PostgreSQL (Production)
# DATABASE_URL=postgresql://username:password@localhost/feedback_db

# Server Configuration
PORT=5000

# Email Configuration (Optional - for future email features)
# MAIL_SERVER=smtp.gmail.com
# MAIL_PORT=587
# MAIL_USE_TLS=True
# MAIL_USERNAME=your-email@example.com
# MAIL_PASSWORD=your-password
'''

# .gitignore
gitignore_content = '''# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg

# Virtual Environment
venv/
ENV/
env/

# Flask
instance/
.webassets-cache

# Database
*.db
*.sqlite
*.sqlite3

# Environment Variables
.env
.flaskenv

# IDE
.vscode/
.idea/
*.swp
*.swo
*~

# OS
.DS_Store
Thumbs.db

# Testing
.pytest_cache/
.coverage
htmlcov/
*.cover

# Logs
*.log

# Migrations (optional - commit if you want)
# migrations/
'''

# pytest.ini
pytest_ini = '''[pytest]
testpaths = tests
python_files = test_*.py
python_classes = Test*
python_functions = test_*
addopts = -v --tb=short
'''

# MongoDB Alternative (app/models_mongo.py)
models_mongo = '''"""
MongoDB models using PyMongo (Alternative to SQLAlchemy).
To use this, install: pip install pymongo flask-pymongo
"""
from flask_pymongo import PyMongo
from datetime import datetime
from bson import ObjectId

mongo = PyMongo()

class FeedbackMongo:
    """Feedback operations for MongoDB."""
    
    collection_name = 'feedback'
    
    @staticmethod
    def create(name, email, feedback_text, rating=None):
        """Create a new feedback entry."""
        feedback = {
            'name': name,
            'email': email,
            'feedback_text': feedback_text,
            'rating': rating,
            'submitted_at': datetime.utcnow()
        }
        result = mongo.db[FeedbackMongo.collection_name].insert_one(feedback)
        return result.inserted_id
    
    @staticmethod
    def find_all(page=1, per_page=10):
        """Get all feedback with pagination."""
        skip = (page - 1) * per_page
        feedbacks = mongo.db[FeedbackMongo.collection_name].find().sort('submitted_at', -1).skip(skip).limit(per_page)
        return list(feedbacks)
    
    @staticmethod
    def find_by_id(feedback_id):
        """Find feedback by ID."""
        return mongo.db[FeedbackMongo.collection_name].find_one({'_id': ObjectId(feedback_id)})
    
    @staticmethod
    def delete(feedback_id):
        """Delete feedback by ID."""
        result = mongo.db[FeedbackMongo.collection_name].delete_one({'_id': ObjectId(feedback_id)})
        return result.deleted_count > 0
    
    @staticmethod
    def count():
        """Count total feedback entries."""
        return mongo.db[FeedbackMongo.collection_name].count_documents({})
'''

# MongoDB configuration (config_mongo.py)
config_mongo = '''"""
MongoDB Configuration (Alternative)
To use this, set MONGO_URI environment variable
"""
import os

class MongoConfig:
    """MongoDB configuration."""
    MONGO_URI = os.environ.get('MONGO_URI') or 'mongodb://localhost:27017/feedback_db'
'''

with open('.env.example', 'w', encoding='utf-8') as f:
    f.write(env_example)

with open('.gitignore', 'w', encoding='utf-8') as f:
    f.write(gitignore_content)

with open('pytest.ini', 'w', encoding='utf-8') as f:
    f.write(pytest_ini)

with open('models_mongo.py', 'w', encoding='utf-8') as f:
    f.write(models_mongo)

with open('config_mongo.py', 'w', encoding='utf-8') as f:
    f.write(config_mongo)

print("✓ .env.example created")
print("✓ .gitignore created")
print("✓ pytest.ini created")
print("✓ models_mongo.py created (MongoDB alternative)")
print("✓ config_mongo.py created (MongoDB config)")
