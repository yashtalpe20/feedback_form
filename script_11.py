
# Create deployment guides

# DEPLOYMENT_GUIDE.md
deployment_guide = '''# Deployment Guide - Flask Feedback Collection System

This guide covers deploying the Flask Feedback Collection System to various cloud platforms.

## Table of Contents
1. [Heroku Deployment](#heroku-deployment)
2. [AWS Deployment](#aws-deployment)
3. [Render Deployment](#render-deployment)
4. [Digital Ocean Deployment](#digital-ocean-deployment)
5. [Environment Variables](#environment-variables)

---

## Heroku Deployment

### Prerequisites
- Heroku account (free tier available)
- Heroku CLI installed
- Git installed

### Step-by-Step Guide

#### 1. Install Heroku CLI
```bash
# macOS
brew tap heroku/brew && brew install heroku

# Windows
# Download from: https://devcenter.heroku.com/articles/heroku-cli

# Linux
curl https://cli-assets.heroku.com/install.sh | sh
```

#### 2. Login to Heroku
```bash
heroku login
```

#### 3. Initialize Git Repository
```bash
git init
git add .
git commit -m "Initial commit"
```

#### 4. Create Heroku Application
```bash
heroku create your-feedback-app-name
```

#### 5. Add PostgreSQL Database
```bash
heroku addons:create heroku-postgresql:mini
```

#### 6. Set Environment Variables
```bash
heroku config:set SECRET_KEY=$(python -c 'import secrets; print(secrets.token_hex(32))')
heroku config:set FLASK_ENV=production
```

#### 7. Deploy to Heroku
```bash
git push heroku main
```

#### 8. Run Database Migrations (if using Flask-Migrate)
```bash
heroku run flask db upgrade
```

#### 9. Open Your Application
```bash
heroku open
```

### Heroku Configuration Files

The following files are already included:

- `Procfile`: Tells Heroku how to run your app
  ```
  web: gunicorn run:app
  ```

- `runtime.txt`: Specifies Python version
  ```
  python-3.11.6
  ```

### Monitoring and Logs
```bash
# View logs
heroku logs --tail

# Check app status
heroku ps

# Scale dynos
heroku ps:scale web=1
```

---

## AWS Deployment

### Option 1: AWS Elastic Beanstalk

#### Prerequisites
- AWS account
- AWS CLI installed
- EB CLI installed

#### 1. Install EB CLI
```bash
pip install awsebcli
```

#### 2. Initialize EB Application
```bash
eb init -p python-3.11 feedback-app --region us-east-1
```

#### 3. Create Environment and Deploy
```bash
eb create feedback-app-env
```

#### 4. Set Environment Variables
```bash
eb setenv SECRET_KEY=your-secret-key
eb setenv FLASK_ENV=production
eb setenv DATABASE_URL=your-database-url
```

#### 5. Deploy Updates
```bash
eb deploy
```

#### 6. Open Application
```bash
eb open
```

### Option 2: AWS EC2

1. Launch EC2 instance (Ubuntu 22.04 recommended)
2. SSH into instance
3. Install dependencies:
```bash
sudo apt update
sudo apt install python3-pip python3-venv nginx
```

4. Clone repository and setup:
```bash
git clone <your-repo>
cd feedback-app
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

5. Configure Nginx and systemd service
6. Start application with Gunicorn

---

## Render Deployment

### Step-by-Step Guide

#### 1. Create Render Account
Visit https://render.com and sign up

#### 2. Connect GitHub Repository
- Click "New +" → "Web Service"
- Connect your GitHub account
- Select your repository

#### 3. Configure Service
- **Name**: feedback-app
- **Environment**: Python 3
- **Build Command**: `pip install -r requirements.txt`
- **Start Command**: `gunicorn run:app`

#### 4. Add Environment Variables
```
SECRET_KEY=your-secret-key
FLASK_ENV=production
```

#### 5. Add Database
- Click "New +" → "PostgreSQL"
- Connect to your web service
- Copy the internal database URL

#### 6. Update Environment Variables
Add the database URL from step 5

#### 7. Deploy
Click "Create Web Service"

### Auto-Deploy
Enable auto-deploy from GitHub for automatic deployments on push

---

## Digital Ocean Deployment

### Option 1: App Platform

#### 1. Create Digital Ocean Account
Visit https://www.digitalocean.com

#### 2. Create App
- Click "Create" → "Apps"
- Connect GitHub repository
- Select branch

#### 3. Configure Resources
- **Resource Type**: Web Service
- **Build Command**: `pip install -r requirements.txt`
- **Run Command**: `gunicorn run:app`

#### 4. Add Database
- Add PostgreSQL database component
- Note the connection string

#### 5. Set Environment Variables
```
SECRET_KEY=your-secret-key
FLASK_ENV=production
DATABASE_URL=${db.DATABASE_URL}
```

#### 6. Deploy
Click "Create Resources"

### Option 2: Droplet

1. Create Ubuntu 22.04 droplet
2. SSH into droplet
3. Install dependencies:
```bash
apt update
apt install python3-pip python3-venv nginx postgresql
```

4. Setup application (similar to EC2)

---

## Environment Variables

### Required Variables
```bash
SECRET_KEY=generate-a-secure-random-key
FLASK_ENV=production
DATABASE_URL=your-database-connection-string
```

### Optional Variables
```bash
PORT=5000
ITEMS_PER_PAGE=10
```

### Generating Secure Secret Key
```python
import secrets
print(secrets.token_hex(32))
```

---

## Database Setup

### PostgreSQL Setup

For production, use PostgreSQL instead of SQLite.

#### 1. Update requirements.txt
Already included:
```
psycopg2-binary==2.9.9
```

#### 2. Set DATABASE_URL
```bash
# Format
DATABASE_URL=postgresql://username:password@host:port/database

# Example
DATABASE_URL=postgresql://user:pass@localhost:5432/feedback_db
```

### MongoDB Setup (Alternative)

#### 1. Install MongoDB dependencies
```bash
pip install pymongo flask-pymongo
```

#### 2. Update configuration
Use `models_mongo.py` and `config_mongo.py` included in the project

#### 3. Set MONGO_URI
```bash
MONGO_URI=mongodb://username:password@host:port/database
```

---

## SSL/HTTPS Configuration

Most platforms (Heroku, Render, DO App Platform) provide automatic SSL.

For custom deployments:
1. Use Let's Encrypt with Certbot
2. Configure Nginx for SSL termination

---

## Monitoring and Maintenance

### Health Checks
Add a health check endpoint in `routes.py`:
```python
@main_bp.route('/health')
def health_check():
    return {'status': 'healthy'}, 200
```

### Logging
Configure logging in `__init__.py`:
```python
import logging
logging.basicConfig(level=logging.INFO)
```

### Backup Strategy
- Regular database backups
- Git repository backups
- Environment variable documentation

---

## Troubleshooting

### Common Issues

#### 1. Application Won't Start
- Check logs: `heroku logs --tail` or platform-specific logs
- Verify all environment variables are set
- Check database connection

#### 2. Database Connection Errors
- Verify DATABASE_URL format
- Check database is running
- Ensure firewall allows connections

#### 3. Static Files Not Loading
- Run `flask collect-static` if needed
- Check static file paths
- Verify CDN for Bootstrap/FontAwesome

#### 4. High Memory Usage
- Reduce worker processes in Gunicorn
- Optimize database queries
- Implement caching

---

## Performance Optimization

### 1. Use CDN for Static Assets
Already configured with Bootstrap and FontAwesome CDN

### 2. Database Connection Pooling
Configure in `config.py`:
```python
SQLALCHEMY_ENGINE_OPTIONS = {
    'pool_size': 10,
    'pool_recycle': 3600,
}
```

### 3. Caching
Install Flask-Caching:
```bash
pip install Flask-Caching
```

### 4. Gunicorn Workers
```bash
gunicorn --workers 4 --threads 2 run:app
```

---

## Security Checklist

- ✅ Use HTTPS in production
- ✅ Set strong SECRET_KEY
- ✅ Enable CSRF protection
- ✅ Validate all user inputs
- ✅ Use parameterized database queries
- ✅ Keep dependencies updated
- ✅ Use environment variables for secrets
- ✅ Implement rate limiting (future enhancement)
- ✅ Regular security audits

---

## Cost Estimates (Monthly)

| Platform | Free Tier | Paid Tier |
|----------|-----------|-----------|
| Heroku | $5 (eco dyno) | $25+ |
| Render | Free | $7+ |
| AWS | Free for 1 year | $10+ |
| Digital Ocean | - | $6+ |

---

## Support and Documentation

- [Flask Documentation](https://flask.palletsprojects.com/)
- [Heroku Python Support](https://devcenter.heroku.com/categories/python-support)
- [AWS Elastic Beanstalk](https://docs.aws.amazon.com/elasticbeanstalk/)
- [Render Documentation](https://render.com/docs)
- [Digital Ocean Tutorials](https://www.digitalocean.com/community/tutorials)
'''

# Create TESTING_GUIDE.md
testing_guide = '''# Testing Guide - Flask Feedback Collection System

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
'''

with open('DEPLOYMENT_GUIDE.md', 'w', encoding='utf-8') as f:
    f.write(deployment_guide)

with open('TESTING_GUIDE.md', 'w', encoding='utf-8') as f:
    f.write(testing_guide)

print("✓ DEPLOYMENT_GUIDE.md created")
print("✓ TESTING_GUIDE.md created")
print("\n" + "="*60)
print("✅ ALL FILES GENERATED SUCCESSFULLY!")
print("="*60)
