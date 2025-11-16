from django import forms
from .models import Book
from django.core.exceptions import ValidationError
import re

class BookForm(forms.ModelForm):
    """
    TASK 2: Secure form with input validation and CSRF protection
    """
    
    class Meta:
        model = Book
        fields = ['title', 'author', 'description', 'published_date', 'isbn']
        widgets = {
            'published_date': forms.DateInput(attrs={'type': 'date'}),
            'description': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Enter book description...'}),
        }
    
    def clean_title(self):
        """TASK 2: XSS protection - validate and sanitize title"""
        title = self.cleaned_data.get('title', '').strip()
        
        # Check for potentially dangerous patterns
        dangerous_patterns = [
            r'<script.*?>.*?</script>',  # Script tags
            r'javascript:',              # JavaScript protocol
            r'on\w+\s*=',               # Event handlers
        ]
        
        for pattern in dangerous_patterns:
            if re.search(pattern, title, re.IGNORECASE):
                raise ValidationError('Invalid characters detected in title.')
        
        if len(title) < 2:
            raise ValidationError('Title must be at least 2 characters long.')
            
        return title
    
    def clean_author(self):
        """TASK 2: Input validation - author name"""
        author = self.cleaned_data.get('author', '').strip()
        
        if not re.match(r'^[A-Za-z\s\-\'\.]+$', author):
            raise ValidationError('Author name contains invalid characters.')
            
        return author
    
    def clean_isbn(self):
        """TASK 2: Input validation - ISBN format"""
        isbn = self.cleaned_data.get('isbn', '').strip()
        isbn = isbn.replace('-', '').replace(' ', '')
        
        if len(isbn) not in [10, 13]:
            raise ValidationError('ISBN must be 10 or 13 digits long.')
        
        if not isbn.isdigit():
            raise ValidationError('ISBN must contain only digits.')
            
        return isbn

class ExampleForm(forms.Form):
    """
    TASK 2: Example form for demonstration
    """
    name = forms.CharField(max_length=100, required=True)
    email = forms.EmailField(required=True)
    message = forms.CharField(widget=forms.Textarea(attrs={'rows': 4}))
    
    def clean_name(self):
        name = self.cleaned_data.get('name', '').strip()
        if len(name) < 2:
            raise ValidationError('Name must be at least 2 characters long.')
        return name
