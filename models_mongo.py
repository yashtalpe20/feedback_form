"""
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
