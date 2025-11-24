from rest_framework import generics
from .models import Author, Book
from .serializers import AuthorSerializer, BookSerializer

class AuthorList(generics.ListAPIView):
    """
    API view to list all authors with their books.
    
    Uses AuthorSerializer which includes nested BookSerializer
    to display all books for each author.
    """
    queryset = Author.objects.prefetch_related('books').all()
    serializer_class = AuthorSerializer

class BookList(generics.ListAPIView):
    """
    API view to list all books.
    
    Uses BookSerializer which includes custom validation
    for publication_year field.
    """
    queryset = Book.objects.select_related('author').all()
    serializer_class = BookSerializer

class BookCreate(generics.CreateAPIView):
    """
    API view to create new books.
    
    Uses BookSerializer with custom validation to ensure
    publication_year is not in the future.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
