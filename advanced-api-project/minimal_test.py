#!/usr/bin/env python3
"""
Minimal test to isolate the 400 error
"""

import requests
import json

BASE_URL = "http://127.0.0.1:8000/api"

# Get token first
token_r = requests.post(
    f"{BASE_URL}/auth-token/",
    json={'username': 'testuser', 'password': 'testpassword123'}
)
print(f"Token response: {token_r.status_code}")
if token_r.status_code == 200:
    token = token_r.json()['token']
    print(f"Token: {token[:20]}...")
else:
    print(f"Token error: {token_r.text}")
    exit(1)

# Get first author
authors_r = requests.get(f"{BASE_URL}/authors/")
print(f"Authors response: {authors_r.status_code}")
if authors_r.status_code == 200:
    authors = authors_r.json()
    if authors:
        author_id = authors[0]['id']
        print(f"Using author ID: {author_id}")
    else:
        print("No authors found!")
        exit(1)
else:
    print(f"Authors error: {authors_r.text}")
    exit(1)

# Test book creation with minimal data
test_data = {
    "title": "Simple Test Book",
    "publication_year": 2020,
    "author": author_id
}

print(f"\nTesting with data: {test_data}")

headers = {'Authorization': f'Token {token}'}
create_r = requests.post(
    f"{BASE_URL}/books/create/",
    json=test_data,
    headers=headers
)

print(f"Create response: {create_r.status_code}")
print(f"Response body: {create_r.text}")

if create_r.status_code == 201:
    print("✅ SUCCESS!")
elif create_r.status_code == 400:
    print("❌ 400 Bad Request - Validation error")
    try:
        errors = create_r.json()
        print(f"Errors: {errors}")
    except:
        print("Could not parse error response")
else:
    print(f"Unexpected status: {create_r.status_code}")
