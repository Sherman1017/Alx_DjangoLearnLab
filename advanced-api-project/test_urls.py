#!/usr/bin/env python3
"""
Test script to verify URL configuration
"""

import os
import sys
import django

# Setup Django
sys.path.append('/Alx_DjangoLearnLab/advanced-api-project')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'advanced_api_project.settings')
django.setup()

print("🔗 TESTING URL CONFIGURATION")
print("=" * 50)

# Test 1: Check main URL configuration
print("1. Checking main URL configuration...")
try:
    from advanced_api_project import urls as main_urls
    print("   ✅ Main URLs module imported successfully")
    
    # Check if api/ is included
    api_included = any('api/' in str(pattern.pattern) for pattern in main_urls.urlpatterns)
    if api_included:
        print("   ✅ API URLs are included in main URLs")
    else:
        print("   ❌ API URLs are NOT included in main URLs")
        
except Exception as e:
    print(f"   ❌ Main URL import failed: {e}")

# Test 2: Check API URL configuration
print("\n2. Checking API URL configuration...")
try:
    from api import urls as api_urls
    print("   ✅ API URLs module imported successfully")
    
    # Check specific patterns
    expected_patterns = ['authors/', 'books/', 'books/create/']
    found_patterns = []
    
    for pattern in api_urls.urlpatterns:
        pattern_str = str(pattern.pattern)
        found_patterns.append(pattern_str)
        print(f"   ✅ Found pattern: {pattern_str}")
    
    # Check if all expected patterns exist
    missing_patterns = [p for p in expected_patterns if p not in found_patterns]
    if not missing_patterns:
        print("   ✅ All expected API URL patterns found")
    else:
        print(f"   ❌ Missing patterns: {missing_patterns}")
        
except Exception as e:
    print(f"   ❌ API URL import failed: {e}")

# Test 3: Test URL resolution
print("\n3. Testing URL resolution...")
try:
    from django.urls import resolve, Resolver404
    
    test_urls = [
        '/api/authors/',
        '/api/books/',
        '/api/books/create/'
    ]
    
    for test_url in test_urls:
        try:
            match = resolve(test_url)
            print(f"   ✅ {test_url} -> {match.view_name}")
        except Resolver404:
            print(f"   ❌ {test_url} -> NOT FOUND")
            
except Exception as e:
    print(f"   ❌ URL resolution test failed: {e}")

# Test 4: Check view imports
print("\n4. Checking view imports...")
try:
    from api.views import AuthorList, BookList, BookCreate
    print("   ✅ All views imported successfully")
    
    # Check if views are callable
    views = [AuthorList, BookList, BookCreate]
    for view in views:
        if hasattr(view, 'as_view'):
            print(f"   ✅ {view.__name__} is a valid API view")
        else:
            print(f"   ❌ {view.__name__} is not a valid API view")
            
except ImportError as e:
    print(f"   ❌ View import failed: {e}")

print("\n" + "=" * 50)
print("🎯 URL CONFIGURATION TEST COMPLETED")
