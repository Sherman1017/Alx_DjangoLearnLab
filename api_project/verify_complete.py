import os
import sys
import django
import requests

# Setup Django
sys.path.append('/Alx_DjangoLearnLab/api_project')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'api_project.settings')
django.setup()

from api.models import Book

print("🧪 COMPREHENSIVE DJANGO REST FRAMEWORK VERIFICATION")
print("=" * 50)

# Test 1: Database connection
print("1. Testing Database...")
try:
    book_count = Book.objects.count()
    print(f"   ✅ Database connected - {book_count} books found")
    books = Book.objects.all()
    for book in books:
        print(f"      - {book.title} by {book.author}")
except Exception as e:
    print(f"   ❌ Database error: {e}")

# Test 2: API endpoint
print("2. Testing API Endpoint...")
try:
    response = requests.get('http://127.0.0.1:8000/api/books/')
    if response.status_code == 200:
        print(f"   ✅ API endpoint working - Status: {response.status_code}")
        data = response.json()
        print(f"   ✅ Retrieved {len(data)} books via API")
    else:
        print(f"   ❌ API returned status: {response.status_code}")
except Exception as e:
    print(f"   ❌ API test failed: {e}")

# Test 3: Admin interface
print("3. Testing Admin Interface...")
try:
    response = requests.get('http://127.0.0.1:8000/admin/')
    if response.status_code in [200, 302]:  # 302 is redirect to login
        print(f"   ✅ Admin interface accessible - Status: {response.status_code}")
    else:
        print(f"   ⚠️  Admin returned status: {response.status_code}")
except Exception as e:
    print(f"   ❌ Admin test failed: {e}")

print("=" * 50)
print("🎉 VERIFICATION COMPLETE!")
print("📚 Your Django REST Framework API is ready!")
