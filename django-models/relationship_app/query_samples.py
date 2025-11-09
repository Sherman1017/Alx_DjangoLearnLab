#!/usr/bin/env python3
import os
import django
import sys

# Add the current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Set up Django environment with correct project name
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'LibraryProject.settings')
django.setup()

from relationship_app.models import Author, Book, Library, Librarian

def sample_queries():
    print("=== Sample Relationship Queries ===\n")
    
    # Query all books by a specific author
    try:
        author = Author.objects.get(name="J.K. Rowling")
        books_by_author = Book.objects.filter(author=author)
        print(f"1. Books by {author.name}:")
        for book in books_by_author:
            print(f"   - {book.title}")
    except Author.DoesNotExist:
        print("1. Author not found - create some data first")
    
    # List all books in a library
    try:
        library = Library.objects.get(name="Central Library")
        books_in_library = library.books.all()
        print(f"\n2. Books in {library.name}:")
        for book in books_in_library:
            print(f"   - {book.title} by {book.author.name}")
    except Library.DoesNotExist:
        print("\n2. Library not found - create some data first")
    
    # Retrieve the librarian for a library
    try:
        library = Library.objects.get(name="Central Library")
        librarian = Librarian.objects.get(library=library)
        print(f"\n3. Librarian for {library.name}: {librarian.name}")
    except (Library.DoesNotExist, Librarian.DoesNotExist):
        print("\n3. Library or Librarian not found - create some data first")

if __name__ == "__main__":
    sample_queries()
