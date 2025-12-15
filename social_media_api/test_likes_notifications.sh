#!/bin/bash
echo "=== Testing Likes and Notifications ==="

# Start server
echo "Starting Django server..."
python manage.py runserver &
SERVER_PID=$!
sleep 3

echo -e "\n1. Testing like endpoint:"
curl -X POST http://127.0.0.1:8000/api/posts/1/like/ 2>/dev/null | head -5

echo -e "\n2. Testing unlike endpoint:"
curl -X POST http://127.0.0.1:8000/api/posts/1/unlike/ 2>/dev/null | head -5

echo -e "\n3. Testing notifications endpoint:"
curl -s http://127.0.0.1:8000/api/notifications/ 2>/dev/null | head -5

echo -e "\n4. Testing mark all read:"
curl -X POST http://127.0.0.1:8000/api/notifications/mark-all-read/ 2>/dev/null | head -5

# Stop server
echo -e "\nStopping server..."
kill $SERVER_PID 2>/dev/null
echo "Test completed!"
