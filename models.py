"""
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
