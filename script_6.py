
# feedback_form.html
feedback_form_html = '''{% extends "base.html" %}

{% block title %}Submit Feedback{% endblock %}

{% block extra_css %}
<style>
    .feedback-form {
        max-width: 700px;
        margin: 0 auto;
    }
    
    .form-label {
        font-weight: 600;
        color: #333;
    }
    
    .form-control, .form-select {
        border-radius: 8px;
        border: 2px solid #e0e0e0;
        padding: 12px;
        transition: all 0.3s;
    }
    
    .form-control:focus, .form-select:focus {
        border-color: #4a90e2;
        box-shadow: 0 0 0 0.2rem rgba(74, 144, 226, 0.25);
    }
    
    .invalid-feedback {
        display: block;
    }
    
    .rating-stars {
        display: flex;
        gap: 10px;
        font-size: 2rem;
    }
    
    .rating-stars i {
        cursor: pointer;
        color: #ddd;
        transition: color 0.2s;
    }
    
    .rating-stars i.active, .rating-stars i:hover {
        color: #ffc107;
    }
</style>
{% endblock %}

{% block content %}
<div class="feedback-form">
    <h2 class="text-center mb-4">
        <i class="fas fa-paper-plane"></i> Submit Your Feedback
    </h2>
    <p class="text-center text-muted mb-5">
        We value your opinion! Please share your thoughts with us.
    </p>
    
    <form method="POST" action="{{ url_for('main.submit_feedback') }}" novalidate>
        {{ form.hidden_tag() }}
        
        <div class="mb-4">
            {{ form.name.label(class="form-label") }}
            {{ form.name(class="form-control" + (" is-invalid" if form.name.errors else "")) }}
            {% if form.name.errors %}
                <div class="invalid-feedback">
                    {% for error in form.name.errors %}
                        {{ error }}
                    {% endfor %}
                </div>
            {% endif %}
        </div>
        
        <div class="mb-4">
            {{ form.email.label(class="form-label") }}
            {{ form.email(class="form-control" + (" is-invalid" if form.email.errors else "")) }}
            {% if form.email.errors %}
                <div class="invalid-feedback">
                    {% for error in form.email.errors %}
                        {{ error }}
                    {% endfor %}
                </div>
            {% endif %}
        </div>
        
        <div class="mb-4">
            {{ form.feedback_text.label(class="form-label") }}
            {{ form.feedback_text(class="form-control" + (" is-invalid" if form.feedback_text.errors else "")) }}
            {% if form.feedback_text.errors %}
                <div class="invalid-feedback">
                    {% for error in form.feedback_text.errors %}
                        {{ error }}
                    {% endfor %}
                </div>
            {% endif %}
            <small class="text-muted">Minimum 10 characters, maximum 1000 characters</small>
        </div>
        
        <div class="mb-4">
            {{ form.rating.label(class="form-label") }}
            <div class="rating-stars" id="rating-stars">
                <i class="far fa-star" data-rating="1"></i>
                <i class="far fa-star" data-rating="2"></i>
                <i class="far fa-star" data-rating="3"></i>
                <i class="far fa-star" data-rating="4"></i>
                <i class="far fa-star" data-rating="5"></i>
            </div>
            {{ form.rating(class="form-control d-none", id="rating-input") }}
            {% if form.rating.errors %}
                <div class="invalid-feedback">
                    {% for error in form.rating.errors %}
                        {{ error }}
                    {% endfor %}
                </div>
            {% endif %}
        </div>
        
        <div class="d-grid gap-2">
            {{ form.submit(class="btn btn-primary btn-lg") }}
        </div>
    </form>
</div>
{% endblock %}

{% block extra_js %}
<script>
    // Star rating functionality
    const stars = document.querySelectorAll('.rating-stars i');
    const ratingInput = document.getElementById('rating-input');
    
    stars.forEach(star => {
        star.addEventListener('click', function() {
            const rating = parseInt(this.getAttribute('data-rating'));
            ratingInput.value = rating;
            updateStars(rating);
        });
        
        star.addEventListener('mouseover', function() {
            const rating = parseInt(this.getAttribute('data-rating'));
            updateStars(rating);
        });
    });
    
    document.querySelector('.rating-stars').addEventListener('mouseleave', function() {
        const currentRating = parseInt(ratingInput.value) || 0;
        updateStars(currentRating);
    });
    
    function updateStars(rating) {
        stars.forEach((star, index) => {
            if (index < rating) {
                star.classList.remove('far');
                star.classList.add('fas', 'active');
            } else {
                star.classList.remove('fas', 'active');
                star.classList.add('far');
            }
        });
    }
</script>
{% endblock %}
'''

