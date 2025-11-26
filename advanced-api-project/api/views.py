from rest_framework import generics, permissions
from .models import Author, Book
from .serializers import AuthorSerializer, BookSerializer

# =============================================================================
# BOOK VIEWS - Complete CRUD operations using generic views
# =============================================================================

class ListView(generics.ListAPIView):
    """
    List all books (Read-Only)
    
    Generic ListAPIView that provides read-only access to all Book instances.
    Accessible to all users (authenticated and unauthenticated).
    """
    queryset = Book.objects.select_related('author').all()
    serializer_class = BookSerializer
    permission_classes = [permissions.AllowAny]  # Public access


class DetailView(generics.RetrieveAPIView):
    """
    Retrieve a single book by ID (Read-Only)
    
    Generic RetrieveAPIView that provides read-only access to a specific Book instance.
    Accessible to all users (authenticated and unauthenticated).
    """
    queryset = Book.objects.select_related('author').all()
    serializer_class = BookSerializer
    permission_classes = [permissions.AllowAny]  # Public access


class CreateView(generics.CreateAPIView):
    """
    Create a new book (Authenticated Users Only)
    
    Generic CreateAPIView that allows creation of new Book instances.
    Restricted to authenticated users only.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated]  # Authenticated users only
    
    def perform_create(self, serializer):
        """Custom method called when creating a new book instance."""
        serializer.save()


class UpdateView(generics.UpdateAPIView):
    """
    Update an existing book (Authenticated Users Only)
    
    Generic UpdateAPIView that allows full updates of Book instances.
    Restricted to authenticated users only.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated]  # Authenticated users only
    
    def perform_update(self, serializer):
        """Custom method called when updating a book instance."""
        serializer.save()


class DeleteView(generics.DestroyAPIView):
    """
    Delete a book (Authenticated Users Only)
    
    Generic DestroyAPIView that allows deletion of Book instances.
    Restricted to authenticated users only.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated]  # Authenticated users only
    
    def perform_destroy(self, instance):
        """Custom method called when deleting a book instance."""
        instance.delete()


# =============================================================================
# AUTHOR VIEWS - Using generic views for authors
# =============================================================================

class AuthorListView(generics.ListAPIView):
    """
    List all authors with their books (Read-Only)
    """
    queryset = Author.objects.prefetch_related('books').all()
    serializer_class = AuthorSerializer
    permission_classes = [permissions.AllowAny]  # Public access


class AuthorDetailView(generics.RetrieveAPIView):
    """
    Retrieve a single author by ID with books (Read-Only)
    """
    queryset = Author.objects.prefetch_related('books').all()
    serializer_class = AuthorSerializer
    permission_classes = [permissions.AllowAny]  # Public access


# =============================================================================
# CUSTOM MIXIN VIEWS - Demonstrating custom view combinations
# =============================================================================

class BookListCreateView(generics.ListCreateAPIView):
    """
    Combined view for listing and creating books with different permissions.
    """
    queryset = Book.objects.select_related('author').all()
    serializer_class = BookSerializer
    
    def get_permissions(self):
        """Custom permission handling based on HTTP method."""
        if self.request.method == 'GET':
            return [permissions.AllowAny()]
        return [permissions.IsAuthenticated()]


class BookRetrieveUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    """
    Combined view for retrieving, updating, and deleting a specific book.
    """
    queryset = Book.objects.select_related('author').all()
    serializer_class = BookSerializer
    
    def get_permissions(self):
        """Custom permission handling based on HTTP method."""
        if self.request.method == 'GET':
            return [permissions.AllowAny()]
        return [permissions.IsAuthenticated()]
