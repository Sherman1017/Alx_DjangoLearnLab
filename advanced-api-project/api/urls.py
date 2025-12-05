from django.urls import path
from . import views

urlpatterns = [
    # Book URLs with explicit names
    path('books/', views.ListView.as_view(), name='book-list'),
    path('books/<int:pk>/', views.DetailView.as_view(), name='book-detail'),
    path('books/create/', views.CreateView.as_view(), name='book-create'),
    path('books/update/', views.UpdateView.as_view(), name='book-update'),
    path('books/delete/', views.DeleteView.as_view(), name='book-delete'),
    
    # Author URLs with explicit names
    path('authors/', views.AuthorListView.as_view(), name='author-list'),
    path('authors/<int:pk>/', views.AuthorDetailView.as_view(), name='author-detail'),
]