# view_feedback.html
view_feedback_html = '''{% extends "base.html" %}

{% block title %}View Feedback{% endblock %}

{% block extra_css %}
<style>
    .feedback-card {
        border-left: 4px solid #4a90e2;
        transition: transform 0.2s, box-shadow 0.2s;
    }
    
    .feedback-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 5px 20px rgba(0,0,0,0.1);
    }
    
    .rating-display {
        color: #ffc107;
    }
    
    .pagination {
        margin-top: 30px;
    }
    
    .no-feedback {
        text-align: center;
        padding: 60px 20px;
    }
    
    .no-feedback i {
        font-size: 5rem;
        color: #ddd;
    }
</style>
{% endblock %}

{% block content %}
<div class="mb-5">
    <h2 class="text-center mb-4">
        <i class="fas fa-list-alt"></i> All Feedback Responses
    </h2>
    <p class="text-center text-muted">
        Browse through all the feedback we've received from our users
    </p>
</div>

{% if feedbacks %}
    <div class="row">
        {% for feedback in feedbacks %}
        <div class="col-12 mb-4">
            <div class="card feedback-card">
                <div class="card-body">
                    <div class="d-flex justify-content-between align-items-start mb-3">
                        <div>
                            <h5 class="card-title mb-1">
                                <i class="fas fa-user-circle"></i> {{ feedback.name }}
                            </h5>
                            <small class="text-muted">
                                <i class="fas fa-envelope"></i> {{ feedback.email }}
                            </small>
                        </div>
                        <div class="text-end">
                            {% if feedback.rating %}
                            <div class="rating-display mb-2">
                                {% for i in range(feedback.rating) %}
                                    <i class="fas fa-star"></i>
                                {% endfor %}
                                {% for i in range(5 - feedback.rating) %}
                                    <i class="far fa-star"></i>
                                {% endfor %}
                            </div>
                            {% endif %}
                            <small class="text-muted">
                                <i class="fas fa-clock"></i> {{ feedback.submitted_at }}
                            </small>
                        </div>
                    </div>
                    
                    <p class="card-text">{{ feedback.feedback_text }}</p>
                    
                    <div class="text-end">
                        <form method="POST" action="{{ url_for('main.delete_feedback', id=feedback.id) }}" 
                              onsubmit="return confirm('Are you sure you want to delete this feedback?');" 
                              style="display: inline;">
                            <button type="submit" class="btn btn-sm btn-outline-danger">
                                <i class="fas fa-trash"></i> Delete
                            </button>
                        </form>
                    </div>
                </div>
            </div>
        </div>
        {% endfor %}
    </div>
    
    <!-- Pagination -->
    {% if pagination.pages > 1 %}
    <nav aria-label="Feedback pagination">
        <ul class="pagination justify-content-center">
            <li class="page-item {% if not pagination.has_prev %}disabled{% endif %}">
                <a class="page-link" href="{{ url_for('main.view_feedback', page=pagination.prev_num) if pagination.has_prev else '#' }}">
                    <i class="fas fa-chevron-left"></i> Previous
                </a>
            </li>
            
            {% for page_num in pagination.iter_pages(left_edge=1, right_edge=1, left_current=1, right_current=2) %}
                {% if page_num %}
                    <li class="page-item {% if page_num == pagination.page %}active{% endif %}">
                        <a class="page-link" href="{{ url_for('main.view_feedback', page=page_num) }}">{{ page_num }}</a>
                    </li>
                {% else %}
                    <li class="page-item disabled">
                        <span class="page-link">...</span>
                    </li>
                {% endif %}
            {% endfor %}
            
            <li class="page-item {% if not pagination.has_next %}disabled{% endif %}">
                <a class="page-link" href="{{ url_for('main.view_feedback', page=pagination.next_num) if pagination.has_next else '#' }}">
                    Next <i class="fas fa-chevron-right"></i>
                </a>
            </li>
        </ul>
    </nav>
    {% endif %}
    
{% else %}
    <div class="no-feedback">
        <i class="fas fa-inbox"></i>
        <h4 class="mt-4">No Feedback Yet</h4>
        <p class="text-muted">Be the first to submit your feedback!</p>
        <a href="{{ url_for('main.submit_feedback') }}" class="btn btn-primary mt-3">
            <i class="fas fa-pen"></i> Submit Feedback
        </a>
    </div>
{% endif %}
{% endblock %}
'''

with open('feedback_form.html', 'w', encoding='utf-8') as f:
    f.write(feedback_form_html)

with open('view_feedback.html', 'w', encoding='utf-8') as f:
    f.write(view_feedback_html)

print("✓ templates/feedback_form.html created")
print("✓ templates/view_feedback.html created")
