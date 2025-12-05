#!/usr/bin/env python3
"""
Final working test with comprehensive error handling
"""

import requests
import json

def test_final():
    BASE_URL = "http://127.0.0.1:8000/api"
    
    print("🎯 FINAL COMPREHENSIVE TEST")
    print("=" * 50)
    
    # 1. Ensure we have data
    print("1. 📊 CHECKING DATABASE STATE")
    authors_r = requests.get(f"{BASE_URL}/authors/")
    if authors_r.status_code == 200:
        authors = authors_r.json()
        print(f"   Authors: {len(authors)}")
        for a in authors:
            print(f"     {a['id']}: {a['name']}")
    else:
        print("   ❌ Cannot access authors")
        return
    
    if not authors:
        print("   ⚠️ No authors - this will cause issues")
        return
    
    # 2. Get token
    print("\n2. 🔐 AUTHENTICATION")
    token_r = requests.post(
        f"{BASE_URL}/auth-token/",
        json={'username': 'testuser', 'password': 'testpassword123'}
    )
    
    if token_r.status_code != 200:
        print(f"   ❌ Token failed: {token_r.status_code}")
        return
    
    token = token_r.json()['token']
    headers = {'Authorization': f'Token {token}'}
    print("   ✅ Token obtained")
    
    # 3. Test each endpoint
    author_id = authors[0]['id']
    test_data = {
        "title": "Working Test Book " + str(hash(token) % 1000),  # Unique title
        "publication_year": 2020,
        "author": author_id
    }
    
    print(f"\n3. 🧪 TESTING WITH DATA: {test_data}")
    
    # Create
    print("   a) Creating book...")
    create_r = requests.post(f"{BASE_URL}/books/create/", json=test_data, headers=headers)
    print(f"      Status: {create_r.status_code}")
    
    if create_r.status_code == 201:
        book = create_r.json()
        book_id = book['id']
        print(f"      ✅ Created: ID {book_id}")
        
        # Read
        print("   b) Reading book...")
        read_r = requests.get(f"{BASE_URL}/books/{book_id}/")
        print(f"      Status: {read_r.status_code}")
        
        # Update
        print("   c) Updating book...")
        update_data = test_data.copy()
        update_data['title'] = "Updated " + update_data['title']
        update_r = requests.put(f"{BASE_URL}/books/{book_id}/update/", json=update_data, headers=headers)
        print(f"      Status: {update_r.status_code}")
        
        # Delete
        print("   d) Deleting book...")
        delete_r = requests.delete(f"{BASE_URL}/books/{book_id}/delete/", headers=headers)
        print(f"      Status: {delete_r.status_code}")
        
        if all([create_r.status_code == 201, 
                read_r.status_code == 200, 
                update_r.status_code == 200,
                delete_r.status_code == 204]):
            print("\n🎉 ALL OPERATIONS SUCCESSFUL!")
        else:
            print("\n⚠️ Some operations had issues")
            
    elif create_r.status_code == 400:
        print("   ❌ Creation failed with 400")
        try:
            errors = create_r.json()
            print(f"      Errors: {errors}")
        except:
            print(f"      Response: {create_r.text}")
    else:
        print(f"   ❌ Unexpected status: {create_r.status_code}")

if __name__ == "__main__":
    test_final()
