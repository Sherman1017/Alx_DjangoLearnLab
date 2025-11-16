# HTTPS Deployment Guide for Django Application

## Task: Implementing HTTPS and Secure Redirects in Django

### Overview
This document provides comprehensive guidance for deploying the Django application with HTTPS enforcement and secure redirects as required by the ALX task.

## 1. Django HTTPS Configuration

### Core Settings Implemented
```python
# HTTPS Enforcement
SECURE_SSL_REDIRECT = True  # Redirect HTTP → HTTPS

# HSTS Configuration
SECURE_HSTS_SECONDS = 31536000  # 1 year
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True

# Secure Cookies
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True

# Security Headers
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'
