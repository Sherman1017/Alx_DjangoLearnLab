import requests
import sys
import time

BASE_URL = "http://localhost:8000"

def test_endpoint(url, name):
    try:
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            print(f"✓ {name}: Accessible")
            return True
        else:
            print(f"✗ {name}: Status {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print(f"✗ {name}: Connection refused")
        return False
    except Exception as e:
        print(f"✗ {name}: Error - {e}")
        return False

def test_registration():
    print("\n=== Testing Registration ===")
    data = {
        'username': 'testuser_auth',
        'email': 'test_auth@example.com',
        'password1': 'TestAuthPass123',
        'password2': 'TestAuthPass123'
    }
    
    try:
        response = requests.post(f"{BASE_URL}/register/", data=data, timeout=5)
        if response.status_code == 200:
            if 'Account created' in response.text:
                print("✓ Registration: Success")
                return True
            else:
                print("✗ Registration: Failed - No success message")
                # Check for errors
                if 'error' in response.text.lower():
                    print("  Contains error messages")
                return False
        else:
            print(f"✗ Registration: Status {response.status_code}")
            return False
    except Exception as e:
        print(f"✗ Registration: Error - {e}")
        return False

def test_login():
    print("\n=== Testing Login ===")
    data = {
        'username': 'testuser_auth',
        'password': 'TestAuthPass123'
    }
    
    try:
        session = requests.Session()
        response = session.post(f"{BASE_URL}/login/", data=data, timeout=5)
        
        if response.status_code == 200:
            if 'Welcome' in response.text or 'home' in response.url:
                print("✓ Login: Success")
                return session
            else:
                print("✗ Login: Failed - Not redirected or no welcome")
                return None
        else:
            print(f"✗ Login: Status {response.status_code}")
            return None
    except Exception as e:
        print(f"✗ Login: Error - {e}")
        return None

def test_profile(session):
    print("\n=== Testing Profile Access ===")
    if not session:
        print("✗ Profile: No authenticated session")
        return False
    
    try:
        response = session.get(f"{BASE_URL}/profile/", timeout=5)
        if response.status_code == 200:
            if 'Your Profile' in response.text:
                print("✓ Profile: Accessible")
                return True
            else:
                print("✗ Profile: Wrong content")
                return False
        else:
            print(f"✗ Profile: Status {response.status_code}")
            return False
    except Exception as e:
        print(f"✗ Profile: Error - {e}")
        return False

def test_logout(session):
    print("\n=== Testing Logout ===")
    if not session:
        print("✗ Logout: No session")
        return False
    
    try:
        response = session.post(f"{BASE_URL}/logout/", timeout=5)
        if response.status_code == 200:
            if 'logged out' in response.text.lower():
                print("✓ Logout: Success")
                return True
            else:
                print("✗ Logout: No logout message")
                return False
        else:
            print(f"✗ Logout: Status {response.status_code}")
            return False
    except Exception as e:
        print(f"✗ Logout: Error - {e}")
        return False

def main():
    print("=== Django Blog Authentication System Test ===")
    
    # Test basic endpoints
    test_endpoint(f"{BASE_URL}/", "Home Page")
    test_endpoint(f"{BASE_URL}/register/", "Registration Page")
    test_endpoint(f"{BASE_URL}/login/", "Login Page")
    
    # Test authentication flow
    if test_registration():
        session = test_login()
        if session:
            test_profile(session)
            test_logout(session)
    
    print("\n=== Manual Testing Instructions ===")
    print("1. Open browser to: http://localhost:8000/")
    print("2. Click 'Register' to create account")
    print("3. Login with credentials")
    print("4. Access Profile page")
    print("5. Test logout")
    print("\nTest Credentials:")
    print("  Username: testuser_auth")
    print("  Password: TestAuthPass123")
    print("  Email: test_auth@example.com")

if __name__ == "__main__":
    main()
