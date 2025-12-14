from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken.views import obtain_auth_token
from .views import BookList, BookViewSet, public_book_list

# Create a router and register our ViewSet
router = DefaultRouter()
router.register(r'books_all', BookViewSet, basename='book_all')

urlpatterns = [
    # Public endpoint - no authentication required
    path('books/public/', public_book_list, name='public-book-list'),
    
    # Protected endpoint - requires authentication for write operations
    path('books/', BookList.as_view(), name='book-list'),
    
    # Authentication endpoints
    path('auth-token/', obtain_auth_token, name='api_token_auth'),
    path('api-auth/', include('rest_framework.urls')),  # For browsable API login
    
    # Include the router URLs for BookViewSet
    path('', include(router.urls)),
]
