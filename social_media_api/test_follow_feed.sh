#!/bin/bash
echo "=== Testing Follow and Feed Functionality ==="

# Start server
echo "Starting Django server..."
python manage.py runserver &
SERVER_PID=$!
sleep 3

# Create test users if needed
echo -e "\n1. Creating test users..."
curl -X POST http://127.0.0.1:8000/api/auth/register/ \
  -H "Content-Type: application/json" \
  -d '{"username": "user1", "email": "user1@test.com", "password": "pass123", "password2": "pass123"}' \
  2>/dev/null | python -m json.tool

curl -X POST http://127.0.0.1:8000/api/auth/register/ \
  -H "Content-Type: application/json" \
  -d '{"username": "user2", "email": "user2@test.com", "password": "pass123", "password2": "pass123"}' \
  2>/dev/null | python -m json.tool

# Test endpoints
echo -e "\n2. Testing follow endpoints:"
echo "   Users list:"
curl -s http://127.0.0.1:8000/api/auth/users/ | python -m json.tool | head -20

echo -e "\n3. Testing feed (before following):"
echo "   Note: Should show message about not following anyone"
curl -s http://127.0.0.1:8000/api/feed/ | python -m json.tool | head -10

echo -e "\n4. Testing posts endpoints:"
curl -s http://127.0.0.1:8000/api/posts/ | python -m json.tool | head -10

# Stop server
echo -e "\nStopping server..."
kill $SERVER_PID 2>/dev/null
echo "Test completed!"
