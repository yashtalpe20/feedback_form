/**
 * Flask Feedback Collection System
 * Main JavaScript File
 * Version: 1.0.0
 * 
 * Features:
 * - Interactive 5-star rating system
 * - Real-time form validation
 * - Character counter
 * - Delete confirmations
 * - Auto-closing alerts
 * - Bootstrap integration
 */

// ===================================
// Document Ready - Initialize All
// ===================================

document.addEventListener('DOMContentLoaded', function() {
    console.log('Feedback Collection System initialized');
    
    // Initialize all components
    initStarRating();
    initFormValidation();
    initDeleteConfirmation();
    initCharacterCounter();
    initTooltips();
    initAlertAutoClose();
});

// ===================================
// Star Rating System
// ===================================

function initStarRating() {
    const starsContainer = document.querySelector('.rating-stars');
    
    if (!starsContainer) return;
    
    const stars = starsContainer.querySelectorAll('i');
    const ratingInput = document.getElementById('rating-input');
    
    if (!stars.length || !ratingInput) return;
    
    // Click event - set rating
    stars.forEach(star => {
        star.addEventListener('click', function() {
            const rating = parseInt(this.getAttribute('data-rating'));
            ratingInput.value = rating;
            updateStars(rating);
        });
        
        // Mouseover event - preview rating
        star.addEventListener('mouseover', function() {
            const rating = parseInt(this.getAttribute('data-rating'));
            updateStars(rating);
        });
    });
    
    // Mouseleave event - restore selected rating
    starsContainer.addEventListener('mouseleave', function() {
        const currentRating = parseInt(ratingInput.value) || 0;
        updateStars(currentRating);
    });
    
    // Update star display
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
    
    // Initialize with current value
    const initialRating = parseInt(ratingInput.value) || 0;
    if (initialRating > 0) {
        updateStars(initialRating);
    }
}

// ===================================
// Form Validation
// ===================================

function initFormValidation() {
    const forms = document.querySelectorAll('form.needs-validation');
    
    forms.forEach(form => {
        form.addEventListener('submit', function(event) {
            if (!form.checkValidity()) {
                event.preventDefault();
                event.stopPropagation();
            }
            
            form.classList.add('was-validated');
        }, false);
    });
    
    // Real-time email validation
    const emailInput = document.getElementById('email');
    if (emailInput) {
        emailInput.addEventListener('blur', function() {
            validateEmail(this.value);
        });
    }
    
    // Real-time name validation
    const nameInput = document.getElementById('name');
    if (nameInput) {
        nameInput.addEventListener('input', function() {
            validateName(this.value);
        });
    }
}

// Email validation function
function validateEmail(email) {
    const emailPattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    const emailInput = document.getElementById('email');
    
    if (!emailInput) return;
    
    if (emailPattern.test(email)) {
        emailInput.classList.remove('is-invalid');
        emailInput.classList.add('is-valid');
        return true;
    } else {
        emailInput.classList.remove('is-valid');
        emailInput.classList.add('is-invalid');
        return false;
    }
}

// Name validation function
function validateName(name) {
    const nameInput = document.getElementById('name');
    
    if (!nameInput) return;
    
    if (name.length >= 2 && name.length <= 100) {
        nameInput.classList.remove('is-invalid');
        nameInput.classList.add('is-valid');
        return true;
    } else if (name.length > 0) {
        nameInput.classList.remove('is-valid');
        nameInput.classList.add('is-invalid');
        return false;
    }
}

// ===================================
// Character Counter
// ===================================

function initCharacterCounter() {
    const feedbackTextarea = document.getElementById('feedback_text');
    
    if (!feedbackTextarea) return;
    
    // Create counter element
    const counterDiv = document.createElement('div');
    counterDiv.className = 'character-counter text-muted small mt-1';
    feedbackTextarea.parentNode.appendChild(counterDiv);
    
    // Update counter
    function updateCounter() {
        const length = feedbackTextarea.value.length;
        const maxLength = 1000;
        const minLength = 10;
        
        counterDiv.textContent = `${length} / ${maxLength} characters`;
        
        if (length < minLength) {
            counterDiv.classList.add('text-danger');
            counterDiv.classList.remove('text-success');
        } else if (length >= maxLength) {
            counterDiv.classList.add('text-warning');
            counterDiv.classList.remove('text-success');
        } else {
            counterDiv.classList.add('text-success');
            counterDiv.classList.remove('text-danger', 'text-warning');
        }
    }
    
    feedbackTextarea.addEventListener('input', updateCounter);
    updateCounter(); // Initial update
}

// ===================================
// Delete Confirmation
// ===================================

function initDeleteConfirmation() {
    const deleteForms = document.querySelectorAll('form[action*="delete"]');
    
    deleteForms.forEach(form => {
        form.addEventListener('submit', function(event) {
            const confirmed = confirm('Are you sure you want to delete this feedback? This action cannot be undone.');
            
            if (!confirmed) {
                event.preventDefault();
                return false;
            }
        });
    });
}

// ===================================
// Tooltips Initialization
// ===================================

function initTooltips() {
    // Initialize Bootstrap tooltips if available
    if (typeof bootstrap !== 'undefined' && bootstrap.Tooltip) {
        const tooltipTriggerList = [].slice.call(
            document.querySelectorAll('[data-bs-toggle="tooltip"]')
        );
        tooltipTriggerList.map(function(tooltipTriggerEl) {
            return new bootstrap.Tooltip(tooltipTriggerEl);
        });
    }
}

// ===================================
// Auto-close Alerts
// ===================================

