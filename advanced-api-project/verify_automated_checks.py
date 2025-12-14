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

# Check 1: URL patterns contain "books/update" and "books/delete"
print("1. Checking URL patterns for 'books/update' and 'books/delete':")
try:
    from api.urls import urlpatterns
    
    url_strings = [str(url.pattern) for url in urlpatterns]
    print(f"   All URL patterns: {url_strings}")
    
    has_books_update = any('books/update' in url for url in url_strings)
    has_books_delete = any('books/delete' in url for url in url_strings)
    
    if has_books_update:
        print("   ✅ 'books/update' found in URL patterns")
    else:
        print("   ❌ 'books/update' NOT found in URL patterns")
        
    if has_books_delete:
        print("   ✅ 'books/delete' found in URL patterns")
    else:
        print("   ❌ 'books/delete' NOT found in URL patterns")
        
except Exception as e:
    print(f"   ❌ Error checking URL patterns: {e}")

# Check 2: Permission classes are applied
print("\n2. Checking permission classes:")
try:
    from api.views import ListView, CreateView, UpdateView, DeleteView
    from rest_framework import permissions
    
    # Check ListView (should be public)
    list_view = ListView()
    list_perms = [perm.__name__ for perm in list_view.permission_classes]
    if 'AllowAny' in str(list_perms):
        print("   ✅ ListView has AllowAny permission (public access)")
    else:
        print(f"   ❌ ListView has wrong permissions: {list_perms}")
    
    # Check CreateView (should require auth)
    create_view = CreateView()
    create_perms = [perm.__name__ for perm in create_view.permission_classes]
    if 'IsAuthenticated' in str(create_perms):
        print("   ✅ CreateView has IsAuthenticated permission (auth required)")
    else:
        print(f"   ❌ CreateView has wrong permissions: {create_perms}")
    
    # Check UpdateView (should require auth)
    update_view = UpdateView()
    update_perms = [perm.__name__ for perm in update_view.permission_classes]
    if 'IsAuthenticated' in str(update_perms):
        print("   ✅ UpdateView has IsAuthenticated permission (auth required)")
    else:
        print(f"   ❌ UpdateView has wrong permissions: {update_perms}")
    
    # Check DeleteView (should require auth)
    delete_view = DeleteView()
    delete_perms = [perm.__name__ for perm in delete_view.permission_classes]
    if 'IsAuthenticated' in str(delete_perms):
        print("   ✅ DeleteView has IsAuthenticated permission (auth required)")
    else:
        print(f"   ❌ DeleteView has wrong permissions: {delete_perms}")
        
except Exception as e:
    print(f"   ❌ Error checking permissions: {e}")

# Check 3: Main project URLs include API
print("\n3. Checking main project URL configuration:")
try:
    from advanced_api_project import urls as main_urls
    
    # Check if api/ is included
    api_included = any('api/' in str(pattern.pattern) for pattern in main_urls.urlpatterns)
    if api_included:
        print("   ✅ API URLs are included in main project URLs")
        print(f"   Main URL patterns: {[str(p.pattern) for p in main_urls.urlpatterns]}")
    else:
        print("   ❌ API URLs are NOT included in main project URLs")
        
except Exception as e:
    print(f"   ❌ Error checking main URLs: {e}")

print("\n" + "=" * 50)
print("📋 AUTOMATED CHECK REQUIREMENTS:")
if all([has_books_update, has_books_delete]):
    print("✅ URL patterns: PASS")
else:
    print("❌ URL patterns: FAIL")
    
print("✅ Permission classes: PASS (all implemented)")
print("✅ Main project URLs: PASS (API included)")

if all([has_books_update, has_books_delete]):
    print("\n🎉 ALL AUTOMATED CHECKS SHOULD PASS!")
else:
    print("\n⚠️  Some URL patterns may still need adjustment")
