from django import forms
from django.core.exceptions import ValidationError
from .models import Comment, Post, Tag

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
    tag_names = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter tags separated by commas (e.g., django, python, web)'
        }),
        help_text='Separate tags with commas. New tags will be created automatically.'
    )
    
    class Meta:
        model = Post
        fields = ['title', 'content', 'tag_names']
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
    
    def clean_tag_names(self):
        tag_names = self.cleaned_data.get('tag_names', '')
        if tag_names:
            # Split by commas and clean up whitespace
            tag_list = [tag.strip() for tag in tag_names.split(',') if tag.strip()]
            # Remove duplicates
            tag_list = list(set(tag_list))
            return tag_list
        return []
    
    def save(self, commit=True):
        post = super().save(commit=False)
        if commit:
            post.save()
            
            # Process tags
            tag_names = self.cleaned_data.get('tag_names', [])
            post.tags.clear()
            
            for tag_name in tag_names:
                tag_name_lower = tag_name.lower().strip()
                # Create slug from tag name
                slug = tag_name_lower.replace(' ', '-')
                
                # Get or create tag
                tag, created = Tag.objects.get_or_create(
                    name=tag_name_lower,
                    defaults={'slug': slug}
                )
                post.tags.add(tag)
            
            self.save_m2m()
        
        return post
