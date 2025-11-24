from django.db import models

class Author(models.Model):
    """
    Author model representing a book author.
    
    Fields:
    - name: CharField - The full name of the author (max 100 characters)
    
    Relationships:
    - One-to-Many with Book model (an author can have multiple books)
    """
    name = models.CharField(max_length=100, help_text="Full name of the author")
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = "Author"
        verbose_name_plural = "Authors"


class Book(models.Model):
    """
    Book model representing a published book.
    
    Fields:
    - title: CharField - The title of the book (max 200 characters)
    - publication_year: IntegerField - The year the book was published
    - author: ForeignKey - Reference to the Author who wrote the book
    
    Relationships:
    - Many-to-One with Author model (each book has one author)
    """
    title = models.CharField(max_length=200, help_text="Title of the book")
    publication_year = models.IntegerField(help_text="Year the book was published")
    author = models.ForeignKey(
        Author, 
        on_delete=models.CASCADE, 
        related_name='books',
        help_text="Author who wrote this book"
    )
    
    def __str__(self):
        return f"{self.title} by {self.author.name}"
    
    class Meta:
        verbose_name = "Book"
        verbose_name_plural = "Books"
        # Ensure unique constraint for book title and author combination
        unique_together = ['title', 'author']
