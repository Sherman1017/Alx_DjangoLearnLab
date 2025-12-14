#!/usr/bin/env python3
"""
Test script for Advanced API Project with Custom Serializers
"""

import os
import sys
import django
from datetime import datetime

# Setup Django
sys.path.append('/Alx_DjangoLearnLab/advanced-api-project')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'advanced_api_project.settings')
django.setup()

from api.models import Author, Book
from api.serializers import AuthorSerializer, BookSerializer

def test_models_and_serializers():
    print("🧪 TESTING ADVANCED API PROJECT SETUP")
    print("=" * 60)
    
    # Test 1: Create test data
    print("1. Creating test authors and books...")
    
    # Create authors
    author1, created = Author.objects.get_or_create(name="J.K. Rowling")
    author2, created = Author.objects.get_or_create(name="George Orwell")
    
    print(f"   ✅ Authors created: {author1.name}, {author2.name}")
    
    # Create books
    book1, created = Book.objects.get_or_create(
        title="Harry Potter and the Philosopher's Stone",
        publication_year=1997,
        author=author1
    )
    
    book2, created = Book.objects.get_or_create(
        title="1984",
        publication_year=1949,
        author=author2
    )
    
    book3, created = Book.objects.get_or_create(
        title="Harry Potter and the Chamber of Secrets",
        publication_year=1998,
        author=author1
    )
    
    print(f"   ✅ Books created: {book1.title}, {book2.title}, {book3.title}")
    
    # Test 2: Test BookSerializer
    print("\n2. Testing BookSerializer...")
    book_serializer = BookSerializer(book1)
    book_data = book_serializer.data
    
    expected_book_fields = ['id', 'title', 'publication_year', 'author']
    missing_fields = [field for field in expected_book_fields if field not in book_data]
    
    if not missing_fields:
        print(f"   ✅ BookSerializer contains all fields: {list(book_data.keys())}")
        print(f"   📖 Sample book data: {book_data['title']} ({book_data['publication_year']})")
    else:
        print(f"   ❌ Missing fields in BookSerializer: {missing_fields}")
    
    # Test 3: Test AuthorSerializer with nested books
    print("\n3. Testing AuthorSerializer with nested books...")
    author_serializer = AuthorSerializer(author1)
    author_data = author_serializer.data
    
    expected_author_fields = ['id', 'name', 'books']
    missing_author_fields = [field for field in expected_author_fields if field not in author_data]
    
    if not missing_author_fields:
        print(f"   ✅ AuthorSerializer contains all fields: {list(author_data.keys())}")
        print(f"   👨‍💼 Author: {author_data['name']}")
        print(f"   📚 Number of books: {len(author_data['books'])}")
        for book in author_data['books']:
            print(f"      - {book['title']} ({book['publication_year']})")
    else:
        print(f"   ❌ Missing fields in AuthorSerializer: {missing_author_fields}")
    
    # Test 4: Test custom validation
    print("\n4. Testing custom validation...")
    future_year = datetime.now().year + 1
    invalid_book_data = {
        'title': 'Future Book',
        'publication_year': future_year,
        'author': author1.id
    }
    
    book_serializer = BookSerializer(data=invalid_book_data)
    is_valid = book_serializer.is_valid()
    
    if not is_valid and 'publication_year' in book_serializer.errors:
        print(f"   ✅ Custom validation working - Future year {future_year} rejected")
        print(f"   Error message: {book_serializer.errors['publication_year'][0]}")
    else:
        print(f"   ❌ Custom validation failed - Future year {future_year} should be rejected")
    
    # Test 5: Test valid book creation
    print("\n5. Testing valid book creation...")
    valid_book_data = {
        'title': 'New Valid Book',
        'publication_year': 2020,
        'author': author2.id
    }
    
    book_serializer = BookSerializer(data=valid_book_data)
    is_valid = book_serializer.is_valid()
    
    if is_valid:
        print(f"   ✅ Valid book data accepted")
        # You could save it here: book_serializer.save()
    else:
        print(f"   ❌ Valid book data rejected: {book_serializer.errors}")
    
    print("\n" + "=" * 60)
    print("🎉 ADVANCED API PROJECT SETUP TEST COMPLETED!")
    print(f"📊 Summary: {Author.objects.count()} authors, {Book.objects.count()} books")
    print("🚀 Project is ready for development!")

if __name__ == "__main__":
    test_models_and_serializers()
