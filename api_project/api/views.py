from rest_framework import generics, viewsets, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from .models import Book
from .serializers import BookSerializer

# Keep the existing BookList but add permissions
class BookList(generics.ListAPIView):
    """
    API endpoint that allows books to be viewed.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]  # Allow read for anyone, write for authenticated

# ViewSet with different permission levels
class BookViewSet(viewsets.ModelViewSet):
    """
    A ViewSet for viewing and editing book instances.
    Provides full CRUD operations: list, create, retrieve, update, destroy
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    
    # Set permissions - different actions can have different permissions
    def get_permissions(self):
        """
        Instantiates and returns the list of permissions that this view requires.
        """
        if self.action == 'list' or self.action == 'retrieve':
            # Allow anyone to view books
            permission_classes = [permissions.AllowAny]
        else:
            # Only allow authenticated users to create, update, delete
            permission_classes = [permissions.IsAuthenticated]
        return [permission() for permission in permission_classes]

# Public view that doesn't require authentication
@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def public_book_list(request):
    """
    Public API endpoint that allows anyone to view books.
    """
    books = Book.objects.all()[:5]  # Limit to 5 books for public view
    serializer = BookSerializer(books, many=True)
    return Response({
        'message': 'Public book list (limited to 5 books)',
        'books': serializer.data
    })
