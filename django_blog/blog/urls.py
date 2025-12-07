from django.urls import path
from . import views

urlpatterns = [
    # Comment URLs
    path('posts/<int:post_id>/', views.post_detail_with_comments, name='post_detail_with_comments'),
    path('posts/<int:post_id>/comments/new/', views.add_comment, name='add_comment'),
    path('comments/<int:comment_id>/edit/', views.edit_comment, name='edit_comment'),
    path('comments/<int:comment_id>/delete/', views.delete_comment, name='delete_comment'),
]
