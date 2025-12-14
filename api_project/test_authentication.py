#!/usr/bin/env python3
import requests
import json

BASE_URL = "http://127.0.0.1:8000/api"

def test_authentication():
    print("🔐 AUTHENTICATION AND PERMISSIONS TEST")
    print("=" * 50)
    
    # Test 1: Public endpoint (no auth required)
    print("1. Testing PUBLIC endpoint (no authentication required):")
    response = requests.get(f"{BASE_URL}/books/public/")
    if response.status_code == 200:
        data = response.json()
        print(f"   ✅ SUCCESS - Public endpoint accessible")
        print(f"   📚 Retrieved {len(data['books'])} books")
    else:
        print(f"   ❌ FAILED - Status: {response.status_code}")
    
    # Test 2: Protected endpoint without token (should fail)
    print("\n2. Testing PROTECTED endpoint WITHOUT token:")
    response = requests.get(f"{BASE_URL}/books/")
    if response.status_code == 200:
        print("   ⚠️  WARNING - Protected endpoint accessible without auth (check permissions)")
    else:
        print(f"   ✅ SUCCESS - Access denied without authentication: {response.status_code}")
    
    # Test 3: Get authentication token
    print("\n3. Getting AUTHENTICATION TOKEN:")
    token_response = requests.post(
        f"{BASE_URL}/auth-token/",
        data={'username': 'testuser', 'password': 'testpassword123'}
    )
    
    if token_response.status_code == 200:
        token_data = token_response.json()
        auth_token = token_data['token']
        print(f"   ✅ SUCCESS - Token obtained: {auth_token[:20]}...")
    else:
        print(f"   ❌ FAILED to get token: {token_response.status_code}")
        print(f"   Response: {token_response.text}")
        # Try with admin user as fallback
        print("   Trying with admin user...")
        token_response = requests.post(
            f"{BASE_URL}/auth-token/",
            data={'username': 'admin', 'password': 'adminpassword'}
        )
        if token_response.status_code == 200:
            token_data = token_response.json()
            auth_token = token_data['token']
            print(f"   ✅ SUCCESS - Admin token obtained: {auth_token[:20]}...")
        else:
            print(f"   ❌ FAILED to get admin token: {token_response.status_code}")
            return
    
    # Test 4: Protected endpoint WITH token
    print("\n4. Testing PROTECTED endpoint WITH token:")
    headers = {'Authorization': f'Token {auth_token}'}
    response = requests.get(f"{BASE_URL}/books/", headers=headers)
    if response.status_code == 200:
        books = response.json()
        print(f"   ✅ SUCCESS - Protected endpoint accessible with token")
        print(f"   📚 Retrieved {len(books)} books")
    else:
        print(f"   ❌ FAILED - Status: {response.status_code}")
    
    # Test 5: Create book with token (should work)
    print("\n5. Testing BOOK CREATION with token:")
    new_book = {
        "title": "Authenticated Book Creation",
        "author": "Token User"
    }
    response = requests.post(
        f"{BASE_URL}/books_all/",
        json=new_book,
        headers=headers
    )
    if response.status_code == 201:
        created_book = response.json()
        print(f"   ✅ SUCCESS - Book created with ID: {created_book['id']}")
        test_book_id = created_book['id']
    else:
        print(f"   ❌ FAILED - Status: {response.status_code}")
        print(f"   Response: {response.text}")
        return
    
    # Test 6: Create book WITHOUT token (should fail)
    print("\n6. Testing BOOK CREATION WITHOUT token (should fail):")
    response = requests.post(
        f"{BASE_URL}/books_all/",
        json={"title": "Unauthorized Book", "author": "Anonymous"}
    )
    if response.status_code == 401:
        print("   ✅ SUCCESS - Creation blocked without authentication")
    else:
        print(f"   ❌ FAILED - Expected 401, got: {response.status_code}")
    
    # Test 7: Test books_all list without token (should work - we set AllowAny for list)
    print("\n7. Testing books_all LIST without token (public read):")
    response = requests.get(f"{BASE_URL}/books_all/")
    if response.status_code == 200:
        books = response.json()
        print(f"   ✅ SUCCESS - Public read allowed: {len(books)} books")
    else:
        print(f"   ❌ FAILED - Status: {response.status_code}")
    
    # Clean up: Delete the test book
    print(f"\n8. Cleaning up - Deleting test book (ID: {test_book_id}):")
    response = requests.delete(
        f"{BASE_URL}/books_all/{test_book_id}/",
        headers=headers
    )
    if response.status_code == 204:
        print("   ✅ SUCCESS - Test book deleted")
    else:
        print(f"   ⚠️  Could not delete test book: {response.status_code}")
    
    print("\n" + "=" * 50)
    print("🎉 AUTHENTICATION TEST COMPLETED!")

if __name__ == "__main__":
    test_authentication()
