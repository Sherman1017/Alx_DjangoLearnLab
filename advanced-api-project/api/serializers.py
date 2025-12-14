from rest_framework import serializers
from .models import Author, Book
from datetime import datetime

class BookSerializer(serializers.ModelSerializer):
    """
    BookSerializer for serializing Book model instances.
    
    Handles:
    - All fields from Book model (id, title, publication_year, author)
    - Custom validation for publication_year to ensure it's not in the future
    - Read-only id field for created instances
    
    Validation:
    - publication_year cannot be greater than current year
    """
    
    class Meta:
        model = Book
        fields = ['id', 'title', 'publication_year', 'author']
        read_only_fields = ['id']
    
    def validate_publication_year(self, value):
        """
        Custom validation for publication_year field.
        
        Ensures that the publication year is not in the future.
        
        Args:
            value (int): The publication year to validate
            
        Returns:
            int: The validated publication year
            
        Raises:
            serializers.ValidationError: If publication year is in the future
        """
        current_year = datetime.now().year
        if value > current_year:
            raise serializers.ValidationError(
                f"Publication year cannot be in the future. Current year is {current_year}."
            )
        return value


class AuthorSerializer(serializers.ModelSerializer):
    """
    AuthorSerializer for serializing Author model instances with nested books.
    
    Handles:
    - name field from Author model
    - Nested BookSerializer for related books
    - Dynamic inclusion of related books using BookSerializer
    
    Features:
    - books field uses BookSerializer to serialize related Book objects
    - books are read-only in this serializer (use BookSerializer for creation)
    - Provides complete author information including their books
    """
    
    # Nested serializer for related books
    books = BookSerializer(many=True, read_only=True)
    
    class Meta:
        model = Author
        fields = ['id', 'name', 'books']
        read_only_fields = ['id', 'books']
    
    def to_representation(self, instance):
        """
        Custom representation to handle nested book data.
        
        This method ensures that when an Author instance is serialized,
        all related books are included in the output using BookSerializer.
        
        Args:
            instance (Author): The Author instance to serialize
            
        Returns:
            dict: Serialized author data with nested books
        """
        representation = super().to_representation(instance)
        # The books field is automatically handled by the nested serializer
        return representation
