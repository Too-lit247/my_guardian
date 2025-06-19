# Test script to verify backend routes are working
import requests
import json

# Test if backend is running
try:
    response = requests.get('http://localhost:8000/admin/')
    print(f"Backend status: {response.status_code}")
    if response.status_code == 200:
        print("✅ Backend is running")
    else:
        print("❌ Backend returned error")
except requests.exceptions.ConnectionError:
    print("❌ Backend is not running or not accessible")
    print("Make sure to run: python manage.py runserver")
    exit()

# Test auth endpoints
auth_endpoints = [
    '/api/auth/login/',
    '/api/auth/me/',
    '/api/auth/register/',
]

for endpoint in auth_endpoints:
    try:
        url = f'http://localhost:8000{endpoint}'
        response = requests.get(url)
        print(f"{endpoint}: {response.status_code}")
    except Exception as e:
        print(f"{endpoint}: ERROR - {e}")

# Test login with sample data
login_data = {
    "username": "fire_regional_mw",
    "password": "admin123",
    "department": "fire",
    "role": "Regional Manager"
}

try:
    response = requests.post(
        'http://localhost:8000/api/auth/login/',
        headers={'Content-Type': 'application/json'},
        data=json.dumps(login_data)
    )
    print(f"\nLogin test: {response.status_code}")
    print(f"Response: {response.text}")
except Exception as e:
    print(f"Login test failed: {e}")
