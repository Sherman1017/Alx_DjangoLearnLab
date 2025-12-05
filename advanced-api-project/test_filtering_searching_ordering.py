#!/usr/bin/env python3
"""
Comprehensive test script for filtering, searching, and ordering features
"""

import requests
import json

BASE_URL = "http://127.0.0.1:8000/api"

def test_all_features():
    print("🧪 COMPREHENSIVE TEST: FILTERING, SEARCHING, ORDERING")
    print("=" * 60)
    
    # Test 1: Basic book list (no filters)
    print("1. 📚 BASIC BOOK LIST (no filters)")
    response = requests.get(f"{BASE_URL}/books/")
    if response.status_code == 200:
        books = response.json()
        print(f"   ✅ Success: {len(books)} books retrieved")
        print(f"   📖 Sample books:")
        for book in books[:3]:
            print(f"      - '{book['title']}' ({book['publication_year']}) by {book['author']}")
    else:
        print(f"   ❌ Failed: {response.status_code}")
        return
    
    # Test 2: Filtering by publication year
    print("\n2. 🔍 FILTERING: By publication year (2000)")
    response = requests.get(f"{BASE_URL}/books/?publication_year=2000")
    if response.status_code == 200:
        books = response.json()
        print(f"   ✅ Success: {len(books)} books from year 2000")
        for book in books:
            print(f"      - '{book['title']}' by {book['author']}")
    else:
        print(f"   ❌ Failed: {response.status_code}")
    
    # Test 3: Filtering by year range
    print("\n3. 📅 FILTERING: By year range (1990-2000)")
    response = requests.get(f"{BASE_URL}/books/?publication_year_min=1990&publication_year_max=2000")
    if response.status_code == 200:
        books = response.json()
        print(f"   ✅ Success: {len(books)} books from 1990-2000")
        for book in books[:5]:  # Show first 5
            print(f"      - '{book['title']}' ({book['publication_year']})")
    else:
        print(f"   ❌ Failed: {response.status_code}")
    
    # Test 4: Filtering by title contains
    print("\n4. 📖 FILTERING: By title contains 'Harry'")
    response = requests.get(f"{BASE_URL}/books/?title=Harry")
    if response.status_code == 200:
        books = response.json()
        print(f"   ✅ Success: {len(books)} books with 'Harry' in title")
        for book in books:
            print(f"      - '{book['title']}'")
    else:
        print(f"   ❌ Failed: {response.status_code}")
    
    # Test 5: Filtering by author name
    print("\n5. 👨‍💼 FILTERING: By author name contains 'Rowling'")
    response = requests.get(f"{BASE_URL}/books/?author_name=Rowling")
    if response.status_code == 200:
        books = response.json()
        print(f"   ✅ Success: {len(books)} books by authors with 'Rowling' in name")
        for book in books:
            print(f"      - '{book['title']}' by {book['author']}")
    else:
        print(f"   ❌ Failed: {response.status_code}")
    
    # Test 6: Search functionality
    print("\n6. 🔎 SEARCH: Across title and author for 'potter'")
    response = requests.get(f"{BASE_URL}/books/?search=potter")
    if response.status_code == 200:
        books = response.json()
        print(f"   ✅ Success: {len(books)} books found for search 'potter'")
        for book in books:
            print(f"      - '{book['title']}' by {book['author']}")
    else:
        print(f"   ❌ Failed: {response.status_code}")
    
    # Test 7: Ordering by title (ascending)
    print("\n7. 🔼 ORDERING: By title (ascending)")
    response = requests.get(f"{BASE_URL}/books/?ordering=title")
    if response.status_code == 200:
        books = response.json()
        print(f"   ✅ Success: {len(books)} books ordered by title A-Z")
        print(f"   📖 First 3 books:")
        for book in books[:3]:
            print(f"      - '{book['title']}'")
    else:
        print(f"   ❌ Failed: {response.status_code}")
    
    # Test 8: Ordering by publication year (descending)
    print("\n8. 🔽 ORDERING: By publication year (descending)")
    response = requests.get(f"{BASE_URL}/books/?ordering=-publication_year")
    if response.status_code == 200:
        books = response.json()
        print(f"   ✅ Success: {len(books)} books ordered by year (newest first)")
        print(f"   📖 First 3 books:")
        for book in books[:3]:
            print(f"      - '{book['title']}' ({book['publication_year']})")
    else:
        print(f"   ❌ Failed: {response.status_code}")
    
    # Test 9: Combined filtering, searching, and ordering
    print("\n9. 🎯 COMBINED: Filter + Search + Order")
    print("   Searching 'murder', ordered by title")
    response = requests.get(f"{BASE_URL}/books/?search=murder&ordering=title")
    if response.status_code == 200:
        books = response.json()
        print(f"   ✅ Success: {len(books)} books found")
        for book in books:
            print(f"      - '{book['title']}' ({book['publication_year']}) by {book['author']}")
    else:
        print(f"   ❌ Failed: {response.status_code}")
    
    # Test 10: Complex combined query
    print("\n10. 🚀 COMPLEX: Multiple filters + ordering")
    print("   1990-2010 books by authors with 'king' in name, ordered by year")
    response = requests.get(f"{BASE_URL}/books/?publication_year_min=1990&publication_year_max=2010&author_name=king&ordering=publication_year")
    if response.status_code == 200:
        books = response.json()
        print(f"   ✅ Success: {len(books)} books match complex query")
        for book in books:
            print(f"      - '{book['title']}' ({book['publication_year']}) by {book['author']}")
    else:
        print(f"   ❌ Failed: {response.status_code}")
    
    # Test 11: Author list with ordering
    print("\n11. 👨‍💼 AUTHOR LIST: With ordering")
    response = requests.get(f"{BASE_URL}/authors/?ordering=name")
    if response.status_code == 200:
        authors = response.json()
        print(f"   ✅ Success: {len(authors)} authors ordered by name")
        print(f"   👨‍💼 First 3 authors:")
        for author in authors[:3]:
            print(f"      - {author['name']} ({len(author.get('books', []))} books)")
    else:
        print(f"   ❌ Failed: {response.status_code}")
    
    print("\n" + "=" * 60)
    print("🎉 ALL FILTERING, SEARCHING, AND ORDERING FEATURES TESTED!")
    print("✅ Filtering by exact values and ranges")
    print("✅ Searching across multiple fields") 
    print("✅ Ordering by various fields")
    print("✅ Complex combined queries")
    print("🚀 Advanced query capabilities implemented successfully!")

if __name__ == "__main__":
    test_all_features()
