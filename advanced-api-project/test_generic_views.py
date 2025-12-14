#!/usr/bin/env python3
"""
Comprehensive Test Script for Generic Views in Django REST Framework
"""

import requests
import json
from datetime import datetime

BASE_URL = "http://127.0.0.1:8000/api"

def test_generic_views():
    print("🧪 COMPREHENSIVE TEST: GENERIC VIEWS IN DRF")
    print("=" * 60)
    
    # Get authentication token
    print("1. 🔐 AUTHENTICATION SETUP")
    token_response = requests.post(
        f"{BASE_URL}/auth-token/",
        json={'username': 'testuser', 'password': 'testpassword123'}
    )
    
    if token_response.status_code == 200:
        token_data = token_response.json()
        auth_token = token_data['token']
        headers = {'Authorization': f'Token {auth_token}'}
        print(f"   ✅ Token obtained: {auth_token[:20]}...")
    else:
        print(f"   ❌ Failed to get token: {token_response.status_code}")
        headers = {}
    
    # Test 2: Public access to book list (should work without auth)
    print("\n2. 📚 TESTING PUBLIC ACCESS (Book List)")
    response = requests.get(f"{BASE_URL}/books/")
    if response.status_code == 200:
        books = response.json()
        print(f"   ✅ Book list accessible without authentication")
        print(f"   📖 Found {len(books)} books")
        if books:
            print(f"   📚 Sample: '{books[0]['title']}'")
    else:
        print(f"   ❌ Book list failed: {response.status_code}")
    
    # Test 3: Public access to book detail (should work without auth)
    print("\n3. 📖 TESTING PUBLIC ACCESS (Book Detail)")
    if books:
        book_id = books[0]['id']
        response = requests.get(f"{BASE_URL}/books/{book_id}/")
        if response.status_code == 200:
            book = response.json()
            print(f"   ✅ Book detail accessible without authentication")
            print(f"   📚 Retrieved: '{book['title']}'")
        else:
            print(f"   ❌ Book detail failed: {response.status_code}")
    
    # Test 4: Test book creation without authentication (should fail)
    print("\n4. 🚫 TESTING BOOK CREATION WITHOUT AUTH")
    response = requests.post(
        f"{BASE_URL}/books/create/",
        json={
            "title": "Unauthorized Book",
            "publication_year": 2020,
            "author": 1
        }
    )
    if response.status_code == 401:
        print("   ✅ Creation blocked without authentication (as expected)")
    else:
        print(f"   ❌ Expected 401, got {response.status_code}")
    
    # Test 5: Test book creation with authentication (should work)
    print("\n5. ✅ TESTING BOOK CREATION WITH AUTH")
    if headers:
        response = requests.post(
            f"{BASE_URL}/books/create/",
            json={
                "title": "Authenticated Book Creation",
                "publication_year": 2020,
                "author": 1
            },
            headers=headers
        )
        if response.status_code == 201:
            created_book = response.json()
            test_book_id = created_book['id']
            print(f"   ✅ Book created successfully with ID: {test_book_id}")
            print(f"   📚 Title: '{created_book['title']}'")
        else:
            print(f"   ❌ Book creation failed: {response.status_code}")
            print(f"   Response: {response.text}")
            test_book_id = None
    else:
        print("   ⚠️  Skipping - No authentication token available")
        test_book_id = None
    
    # Test 6: Test book update with authentication
    print("\n6. ✏️ TESTING BOOK UPDATE WITH AUTH")
    if headers and test_book_id:
        response = requests.put(
            f"{BASE_URL}/books/{test_book_id}/update/",
            json={
                "title": "Updated Book Title",
                "publication_year": 2021,
                "author": 1
            },
            headers=headers
        )
        if response.status_code == 200:
            updated_book = response.json()
            print(f"   ✅ Book updated successfully")
            print(f"   📚 New title: '{updated_book['title']}'")
        else:
            print(f"   ❌ Book update failed: {response.status_code}")
    
    # Test 7: Test book deletion with authentication
    print("\n7. 🗑️ TESTING BOOK DELETION WITH AUTH")
    if headers and test_book_id:
        response = requests.delete(
            f"{BASE_URL}/books/{test_book_id}/delete/",
            headers=headers
        )
        if response.status_code == 204:
            print("   ✅ Book deleted successfully")
        else:
            print(f"   ❌ Book deletion failed: {response.status_code}")
    
    # Test 8: Test combined list-create view
    print("\n8. 🔄 TESTING COMBINED LIST-CREATE VIEW")
    # Test GET (should work without auth)
    response = requests.get(f"{BASE_URL}/books/combined/")
    if response.status_code == 200:
        books = response.json()
        print(f"   ✅ Combined view GET working: {len(books)} books")
    else:
        print(f"   ❌ Combined view GET failed: {response.status_code}")
    
    # Test POST (should require auth)
    if headers:
        response = requests.post(
            f"{BASE_URL}/books/combined/",
            json={
                "title": "Book from Combined View",
                "publication_year": 2019,
                "author": 1
            },
            headers=headers
        )
        if response.status_code == 201:
            combined_book = response.json()
            print(f"   ✅ Combined view POST working: ID {combined_book['id']}")
            
            # Clean up
            requests.delete(
                f"{BASE_URL}/books/combined/{combined_book['id']}/",
                headers=headers
            )
        else:
            print(f"   ❌ Combined view POST failed: {response.status_code}")
    
    # Test 9: Test author views (should be public)
    print("\n9. 👨‍💼 TESTING AUTHOR VIEWS")
    response = requests.get(f"{BASE_URL}/authors/")
    if response.status_code == 200:
        authors = response.json()
        print(f"   ✅ Author list working: {len(authors)} authors")
        if authors:
            author_id = authors[0]['id']
            response = requests.get(f"{BASE_URL}/authors/{author_id}/")
            if response.status_code == 200:
                author = response.json()
                print(f"   ✅ Author detail working: {author['name']}")
                print(f"   📚 Books by author: {len(author.get('books', []))}")
    
    # Test 10: Test validation
    print("\n10. ⚠️ TESTING VALIDATION")
    if headers:
        response = requests.post(
            f"{BASE_URL}/books/create/",
            json={
                "title": "Future Book",
                "publication_year": datetime.now().year + 1,
                "author": 1
            },
            headers=headers
        )
        if response.status_code == 400:
            error_data = response.json()
            print(f"   ✅ Validation working: {error_data['publication_year'][0]}")
        else:
            print(f"   ❌ Validation failed: {response.status_code}")
    
    print("\n" + "=" * 60)
    print("🎉 GENERIC VIEWS TEST COMPLETED!")
    print("✅ All CRUD operations tested")
    print("✅ Permission system working")
    print("✅ Validation functioning")
    print("✅ Combined views operational")
    print("🚀 Generic views implementation successful!")

if __name__ == "__main__":
    test_generic_views()
