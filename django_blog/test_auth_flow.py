import requests
import time

BASE_URL = "http://localhost:8000"

print("Testing authentication system...")

# Test 1: Home page
print("\n1. Testing home page...")
try:
    response = requests.get(BASE_URL + "/", timeout=5)
    if response.status_code == 200:
        print("   ✅ Home page accessible")
        if "Welcome to Django Blog" in response.text:
            print("   ✅ Correct content displayed")
        else:
            print("   ⚠ Home page content issue")
    else:
        print(f"   ❌ Home page error: {response.status_code}")
except Exception as e:
    print(f"   ❌ Home page error: {e}")

# Test 2: Registration page
print("\n2. Testing registration page...")
try:
    response = requests.get(BASE_URL + "/register/", timeout=5)
    if response.status_code == 200:
        print("   ✅ Registration page accessible")
        if "Create New Account" in response.text:
            print("   ✅ Registration form present")
        else:
            print("   ⚠ Registration form missing")
    else:
        print(f"   ❌ Registration page error: {response.status_code}")
except Exception as e:
    print(f"   ❌ Registration page error: {e}")

# Test 3: Login page
print("\n3. Testing login page...")
try:
    response = requests.get(BASE_URL + "/login/", timeout=5)
    if response.status_code == 200:
        print("   ✅ Login page accessible")
        if "Login to Your Account" in response.text:
            print("   ✅ Login form present")
        else:
            print("   ⚠ Login form missing")
    else:
        print(f"   ❌ Login page error: {response.status_code}")
except Exception as e:
    print(f"   ❌ Login page error: {e}")

# Test 4: Profile page (should redirect when not logged in)
print("\n4. Testing profile page (unauthenticated)...")
try:
    response = requests.get(BASE_URL + "/profile/", timeout=5, allow_redirects=False)
    if response.status_code in [302, 301]:
        print("   ✅ Profile page redirects when not authenticated")
    else:
        print(f"   ⚠ Profile page returned {response.status_code} instead of redirect")
except Exception as e:
    print(f"   ❌ Profile page error: {e}")

print("\n=== Manual Testing Instructions ===")
print(f"1. Open browser to: {BASE_URL}/")
print(f"2. Register at: {BASE_URL}/register/")
print(f"3. Login at: {BASE_URL}/login/")
print(f"4. Test profile at: {BASE_URL}/profile/ (after login)")
print(f"\nTest credentials:")
print("  Username: testuser")
print("  Password: testpass123")
print("  Admin: admin/admin123")
