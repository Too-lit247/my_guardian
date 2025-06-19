# Check if users exist and test login
from accounts.models import User
import requests
import json

print("=== CHECKING USERS IN DATABASE ===")

# Check if any users exist
users = User.objects.all()
print(f"Total users in database: {users.count()}")

if users.count() == 0:
    print("❌ No users found! Need to create sample data first.")
    print("Run: python manage.py shell < scripts/create_malawian_sample_data.py")
else:
    print("\n📋 Available users:")
    for user in users[:10]:  # Show first 10 users
        print(f"  - {user.username} | {user.full_name} | {user.department} | {user.role}")

# Check for specific test user
test_user = User.objects.filter(username='fire_regional_mw').first()
if test_user:
    print(f"\n✅ Test user found: {test_user.username}")
    print(f"   Full name: {test_user.full_name}")
    print(f"   Department: {test_user.department}")
    print(f"   Role: {test_user.role}")
    print(f"   Is active: {test_user.is_active}")
    
    # Test password
    if test_user.check_password('admin123'):
        print("   ✅ Password is correct")
    else:
        print("   ❌ Password is incorrect")
        # Reset password
        test_user.set_password('admin123')
        test_user.save()
        print("   🔧 Password reset to 'admin123'")
else:
    print("❌ Test user 'fire_regional_mw' not found")
    print("Creating test user...")
    
    # Create a simple test user
    test_user = User.objects.create_user(
        username='admin',
        email='admin@test.com',
        password='admin123',
        full_name='Test Admin',
        department='admin',
        role='System Administrator'
    )
    print(f"✅ Created test user: {test_user.username}")

print("\n=== TESTING LOGIN API ===")

# Test login with correct data
login_data = {
    "username": "admin",
    "password": "admin123",
    "department": "admin",
    "role": "System Administrator"
}

try:
    response = requests.post(
        'http://localhost:8000/api/auth/login/',
        headers={'Content-Type': 'application/json'},
        data=json.dumps(login_data)
    )
    print(f"Login test status: {response.status_code}")
    
    if response.status_code == 200:
        print("✅ Login successful!")
        data = response.json()
        print(f"Access token: {data.get('access', 'Not found')[:50]}...")
    else:
        print(f"❌ Login failed: {response.text}")
        
except Exception as e:
    print(f"❌ Login test error: {e}")

# Also test if fire_regional_mw exists and works
if User.objects.filter(username='fire_regional_mw').exists():
    fire_login_data = {
        "username": "fire_regional_mw",
        "password": "admin123",
        "department": "fire",
        "role": "Regional Manager"
    }
    
    try:
        response = requests.post(
            'http://localhost:8000/api/auth/login/',
            headers={'Content-Type': 'application/json'},
            data=json.dumps(fire_login_data)
        )
        print(f"\nFire regional login status: {response.status_code}")
        if response.status_code == 200:
            print("✅ Fire regional login successful!")
        else:
            print(f"❌ Fire regional login failed: {response.text}")
    except Exception as e:
        print(f"❌ Fire regional login error: {e}")
