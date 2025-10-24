# Testing Guide - Flask Feedback Collection System

Comprehensive guide for testing the Flask Feedback Collection System.

## Table of Contents
1. [Test Setup](#test-setup)
2. [Running Tests](#running-tests)
3. [Test Structure](#test-structure)
4. [Writing Tests](#writing-tests)
5. [Code Coverage](#code-coverage)

---

## Test Setup

### Prerequisites
```bash
pip install pytest pytest-cov
```

### Test Configuration

The test configuration is defined in `pytest.ini`:
```ini
[pytest]
testpaths = tests
python_files = test_*.py
python_classes = Test*
python_functions = test_*
addopts = -v --tb=short
```

---

## Running Tests

### Run All Tests
```bash
pytest
```

### Run with Verbose Output
```bash
pytest -v
```

### Run Specific Test File
```bash
pytest tests/test_routes.py
```

### Run Specific Test Class
```bash
pytest tests/test_routes.py::TestRoutes
```

### Run Specific Test Function
```bash
pytest tests/test_routes.py::TestRoutes::test_index_route
```

### Run Tests Matching Pattern
```bash
pytest -k "feedback"
```

---

## Test Structure

### Directory Structure
```
tests/
├── __init__.py          # Test package initialization
├── conftest.py          # Shared fixtures
└── test_routes.py       # Route and functionality tests
```

### Test Classes

#### 1. TestRoutes
Tests for application routes and views

#### 2. TestModels
Tests for database models

#### 3. TestForms
Tests for form validation

---

## Test Fixtures

### Available Fixtures

#### app
Creates a test application instance with testing configuration
```python
@pytest.fixture()
def app():
    app = create_app('testing')
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()
```

#### client
Provides a test client for making requests
```python
@pytest.fixture()
def client(app):
    return app.test_client()
```

#### runner
Provides a CLI test runner
```python
@pytest.fixture()
def runner(app):
    return app.test_cli_runner()
```

#### sample_feedback
Creates sample feedback data for testing
```python
@pytest.fixture()
def sample_feedback(app):
    with app.app_context():
        feedback = Feedback(
            name="Test User",
            email="test@example.com",
            feedback_text="Test feedback message",
            rating=5
        )
        db.session.add(feedback)
        db.session.commit()
        return feedback
```

---

## Writing Tests

### Basic Test Structure

```python
def test_function_name(client, app):
    """Test description."""
    # Arrange
    data = {'key': 'value'}

    # Act
    response = client.get('/route')

    # Assert
    assert response.status_code == 200
```

### Testing GET Requests

```python
def test_home_page(client):
    """Test home page loads successfully."""
    response = client.get('/')
    assert response.status_code == 200
    assert b'Welcome' in response.data
```

### Testing POST Requests

```python
def test_submit_feedback(client, app):
    """Test feedback submission."""
    data = {
        'name': 'John Doe',
        'email': 'john@example.com',
        'feedback_text': 'Great service!',
        'rating': 5
    }

    response = client.post('/feedback/submit', data=data)
    assert response.status_code == 200 or response.status_code == 302
```

### Testing Database Operations

```python
def test_database_insert(app):
    """Test inserting data into database."""
    with app.app_context():
        feedback = Feedback(
            name="Test",
            email="test@test.com",
            feedback_text="Test message",
            rating=4
        )
        db.session.add(feedback)
        db.session.commit()

        retrieved = Feedback.query.filter_by(email="test@test.com").first()
        assert retrieved is not None
        assert retrieved.name == "Test"
```

### Testing Form Validation

```python
def test_invalid_email(client):
    """Test form validation for invalid email."""
    data = {
        'name': 'Test',
        'email': 'invalid-email',
        'feedback_text': 'Test message',
        'rating': 3
    }

    response = client.post('/feedback/submit', data=data)
    assert b'valid email' in response.data
```

---

## Code Coverage

### Generate Coverage Report

```bash
pytest --cov=app
```

### Generate HTML Coverage Report

```bash
pytest --cov=app --cov-report=html
```

Then open `htmlcov/index.html` in your browser.

### Coverage by File

```bash
pytest --cov=app --cov-report=term-missing
```

### Minimum Coverage Requirement

Add to `pytest.ini`:
```ini
[pytest]
addopts = --cov=app --cov-fail-under=80
```

---

## Test Examples

### Complete Test Example

```python
class TestFeedbackSubmission:
    """Test feedback submission functionality."""

    def test_valid_submission(self, client, app):
        """Test submitting valid feedback."""
        data = {
            'name': 'Alice Johnson',
            'email': 'alice@example.com',
            'feedback_text': 'Excellent service! Very satisfied.',
            'rating': 5
        }

        response = client.post('/feedback/submit', 
                              data=data, 
                              follow_redirects=True)

        assert response.status_code == 200

        with app.app_context():
            feedback = Feedback.query.filter_by(
                email='alice@example.com'
            ).first()
            assert feedback is not None
            assert feedback.name == 'Alice Johnson'
            assert feedback.rating == 5

    def test_missing_required_fields(self, client):
        """Test submission with missing fields."""
        data = {
            'name': '',
            'email': 'test@example.com',
            'feedback_text': '',
            'rating': 3
        }

        response = client.post('/feedback/submit', data=data)
        assert response.status_code == 200
        assert b'required' in response.data.lower()

    def test_invalid_rating(self, client):
        """Test submission with invalid rating."""
        data = {
            'name': 'Test User',
            'email': 'test@example.com',
            'feedback_text': 'Test feedback message here',
            'rating': 10
        }

        response = client.post('/feedback/submit', data=data)
        assert response.status_code == 200
```

---

## Continuous Integration

### GitHub Actions Example

Create `.github/workflows/tests.yml`:

```yaml
name: Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest

    steps:
    - uses: actions/checkout@v2

    - name: Set up Python
      uses: actions/setup-python@v2
      with:
        python-version: '3.11'

    - name: Install dependencies
      run: |
        pip install -r requirements.txt
        pip install pytest pytest-cov

    - name: Run tests
      run: |
        pytest --cov=app --cov-report=xml

    - name: Upload coverage
      uses: codecov/codecov-action@v2
```

---

## Best Practices

1. **Test Isolation**: Each test should be independent
2. **Clear Names**: Use descriptive test names
3. **Arrange-Act-Assert**: Follow AAA pattern
4. **Test Edge Cases**: Include boundary conditions
5. **Mock External Services**: Don't depend on external APIs
6. **Fast Tests**: Keep tests quick to run
7. **Comprehensive Coverage**: Aim for 80%+ coverage

---

## Debugging Tests

### Print Debug Information

```python
def test_with_debug(client, app):
    response = client.get('/')
    print(f"Status: {response.status_code}")
    print(f"Data: {response.data}")
    assert response.status_code == 200
```

Run with:
```bash
pytest -s  # Show print statements
```

### Use pdb Debugger

```python
def test_with_debugger(client):
    response = client.get('/')
    import pdb; pdb.set_trace()
    assert response.status_code == 200
```

---

## Performance Testing

### Install locust

```bash
pip install locust
```

### Create locustfile.py

```python
from locust import HttpUser, task, between

class FeedbackUser(HttpUser):
    wait_time = between(1, 3)

    @task
    def view_home(self):
        self.client.get("/")

    @task
    def submit_feedback(self):
        self.client.post("/feedback/submit", data={
            'name': 'Load Test User',
            'email': 'loadtest@example.com',
            'feedback_text': 'Performance testing feedback',
            'rating': 4
        })
```

Run:
```bash
locust -f locustfile.py
```

---

## Troubleshooting Tests

### Common Issues

1. **Database conflicts**: Ensure test database is separate
2. **CSRF tokens**: Disable in testing config
3. **Session handling**: Use `follow_redirects=True`
4. **Fixture scope**: Understand function vs module scope

---

## Resources

- [pytest Documentation](https://docs.pytest.org/)
- [Flask Testing Guide](https://flask.palletsprojects.com/testing/)
- [Coverage.py](https://coverage.readthedocs.io/)
