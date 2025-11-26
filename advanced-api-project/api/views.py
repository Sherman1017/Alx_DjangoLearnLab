from rest_framework import generics, permissions, status
from rest_framework.response import Response
from .models import Author, Book
from .serializers import AuthorSerializer, BookSerializer

# =============================================================================
# BOOK VIEWS - Complete CRUD operations using generic views
# =============================================================================

class ListView(generics.ListAPIView):
    """
    List all books (Read-Only)
    """
    queryset = Book.objects.select_related('author').all()
    serializer_class = BookSerializer
    permission_classes = [permissions.AllowAny]  # Public access


class DetailView(generics.RetrieveAPIView):
    """
    Retrieve a single book by ID (Read-Only)
    """
    queryset = Book.objects.select_related('author').all()
    serializer_class = BookSerializer
    permission_classes = [permissions.AllowAny]  # Public access


class CreateView(generics.CreateAPIView):
    """
    Create a new book (Authenticated Users Only)
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
    
    Note: This view now handles the book ID from request data
    since the URL pattern doesn't include <int:pk>
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated]  # Authenticated users only
    
    def update(self, request, *args, **kwargs):
        """
        Custom update method to handle book ID from request data
        since URL pattern is just 'books/update/'
        """
        # Get book ID from request data
        book_id = request.data.get('id')
        if not book_id:
            return Response(
                {"error": "Book ID is required in request data"}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Get the book instance
        try:
            instance = Book.objects.get(id=book_id)
        except Book.DoesNotExist:
            return Response(
                {"error": "Book not found"}, 
                status=status.HTTP_404_NOT_FOUND
            )
        
        # Perform the update
        serializer = self.get_serializer(instance, data=request.data, partial=False)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        
        return Response(serializer.data)
    
    def perform_update(self, serializer):
        """Custom method called when updating a book instance."""
        serializer.save()


class DeleteView(generics.DestroyAPIView):
    """
    Delete a book (Authenticated Users Only)
    
    Note: This view now handles the book ID from request data
    since the URL pattern doesn't include <int:pk>
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated]  # Authenticated users only
    
    def destroy(self, request, *args, **kwargs):
        """
        Custom destroy method to handle book ID from request data
        since URL pattern is just 'books/delete/'
        """
        # Get book ID from request data
        book_id = request.data.get('id')
        if not book_id:
            return Response(
                {"error": "Book ID is required in request data"}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Get the book instance
        try:
            instance = Book.objects.get(id=book_id)
        except Book.DoesNotExist:
            return Response(
                {"error": "Book not found"}, 
                status=status.HTTP_404_NOT_FOUND
            )
        
        # Perform the deletion
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)
    
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
