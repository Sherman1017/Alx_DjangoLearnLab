#!/bin/bash

echo "=== Testing Django Blog Authentication System ==="
echo ""

cd /Alx_DjangoLearnLab/django_blog

# Check if server is running
if ! curl -s http://localhost:8000/ > /dev/null 2>&1; then
    echo "Starting Django server..."
    python3 manage.py runserver 0.0.0.0:8000 > /tmp/django.log 2>&1 &
    SERVER_PID=$!
    sleep 5
fi

echo "1. Testing Home Page (Unauthenticated)..."
curl -s http://localhost:8000/ | grep -q "Login" && echo "✓ Login link present" || echo "✗ Login link missing"

echo -e "\n2. Testing Registration Page..."
curl -s http://localhost:8000/register/ | grep -q "Create New Account" && echo "✓ Registration page accessible" || echo "✗ Registration page inaccessible"

echo -e "\n3. Testing Login Page..."
curl -s http://localhost:8000/login/ | grep -q "Login to Your Account" && echo "✓ Login page accessible" || echo "✗ Login page inaccessible"

echo -e "\n4. Testing Registration (Create test user)..."
# Create a test user via registration
REG_DATA="username=testuser&email=test@example.com&password1=TestPass123&password2=TestPass123"
curl -s -X POST http://localhost:8000/register/ \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "$REG_DATA" > /tmp/register_output.html

if grep -q "Account created" /tmp/register_output.html; then
    echo "✓ User registration successful"
else
    echo "✗ User registration failed"
    echo "  Checking for errors..."
    grep -o "error.*" /tmp/register_output.html | head -5
fi

echo -e "\n5. Testing Login with new user..."
# Login with the new user
LOGIN_DATA="username=testuser&password=TestPass123"
curl -s -X POST http://localhost:8000/login/ \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "$LOGIN_DATA" \
  -c /tmp/cookies.txt > /tmp/login_output.html

if grep -q "Welcome" /tmp/login_output.html; then
    echo "✓ Login successful"
    # Extract session cookie
    SESSION_COOKIE=$(grep sessionid /tmp/cookies.txt | awk '{print $7}')
    echo "  Session cookie obtained"
else
    echo "✗ Login failed"
fi

echo -e "\n6. Testing Profile Page (Authenticated)..."
if [ -n "$SESSION_COOKIE" ]; then
    curl -s http://localhost:8000/profile/ \
      -b "sessionid=$SESSION_COOKIE" | grep -q "Your Profile" && echo "✓ Profile page accessible" || echo "✗ Profile page inaccessible"
else
    echo "⚠ Cannot test profile without authentication"
fi

echo -e "\n7. Testing Profile Update..."
if [ -n "$SESSION_COOKIE" ]; then
    UPDATE_DATA="username=testuser&email=updated@example.com&bio=This+is+my+new+bio"
    curl -s -X POST http://localhost:8000/profile/ \
      -H "Content-Type: application/x-www-form-urlencoded" \
      -b "sessionid=$SESSION_COOKIE" \
      -d "$UPDATE_DATA" > /tmp/profile_update.html
    
    if grep -q "profile has been updated" /tmp/profile_update.html; then
        echo "✓ Profile update successful"
    else
        echo "✗ Profile update failed"
    fi
fi

echo -e "\n8. Testing Logout..."
if [ -n "$SESSION_COOKIE" ]; then
    curl -s -X POST http://localhost:8000/logout/ \
      -b "sessionid=$SESSION_COOKIE" > /tmp/logout.html
    
    if grep -q "logged out" /tmp/logout.html; then
        echo "✓ Logout successful"
    else
        echo "✗ Logout failed"
    fi
fi

echo -e "\n9. Testing Protected Pages After Logout..."
curl -s http://localhost:8000/profile/ | grep -q "login" && echo "✓ Profile page redirects to login when not authenticated" || echo "✗ Profile page doesn't redirect"

echo -e "\n10. Creating Superuser for Admin Testing..."
echo "from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.create_superuser('admin', 'admin@example.com', 'admin123')" | python3 manage.py shell
echo "✓ Superuser created: admin/admin123"

echo -e "\n=== Authentication System Test Complete ==="
echo ""
echo "Manual Testing URLs:"
echo "  Home: http://localhost:8000/"
echo "  Register: http://localhost:8000/register/"
echo "  Login: http://localhost:8000/login/"
echo "  Profile: http://localhost:8000/profile/ (requires login)"
echo "  Admin: http://localhost:8000/admin/ (admin/admin123)"
echo ""
echo "Test Credentials:"
echo "  Regular user: testuser/TestPass123"
echo "  Admin: admin/admin123"

# Clean up
rm -f /tmp/*.html /tmp/cookies.txt 2>/dev/null

# Stop server if we started it
if [ -n "$SERVER_PID" ]; then
    kill $SERVER_PID 2>/dev/null
fi
