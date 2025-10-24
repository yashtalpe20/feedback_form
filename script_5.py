
# 6. Create HTML Templates

# base.html
base_html = '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{% block title %}Feedback Collection System{% endblock %}</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <style>
        :root {
            --primary-color: #4a90e2;
            --secondary-color: #50c878;
            --danger-color: #e74c3c;
        }
        
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding-bottom: 50px;
        }
        
        .navbar {
            background: rgba(255, 255, 255, 0.95) !important;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }
        
        .container-main {
            background: white;
            border-radius: 15px;
            box-shadow: 0 10px 40px rgba(0,0,0,0.2);
            padding: 40px;
            margin-top: 30px;
        }
        
        .alert {
            border-radius: 10px;
            margin-bottom: 20px;
        }
        
        .btn-primary {
            background-color: var(--primary-color);
            border: none;
            padding: 12px 30px;
            border-radius: 8px;
            transition: all 0.3s;
        }
        
        .btn-primary:hover {
            background-color: #357abd;
            transform: translateY(-2px);
            box-shadow: 0 5px 15px rgba(74, 144, 226, 0.3);
        }
        
        .footer {
            text-align: center;
            color: white;
            padding: 20px;
            margin-top: 50px;
        }
    </style>
    {% block extra_css %}{% endblock %}
</head>
<body>
    <nav class="navbar navbar-expand-lg navbar-light">
        <div class="container">
            <a class="navbar-brand" href="{{ url_for('main.index') }}">
                <i class="fas fa-comments"></i> Feedback System
            </a>
            <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav">
                <span class="navbar-toggler-icon"></span>
            </button>
            <div class="collapse navbar-collapse" id="navbarNav">
                <ul class="navbar-nav ms-auto">
                    <li class="nav-item">
                        <a class="nav-link" href="{{ url_for('main.index') }}">
                            <i class="fas fa-home"></i> Home
                        </a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link" href="{{ url_for('main.submit_feedback') }}">
                            <i class="fas fa-pen"></i> Submit Feedback
                        </a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link" href="{{ url_for('main.view_feedback') }}">
                            <i class="fas fa-list"></i> View Feedback
                        </a>
                    </li>
                </ul>
            </div>
        </div>
    </nav>

    <div class="container">
        {% with messages = get_flashed_messages(with_categories=true) %}
            {% if messages %}
                {% for category, message in messages %}
                    <div class="alert alert-{{ 'success' if category == 'success' else 'danger' }} alert-dismissible fade show mt-3" role="alert">
                        {{ message }}
                        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
                    </div>
                {% endfor %}
            {% endif %}
        {% endwith %}

        <div class="container-main">
            {% block content %}{% endblock %}
        </div>
    </div>

    <div class="footer">
        <p>&copy; 2025 Feedback Collection System | Built with Flask</p>
    </div>

    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
    {% block extra_js %}{% endblock %}
</body>
</html>
'''

# index.html
index_html = '''{% extends "base.html" %}

{% block title %}Home - Feedback Collection System{% endblock %}

{% block content %}
<div class="text-center">
    <h1 class="display-4 mb-4">
        <i class="fas fa-comments text-primary"></i>
        Welcome to Feedback Collection System
    </h1>
    <p class="lead text-muted mb-4">
        Your feedback matters! Help us improve by sharing your thoughts and experiences.
    </p>
    
    <div class="row mt-5">
        <div class="col-md-4 mb-4">
            <div class="card border-0 shadow-sm h-100">
                <div class="card-body text-center">
                    <i class="fas fa-pen-fancy fa-3x text-primary mb-3"></i>
                    <h5 class="card-title">Submit Feedback</h5>
                    <p class="card-text">Share your thoughts and help us improve our services.</p>
                    <a href="{{ url_for('main.submit_feedback') }}" class="btn btn-primary">
                        Get Started <i class="fas fa-arrow-right"></i>
                    </a>
                </div>
            </div>
        </div>
        
        <div class="col-md-4 mb-4">
            <div class="card border-0 shadow-sm h-100">
                <div class="card-body text-center">
                    <i class="fas fa-chart-bar fa-3x text-success mb-3"></i>
                    <h5 class="card-title">View Responses</h5>
                    <p class="card-text">Browse through all the feedback we've received.</p>
                    <a href="{{ url_for('main.view_feedback') }}" class="btn btn-success">
                        View All <i class="fas fa-arrow-right"></i>
                    </a>
                </div>
            </div>
        </div>
        
        <div class="col-md-4 mb-4">
            <div class="card border-0 shadow-sm h-100">
                <div class="card-body text-center">
                    <i class="fas fa-database fa-3x text-info mb-3"></i>
                    <h5 class="card-title">Total Feedback</h5>
                    <p class="card-text">We have collected feedback from our users.</p>
                    <h2 class="text-primary">{{ feedback_count }}</h2>
                    <small class="text-muted">responses collected</small>
                </div>
            </div>
        </div>
    </div>
    
    <div class="alert alert-info mt-5" role="alert">
        <i class="fas fa-info-circle"></i>
        <strong>Note:</strong> All feedback is anonymous and will be used solely for improvement purposes.
    </div>
</div>
{% endblock %}
'''

with open('base.html', 'w', encoding='utf-8') as f:
    f.write(base_html)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(index_html)

print("✓ templates/base.html created")
print("✓ templates/index.html created")
