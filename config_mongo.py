"""
MongoDB Configuration (Alternative)
To use this, set MONGO_URI environment variable
"""
import os

class MongoConfig:
    """MongoDB configuration."""
    MONGO_URI = os.environ.get('MONGO_URI') or 'mongodb://localhost:27017/feedback_db'
