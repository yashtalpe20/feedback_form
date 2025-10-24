# Deployment Guide - Flask Feedback Collection System

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
