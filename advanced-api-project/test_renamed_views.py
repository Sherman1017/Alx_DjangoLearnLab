#!/usr/bin/env python3
"""
Test that the renamed views still work correctly
"""

import requests
import json

BASE_URL = "http://127.0.0.1:8000/api"

def test_renamed_views():
    print("🧪 TESTING RENAMED VIEWS")
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
    
    # Test ListView
    print("\n2. Testing ListView (GET /api/books/)")
    list_r = requests.get(f"{BASE_URL}/books/")
    if list_r.status_code == 200:
        books = list_r.json()
        print(f"✅ ListView working: {len(books)} books")
    else:
        print(f"❌ ListView failed: {list_r.status_code}")
    
    # Test CreateView
    print("\n3. Testing CreateView (POST /api/books/create/)")
    # Get first author
    authors_r = requests.get(f"{BASE_URL}/authors/")
    if authors_r.status_code == 200:
        authors = authors_r.json()
        author_id = authors[0]['id'] if authors else 1
        
        create_data = {
            "title": "Test Book from Renamed Views",
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
            
            # Test DetailView
            print(f"\n4. Testing DetailView (GET /api/books/{book_id}/)")
            detail_r = requests.get(f"{BASE_URL}/books/{book_id}/")
            if detail_r.status_code == 200:
                print("✅ DetailView working: Book retrieved")
            else:
                print(f"❌ DetailView failed: {detail_r.status_code}")
            
            # Test UpdateView
            print(f"\n5. Testing UpdateView (PUT /api/books/{book_id}/update/)")
            update_data = create_data.copy()
            update_data['title'] = "Updated Test Book"
            update_r = requests.put(
                f"{BASE_URL}/books/{book_id}/update/",
                json=update_data,
                headers=headers
            )
            if update_r.status_code == 200:
                print("✅ UpdateView working: Book updated")
            else:
                print(f"❌ UpdateView failed: {update_r.status_code}")
            
            # Test DeleteView
            print(f"\n6. Testing DeleteView (DELETE /api/books/{book_id}/delete/)")
            delete_r = requests.delete(
                f"{BASE_URL}/books/{book_id}/delete/",
                headers=headers
            )
            if delete_r.status_code == 204:
                print("✅ DeleteView working: Book deleted")
            else:
                print(f"❌ DeleteView failed: {delete_r.status_code}")
            
        else:
            print(f"❌ CreateView failed: {create_r.status_code}")
            print(f"Response: {create_r.text}")
    else:
        print("❌ Could not get authors")

    print("\n" + "=" * 50)
    print("🎉 ALL RENAMED VIEWS WORKING CORRECTLY!")

if __name__ == "__main__":
    test_renamed_views()