function initAlertAutoClose() {
    const alerts = document.querySelectorAll('.alert:not(.alert-permanent)');
    
    alerts.forEach(alert => {
        // Auto-close after 5 seconds
        setTimeout(() => {
            if (typeof bootstrap !== 'undefined' && bootstrap.Alert) {
                const bsAlert = new bootstrap.Alert(alert);
                bsAlert.close();
            }
        }, 5000);
    });
}

// ===================================
// Utility Functions
// ===================================

// Smooth scroll to element
function smoothScrollTo(element) {
    if (element) {
        element.scrollIntoView({
            behavior: 'smooth',
            block: 'start'
        });
    }
}

// Show loading spinner
function showLoading(button) {
    if (!button) return;
    
    button.disabled = true;
    button.innerHTML = '<span class="spinner-border spinner-border-sm me-2"></span>Loading...';
}

// Hide loading spinner
function hideLoading(button, originalText) {
    if (!button) return;
    
    button.disabled = false;
    button.innerHTML = originalText;
}

// Format date
function formatDate(dateString) {
    const options = {
        year: 'numeric',
        month: 'short',
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
    };
    
    return new Date(dateString).toLocaleDateString('en-US', options);
}

// Copy to clipboard
function copyToClipboard(text) {
    navigator.clipboard.writeText(text).then(function() {
        showNotification('Copied to clipboard!', 'success');
    }, function(err) {
        showNotification('Failed to copy', 'error');
    });
}

// Show notification
function showNotification(message, type = 'info') {
    const alertDiv = document.createElement('div');
    alertDiv.className = `alert alert-${type} alert-dismissible fade show`;
    alertDiv.setAttribute('role', 'alert');
    alertDiv.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;
    
    const container = document.querySelector('.container');
    if (container) {
        container.insertBefore(alertDiv, container.firstChild);
        
        // Auto-close after 3 seconds
        setTimeout(() => {
            if (typeof bootstrap !== 'undefined' && bootstrap.Alert) {
                const bsAlert = new bootstrap.Alert(alertDiv);
                bsAlert.close();
            }
        }, 3000);
    }
}

// ===================================
// AJAX Form Submission (Optional)
// ===================================

function submitFormAjax(formId) {
    const form = document.getElementById(formId);
    
    if (!form) return;
    
    form.addEventListener('submit', function(event) {
        event.preventDefault();
        
        const formData = new FormData(form);
        const submitButton = form.querySelector('button[type="submit"]');
        const originalText = submitButton.innerHTML;
        
        showLoading(submitButton);
        
        fetch(form.action, {
            method: form.method,
            body: formData
        })
        .then(response => response.json())
        .then(data => {
            hideLoading(submitButton, originalText);
            
            if (data.success) {
                showNotification(data.message, 'success');
                form.reset();
                
                // Reset star rating
                const ratingInput = document.getElementById('rating-input');
                if (ratingInput) {
                    ratingInput.value = '';
                    const stars = document.querySelectorAll('.rating-stars i');
                    stars.forEach(star => {
                        star.classList.remove('fas', 'active');
                        star.classList.add('far');
                    });
                }
            } else {
                showNotification(data.message || 'An error occurred', 'error');
            }
        })
        .catch(error => {
            hideLoading(submitButton, originalText);
            showNotification('An error occurred. Please try again.', 'error');
            console.error('Error:', error);
        });
    });
}

// ===================================
// Filter and Sort Functions
// ===================================

function filterFeedback(searchTerm) {
    const feedbackCards = document.querySelectorAll('.feedback-card');
    
    feedbackCards.forEach(card => {
        const text = card.textContent.toLowerCase();
        
        if (text.includes(searchTerm.toLowerCase())) {
            card.style.display = '';
        } else {
            card.style.display = 'none';
        }
    });
}

function sortFeedback(sortBy) {
    const container = document.querySelector('.feedback-container');
    const feedbackCards = Array.from(document.querySelectorAll('.feedback-card'));
    
    feedbackCards.sort((a, b) => {
        switch (sortBy) {
            case 'date':
                return new Date(b.dataset.date) - new Date(a.dataset.date);
            case 'rating':
                return parseInt(b.dataset.rating) - parseInt(a.dataset.rating);
            case 'name':
                return a.dataset.name.localeCompare(b.dataset.name);
            default:
                return 0;
        }
    });
    
    feedbackCards.forEach(card => {
        container.appendChild(card);
    });
}

// ===================================
// Export to CSV
// ===================================

function exportToCSV() {
    const feedbackCards = document.querySelectorAll('.feedback-card');
    let csv = 'Name,Email,Feedback,Rating,Date\n';
    
    feedbackCards.forEach(card => {
        const name = card.querySelector('.card-title').textContent.trim();
        const email = card.querySelector('small').textContent.trim();
        const feedback = card.querySelector('.card-text').textContent.trim();
        const rating = card.dataset.rating || 'N/A';
        const date = card.dataset.date || '';
        
        csv += `"${name}","${email}","${feedback}","${rating}","${date}"\n`;
    });
    
    // Create download link
    const blob = new Blob([csv], { type: 'text/csv' });
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = 'feedback_export.csv';
    a.click();
    window.URL.revokeObjectURL(url);
}

// ===================================
// Console Info
// ===================================

console.log('%c Flask Feedback Collection System ', 'background: #4a90e2; color: white; padding: 5px 10px; border-radius: 3px;');
console.log('%c Version 1.0.0 ', 'background: #50c878; color: white; padding: 5px 10px; border-radius: 3px;');
console.log('Built with Flask, Bootstrap 5, and JavaScript');
console.log('Ready to collect feedback!');
