# LibraryProject - ALX Django Advanced Features & Security

This project implements all advanced Django features and security practices as required by the ALX curriculum.

## Tasks Implemented

### Task 0: Custom User Model
- Custom User model extending AbstractUser
- Additional fields: date_of_birth, profile_photo
- Email-based authentication instead of username
- Custom User Manager with create_user and create_superuser methods

### Task 1: Permissions & Groups
- Custom permissions: can_view, can_create, can_edit, can_delete
- Permission-protected views using @permission_required decorators
- Group-based access control system

### Task 2: Security Best Practices
- CSRF protection in all forms
- XSS prevention through input validation
- SQL injection prevention using Django ORM
- Secure form handling and data validation

### Task 3: HTTPS & Secure Redirects
- SECURE_SSL_REDIRECT = True
- HSTS configuration with 1-year duration
- Secure cookies (SESSION_COOKIE_SECURE, CSRF_COOKIE_SECURE)
- Security headers implementation

## Project Structure
- `LibraryProject/` - Django project configuration
- `bookshelf/` - Main application with all implemented features
- Custom User model, permissions, security features all integrated

## Setup
1. Run migrations: `python manage.py migrate`
2. Create superuser: `python manage.py createsuperuser`
3. Start server: `python manage.py runserver`
