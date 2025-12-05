#!/usr/bin/env python3
"""
URL Configuration Verification Script
"""

import os
import sys
import django

# Setup Django
sys.path.append('/Alx_DjangoLearnLab/advanced-api-project')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'advanced_api_project.settings')
django.setup()

from django.urls import resolve, Resolver404

print("🔗 URL CONFIGURATION VERIFICATION")
print("=" * 50)

# Test URLs that should work
test_urls = [
    '/api/auth-token/',
    '/api/books/',
    '/api/books/1/',
    '/api/books/create/',
    '/api/books/1/update/',
    '/api/books/1/delete/',
    '/api/books/combined/',
    '/api/books/combined/1/',
    '/api/authors/',
    '/api/authors/1/',
]

print("Testing URL resolution:")
for url in test_urls:
    try:
        match = resolve(url)
        print(f"✅ {url} -> {match.view_name}")
    except Resolver404:
        print(f"❌ {url} -> NOT FOUND")

print("\n" + "=" * 50)
print("🎯 URL VERIFICATION COMPLETED")
