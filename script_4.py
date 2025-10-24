
# 5. app/routes.py - Application Routes
routes_content = '''"""
Routes for the Feedback Application.
"""
from flask import Blueprint, render_template, redirect, url_for, flash, request
from app import db
from app.models import Feedback
from app.forms import FeedbackForm

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    """Home page with welcome message."""
    feedback_count = Feedback.query.count()
    return render_template('index.html', feedback_count=feedback_count)

@main_bp.route('/feedback/submit', methods=['GET', 'POST'])
def submit_feedback():
    """Submit feedback form."""
    form = FeedbackForm()
    
    if form.validate_on_submit():
        # Create new feedback entry
        feedback = Feedback(
            name=form.name.data,
            email=form.email.data,
            feedback_text=form.feedback_text.data,
            rating=form.rating.data
        )
        
        try:
            db.session.add(feedback)
            db.session.commit()
            flash('Thank you for your feedback! Your response has been recorded.', 'success')
            return redirect(url_for('main.submit_feedback'))
        except Exception as e:
            db.session.rollback()
            flash('An error occurred while submitting your feedback. Please try again.', 'error')
            print(f"Error: {e}")
    
    return render_template('feedback_form.html', form=form)

@main_bp.route('/feedback/view')
def view_feedback():
    """View all submitted feedback with pagination."""
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    
    # Get feedback with pagination, ordered by most recent first
    pagination = Feedback.query.order_by(Feedback.submitted_at.desc()).paginate(
        page=page,
        per_page=per_page,
        error_out=False
    )
    
    feedbacks = pagination.items
    
    return render_template(
        'view_feedback.html',
        feedbacks=feedbacks,
        pagination=pagination
    )

@main_bp.route('/feedback/delete/<int:id>', methods=['POST'])
def delete_feedback(id):
    """Delete a specific feedback entry (admin function)."""
    feedback = Feedback.query.get_or_404(id)
    
    try:
        db.session.delete(feedback)
        db.session.commit()
        flash('Feedback deleted successfully.', 'success')
    except Exception as e:
        db.session.rollback()
        flash('An error occurred while deleting the feedback.', 'error')
        print(f"Error: {e}")
    
    return redirect(url_for('main.view_feedback'))

@main_bp.errorhandler(404)
def not_found_error(error):
    """Handle 404 errors."""
    return render_template('404.html'), 404

@main_bp.errorhandler(500)
def internal_error(error):
    """Handle 500 errors."""
    db.session.rollback()
    return render_template('500.html'), 500
'''

with open('routes.py', 'w', encoding='utf-8') as f:
    f.write(routes_content)

print("✓ app/routes.py created")
