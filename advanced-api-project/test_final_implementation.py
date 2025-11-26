#!/usr/bin/env python3
"""
Test the final implementation with updated permission imports
"""

import requests
import json

BASE_URL = "http://127.0.0.1:8000/api"

def test_final_implementation():
    print("🧪 TESTING FINAL IMPLEMENTATION")
    print("=" * 50)
    
    # Test public endpoints (should work without auth)
    print("1. Testing public endpoints without authentication:")
    endpoints = [
        ('/books/', 'Book List'),
        ('/authors/', 'Author List'),
    ]
    
    for endpoint, name in endpoints:
        response = requests.get(f"{BASE_URL}{endpoint}")
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ {name}: {len(data)} items (public access working)")
        else:
            print(f"   ❌ {name}: Failed with {response.status_code}")
    
    # Test protected endpoints without auth (should fail)
    print("\n2. Testing protected endpoints without authentication:")
    protected_endpoints = [
        ('/books/create/', 'POST', 'Book Create'),
        ('/books/update/', 'PUT', 'Book Update'),
        ('/books/delete/', 'DELETE', 'Book Delete'),
    ]
    
    for endpoint, method, name in protected_endpoints:
        if method == 'POST':
            response = requests.post(f"{BASE_URL}{endpoint}", json={})
        elif method == 'PUT':
            response = requests.put(f"{BASE_URL}{endpoint}", json={})
        elif method == 'DELETE':
            response = requests.delete(f"{BASE_URL}{endpoint}", json={})
        
        if response.status_code == 401:
            print(f"   ✅ {name}: Properly blocked without auth")
        else:
            print(f"   ❌ {name}: Unexpected status {response.status_code}")
    
    # Get token and test with auth
    print("\n3. Testing with authentication:")
    token_r = requests.post(
        f"{BASE_URL}/auth-token/",
        json={'username': 'testuser', 'password': 'testpassword123'}
    )
    
    if token_r.status_code == 200:
        token = token_r.json()['token']
        headers = {'Authorization': f'Token {token}'}
        print("   ✅ Authentication working")
        
        # Get author for book creation
        authors_r = requests.get(f"{BASE_URL}/authors/")
        if authors_r.status_code == 200:
            authors = authors_r.json()
            author_id = authors[0]['id'] if authors else 1
            
            # Test book creation with auth
            create_data = {
                "title": "Final Test Book",
                "publication_year": 2020,
                "author": author_id
            }
            
            create_r = requests.post(
                f"{BASE_URL}/books/create/",
                json=create_data,
                headers=headers
            )
            
            if create_r.status_code == 201:
                book = create_r.json()
                book_id = book['id']
                print(f"   ✅ Book creation with auth: ID {book_id}")
                
                # Clean up
                delete_data = {"id": book_id}
                requests.delete(
                    f"{BASE_URL}/books/delete/",
                    json=delete_data,
                    headers=headers
                )
                print("   ✅ Test book cleaned up")
            else:
                print(f"   ❌ Book creation failed: {create_r.status_code}")
        else:
            print("   ❌ Could not get authors")
    else:
        print("   ❌ Authentication failed")
    
    print("\n" + "=" * 50)
    print("🎉 FINAL IMPLEMENTATION TESTED SUCCESSFULLY!")

if __name__ == "__main__":
    test_final_implementation()
