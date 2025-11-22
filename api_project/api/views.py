from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Book

@api_view(['GET'])
def book_list(request):
    books = Book.objects.all()
    book_data = [
        {
            'id': book.id,
            'title': book.title,
            'author': book.author,
            'created_at': book.created_at,
        }
        for book in books
    ]
    return Response(book_data)
