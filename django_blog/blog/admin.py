from django.contrib import admin
from .models import Post, Comment
from taggit.models import Tag

# Unregister default Tag model from taggit
admin.site.unregister(Tag)

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'created_at', 'updated_at']
    list_filter = ['created_at', 'author', 'tags']
    search_fields = ['title', 'content']
    filter_horizontal = ['tags']

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['post', 'author', 'created_at', 'updated_at']
    list_filter = ['created_at', 'author', 'post']
    search_fields = ['content', 'author__username']
    readonly_fields = ['created_at', 'updated_at']
