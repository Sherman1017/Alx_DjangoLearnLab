#!/usr/bin/env python3
import requests
import json

BASE_URL = "http://127.0.0.1:8000/api"

def test_authentication_fixed():
    print("🔐 FIXED AUTHENTICATION TEST")
    print("=" * 50)
    
    # Test 1: Public endpoint
    print("1. Testing PUBLIC endpoint:")
    try:
        response = requests.get(f"{BASE_URL}/books/public/")
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ SUCCESS - Public endpoint accessible")
            print(f"   📚 {len(data['books'])} books in public list")
        else:
            print(f"   ❌ FAILED - Status: {response.status_code}")
    except Exception as e:
        print(f"   ❌ ERROR: {e}")
    
    # Test 2: Get authentication token
    print("\n2. Getting AUTHENTICATION TOKEN:")
    try:
        token_response = requests.post(
            f"{BASE_URL}/auth-token/",
            json={'username': 'admin', 'password': 'adminpassword'}
        )
        
        if token_response.status_code == 200:
            token_data = token_response.json()
            auth_token = token_data['token']
            print(f"   ✅ SUCCESS - Token obtained: {auth_token[:20]}...")
            
            # Test 3: Use token to access protected endpoint
            print("\n3. Testing PROTECTED endpoint WITH token:")
            headers = {'Authorization': f'Token {auth_token}'}
            response = requests.get(f"{BASE_URL}/books/", headers=headers)
            
            if response.status_code == 200:
                books = response.json()
                print(f"   ✅ SUCCESS - Protected endpoint accessible")
                print(f"   📚 {len(books)} books retrieved")
            else:
                print(f"   ❌ FAILED - Status: {response.status_code}")
                
            # Test 4: Create book with token
            print("\n4. Testing BOOK CREATION with token:")
            new_book = {
                "title": "Secure Book Creation",
                "author": "Authenticated User"
            }
            response = requests.post(
                f"{BASE_URL}/books_all/",
                json=new_book,
                headers=headers
            )
            
            if response.status_code == 201:
                created_book = response.json()
                print(f"   ✅ SUCCESS - Book created with ID: {created_book['id']}")
                
                # Clean up
                delete_response = requests.delete(
                    f"{BASE_URL}/books_all/{created_book['id']}/",
                    headers=headers
                )
                if delete_response.status_code == 204:
                    print("   ✅ Test book cleaned up")
                else:
                    print("   ⚠️ Could not clean up test book")
                    
            else:
                print(f"   ❌ FAILED - Status: {response.status_code}")
                print(f"   Response: {response.text}")
                
        else:
            print(f"   ❌ FAILED to get token: {token_response.status_code}")
            print(f"   Response: {token_response.text}")
            
    except Exception as e:
        print(f"   ❌ ERROR: {e}")
    
    # Test 5: Test without token (should work for public endpoints)
    print("\n5. Testing books_all LIST without token:")
    try:
        response = requests.get(f"{BASE_URL}/books_all/")
        if response.status_code == 200:
            books = response.json()
            print(f"   ✅ SUCCESS - Public read allowed: {len(books)} books")
        else:
            print(f"   ❌ FAILED - Status: {response.status_code}")
    except Exception as e:
        print(f"   ❌ ERROR: {e}")
    
    print("\n" + "=" * 50)
    print("🎉 AUTHENTICATION TEST COMPLETED!")

if __name__ == "__main__":
    test_authentication_fixed()
