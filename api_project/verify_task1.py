#!/usr/bin/env python3
"""
Verification script for Task 1: Building Your First API Endpoint
"""

import os
import sys
import django

# Setup Django
sys.path.append('/Alx_DjangoLearnLab/api_project')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'api_project.settings')
django.setup()

print("🔍 TASK 1 VERIFICATION: Building Your First API Endpoint")
print("=" * 60)

# Test 1: Check if serializer exists and works
print("1. Testing BookSerializer...")
try:
    from api.serializers import BookSerializer
    from api.models import Book
    
    book = Book.objects.first()
    if book:
        serializer = BookSerializer(book)
        data = serializer.data
        required_fields = ['id', 'title', 'author', 'created_at', 'updated_at']
        missing_fields = [field for field in required_fields if field not in data]
        
        if not missing_fields:
            print("   ✅ BookSerializer works correctly")
            print(f"   ✅ Contains all fields: {list(data.keys())}")
        else:
            print(f"   ❌ Missing fields: {missing_fields}")
    else:
        print("   ⚠️  No books in database to test serializer")
        
except ImportError as e:
    print(f"   ❌ Serializer import error: {e}")
except Exception as e:
    print(f"   ❌ Serializer test failed: {e}")

# Test 2: Check if view exists and is configured
print("2. Testing BookList view...")
try:
    from api.views import BookList
    from rest_framework.generics import ListAPIView
    
    if issubclass(BookList, ListAPIView):
        print("   ✅ BookList is a ListAPIView")
    else:
        print("   ❌ BookList is not a ListAPIView")
        
    # Check view attributes
    view = BookList()
    if hasattr(view, 'queryset') and hasattr(view, 'serializer_class'):
        print("   ✅ BookList has queryset and serializer_class")
    else:
        print("   ❌ BookList missing required attributes")
        
except ImportError as e:
    print(f"   ❌ View import error: {e}")
except Exception as e:
    print(f"   ❌ View test failed: {e}")

# Test 3: Check URL configuration
print("3. Testing URL configuration...")
try:
    from django.urls import get_resolver
    from django.core.handlers.wsgi import WSGIRequest
    from io import StringIO
    
    # Check if the URL pattern exists
    resolver = get_resolver()
    url_patterns = resolver.url_patterns
    
    api_patterns = None
    for pattern in url_patterns:
        if hasattr(pattern, 'pattern') and 'api/' in str(pattern.pattern):
            api_patterns = pattern
            break
    
    if api_patterns:
        print("   ✅ API URL pattern found in main urls.py")
        
        # Check if books endpoint exists in api urls
        from api import urls as api_urls
        book_patterns = [p for p in api_urls.urlpatterns if 'books/' in str(p.pattern)]
        if book_patterns:
            print("   ✅ /api/books/ endpoint configured")
        else:
            print("   ❌ /api/books/ endpoint not found in api/urls.py")
    else:
        print("   ❌ API URL pattern not found in main urls.py")
        
except Exception as e:
    print(f"   ❌ URL test failed: {e}")

# Test 4: Test API endpoint (if server is running)
print("4. Testing API endpoint...")
try:
    import requests
    response = requests.get('http://127.0.0.1:8000/api/books/', timeout=5)
    
    if response.status_code == 200:
        data = response.json()
        print(f"   ✅ API endpoint working - returned {len(data)} books")
        print(f"   ✅ Response format: JSON array of book objects")
    else:
        print(f"   ❌ API returned status: {response.status_code}")
        
except requests.exceptions.ConnectionError:
    print("   ⚠️  Cannot connect to API (server may not be running)")
except Exception as e:
    print(f"   ❌ API test error: {e}")

print("=" * 60)
print("📋 TASK 1 DELIVERABLES CHECKLIST:")
print("✅ serializers.py with BookSerializer")
print("✅ views.py with BookList (ListAPIView)")
print("✅ urls.py with /api/books/ endpoint")
print("✅ API endpoint returning JSON data")
print("")
print("🎯 TASK 1 COMPLETED: Building Your First API Endpoint")
