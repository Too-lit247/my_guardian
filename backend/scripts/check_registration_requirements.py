import requests
import json

def check_registration_requirements():
    print("=== REGISTRATION ENDPOINT REQUIREMENTS ===\n")
    
    print("📋 REQUIRED FIELDS for /api/accounts/register/:")
    print("-" * 50)
    print("✅ REQUIRED - username (must be unique)")
    print("✅ REQUIRED - email (must be unique and valid)")
    print("✅ REQUIRED - full_name")
    print("✅ REQUIRED - password (must meet validation)")
    print("✅ REQUIRED - department")
    print("⚪ OPTIONAL - phone_number")
    
    print("\n" + "="*60)
    print("📝 DEPARTMENT CHOICES:")
    print("-" * 30)
    print("  • fire - Fire Department")
    print("  • police - Police Department") 
    print("  • medical - Medical Department")
    print("  • admin - System Administrator")
    
    print("\n" + "="*60)
    print("🔧 EXAMPLE REGISTRATION REQUEST:")
    print("-" * 40)
    
    example = {
        "username": "john_doe",
        "email": "john.doe@fire.gov.mw", 
        "full_name": "John Doe",
        "phone_number": "+265991234567",
        "password": "SecurePassword123!",
        "department": "fire"
    }
    
    print(json.dumps(example, indent=2))
    
    print("\n" + "="*60)
    print("⚠️  IMPORTANT NOTES:")
    print("-" * 25)
    print("• Users will be created as INACTIVE by default")
    print("• Admin approval required before login")
    print("• Role will be automatically set to 'Field User'")
    print("• Password must meet Django validation requirements")
    print("• Email must be unique")
    print("• Username must be unique")
    
    print("\n" + "="*60)
    print("🧪 TESTING REGISTRATION ENDPOINT:")
    print("-" * 40)
    
    # Test the endpoint
    url = "http://127.0.0.1:8000/api/auth/register/"
    
    test_data = {
        "username": "test_user_123",
        "email": "test123@example.com",
        "full_name": "Test User",
        "phone_number": "+265991234567",
        "password": "TestPassword123!",
        "department": "fire"
    }
    
    try:
        print(f"Making POST request to: {url}")
        print(f"With data: {json.dumps(test_data, indent=2)}")
        
        response = requests.post(url, json=test_data)
        
        print(f"\n📊 RESPONSE:")
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.text}")
        
        if response.status_code == 400:
            print("\n❌ BAD REQUEST - Check the error details above")
            try:
                error_data = response.json()
                print("Specific errors:")
                for field, errors in error_data.items():
                    print(f"  • {field}: {errors}")
            except:
                print("Could not parse error response")
                
        elif response.status_code == 201:
            print("\n✅ SUCCESS - User registered successfully")
            
        elif response.status_code == 500:
            print("\n🔥 SERVER ERROR - Check Django server logs")
            
    except requests.exceptions.ConnectionError:
        print("\n❌ CONNECTION ERROR")
        print("Make sure Django server is running:")
        print("cd backend && python manage.py runserver")
        
    except Exception as e:
        print(f"\n❌ ERROR: {e}")

if __name__ == "__main__":
    check_registration_requirements()

