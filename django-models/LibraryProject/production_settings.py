"""
Production settings for LibraryProject
"""
import os
from .settings import *

# Security settings for production
DEBUG = False

# Generate a secure secret key (in production, use environment variable)
SECRET_KEY = os.environ.get('SECRET_KEY', 'your-very-long-random-secret-key-here')

# Security headers
SECURE_HSTS_SECONDS = 31536000  # 1 year
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True

# SSL/HTTPS settings
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True

# Other security settings
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'

# Allowed hosts for production
ALLOWED_HOSTS = ['your-production-domain.com', 'www.your-production-domain.com']

# Database configuration for production (example)
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql',
#         'NAME': 'mydatabase',
#         'USER': 'mydatabaseuser',
#         'PASSWORD': 'mypassword',
#         'HOST': 'localhost',
#         'PORT': '5432',
#     }
# }
