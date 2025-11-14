from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, permission_required
from django.db.models import Q
from django.core.paginator import Paginator
from django.contrib import messages
from django.utils.html import escape
from .models import Book
from .forms import BookForm
import logging

logger = logging.getLogger(__name__)

@login_required
def book_list(request):
    """
    Secure book listing view with proper input validation and SQL injection prevention.
    Uses Django ORM to safely handle database queries.
    """
    books = Book.objects.all()
    
    # Safe search functionality using Django ORM (prevents SQL injection)
    search_query = request.GET.get('q', '').strip()
    if search_query:
        # Escape user input to prevent XSS in template rendering
        safe_search_query = escape(search_query)
        
        # Use Django ORM to safely query the database
        books = books.filter(
            Q(title__icontains=safe_search_query) |
            Q(author__icontains=safe_search_query) |
            Q(isbn__icontains=safe_search_query)
        )
        
        # Log the search for security monitoring
        logger.info(f"User {request.user.email} searched for: {safe_search_query}")
    
    # Safe pagination
    paginator = Paginator(books, 10)  # Show 10 books per page
    page_number = request.GET.get('page', 1)
    
    try:
        page_number = int(page_number)
    except (TypeError, ValueError):
        page_number = 1
    
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'search_query': escape(search_query),  # Escape for safe template rendering
    }
    
    return render(request, 'bookshelf/book_list.html', context)

@login_required
@permission_required('bookshelf.can_manage_books', raise_exception=True)
def add_book(request):
    """
    Secure book creation view with CSRF protection and input validation.
    """
    if request.method == 'POST':
        form = BookForm(request.POST)
        if form.is_valid():
            # Secure: Save with user reference without exposing user manipulation
            book = form.save(commit=False)
            book.created_by = request.user  # Safe assignment
            book.save()
            
            messages.success(request, 'Book added successfully!')
            return redirect('book_list')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = BookForm()
    
    return render(request, 'bookshelf/form_example.html', {'form': form})

@login_required
def book_detail(request, book_id):
    """
    Secure book detail view using get_object_or_404 to prevent information leakage.
    """
    # Safe: get_object_or_404 prevents exposing existence of objects
    book = get_object_or_404(Book, id=book_id)
    
    # Additional permission check if needed
    if not request.user.has_perm('bookshelf.can_manage_books'):
        messages.warning(request, 'You need permission to view book details.')
        return redirect('book_list')
    
    context = {
        'book': book,
    }
    
    return render(request, 'bookshelf/book_detail.html', context)

# Example of what NOT to do (for educational purposes)
def unsafe_search_example(request):
    """
    UNSAFE EXAMPLE: Demonstrating SQL injection vulnerability.
    DO NOT USE IN PRODUCTION!
    """
    if request.method == 'GET':
        search_term = request.GET.get('search', '')
        
        # UNSAFE: Direct string formatting in raw SQL (VULNERABLE TO SQL INJECTION)
        # books = Book.objects.raw(f"SELECT * FROM bookshelf_book WHERE title LIKE '%{search_term}%'")
        
        # SAFE: Use Django ORM or parameterized queries
        books = Book.objects.filter(title__icontains=search_term)
        
        # Even safer: escape the input
        from django.utils.html import escape
        safe_search_term = escape(search_term)
        books = Book.objects.filter(title__icontains=safe_search_term)
        
    return render(request, 'bookshelf/search.html', {'books': books})
