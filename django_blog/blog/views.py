from django.shortcuts import render
from django.db.models import Q

def home(request):
    return render(request, 'home.html')

def search(request):
    query = request.GET.get('q', '')
    # Using Q objects for search functionality
    return render(request, 'search.html', {'query': query})
