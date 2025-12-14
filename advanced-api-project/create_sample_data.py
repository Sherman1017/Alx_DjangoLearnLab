#!/usr/bin/env python3
"""
Script to create sample data for testing filtering, searching, and ordering
"""

import os
import sys
import django

# Setup Django
sys.path.append('/Alx_DjangoLearnLab/advanced-api-project')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'advanced_api_project.settings')
django.setup()

from api.models import Author, Book

def create_sample_data():
    print("📚 Creating sample data for filtering testing...")
    
    # Clear existing data
    Book.objects.all().delete()
    Author.objects.all().delete()
    
    # Create authors
    authors_data = [
        {'name': 'J.K. Rowling'},
        {'name': 'George Orwell'},
        {'name': 'Jane Austen'},
        {'name': 'J.R.R. Tolkien'},
        {'name': 'Agatha Christie'},
        {'name': 'Stephen King'},
        {'name': 'Ernest Hemingway'},
    ]
    
    authors = {}
    for author_data in authors_data:
        author, created = Author.objects.get_or_create(**author_data)
        authors[author_data['name']] = author
        print(f"✅ Created author: {author.name}")
    
    # Create books with varied data for testing filtering
    books_data = [
        # J.K. Rowling books
        {'title': 'Harry Potter and the Philosopher\'s Stone', 'publication_year': 1997, 'author': authors['J.K. Rowling']},
        {'title': 'Harry Potter and the Chamber of Secrets', 'publication_year': 1998, 'author': authors['J.K. Rowling']},
        {'title': 'Harry Potter and the Prisoner of Azkaban', 'publication_year': 1999, 'author': authors['J.K. Rowling']},
        {'title': 'Harry Potter and the Goblet of Fire', 'publication_year': 2000, 'author': authors['J.K. Rowling']},
        {'title': 'The Casual Vacancy', 'publication_year': 2012, 'author': authors['J.K. Rowling']},
        
        # George Orwell books
        {'title': '1984', 'publication_year': 1949, 'author': authors['George Orwell']},
        {'title': 'Animal Farm', 'publication_year': 1945, 'author': authors['George Orwell']},
        
        # Jane Austen books
        {'title': 'Pride and Prejudice', 'publication_year': 1813, 'author': authors['Jane Austen']},
        {'title': 'Sense and Sensibility', 'publication_year': 1811, 'author': authors['Jane Austen']},
        {'title': 'Emma', 'publication_year': 1815, 'author': authors['Jane Austen']},
        
        # J.R.R. Tolkien books
        {'title': 'The Hobbit', 'publication_year': 1937, 'author': authors['J.R.R. Tolkien']},
        {'title': 'The Fellowship of the Ring', 'publication_year': 1954, 'author': authors['J.R.R. Tolkien']},
        {'title': 'The Two Towers', 'publication_year': 1954, 'author': authors['J.R.R. Tolkien']},
        {'title': 'The Return of the King', 'publication_year': 1955, 'author': authors['J.R.R. Tolkien']},
        
        # Agatha Christie books
        {'title': 'Murder on the Orient Express', 'publication_year': 1934, 'author': authors['Agatha Christie']},
        {'title': 'Death on the Nile', 'publication_year': 1937, 'author': authors['Agatha Christie']},
        {'title': 'The ABC Murders', 'publication_year': 1936, 'author': authors['Agatha Christie']},
        
        # Stephen King books
        {'title': 'The Shining', 'publication_year': 1977, 'author': authors['Stephen King']},
        {'title': 'It', 'publication_year': 1986, 'author': authors['Stephen King']},
        {'title': 'The Stand', 'publication_year': 1978, 'author': authors['Stephen King']},
        
        # Ernest Hemingway books
        {'title': 'The Old Man and the Sea', 'publication_year': 1952, 'author': authors['Ernest Hemingway']},
        {'title': 'A Farewell to Arms', 'publication_year': 1929, 'author': authors['Ernest Hemingway']},
    ]
    
    for book_data in books_data:
        book, created = Book.objects.get_or_create(
            title=book_data['title'],
            defaults={
                'publication_year': book_data['publication_year'],
                'author': book_data['author']
            }
        )
        if created:
            print(f"✅ Created book: '{book.title}' ({book.publication_year}) by {book.author.name}")
    
    print(f"\n📊 Sample data created:")
    print(f"   Authors: {Author.objects.count()}")
    print(f"   Books: {Book.objects.count()}")
    
    # Show some statistics
    from django.db.models import Count, Min, Max
    stats = Book.objects.aggregate(
        total_books=Count('id'),
        earliest_year=Min('publication_year'),
        latest_year=Max('publication_year'),
        unique_authors=Count('author', distinct=True)
    )
    
    print(f"   Publication years: {stats['earliest_year']} - {stats['latest_year']}")
    print(f"   Unique authors: {stats['unique_authors']}")

if __name__ == "__main__":
    create_sample_data()
