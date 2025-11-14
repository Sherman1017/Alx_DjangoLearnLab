from django.db import models
from django.conf import settings
from django.core.validators import MinLengthValidator, MaxLengthValidator

class Book(models.Model):
    """
    Secure book model with proper validation to prevent various attacks.
    """
    title = models.CharField(
        max_length=200,
        validators=[
            MinLengthValidator(2, "Title must be at least 2 characters long."),
            MaxLengthValidator(200, "Title cannot exceed 200 characters.")
        ],
        help_text="Enter the book title (2-200 characters)"
    )
    author = models.CharField(
        max_length=100,
        validators=[
            MinLengthValidator(2, "Author name must be at least 2 characters long."),
            MaxLengthValidator(100, "Author name cannot exceed 100 characters.")
        ]
    )
    description = models.TextField(
        max_length=1000,
        validators=[MaxLengthValidator(1000)],
        blank=True,
        help_text="Brief description of the book (max 1000 characters)"
    )
    published_date = models.DateField()
    isbn = models.CharField(
        max_length=13,
        validators=[MinLengthValidator(10)],
        unique=True,
        help_text="International Standard Book Number"
    )
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='books'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        permissions = [
            ("can_manage_books", "Can create, update, and delete books"),
        ]

    def __str__(self):
        return f"{self.title} by {self.author}"

    def clean(self):
        """
        Additional model-level validation to ensure data integrity.
        """
        from django.core.exceptions import ValidationError
        if self.title and len(self.title.strip()) < 2:
            raise ValidationError({'title': 'Title must be meaningful.'})
        if self.isbn and not self.isbn.isdigit():
            raise ValidationError({'isbn': 'ISBN should contain only digits.'})
