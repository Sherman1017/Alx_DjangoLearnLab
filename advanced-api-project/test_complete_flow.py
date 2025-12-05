#!/usr/bin/env python3
"""
Complete test flow with proper data setup
"""

import requests
import json

BASE_URL = "http://127.0.0.1:8000/api"

def test_complete_flow():
    print("🧪 COMPLETE FLOW TEST WITH PROPER DATA")
    print("=" * 50)
    
    # Step 1: Get authentication token
    print("1. 🔐 GETTING AUTHENTICATION TOKEN")
    token_response = requests.post(
        f"{BASE_URL}/auth-token/",
        json={'username': 'testuser', 'password': 'testpassword123'}
    )
    
    if token_response.status_code != 200:
        print(f"❌ Failed to get token: {token_response.status_code}")
        print(f"Response: {token_response.text}")
        return
    
    token_data = token_response.json()
    auth_token = token_data['token']
    headers = {'Authorization': f'Token {auth_token}'}
    print(f"✅ Token obtained: {auth_token[:20]}...")
    
    # Step 2: Get available authors (public endpoint)
    print("\n2. 📚 CHECKING AVAILABLE AUTHORS")
    authors_response = requests.get(f"{BASE_URL}/authors/")
    if authors_response.status_code == 200:
        authors = authors_response.json()
        print(f"✅ Found {len(authors)} authors")
        for author in authors:
            print(f"   👨‍💼 {author['id']}: {author['name']}")
        
        if not authors:
            print("❌ No authors found - this will cause book creation to fail")
            return
        
        author_id = authors[0]['id']
    else:
        print(f"❌ Failed to get authors: {authors_response.status_code}")
        return
    
    # Step 3: Test book creation with valid data
    print(f"\n3. ✅ TESTING BOOK CREATION (using author ID: {author_id})")
    book_data = {
        "title": "The Great Gatsby",
        "publication_year": 1925,
        "author": author_id
    }
    
    create_response = requests.post(
        f"{BASE_URL}/books/create/",
        json=book_data,
        headers=headers
    )
    
    print(f"Status Code: {create_response.status_code}")
    
    if create_response.status_code == 201:
        created_book = create_response.json()
        test_book_id = created_book['id']
        print("✅ BOOK CREATION SUCCESSFUL!")
        print(f"   Book ID: {test_book_id}")
        print(f"   Title: {created_book['title']}")
        print(f"   Publication Year: {created_book['publication_year']}")
        print(f"   Author ID: {created_book['author']}")
    else:
        print("❌ BOOK CREATION FAILED")
        try:
            error_data = create_response.json()
            print(f"   Errors: {error_data}")
        except:
            print(f"   Response: {create_response.text}")
        return
    
    # Step 4: Test retrieving the created book
    print(f"\n4. 📖 TESTING BOOK RETRIEVAL")
    retrieve_response = requests.get(f"{BASE_URL}/books/{test_book_id}/")
    if retrieve_response.status_code == 200:
        retrieved_book = retrieve_response.json()
        print("✅ BOOK RETRIEVAL SUCCESSFUL")
        print(f"   Title: {retrieved_book['title']}")
    else:
        print(f"❌ Book retrieval failed: {retrieve_response.status_code}")
    
    # Step 5: Test book update
    print(f"\n5. ✏️ TESTING BOOK UPDATE")
    update_data = {
        "title": "The Great Gatsby - Revised Edition",
        "publication_year": 1925,
        "author": author_id
    }
    
    update_response = requests.put(
        f"{BASE_URL}/books/{test_book_id}/update/",
        json=update_data,
        headers=headers
    )
    
    if update_response.status_code == 200:
        updated_book = update_response.json()
        print("✅ BOOK UPDATE SUCCESSFUL")
        print(f"   New Title: {updated_book['title']}")
    else:
        print(f"❌ Book update failed: {update_response.status_code}")
    
    # Step 6: Test book deletion
    print(f"\n6. 🗑️ TESTING BOOK DELETION")
    delete_response = requests.delete(
        f"{BASE_URL}/books/{test_book_id}/delete/",
        headers=headers
    )
    
    if delete_response.status_code == 204:
        print("✅ BOOK DELETION SUCCESSFUL")
    else:
        print(f"❌ Book deletion failed: {delete_response.status_code}")
    
    # Step 7: Verify book is gone
    print(f"\n7. 🔍 VERIFYING BOOK DELETION")
    verify_response = requests.get(f"{BASE_URL}/books/{test_book_id}/")
    if verify_response.status_code == 404:
        print("✅ BOOK DELETION VERIFIED (404 Not Found)")
    else:
        print(f"⚠️ Book might still exist: {verify_response.status_code}")
    
    print("\n" + "=" * 50)
    print("🎉 COMPLETE FLOW TEST FINISHED!")

if __name__ == "__main__":
    test_complete_flow()
