#!/bin/bash

echo "🧪 Testing Production Configuration..."

# Test 1: Settings import
echo "1. Testing production settings import..."
python -c "
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'social_media_api.production_settings')
try:
    from django.conf import settings
    print('✅ Production settings import successful')
    print(f'   DEBUG: {settings.DEBUG}')
    print(f'   ALLOWED_HOSTS: {settings.ALLOWED_HOSTS}')
except Exception as e:
    print(f'❌ Error: {e}')
"

# Test 2: Database connection
echo -e "\n2. Testing database configuration..."
python -c "
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'social_media_api.production_settings')
os.environ.setdefault('DATABASE_URL', 'sqlite:///test.db')
from django.conf import settings
try:
    from django.db import connection
    connection.ensure_connection()
    print('✅ Database configuration valid')
except Exception as e:
    print(f'❌ Database error: {e}')
"

# Test 3: Static files configuration
echo -e "\n3. Testing static files configuration..."
python -c "
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'social_media_api.production_settings')
from django.conf import settings
print(f'✅ Static URL: {settings.STATIC_URL}')
print(f'✅ Static Root: {settings.STATIC_ROOT}')
print(f'✅ Media URL: {settings.MEDIA_URL}')
print(f'✅ Media Root: {settings.MEDIA_ROOT}')
"

# Test 4: Security settings
echo -e "\n4. Testing security settings..."
python -c "
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'social_media_api.production_settings')
from django.conf import settings
security_settings = [
    ('SECURE_SSL_REDIRECT', settings.SECURE_SSL_REDIRECT),
    ('SESSION_COOKIE_SECURE', settings.SESSION_COOKIE_SECURE),
    ('CSRF_COOKIE_SECURE', settings.CSRF_COOKIE_SECURE),
    ('SECURE_BROWSER_XSS_FILTER', settings.SECURE_BROWSER_XSS_FILTER),
]
for name, value in security_settings:
    status = '✅' if value else '⚠️'
    print(f'{status} {name}: {value}')
"

echo -e "\n🎉 Production configuration tests completed!"
