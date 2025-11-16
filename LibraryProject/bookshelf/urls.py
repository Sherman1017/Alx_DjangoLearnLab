from django.urls import path
from . import views

app_name = 'bookshelf'

urlpatterns = [
    path('', views.book_list, name='book_list'),
    path('add/', views.add_book, name='add_book'),
    path('<int:book_id>/', views.book_detail, name='book_detail'),
    # Educational endpoint (not for production)
    path('unsafe-search/', views.unsafe_search_example, name='unsafe_search_example'),
]
