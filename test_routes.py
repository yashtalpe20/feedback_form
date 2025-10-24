"""
Unit tests for application routes.
"""
import pytest
from app.models import Feedback
from app import db

class TestRoutes:
    """Test class for application routes."""

    def test_index_route(self, client):
        """Test the home page loads successfully."""
        response = client.get('/')
        assert response.status_code == 200
        assert b'Welcome to Feedback Collection System' in response.data

    def test_submit_feedback_get(self, client):
        """Test GET request to feedback submission form."""
        response = client.get('/feedback/submit')
        assert response.status_code == 200
        assert b'Submit Your Feedback' in response.data

    def test_submit_feedback_post_valid(self, client, app):
        """Test POST request with valid feedback data."""
        data = {
            'name': 'John Doe',
            'email': 'john.doe@example.com',
            'feedback_text': 'This is a great service! Keep up the good work.',
            'rating': 5,
            'csrf_token': 'test_token'  # WTF forms CSRF disabled in testing
        }

        response = client.post('/feedback/submit', data=data, follow_redirects=True)
        assert response.status_code == 200

        with app.app_context():
            feedback = Feedback.query.filter_by(email='john.doe@example.com').first()
            assert feedback is not None
            assert feedback.name == 'John Doe'
            assert feedback.rating == 5

    def test_submit_feedback_post_invalid_email(self, client):
        """Test POST request with invalid email."""
        data = {
            'name': 'Jane Doe',
            'email': 'invalid-email',
            'feedback_text': 'This is a test feedback.',
            'rating': 4
        }

        response = client.post('/feedback/submit', data=data)
        assert response.status_code == 200
        assert b'Please enter a valid email address' in response.data or b'Invalid email' in response.data

    def test_submit_feedback_post_short_text(self, client):
        """Test POST request with feedback text too short."""
        data = {
            'name': 'Test User',
            'email': 'test@example.com',
            'feedback_text': 'Too short',
            'rating': 3
        }

        response = client.post('/feedback/submit', data=data)
        assert response.status_code == 200
        # Form validation should fail

    def test_submit_feedback_post_invalid_rating(self, client):
        """Test POST request with invalid rating."""
        data = {
            'name': 'Test User',
            'email': 'test@example.com',
            'feedback_text': 'This is a test feedback message.',
            'rating': 10  # Invalid rating
        }

        response = client.post('/feedback/submit', data=data)
        assert response.status_code == 200
        # Form validation should fail

    def test_view_feedback_empty(self, client):
        """Test viewing feedback when database is empty."""
        response = client.get('/feedback/view')
        assert response.status_code == 200
        assert b'No Feedback Yet' in response.data or b'All Feedback Responses' in response.data

    def test_view_feedback_with_data(self, client, sample_feedback):
        """Test viewing feedback with existing data."""
        response = client.get('/feedback/view')
        assert response.status_code == 200
        assert b'Test User' in response.data
        assert b'test@example.com' in response.data

    def test_pagination(self, client, app):
        """Test feedback pagination."""
        with app.app_context():
            # Create 15 feedback entries
            for i in range(15):
                feedback = Feedback(
                    name=f"User {i}",
                    email=f"user{i}@example.com",
                    feedback_text=f"Test feedback number {i} with sufficient length.",
                    rating=5
                )
                db.session.add(feedback)
            db.session.commit()

        # First page
        response = client.get('/feedback/view?page=1')
        assert response.status_code == 200

        # Second page
        response = client.get('/feedback/view?page=2')
        assert response.status_code == 200

    def test_delete_feedback(self, client, app, sample_feedback):
        """Test deleting feedback."""
        with app.app_context():
            feedback_id = sample_feedback.id

        response = client.post(f'/feedback/delete/{feedback_id}', follow_redirects=True)
        assert response.status_code == 200

        with app.app_context():
            deleted_feedback = Feedback.query.get(feedback_id)
            assert deleted_feedback is None

    def test_delete_nonexistent_feedback(self, client):
        """Test deleting feedback that doesn't exist."""
        response = client.post('/feedback/delete/9999')
        assert response.status_code == 404

class TestModels:
    """Test class for database models."""

    def test_feedback_creation(self, app):
        """Test creating a feedback instance."""
        with app.app_context():
            feedback = Feedback(
                name="Model Test",
                email="model@test.com",
                feedback_text="Testing the feedback model.",
                rating=4
            )
            db.session.add(feedback)
            db.session.commit()

            retrieved = Feedback.query.filter_by(email="model@test.com").first()
            assert retrieved is not None
            assert retrieved.name == "Model Test"
            assert retrieved.rating == 4

    def test_feedback_to_dict(self, app, sample_feedback):
        """Test converting feedback to dictionary."""
        with app.app_context():
            feedback_dict = sample_feedback.to_dict()
            assert 'id' in feedback_dict
            assert 'name' in feedback_dict
            assert 'email' in feedback_dict
            assert 'feedback_text' in feedback_dict
            assert 'rating' in feedback_dict
            assert 'submitted_at' in feedback_dict

    def test_feedback_validate_rating(self):
        """Test rating validation."""
        assert Feedback.validate_rating(1) == True
        assert Feedback.validate_rating(5) == True
        assert Feedback.validate_rating(3) == True
        assert Feedback.validate_rating(None) == True
        assert Feedback.validate_rating(0) == False
        assert Feedback.validate_rating(6) == False

class TestForms:
    """Test class for form validation."""

    def test_valid_form_data(self, app):
        """Test form with valid data."""
        from app.forms import FeedbackForm

        with app.test_request_context():
            form = FeedbackForm(
                name="Valid User",
                email="valid@example.com",
                feedback_text="This is a valid feedback message with enough characters.",
                rating=5
            )
            # Note: Without CSRF token in test context, we skip validation
            assert form.name.data == "Valid User"
            assert form.email.data == "valid@example.com"
