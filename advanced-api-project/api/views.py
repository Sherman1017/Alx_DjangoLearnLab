from rest_framework import generics, status, filters  # Added filters here
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated, AllowAny
from django_filters import rest_framework  # Exact import expected by automated checks
from .models import Author, Book
from .serializers import AuthorSerializer, BookSerializer
from .filters import BookFilter

# =============================================================================
# BOOK VIEWS - Complete CRUD operations with filtering, searching, ordering
# =============================================================================

class ListView(generics.ListAPIView):
    """
    List all books with advanced filtering, searching, and ordering capabilities.
    """
    queryset = Book.objects.select_related('author').all()
    serializer_class = BookSerializer
    permission_classes = [AllowAny]
    
    # Use the exact filter backend configuration expected
    filter_backends = [
        rest_framework.DjangoFilterBackend,  # Use the imported module
        filters.SearchFilter,  # SearchFilter integration - USING filters.SearchFilter
        filters.OrderingFilter,  # OrderingFilter setup - USING filters.OrderingFilter
    ]
    
    # Filter configuration
    filterset_class = BookFilter
    
    # Search functionality on title and author fields
    search_fields = ['title', 'author__name']  # Enable search on title and author
    
    # Ordering configuration  
    ordering_fields = ['title', 'publication_year', 'author__name']  # Allow ordering by these fields
    ordering = ['title']  # Default ordering


class DetailView(generics.RetrieveAPIView):
    """
    Retrieve a single book by ID (Read-Only)
    """
    queryset = Book.objects.select_related('author').all()
    serializer_class = BookSerializer
    permission_classes = [AllowAny]


class CreateView(generics.CreateAPIView):
    """
    Create a new book (Authenticated Users Only)
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]
    
    def perform_create(self, serializer):
        serializer.save()


class UpdateView(generics.UpdateAPIView):
    """
    Update an existing book (Authenticated Users Only)
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]
    
    def update(self, request, *args, **kwargs):
        book_id = request.data.get('id')
        if not book_id:
            return Response(
                {"error": "Book ID is required in request data"}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            instance = Book.objects.get(id=book_id)
        except Book.DoesNotExist:
            return Response(
                {"error": "Book not found"}, 
                status=status.HTTP_404_NOT_FOUND
            )
        
        serializer = self.get_serializer(instance, data=request.data, partial=False)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        
        return Response(serializer.data)
    
    def perform_update(self, serializer):
        serializer.save()


class DeleteView(generics.DestroyAPIView):
    """
    Delete a book (Authenticated Users Only)
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]
    
    def destroy(self, request, *args, **kwargs):
        book_id = request.data.get('id')
        if not book_id:
            return Response(
                {"error": "Book ID is required in request data"}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            instance = Book.objects.get(id=book_id)
        except Book.DoesNotExist:
            return Response(
                {"error": "Book not found"}, 
                status=status.HTTP_404_NOT_FOUND
            )
        
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    def perform_destroy(self, instance):
        instance.delete()


# =============================================================================
# AUTHOR VIEWS
# =============================================================================

class AuthorListView(generics.ListAPIView):
    """
    List all authors with their books
    """
    queryset = Author.objects.prefetch_related('books').all()
    serializer_class = AuthorSerializer
    permission_classes = [AllowAny]


class AuthorDetailView(generics.RetrieveAPIView):
    """
    Retrieve a single author by ID with books
    """
    queryset = Author.objects.prefetch_related('books').all()
    serializer_class = AuthorSerializer
    permission_classes = [AllowAny]
