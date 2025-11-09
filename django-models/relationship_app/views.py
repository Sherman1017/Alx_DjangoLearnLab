from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import DetailView, ListView
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required, user_passes_test, permission_required
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib import messages
from django.urls import reverse_lazy
from .models import Book, Library, Author, UserProfile
from .forms import BookForm

# Helper function to check user roles
def is_admin(user):
    return user.is_authenticated and hasattr(user, 'userprofile') and user.userprofile.role == 'Admin'

def is_librarian(user):
    return user.is_authenticated and hasattr(user, 'userprofile') and user.userprofile.role == 'Librarian'

def is_member(user):
    return user.is_authenticated and hasattr(user, 'userprofile') and user.userprofile.role == 'Member'

# Function-based view to list all books
def book_list(request):
    books = Book.objects.all()
    return render(request, 'relationship_app/list_books.html', {'books': books})

# Class-based view to display library details
class LibraryDetailView(DetailView):
    model = Library
    template_name = 'relationship_app/library_detail.html'
    context_object_name = 'library'

# Class-based view to list all libraries
class LibraryListView(ListView):
    model = Library
    template_name = 'relationship_app/library_list.html'
    context_object_name = 'libraries'

# Authentication Views
def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('relationship_app:book_list')
    else:
        form = UserCreationForm()
    return render(request, 'relationship_app/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('relationship_app:book_list')
    else:
        form = AuthenticationForm()
    return render(request, 'relationship_app/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return render(request, 'relationship_app/logout.html')

# Role-Based Views
@login_required
@user_passes_test(is_admin)
def admin_view(request):
    return render(request, 'relationship_app/admin_view.html')

@login_required
@user_passes_test(is_librarian)
def librarian_view(request):
    return render(request, 'relationship_app/librarian_view.html')

@login_required
@user_passes_test(is_member)
def member_view(request):
    return render(request, 'relationship_app/member_view.html')

# View to manage user roles (Admin only)
@login_required
@user_passes_test(is_admin)
def manage_roles(request):
    users = User.objects.all().select_related('userprofile')
    if request.method == 'POST':
        user_id = request.POST.get('user_id')
        new_role = request.POST.get('role')
        try:
            user_profile = UserProfile.objects.get(user_id=user_id)
            user_profile.role = new_role
            user_profile.save()
        except UserProfile.DoesNotExist:
            pass
        return redirect('relationship_app:manage_roles')
    
    return render(request, 'relationship_app/manage_roles.html', {'users': users})

# Custom Permission Protected Views for Books
@login_required
@permission_required('relationship_app.can_add_book', raise_exception=True)
def add_book(request):
    if request.method == 'POST':
        form = BookForm(request.POST)
        if form.is_valid():
            book = form.save()
            messages.success(request, f'Book "{book.title}" added successfully!')
            return redirect('relationship_app:book_list')
    else:
        form = BookForm()
    
    return render(request, 'relationship_app/book_form.html', {
        'form': form,
        'title': 'Add New Book',
        'action': 'Add'
    })

@login_required
@permission_required('relationship_app.can_change_book', raise_exception=True)
def edit_book(request, pk):
    book = get_object_or_404(Book, pk=pk)
    
    if request.method == 'POST':
        form = BookForm(request.POST, instance=book)
        if form.is_valid():
            book = form.save()
            messages.success(request, f'Book "{book.title}" updated successfully!')
            return redirect('relationship_app:book_list')
    else:
        form = BookForm(instance=book)
    
    return render(request, 'relationship_app/book_form.html', {
        'form': form,
        'title': f'Edit Book: {book.title}',
        'action': 'Update'
    })

@login_required
@permission_required('relationship_app.can_delete_book', raise_exception=True)
def delete_book(request, pk):
    book = get_object_or_404(Book, pk=pk)
    
    if request.method == 'POST':
        book_title = book.title
        book.delete()
        messages.success(request, f'Book "{book_title}" deleted successfully!')
        return redirect('relationship_app:book_list')
    
    return render(request, 'relationship_app/book_confirm_delete.html', {
        'book': book
    })

# Book list with management options (shows actions based on permissions)
@login_required
def manage_books(request):
    books = Book.objects.all()
    can_add = request.user.has_perm('relationship_app.can_add_book')
    can_change = request.user.has_perm('relationship_app.can_change_book')
    can_delete = request.user.has_perm('relationship_app.can_delete_book')
    
    return render(request, 'relationship_app/manage_books.html', {
        'books': books,
        'can_add': can_add,
        'can_change': can_change,
        'can_delete': can_delete,
    })
