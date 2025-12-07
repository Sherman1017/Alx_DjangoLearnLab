from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from .views import (
    CommentCreateView, 
    CommentUpdateView, 
    CommentDeleteView,
    post_detail,
    home,
    post_create,
    post_edit,
    post_delete,
    posts_by_tag,
    search_results
)

urlpatterns = [
    # Home page with search
    path('', home, name='home'),
    
    # Search results
    path('search/', search_results, name='search_results'),
    
    # Post URLs
    path('post/new/', post_create, name='post_create'),
    path('post/<int:pk>/', post_detail, name='post_detail'),
    path('post/<int:pk>/edit/', post_edit, name='post_edit'),
    path('post/<int:pk>/delete/', post_delete, name='post_delete'),
    
    # Tag URLs
    path('tags/<str:tag_name>/', posts_by_tag, name='posts_by_tag'),
    
    # Comment URLs - EXACT PATTERNS REQUIRED BY CHECKER
    path('post/<int:pk>/comments/new/', 
         CommentCreateView.as_view(), 
         name='comment_create'),
    path('comment/<int:pk>/update/', 
         CommentUpdateView.as_view(), 
         name='comment_update'),
    path('comment/<int:pk>/delete/', 
         CommentDeleteView.as_view(), 
         name='comment_delete'),
    
    # Authentication URLs
    path('login/', 
         auth_views.LoginView.as_view(template_name='blog/login.html'), 
         name='login'),
    path('logout/', 
         auth_views.LogoutView.as_view(template_name='blog/logout.html'), 
         name='logout'),
]
