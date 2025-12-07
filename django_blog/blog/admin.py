from django.contrib import admin
from .models import Post, Comment

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'created_at', 'updated_at']
    list_filter = ['created_at', 'author']
    search_fields = ['title', 'content']

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['post', 'author', 'content', 'created_at', 'updated_at']
    list_filter = ['created_at', 'author', 'post']
    search_fields = ['content', 'author__username']
    readonly_fields = ['created_at', 'updated_at']
