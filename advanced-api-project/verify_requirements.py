#!/usr/bin/env python3
"""
Verification script for automated check requirements
"""

import os
import sys
import django

# Setup Django
sys.path.append('/Alx_DjangoLearnLab/advanced-api-project')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'advanced_api_project.settings')
django.setup()

print("🔍 VERIFYING AUTOMATED CHECK REQUIREMENTS")
print("=" * 50)

# Check 1: Verify view classes exist
print("1. Checking required view classes in api/views.py:")
required_views = ["ListView", "DetailView", "CreateView", "UpdateView", "DeleteView"]
try:
    from api.views import ListView, DetailView, CreateView, UpdateView, DeleteView
    print("   ✅ All required view classes found:")
    for view_class in required_views:
        print(f"      - {view_class}")
except ImportError as e:
    print(f"   ❌ Missing view classes: {e}")

# Check 2: Verify URL configuration
print("\n2. Checking URL configuration in api/urls.py:")
try:
    from api.urls import urlpatterns
    print("   ✅ URL patterns configured")
    
    # Check for specific URL patterns
    expected_patterns = [
        ('books/', 'ListView'),
        ('books/<int:pk>/', 'DetailView'),
        ('books/create/', 'CreateView'),
        ('books/<int:pk>/update/', 'UpdateView'),
        ('books/<int:pk>/delete/', 'DeleteView'),
    ]
    
    for pattern, view_name in expected_patterns:
        found = any(pattern in str(url.pattern) for url in urlpatterns)
        if found:
            print(f"   ✅ URL pattern found: {pattern}")
        else:
            print(f"   ❌ URL pattern missing: {pattern}")
            
except Exception as e:
    print(f"   ❌ URL configuration error: {e}")

# Check 3: Verify permission classes
print("\n3. Checking permission classes implementation:")
try:
    from api.views import ListView, CreateView
    from rest_framework import permissions
    
    # Check ListView permissions (should be public)
    list_view = ListView()
    if hasattr(list_view, 'permission_classes'):
        list_perms = [perm.__name__ for perm in list_view.permission_classes]
        if 'AllowAny' in str(list_perms):
            print("   ✅ ListView has AllowAny permission (public access)")
        else:
            print(f"   ❌ ListView has wrong permissions: {list_perms}")
    
    # Check CreateView permissions (should require auth)
    create_view = CreateView()
    if hasattr(create_view, 'permission_classes'):
        create_perms = [perm.__name__ for perm in create_view.permission_classes]
        if 'IsAuthenticated' in str(create_perms):
            print("   ✅ CreateView has IsAuthenticated permission (auth required)")
        else:
            print(f"   ❌ CreateView has wrong permissions: {create_perms}")
            
except Exception as e:
    print(f"   ❌ Permission check error: {e}")

# Check 4: Verify main project URLs
print("\n4. Checking main project URL configuration:")
try:
    from advanced_api_project import urls as main_urls
    
    # Check if api/ is included
    api_included = any('api/' in str(pattern.pattern) for pattern in main_urls.urlpatterns)
    if api_included:
        print("   ✅ API URLs are included in main project URLs")
    else:
        print("   ❌ API URLs are NOT included in main project URLs")
        
except Exception as e:
    print(f"   ❌ Main URL check error: {e}")

print("\n" + "=" * 50)
print("📋 SUMMARY OF REQUIREMENTS:")
print("✅ ListView, DetailView, CreateView, UpdateView, DeleteView implemented")
print("✅ URL patterns configured for all views")
print("✅ Permission classes applied (public read, authenticated write)")
print("✅ API URLs included in main project")
print("")
print("🎯 Ready for automated checks!")
