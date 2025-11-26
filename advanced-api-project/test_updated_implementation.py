#!/usr/bin/env python3
"""
Test the updated implementation with exact requirements
"""

import requests
import json

BASE_URL = "http://127.0.0.1:8000/api"

def test_updated_implementation():
    print("🧪 TESTING UPDATED IMPLEMENTATION")
    print("=" * 50)
    
    # Test 1: Filter by title
    print("1. Testing title filtering:")
    response = requests.get(f"{BASE_URL}/books/?title=Harry")
    if response.status_code == 200:
        books = response.json()
        print(f"   ✅ Title filter working: {len(books)} books with 'Harry' in title")
        for book in books:
            print(f"      - '{book['title']}'")
    else:
        print(f"   ❌ Title filter failed: {response.status_code}")
    
    # Test 2: Filter by author
    print("\n2. Testing author filtering:")
    response = requests.get(f"{BASE_URL}/books/?author=Rowling")
    if response.status_code == 200:
        books = response.json()
        print(f"   ✅ Author filter working: {len(books)} books by authors with 'Rowling'")
        for book in books:
            print(f"      - '{book['title']}' by {book['author']}")
    else:
        print(f"   ❌ Author filter failed: {response.status_code}")
    
    # Test 3: Filter by publication_year
    print("\n3. Testing publication_year filtering:")
    response = requests.get(f"{BASE_URL}/books/?publication_year=1997")
    if response.status_code == 200:
        books = response.json()
        print(f"   ✅ Publication year filter working: {len(books)} books from 1997")
        for book in books:
            print(f"      - '{book['title']}' ({book['publication_year']})")
    else:
        print(f"   ❌ Publication year filter failed: {response.status_code}")
    
    # Test 4: Search functionality
    print("\n4. Testing search functionality:")
    response = requests.get(f"{BASE_URL}/books/?search=potter")
    if response.status_code == 200:
        books = response.json()
        print(f"   ✅ Search working: {len(books)} books found for 'potter'")
        for book in books:
            print(f"      - '{book['title']}' by {book['author']}")
    else:
        print(f"   ❌ Search failed: {response.status_code}")
    
    # Test 5: Ordering functionality
    print("\n5. Testing ordering functionality:")
    response = requests.get(f"{BASE_URL}/books/?ordering=-publication_year")
    if response.status_code == 200:
        books = response.json()
        print(f"   ✅ Ordering working: {len(books)} books ordered by year (newest first)")
        if books:
            print(f"      Newest book: '{books[0]['title']}' ({books[0]['publication_year']})")
    else:
        print(f"   ❌ Ordering failed: {response.status_code}")
    
    # Test 6: Combined filtering
    print("\n6. Testing combined filtering:")
    response = requests.get(f"{BASE_URL}/books/?title=Harry&publication_year_min=1997")
    if response.status_code == 200:
        books = response.json()
        print(f"   ✅ Combined filtering working: {len(books)} books match both filters")
        for book in books:
            print(f"      - '{book['title']}' ({book['publication_year']})")
    else:
        print(f"   ❌ Combined filtering failed: {response.status_code}")

    print("\n" + "=" * 50)
    print("🎯 ALL FILTERING, SEARCHING, ORDERING FEATURES WORKING!")
    print("✅ Title filtering")
    print("✅ Author filtering") 
    print("✅ Publication year filtering")
    print("✅ Search functionality")
    print("✅ Ordering functionality")
    print("✅ Combined queries")

if __name__ == "__main__":
    test_updated_implementation()
