"""
Custom filters for the Book model to enable advanced filtering capabilities.
"""
import django_filters
from .models import Book

class BookFilter(django_filters.FilterSet):
    """
    FilterSet for Book model that provides comprehensive filtering options.
    Includes filtering by title, author, and publication_year as required.
    """
    
    # Filter by publication_year (exact match)
    publication_year = django_filters.NumberFilter(
        field_name='publication_year',
        lookup_expr='exact',
        help_text="Filter by exact publication year"
    )
    
    # Filter by title (case-insensitive contains)
    title = django_filters.CharFilter(
        field_name='title',
        lookup_expr='icontains', 
        help_text="Filter by title (case-insensitive contains)"
    )
    
    # Filter by author name (case-insensitive contains)
    author = django_filters.CharFilter(
        field_name='author__name',
        lookup_expr='icontains',
        help_text="Filter by author name (case-insensitive contains)"
    )
    
    # Additional useful filters
    publication_year_min = django_filters.NumberFilter(
        field_name='publication_year', 
        lookup_expr='gte',
        help_text="Filter books published after or in this year"
    )
    
    publication_year_max = django_filters.NumberFilter(
        field_name='publication_year',
        lookup_expr='lte', 
        help_text="Filter books published before or in this year"
    )
    
    class Meta:
        model = Book
        fields = [
            'publication_year',  # Required: filter by publication_year
            'title',             # Required: filter by title  
            'author',            # Required: filter by author
            'publication_year_min',
            'publication_year_max',
        ]
