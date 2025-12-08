from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from .views import (
    CommentCreateView, 
    CommentUpdateView, 
    CommentDeleteView
)

urlpatterns = [
    # Home and search
    path('', views.home, name='home'),
    path('search/', views.search_results, name='search_results'),
    
    # Posts
    path('post/new/', views.post_create, name='post_create'),
    path('post/<int:pk>/', views.post_detail, name='post_detail'),
    path('post/<int:pk>/edit/', views.post_edit, name='post_edit'),
    path('post/<int:pk>/delete/', views.post_delete, name='post_delete'),
    
    # Comments (with exact patterns from earlier tasks)
    path('post/<int:pk>/comments/new/', 
         CommentCreateView.as_view(), 
         name='comment_create'),
    path('comment/<int:pk>/update/', 
         CommentUpdateView.as_view(), 
         name='comment_update'),
    path('comment/<int:pk>/delete/', 
         CommentDeleteView.as_view(), 
         name='comment_delete'),
    
    # Authentication
    path('login/', 
         auth_views.LoginView.as_view(template_name='blog/login.html'), 
         name='login'),
    path('logout/', 
         auth_views.LogoutView.as_view(), 
         name='logout'),
]
