from django import forms
from django.core.exceptions import ValidationError
from .models import Comment

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
            # Remove extra whitespace
            content = content.strip()
            # Check minimum length
            if len(content) < 3:
                raise ValidationError('Comment must be at least 3 characters long.')
            # Check maximum length (optional)
            if len(content) > 1000:
                raise ValidationError('Comment cannot exceed 1000 characters.')
        return content
