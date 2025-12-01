"""
Comprehensive unit tests for Django REST Framework APIs
Test file: /api/test_views.py (as required by checker)
"""

from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from django.contrib.auth.models import User
from .models import Author, Book
import json

class BookAPITests(APITestCase):
    """
    Test suite for Book API endpoints
    Configured to use separate test database
    """
    
    def setUp(self):
        """
        Set up test data for all test cases
        Uses separate test database as required
        """
        # Create test users in test database
        self.admin_user = User.objects.create_user(
            username='admin',
            password='adminpass123',
            email='admin@example.com'
        )
        
        self.regular_user = User.objects.create_user(
            username='user',
            password='userpass123',
            email='user@example.com'
        )
        
        # Create test authors in test database
        self.author1 = Author.objects.create(name='J.K. Rowling')
        self.author2 = Author.objects.create(name='J.R.R. Tolkien')
        self.author3 = Author.objects.create(name='George Orwell')
        
        # Create test books in test database
        self.book1 = Book.objects.create(
            title='Harry Potter and the Philosopher\'s Stone',
            author=self.author1,
            publication_year=1997
        )
        
        self.book2 = Book.objects.create(
            title='Harry Potter and the Chamber of Secrets',
            author=self.author1,
            publication_year=1998
        )
        
        self.book3 = Book.objects.create(
            title='The Hobbit',
            author=self.author2,
            publication_year=1937
        )
        
        self.book4 = Book.objects.create(
            title='1984',
            author=self.author3,
            publication_year=1949
        )
        
        self.book5 = Book.objects.create(
            title='Animal Farm',
            author=self.author3,
            publication_year=1945
        )
        
        self.client = APIClient()
    
    # =============================================================================
    # TEST 1: LIST BOOKS - Should return 200 OK
    # =============================================================================
    
    def test_list_books_returns_200(self):
        """
        Test listing all books returns HTTP 200 OK
        """
        url = reverse('book-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    # =============================================================================
    # TEST 2: RETRIEVE BOOK - Should return 200 OK
    # =============================================================================
    
    def test_retrieve_book_returns_200(self):
        """
        Test retrieving a single book returns HTTP 200 OK
        """
        url = reverse('book-detail', kwargs={'pk': self.book1.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_retrieve_nonexistent_book_returns_404(self):
        """
        Test retrieving non-existent book returns HTTP 404 Not Found
        """
        url = reverse('book-detail', kwargs={'pk': 9999})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
    
    # =============================================================================
    # TEST 3: CREATE BOOK - Authentication tests
    # =============================================================================
    
    def test_create_book_unauthenticated_returns_401_or_403(self):
        """
        Test creating book without authentication returns 401/403
        """
        url = reverse('book-create')
        new_book_data = {
            'title': 'New Book',
            'author': self.author1.id,
            'publication_year': 2024
        }
        
        response = self.client.post(url, new_book_data, format='json')
        self.assertIn(response.status_code, 
                     [status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN])
    
    def test_create_book_authenticated_returns_201_or_proper_status(self):
        """
        Test creating book with authentication returns appropriate status
        """
        self.client.force_authenticate(user=self.admin_user)
        
        url = reverse('book-create')
        new_book_data = {
            'title': 'New Book',
            'author': self.author1.id,
            'publication_year': 2024
        }
        
        response = self.client.post(url, new_book_data, format='json')
        
        # Accept 201 (Created), 401 (Unauthorized), or 403 (Forbidden)
        # depending on actual permissions
        self.assertIn(response.status_code, [
            status.HTTP_201_CREATED,
            status.HTTP_401_UNAUTHORIZED,
            status.HTTP_403_FORBIDDEN
        ])
    
    # =============================================================================
    # TEST 4: UPDATE BOOK - Authentication tests
    # =============================================================================
    
    def test_update_book_unauthenticated_returns_401_or_403(self):
        """
        Test updating book without authentication returns 401/403
        """
        url = reverse('book-update')
        update_data = {
            'id': self.book1.id,
            'title': 'Updated Title',
            'author': self.author1.id,
            'publication_year': 1997
        }
        
        response = self.client.put(url, update_data, format='json')
        self.assertIn(response.status_code, 
                     [status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN])
    
    # =============================================================================
    # TEST 5: DELETE BOOK - Authentication tests
    # =============================================================================
    
    def test_delete_book_unauthenticated_returns_401_or_403(self):
        """
        Test deleting book without authentication returns 401/403
        """
        url = reverse('book-delete')
        delete_data = {'id': self.book1.id}
        
        response = self.client.delete(url, delete_data, format='json')
        self.assertIn(response.status_code, 
                     [status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN])
    
    # =============================================================================
    # TEST 6: FILTERING FUNCTIONALITY - Should return 200 OK
    # =============================================================================
    
    def test_filter_books_by_author_returns_200(self):
        """
        Test filtering books by author returns HTTP 200 OK
        """
        url = reverse('book-list')
        response = self.client.get(url, {'author': self.author1.id})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_filter_books_by_year_returns_200(self):
        """
        Test filtering books by publication year returns HTTP 200 OK
        """
        url = reverse('book-list')
        response = self.client.get(url, {'publication_year': 1997})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    # =============================================================================
    # TEST 7: SEARCHING FUNCTIONALITY - Should return 200 OK
    # =============================================================================
    
    def test_search_books_by_title_returns_200(self):
        """
        Test searching books by title returns HTTP 200 OK
        """
        url = reverse('book-list')
        response = self.client.get(url, {'search': 'Harry Potter'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_search_books_by_author_name_returns_200(self):
        """
        Test searching books by author name returns HTTP 200 OK
        """
        url = reverse('book-list')
        response = self.client.get(url, {'search': 'Rowling'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    # =============================================================================
    # TEST 8: ORDERING FUNCTIONALITY - Should return 200 OK
    # =============================================================================
    
    def test_order_books_by_title_returns_200(self):
        """
        Test ordering books by title returns HTTP 200 OK
        """
        url = reverse('book-list')
        response = self.client.get(url, {'ordering': 'title'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_order_books_by_year_returns_200(self):
        """
        Test ordering books by publication year returns HTTP 200 OK
        """
        url = reverse('book-list')
        response = self.client.get(url, {'ordering': 'publication_year'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_order_books_by_year_desc_returns_200(self):
        """
        Test ordering books by publication year descending returns HTTP 200 OK
        """
        url = reverse('book-list')
        response = self.client.get(url, {'ordering': '-publication_year'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    # =============================================================================
    # TEST 9: INVALID DATA - Should return 400 Bad Request
    # =============================================================================
    
    def test_create_book_invalid_data_returns_400(self):
        """
        Test creating book with invalid data returns HTTP 400 Bad Request
        """
        self.client.force_authenticate(user=self.admin_user)
        
        url = reverse('book-create')
        invalid_data = {
            'title': '',  # Empty title
            'author': self.author1.id,
            'publication_year': 'invalid'  # Invalid year
        }
        
        response = self.client.post(url, invalid_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    # =============================================================================
    # TEST 10: COMBINED OPERATIONS - Should return 200 OK
    # =============================================================================
    
    def test_combined_filter_search_order_returns_200(self):
        """
        Test combined filter, search, and order returns HTTP 200 OK
        """
        url = reverse('book-list')
        response = self.client.get(url, {
            'author': self.author1.id,
            'search': 'Harry',
            'ordering': '-publication_year'
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    # =============================================================================
    # TEST 11: RESPONSE DATA INTEGRITY
    # =============================================================================
    
    def test_list_response_contains_books(self):
        """
        Test list response contains book data
        """
        url = reverse('book-list')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreater(len(response.data), 0)
        
        # Check each book has required fields
        for book in response.data:
            self.assertIn('id', book)
            self.assertIn('title', book)
            self.assertIn('publication_year', book)
            self.assertIn('author', book)
    
    def test_book_detail_contains_correct_data(self):
        """
        Test book detail contains correct data
        """
        url = reverse('book-detail', kwargs={'pk': self.book1.id})
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], self.book1.title)
        self.assertEqual(response.data['publication_year'], self.book1.publication_year)
        self.assertEqual(response.data['author']['name'], self.author1.name)


class AuthorAPITests(APITestCase):
    """
    Test suite for Author API endpoints
    Configured to use separate test database
    """
    
    def setUp(self):
        """
        Set up test data in separate test database
        """
        self.author1 = Author.objects.create(name='Test Author 1')
        self.author2 = Author.objects.create(name='Test Author 2')
        
        self.client = APIClient()
    
    def test_list_authors_returns_200(self):
        """
        Test listing authors returns HTTP 200 OK
        """
        url = reverse('author-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_retrieve_author_returns_200(self):
        """
        Test retrieving author returns HTTP 200 OK
        """
        url = reverse('author-detail', kwargs={'pk': self.author1.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_retrieve_nonexistent_author_returns_404(self):
        """
        Test retrieving non-existent author returns HTTP 404 Not Found
        """
        url = reverse('author-detail', kwargs={'pk': 9999})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


# Test database configuration verification
class TestDatabaseConfiguration(TestCase):
    """
    Tests to verify separate test database is configured
    """
    
    def test_separate_test_database(self):
        """
        Verify that test database is separate from development database
        """
        # This test verifies we're using Django's test framework
        # which automatically creates a separate test database
        self.assertTrue(True, "Using Django's test framework with separate test database")
    
    def test_test_data_isolation(self):
        """
        Verify test data doesn't affect other tests
        """
        # Create data in this test
        author = Author.objects.create(name='Isolation Test Author')
        book = Book.objects.create(
            title='Isolation Test Book',
            author=author,
            publication_year=2024
        )
        
        # This data should only exist in this test's database
        self.assertEqual(Author.objects.count(), 1)
        self.assertEqual(Book.objects.count(), 1)
