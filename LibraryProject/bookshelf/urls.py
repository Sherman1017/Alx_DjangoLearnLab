from django.urls import path
from . import views

app_name = 'bookshelf'

urlpatterns = [
    # TASK 1: Permission-protected book views
    path('books/', views.book_list, name='book_list'),
    path('books/add/', views.add_book, name='add_book'),
    path('books/<int:book_id>/edit/', views.edit_book, name='edit_book'),
    path('books/<int:book_id>/delete/', views.delete_book, name='delete_book'),
    
    # TASK 2 & 3: Security demonstration views
    path('', views.security_demo, name='security_demo'),
    path('security/headers-check/', views.security_headers_check, name='headers_check'),
    path('form-example/', views.form_example_view, name='form_example'),
]
