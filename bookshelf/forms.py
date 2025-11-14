from django import forms
from .models import Book
from django.core.exceptions import ValidationError
import re

class BookForm(forms.ModelForm):
    """
    Secure form with proper input validation and sanitization.
    Includes CSRF protection automatically.
    """
    
    class Meta:
        model = Book
        fields = ['title', 'author', 'description', 'published_date', 'isbn']
        widgets = {
            'published_date': forms.DateInput(attrs={'type': 'date'}),
            'description': forms.Textarea(attrs={'rows': 4}),
        }
    
    def clean_title(self):
        """Validate and sanitize title input."""
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
        """Validate author name."""
        author = self.cleaned_data.get('author', '').strip()
        
        # Basic sanitization - allow only letters, spaces, and common punctuation
        if not re.match(r'^[A-Za-z\s\-\'\.]+$', author):
            raise ValidationError('Author name contains invalid characters.')
            
        return author
    
    def clean_isbn(self):
        """Validate ISBN format."""
        isbn = self.cleaned_data.get('isbn', '').strip()
        
        # Remove any hyphens or spaces
        isbn = isbn.replace('-', '').replace(' ', '')
        
        # Validate ISBN length and format
        if len(isbn) not in [10, 13]:
            raise ValidationError('ISBN must be 10 or 13 digits long.')
        
        if not isbn.isdigit():
            raise ValidationError('ISBN must contain only digits.')
            
        return isbn
