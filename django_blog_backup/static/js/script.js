// Main JavaScript for Django Blog

document.addEventListener('DOMContentLoaded', function() {
    // Auto-hide messages after 5 seconds
    const messages = document.querySelectorAll('.alert');
    messages.forEach(function(message) {
        setTimeout(function() {
            message.style.transition = 'opacity 0.5s ease';
            message.style.opacity = '0';
            setTimeout(function() {
                message.remove();
            }, 500);
        }, 5000);
    });
    
    // Form validation enhancement
    const forms = document.querySelectorAll('form');
    forms.forEach(function(form) {
        // Skip logout form
        if (form.classList.contains('logout-form')) return;
        
        form.addEventListener('submit', function(e) {
            const requiredFields = form.querySelectorAll('[required]');
            let isValid = true;
            
            requiredFields.forEach(function(field) {
                if (!field.value.trim()) {
                    isValid = false;
                    field.style.borderColor = '#dc3545';
                    
                    // Add error message if not present
                    if (!field.nextElementSibling || !field.nextElementSibling.classList.contains('error-message')) {
                        const errorDiv = document.createElement('div');
                        errorDiv.className = 'error-message';
                        errorDiv.textContent = 'This field is required.';
                        field.parentNode.insertBefore(errorDiv, field.nextSibling);
                    }
                } else {
                    field.style.borderColor = '';
                    
                    // Remove error message if present
                    if (field.nextElementSibling && field.nextElementSibling.classList.contains('error-message')) {
                        field.nextElementSibling.remove();
                    }
                }
            });
            
            // Password confirmation check
            const password1 = form.querySelector('#id_password1');
            const password2 = form.querySelector('#id_password2');
            if (password1 && password2 && password1.value !== password2.value) {
                isValid = false;
                password2.style.borderColor = '#dc3545';
                
                if (!password2.nextElementSibling || !password2.nextElementSibling.classList.contains('error-message')) {
                    const errorDiv = document.createElement('div');
                    errorDiv.className = 'error-message';
                    errorDiv.textContent = 'Passwords do not match.';
                    password2.parentNode.insertBefore(errorDiv, password2.nextSibling);
                }
            }
            
            if (!isValid) {
                e.preventDefault();
                // Scroll to first error
                const firstError = form.querySelector('.error-message');
                if (firstError) {
                    firstError.scrollIntoView({ behavior: 'smooth', block: 'center' });
                }
            }
        });
    });
    
    // Confirm delete actions
    const deleteButtons = document.querySelectorAll('.btn-delete, .logout-form button');
    deleteButtons.forEach(function(button) {
        button.addEventListener('click', function(e) {
            if (button.classList.contains('btn-delete')) {
                if (!confirm('Are you sure you want to delete this post? This action cannot be undone.')) {
                    e.preventDefault();
                }
            } else if (button.closest('.logout-form')) {
                if (!confirm('Are you sure you want to log out?')) {
                    e.preventDefault();
                }
            }
        });
    });
    
    // Password visibility toggle
    const passwordFields = document.querySelectorAll('input[type="password"]');
    passwordFields.forEach(function(field) {
        const wrapper = document.createElement('div');
        wrapper.style.position = 'relative';
        wrapper.style.width = '100%';
        
        const toggleBtn = document.createElement('button');
        toggleBtn.type = 'button';
        toggleBtn.className = 'password-toggle';
        toggleBtn.innerHTML = '👁️';
        toggleBtn.style.background = 'none';
        toggleBtn.style.border = 'none';
        toggleBtn.style.cursor = 'pointer';
        toggleBtn.style.position = 'absolute';
        toggleBtn.style.right = '10px';
        toggleBtn.style.top = '50%';
        toggleBtn.style.transform = 'translateY(-50%)';
        toggleBtn.style.fontSize = '1.2em';
        
        field.parentNode.insertBefore(wrapper, field);
        wrapper.appendChild(field);
        wrapper.appendChild(toggleBtn);
        
        toggleBtn.addEventListener('click', function() {
            if (field.type === 'password') {
                field.type = 'text';
                toggleBtn.innerHTML = '👁️‍🗨️';
            } else {
                field.type = 'password';
                toggleBtn.innerHTML = '👁️';
            }
        });
    });
});
