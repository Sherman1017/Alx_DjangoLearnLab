from django import forms
from django.core.exceptions import ValidationError
from .models import Comment, Post
from taggit.models import Tag

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Write your comment here...'
            }),
        }
    
    def clean_content(self):
        content = self.cleaned_data.get('content')
        if content:
            content = content.strip()
            if len(content) < 3:
                raise ValidationError('Comment must be at least 3 characters long.')
            if len(content) > 1000:
                raise ValidationError('Comment cannot exceed 1000 characters.')
        return content

class PostForm(forms.ModelForm):
    tags = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter tags separated by commas (e.g., django, python, web)'
        }),
        help_text='Separate tags with commas'
    )
    
    class Meta:
        model = Post
        fields = ['title', 'content', 'tags']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter post title'
            }),
            'content': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 10,
                'placeholder': 'Write your post content here...'
            }),
        }
    
    def clean_tags(self):
        tags = self.cleaned_data.get('tags', '')
        if tags:
            # Split by commas and clean up whitespace
            tag_list = [tag.strip() for tag in tags.split(',') if tag.strip()]
            # Remove duplicates
            tag_list = list(set(tag_list))
            return tag_list
        return []
    
    def save(self, commit=True):
        post = super().save(commit=False)
        if commit:
            post.save()
            # Clear existing tags and add new ones
            post.tags.clear()
            for tag in self.cleaned_data['tags']:
                post.tags.add(tag)
            self.save_m2m()
        return post
