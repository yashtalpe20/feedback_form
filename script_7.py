
# 7. Create run.py - Application entry point
run_py_content = '''"""
Application entry point for the Flask Feedback Application.
"""
import os
from app import create_app

app = create_app(os.environ.get('FLASK_ENV', 'development'))

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
'''

# 8. Create requirements.txt
requirements_content = '''Flask==3.0.0
Flask-SQLAlchemy==3.1.1
Flask-Migrate==4.0.5
Flask-WTF==1.2.1
WTForms==3.1.1
email-validator==2.1.0
python-dotenv==1.0.0
gunicorn==21.2.0
psycopg2-binary==2.9.9
'''

# 9. Create Procfile for Heroku
procfile_content = '''web: gunicorn run:app
'''

# 10. Create runtime.txt
runtime_content = '''python-3.11.6
'''

with open('run.py', 'w', encoding='utf-8') as f:
    f.write(run_py_content)

with open('requirements.txt', 'w', encoding='utf-8') as f:
    f.write(requirements_content)

with open('Procfile', 'w', encoding='utf-8') as f:
    f.write(procfile_content)

with open('runtime.txt', 'w', encoding='utf-8') as f:
    f.write(runtime_content)

print("✓ run.py created")
print("✓ requirements.txt created")
print("✓ Procfile created (for Heroku deployment)")
print("✓ runtime.txt created (for Heroku deployment)")
