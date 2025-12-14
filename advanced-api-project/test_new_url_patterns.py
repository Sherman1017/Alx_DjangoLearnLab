#!/usr/bin/env python3
"""
Test script for the new URL patterns
"""

import requests
import json

BASE_URL = "http://127.0.0.1:8000/api"

def test_new_url_patterns():
    print("🧪 TESTING NEW URL PATTERNS")
    print("=" * 50)
    
    # Get authentication token
    print("1. Getting authentication token...")
    token_r = requests.post(
        f"{BASE_URL}/auth-token/",
        json={'username': 'testuser', 'password': 'testpassword123'}
    )
    
    if token_r.status_code != 200:
        print("❌ Token failed")
        return
    
    token = token_r.json()['token']
    headers = {'Authorization': f'Token {token}'}
    print("✅ Token obtained")
    
    # Get first author
    authors_r = requests.get(f"{BASE_URL}/authors/")
    if authors_r.status_code != 200:
        print("❌ Could not get authors")
        return
    
    authors = authors_r.json()
    author_id = authors[0]['id'] if authors else 1
    
    # Test CreateView
    print("\n2. Testing CreateView (POST /api/books/create/)")
    create_data = {
        "title": "Test Book for New URL Patterns",
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
        print(f"✅ CreateView working: Book ID {book_id} created")
        
        # Test UpdateView with new pattern (books/update/)
        print("\n3. Testing UpdateView (PUT /api/books/update/)")
        update_data = {
            "id": book_id,  # Book ID in request data
            "title": "Updated Test Book Title",
            "publication_year": 2021,
            "author": author_id
        }
        
        update_r = requests.put(
            f"{BASE_URL}/books/update/",
            json=update_data,
            headers=headers
        )
        
        if update_r.status_code == 200:
            updated_book = update_r.json()
            print("✅ UpdateView working: Book updated")
            print(f"   New title: {updated_book['title']}")
        else:
            print(f"❌ UpdateView failed: {update_r.status_code}")
            print(f"   Response: {update_r.text}")
        
        # Test DeleteView with new pattern (books/delete/)
        print("\n4. Testing DeleteView (DELETE /api/books/delete/)")
        delete_data = {
            "id": book_id  # Book ID in request data
        }
        
        delete_r = requests.delete(
            f"{BASE_URL}/books/delete/",
            json=delete_data,
            headers=headers
        )
        
        if delete_r.status_code == 204:
            print("✅ DeleteView working: Book deleted")
        else:
            print(f"❌ DeleteView failed: {delete_r.status_code}")
            print(f"   Response: {delete_r.text}")
            
    else:
        print(f"❌ CreateView failed: {create_r.status_code}")
        print(f"Response: {create_r.text}")

    print("\n" + "=" * 50)
    print("🎉 NEW URL PATTERNS TESTED!")

if __name__ == "__main__":
    test_new_url_patterns()
