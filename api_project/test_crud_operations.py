#!/usr/bin/env python3
import requests
import json

BASE_URL = "http://127.0.0.1:8000/api/books_all"

def test_crud_operations():
    print("🧪 COMPREHENSIVE CRUD OPERATIONS TEST")
    print("=" * 50)
    
    # Test 1: List all books
    print("1. LIST all books (GET /books_all/):")
    response = requests.get(BASE_URL + "/")
    if response.status_code == 200:
        books = response.json()
        print(f"   ✅ SUCCESS - {len(books)} books retrieved")
        for book in books[:3]:  # Show first 3 books
            print(f"      ID: {book['id']}, Title: {book['title']}")
    else:
        print(f"   ❌ FAILED - Status: {response.status_code}")
    
    # Test 2: Create a new book
    print("\n2. CREATE new book (POST /books_all/):")
    new_book = {
        "title": "Brave New World",
        "author": "Aldous Huxley"
    }
    response = requests.post(BASE_URL + "/", json=new_book)
    if response.status_code == 201:
        created_book = response.json()
        print(f"   ✅ SUCCESS - Book created with ID: {created_book['id']}")
        test_book_id = created_book['id']
    else:
        print(f"   ❌ FAILED - Status: {response.status_code}")
        print(f"   Response: {response.text}")
        return
    
    # Test 3: Retrieve the created book
    print(f"\n3. RETRIEVE book (GET /books_all/{test_book_id}/):")
    response = requests.get(f"{BASE_URL}/{test_book_id}/")
    if response.status_code == 200:
        book = response.json()
        print(f"   ✅ SUCCESS - Retrieved: {book['title']} by {book['author']}")
    else:
        print(f"   ❌ FAILED - Status: {response.status_code}")
    
    # Test 4: Update the book
    print(f"\n4. UPDATE book (PUT /books_all/{test_book_id}/):")
    updated_data = {
        "title": "Brave New World - Revised Edition",
        "author": "Aldous Huxley"
    }
    response = requests.put(f"{BASE_URL}/{test_book_id}/", json=updated_data)
    if response.status_code == 200:
        updated_book = response.json()
        print(f"   ✅ SUCCESS - Updated to: {updated_book['title']}")
    else:
        print(f"   ❌ FAILED - Status: {response.status_code}")
    
    # Test 5: Delete the book
    print(f"\n5. DELETE book (DELETE /books_all/{test_book_id}/):")
    response = requests.delete(f"{BASE_URL}/{test_book_id}/")
    if response.status_code == 204:
        print("   ✅ SUCCESS - Book deleted")
    else:
        print(f"   ❌ FAILED - Status: {response.status_code}")
    
    # Verify deletion
    print(f"\n6. VERIFY deletion (GET /books_all/{test_book_id}/):")
    response = requests.get(f"{BASE_URL}/{test_book_id}/")
    if response.status_code == 404:
        print("   ✅ SUCCESS - Book not found (as expected)")
    else:
        print(f"   ❌ FAILED - Book still exists? Status: {response.status_code}")
    
    print("\n" + "=" * 50)
    print("🎉 CRUD OPERATIONS TEST COMPLETED!")

if __name__ == "__main__":
    test_crud_operations()
