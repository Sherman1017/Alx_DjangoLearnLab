#!/usr/bin/env python3
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'LibraryProject.settings')
django.setup()

from django.test import Client
from django.contrib.auth.models import User
from relationship_app.models import Book, Author
from django.urls import reverse

print("=== TESTING CUSTOM PERMISSIONS ===")
print("=" * 35)

client = Client(HTTP_HOST='localhost')

# Test users
test_users = [
    {'username': 'admin_user', 'role': 'Admin', 'password': 'test123'},
    {'username': 'librarian_user', 'role': 'Librarian', 'password': 'test123'},
    {'username': 'member_user', 'role': 'Member', 'password': 'test123'},
]

# Ensure we have at least one author and book for testing
author, created = Author.objects.get_or_create(name="Test Author")
book, created = Book.objects.get_or_create(title="Test Book", author=author)

print("Testing book management permissions:")

for user_info in test_users:
    print(f"\n👤 Testing: {user_info['username']} ({user_info['role']})")
    print("-" * 35)
    
    # Login
    login_success = client.login(username=user_info['username'], password=user_info['password'])
    print(f"  Login: {'✅ Success' if login_success else '❌ Failed'}")
    
    if login_success:
        # Test access to book management views
        views_to_test = [
            ('relationship_app:add_book', 'Add Book', {}),
            ('relationship_app:edit_book', 'Edit Book', {'pk': book.pk}),
            ('relationship_app:delete_book', 'Delete Book', {'pk': book.pk}),
            ('relationship_app:manage_books', 'Manage Books', {}),
        ]
        
        for view_name, description, kwargs in views_to_test:
            try:
                url = reverse(view_name, kwargs=kwargs)
                response = client.get(url)
                
                if response.status_code == 200:
                    print(f"  ✅ {description:20} -> ACCESS GRANTED")
                elif response.status_code == 403:
                    print(f"  ❌ {description:20} -> PERMISSION DENIED")
                elif response.status_code == 302:
                    # Check if redirect is to login (permission issue) or somewhere else
                    if response.url.startswith('/relationship/login'):
                        print(f"  🔐 {description:20} -> REDIRECTED TO LOGIN")
                    else:
                        print(f"  🔄 {description:20} -> REDIRECTED")
                else:
                    print(f"  ⚠️  {description:20} -> Status: {response.status_code}")
                    
            except Exception as e:
                print(f"  ❌ {description:20} -> ERROR: {e}")
    
    client.logout()

print("\n🎉 CUSTOM PERMISSIONS TEST COMPLETE!")
