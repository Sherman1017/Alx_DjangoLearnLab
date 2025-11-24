from django.urls import path
from . import views

urlpatterns = [
    path('authors/', views.AuthorList.as_view(), name='author-list'),
    path('books/', views.BookList.as_view(), name='book-list'),
    path('books/create/', views.BookCreate.as_view(), name='book-create'),
]
