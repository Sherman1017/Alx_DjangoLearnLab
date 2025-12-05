#!/usr/bin/env python3
"""
Debug script to test serializer validation
"""

import os
import sys
import django

# Setup Django
sys.path.append('/Alx_DjangoLearnLab/advanced-api-project')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'advanced_api_project.settings')
django.setup()

from api.models import Author
from api.serializers import BookSerializer

print("🔧 DEBUGGING SERIALIZER VALIDATION")
print("=" * 50)

# Check available authors
authors = Author.objects.all()
print("Available authors:")
for author in authors:
    print(f"  ID: {author.id}, Name: {author.name}")

if not authors:
    print("❌ No authors found! This is likely the issue.")
    sys.exit(1)

# Test serializer with valid data
test_data = {
    "title": "Test Book Debug",
    "publication_year": 2020,
    "author": authors[0].id
}

print(f"\nTesting serializer with data: {test_data}")

serializer = BookSerializer(data=test_data)
if serializer.is_valid():
    print("✅ Serializer validation PASSED")
    print(f"Validated data: {serializer.validated_data}")
else:
    print("❌ Serializer validation FAILED")
    print(f"Errors: {serializer.errors}")

# Test with invalid data
invalid_data = {
    "title": "",  # Empty title
    "publication_year": 2030,  # Future year
    "author": 999  # Non-existent author
}

print(f"\nTesting with invalid data: {invalid_data}")
serializer = BookSerializer(data=invalid_data)
if not serializer.is_valid():
    print("✅ Serializer correctly rejected invalid data")
    print(f"Errors: {serializer.errors}")
