
# 4. app/forms.py - WTForms for validation
forms_content = '''"""
Forms for the Feedback Application using Flask-WTF.
"""
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, IntegerField, SubmitField
from wtforms.validators import DataRequired, Email, Length, NumberRange, Optional

class FeedbackForm(FlaskForm):
    """Form for submitting feedback."""
    
    name = StringField(
        'Name',
        validators=[
            DataRequired(message='Name is required'),
            Length(min=2, max=100, message='Name must be between 2 and 100 characters')
        ],
        render_kw={"placeholder": "Enter your full name"}
    )
    
    email = StringField(
        'Email',
        validators=[
            DataRequired(message='Email is required'),
            Email(message='Please enter a valid email address'),
            Length(max=120, message='Email must not exceed 120 characters')
        ],
        render_kw={"placeholder": "your.email@example.com"}
    )
    
    feedback_text = TextAreaField(
        'Feedback',
        validators=[
            DataRequired(message='Feedback is required'),
            Length(min=10, max=1000, message='Feedback must be between 10 and 1000 characters')
        ],
        render_kw={"placeholder": "Share your thoughts...", "rows": 5}
    )
    
    rating = IntegerField(
        'Rating (1-5)',
        validators=[
            Optional(),
            NumberRange(min=1, max=5, message='Rating must be between 1 and 5')
        ],
        render_kw={"placeholder": "Rate from 1 to 5"}
    )
    
    submit = SubmitField('Submit Feedback')
'''

with open('forms.py', 'w', encoding='utf-8') as f:
    f.write(forms_content)

print("✓ app/forms.py created")
