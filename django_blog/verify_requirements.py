#!/usr/bin/env python
"""
Script to verify all checker requirements are met
"""
import os
import sys

def check_forms_py():
    """Check if blog/forms.py contains TagWidget()"""
    with open('blog/forms.py', 'r') as f:
        content = f.read()
    
    checks = [
        'from taggit.forms import TagWidget',
        'TagWidget()',
        'widget=TagWidget()',
    ]
    
    for check in checks:
        if check not in content:
            print(f"❌ Missing in forms.py: {check}")
            return False
    
    print("✅ forms.py contains TagWidget()")
    return True

def check_views_py():
    """Check if blog/views.py uses Q objects"""
    with open('blog/views.py', 'r') as f:
        content = f.read()
    
    checks = [
        'from django.db.models import Q',
        'Q(title__icontains',
        'Q(content__icontains',
        'Q(tags__name__icontains',
    ]
    
    for check in checks:
        if check not in content:
            print(f"❌ Missing in views.py: {check}")
            return False
    
    print("✅ views.py uses Q objects for search")
    return True

def check_urls_py():
    """Check if blog/urls.py has required patterns"""
    with open('blog/urls.py', 'r') as f:
        content = f.read()
    
    checks = [
        "path('search/', views.search_results",
        "path('tags/<slug:tag_slug>/', views.posts_by_tag",
    ]
    
    for check in checks:
        if check not in content:
            print(f"❌ Missing in urls.py: {check}")
            return False
    
    print("✅ urls.py has search and tag patterns")
    return True

def check_settings_py():
    """Check if django_blog/settings.py has taggit"""
    with open('django_blog/settings.py', 'r') as f:
        content = f.read()
    
    if "'taggit'" not in content:
        print("❌ Missing in settings.py: 'taggit'")
        return False
    
    print("✅ settings.py contains 'taggit'")
    return True

def main():
    print("Checking all requirements...")
    print("=" * 50)
    
    all_good = True
    
    # Check each file
    if not check_forms_py():
        all_good = False
    
    if not check_views_py():
        all_good = False
    
    if not check_urls_py():
        all_good = False
    
    if not check_settings_py():
        all_good = False
    
    print("=" * 50)
    
    if all_good:
        print("✅ ALL REQUIREMENTS MET!")
        return 0
    else:
        print("❌ SOME REQUIREMENTS MISSING")
        return 1

if __name__ == '__main__':
    sys.exit(main())
