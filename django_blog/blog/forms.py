from django import forms
from django.core.exceptions import ValidationError
from taggit.forms import TagWidget  # For tagging
from .models import Comment, Post

# CommentForm with validation as required
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={
                'rows': 3,
                'placeholder': 'Write your comment here...'
            }),
        }
    
    def clean_content(self):  # Validation rules
        content = self.cleaned_data.get('content')
        if content:
            content = content.strip()
            if len(content) < 3:
                raise ValidationError('Comment must be at least 3 characters long.')
        return content

# PostForm with TagWidget for tagging
class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content', 'tags']
        widgets = {
            'tags': TagWidget(),  # TagWidget() used here
        }
