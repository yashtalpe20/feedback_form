"""
Pytest configuration and fixtures for testing.
"""
import pytest
from app import create_app, db
from app.models import Feedback

@pytest.fixture()
def app():
    """Create and configure a test application instance."""
    app = create_app('testing')

    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()

@pytest.fixture()
def client(app):
    """Create a test client for the app."""
    return app.test_client()

@pytest.fixture()
def runner(app):
    """Create a test CLI runner."""
    return app.test_cli_runner()

@pytest.fixture()
def sample_feedback(app):
    """Create sample feedback for testing."""
    with app.app_context():
        feedback = Feedback(
            name="Test User",
            email="test@example.com",
            feedback_text="This is a test feedback message for testing purposes.",
            rating=5
        )
        db.session.add(feedback)
        db.session.commit()
        return feedback
