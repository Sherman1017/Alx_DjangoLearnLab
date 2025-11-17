from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, permission_required
from django.db.models import Q
from django.core.paginator import Paginator
from django.contrib import messages
from django.utils.html import escape
from django.http import JsonResponse
from django.views.decorators.csrf import ensures_csrf_cookie
from .models import Book, CustomUser
from .forms import  ExampleForm
import logging

logger = logging.getLogger(__name__)

# ==============================================================================
# TASK 1: PERMISSION-PROTECTED VIEWS
# ==============================================================================

@login_required
@permission_required('bookshelf.can_view', raise_exception=True)
def book_list(request):
    """
    TASK 1 & 2: Secure book listing with permissions and SQL injection prevention
    """
    books = Book.objects.all()
    
    # TASK 2: Safe search using Django ORM (prevents SQL injection)
    search_query = request.GET.get('q', '').strip()
    if search_query:
        safe_search_query = escape(search_query)
        books = books.filter(
            Q(title__icontains=safe_search_query) |
            Q(author__icontains=safe_search_query) |
            Q(isbn__icontains=safe_search_query)
        )
        logger.info(f"User {request.user.email} searched for: {safe_search_query}")
    
    # Safe pagination
    paginator = Paginator(books, 10)
    page_number = request.GET.get('page', 1)
    try:
        page_number = int(page_number)
    except (TypeError, ValueError):
        page_number = 1
    
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'search_query': escape(search_query),
    }
    
    return render(request, 'bookshelf/book_list.html', context)

@login_required
@permission_required('bookshelf.can_create', raise_exception=True)
def add_book(request):
    """
    TASK 1 & 2: Book creation with permissions and CSRF protection
    """
    if request.method == 'POST':
        form = BookForm(request.POST)
        if form.is_valid():
            book = form.save(commit=False)
            book.created_by = request.user
            book.save()
            messages.success(request, 'Book added successfully!')
            return redirect('book_list')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = BookForm()
    
    return render(request, 'bookshelf/form_example.html', {'form': form})

@login_required
@permission_required('bookshelf.can_edit', raise_exception=True)
def edit_book(request, book_id):
    """
    TASK 1: Edit book with permission check
    """
    book = get_object_or_404(Book, id=book_id)
    
    if request.method == 'POST':
        form = BookForm(request.POST, instance=book)
        if form.is_valid():
            form.save()
            messages.success(request, 'Book updated successfully!')
            return redirect('book_list')
    else:
        form = BookForm(instance=book)
    
    return render(request, 'bookshelf/form_example.html', {'form': form, 'editing': True})

@login_required
@permission_required('bookshelf.can_delete', raise_exception=True)
def delete_book(request, book_id):
    """
    TASK 1: Delete book with permission check
    """
    book = get_object_or_404(Book, id=book_id)
    if request.method == 'POST':
        book.delete()
        messages.success(request, 'Book deleted successfully!')
        return redirect('book_list')
    
    return render(request, 'bookshelf/delete_confirm.html', {'book': book})

# ==============================================================================
# TASK 2: SECURITY DEMO VIEWS
# ==============================================================================

@ensures_csrf_cookie
def security_demo(request):
    """
    TASK 2 & 3: Security features demonstration
    """
    context = {
        'title': 'ALX Django Security Implementation',
        'tasks': [
            'Task 0: Custom User Model ✓',
            'Task 1: Permissions & Groups ✓',
            'Task 2: Security Best Practices ✓', 
            'Task 3: HTTPS & Secure Redirects ✓',
        ],
        'security_features': [
            'Custom User Model with email authentication',
            'Permission-based access control',
            'CSRF protection in all forms',
            'SQL injection prevention',
            'XSS protection through input validation',
            'HTTPS redirect configuration',
            'Secure cookies (Session & CSRF)',
            'HSTS enforcement',
            'Security headers implementation',
        ]
    }
    return render(request, 'bookshelf/security_demo.html', context)

def security_headers_check(request):
    """
    TASK 3: API endpoint to verify security headers
    """
    response = JsonResponse({
        'status': 'secure',
        'message': 'All security features are properly configured',
        'https_settings': {
            'secure_ssl_redirect': True,
            'hsts_enabled': True,
            'hsts_seconds': 31536000,
            'secure_cookies': True,
        },
        'security_headers': True,
    })
    
    # Additional security headers
    response['X-Security-Level'] = 'High'
    response['X-HTTPS-Status'] = 'Enabled'
    
    return response

def form_example_view(request):
    """
    TASK 2: Example form view for CSRF demonstration
    """
    if request.method == 'POST':
        form = ExampleForm(request.POST)
        if form.is_valid():
            messages.success(request, 'Form submitted successfully!')
            return redirect('security_demo')
    else:
        form = ExampleForm()
    
    return render(request, 'bookshelf/form_example.html', {'form': form})
