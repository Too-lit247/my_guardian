import requests
import json

# Test the registration endpoint
def test_registration():
    url = "http://localhost:8000/api/accounts/register/"
    
    # Required fields for registration
    registration_data = {
        "username": "testuser123",
        "email": "testuser@example.com", 
        "full_name": "Test User",
        "phone_number": "+265991234567",  # Optional but good to include
        "password": "SecurePass123!",
        "department": "fire"  # Must be one of: fire, police, medical, admin
    }
    
    print("Testing registration endpoint...")
    print(f"URL: {url}")
    print(f"Data: {json.dumps(registration_data, indent=2)}")
    
    try:
        response = requests.post(url, json=registration_data)
        print(f"\nResponse Status: {response.status_code}")
        print(f"Response Headers: {dict(response.headers)}")
        print(f"Response Body: {response.text}")
        
        if response.status_code == 201:
            print("✅ Registration successful!")
        else:
            print("❌ Registration failed!")
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Request failed: {e}")

def test_registration_with_missing_fields():
    url = "http://localhost:8000/api/accounts/register/"
    
    # Test with missing required fields
    test_cases = [
        {
            "name": "Missing username",
            "data": {
                "email": "test@example.com",
                "full_name": "Test User",
                "password": "SecurePass123!",
                "department": "fire"
            }
        },
        {
            "name": "Missing email", 
            "data": {
                "username": "testuser",
                "full_name": "Test User",
                "password": "SecurePass123!",
                "department": "fire"
            }
        },
        {
            "name": "Missing department",
            "data": {
                "username": "testuser",
                "email": "test@example.com",
                "full_name": "Test User", 
                "password": "SecurePass123!"
            }
        },
        {
            "name": "Invalid department",
            "data": {
                "username": "testuser",
                "email": "test@example.com",
                "full_name": "Test User",
                "password": "SecurePass123!",
                "department": "invalid_dept"
            }
        }
    ]
    
    for test_case in test_cases:
        print(f"\n--- Testing: {test_case['name']} ---")
        try:
            response = requests.post(url, json=test_case['data'])
            print(f"Status: {response.status_code}")
            print(f"Response: {response.text}")
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    print("=== REGISTRATION ENDPOINT TESTING ===\n")
    
    # Test successful registration
    test_registration()
    
    print("\n" + "="*50)
    print("TESTING ERROR CASES")
    print("="*50)
    
    # Test error cases
    test_registration_with_missing_fields()
