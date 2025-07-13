#!/usr/bin/env python
import os
import sys
import django
import json

# Add the project directory to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'emergency_system.settings')
django.setup()

from devices.models import DepartmentRegistration
from devices.serializers import DepartmentRegistrationSerializer
from accounts.models import RegistrationRequest
from accounts.serializers import RegistrationRequestSerializer

def test_department_registration():
    """Test department registration validation"""
    print("🧪 Testing Department Registration")
    print("=" * 60)
    
    # Test 1: Check required fields for DepartmentRegistration
    print("\n1️⃣ Testing DepartmentRegistration Model Fields:")
    print("-" * 50)
    
    # Get model fields
    dept_fields = DepartmentRegistration._meta.get_fields()
    required_fields = []
    optional_fields = []
    
    for field in dept_fields:
        if hasattr(field, 'blank') and hasattr(field, 'null'):
            if not field.blank and not field.null and not hasattr(field, 'default'):
                required_fields.append(field.name)
            else:
                optional_fields.append(field.name)
    
    print(f"📋 Required fields: {required_fields}")
    print(f"⚪ Optional fields: {optional_fields}")
    
    # Test 2: Test serializer validation
    print("\n2️⃣ Testing DepartmentRegistrationSerializer:")
    print("-" * 50)
    
    # Test with minimal data
    minimal_data = {
        'department_name': 'Test Fire Department',
        'department_type': 'fire',
        'contact_person': 'John Doe',
        'contact_email': 'john@testfire.com',
        'contact_phone': '+1234567890',
        'address': '123 Main St',
        'city': 'Test City',
        'state': 'Test State',
        'zip_code': '12345',
        'coverage_description': 'Test coverage area',
        'population_served': 50000,
        'regional_manager_name': 'Jane Manager',
        'regional_manager_email': 'jane@testfire.com',
        'regional_manager_phone': '+1234567891',
        'regional_manager_credentials': 'Fire Chief Certification'
    }
    
    print("Testing with minimal required data...")

    # Create a mock request object
    class MockRequest:
        pass

    mock_request = MockRequest()
    context = {'request': mock_request}

    serializer = DepartmentRegistrationSerializer(data=minimal_data, context=context)
    if serializer.is_valid():
        print("✅ Minimal data validation: PASSED")
        print(f"   Valid fields: {list(serializer.validated_data.keys())}")
    else:
        print("❌ Minimal data validation: FAILED")
        print(f"   Errors: {serializer.errors}")
    
    # Test 3: Test with missing required fields
    print("\n3️⃣ Testing Missing Required Fields:")
    print("-" * 50)
    
    test_cases = [
        ('department_name', 'Missing department name'),
        ('department_type', 'Missing department type'),
        ('contact_email', 'Missing contact email'),
        ('contact_person', 'Missing contact person'),
    ]
    
    for field, description in test_cases:
        test_data = minimal_data.copy()
        del test_data[field]
        
        serializer = DepartmentRegistrationSerializer(data=test_data)
        if not serializer.is_valid():
            print(f"✅ {description}: Correctly rejected")
            if field in serializer.errors:
                print(f"   Error: {serializer.errors[field]}")
        else:
            print(f"❌ {description}: Incorrectly accepted")
    
    # Test 4: Test RegistrationRequest (accounts app)
    print("\n4️⃣ Testing RegistrationRequest (accounts app):")
    print("-" * 50)
    
    reg_request_data = {
        'registration_type': 'organization',
        'organization_name': 'Test Emergency Services',
        'department': 'fire',
        'region': 'central',
        'full_name': 'John Doe',
        'email': 'john@test.com',
        'phone_number': '+1234567890',
        'address': '123 Test St, Test City, TS 12345',
        'latitude': 40.7128,
        'longitude': -74.0060
    }
    
    reg_serializer = RegistrationRequestSerializer(data=reg_request_data)
    if reg_serializer.is_valid():
        print("✅ RegistrationRequest validation: PASSED")
    else:
        print("❌ RegistrationRequest validation: FAILED")
        print(f"   Errors: {reg_serializer.errors}")
    
    # Test 5: Check existing registrations
    print("\n5️⃣ Checking Existing Data:")
    print("-" * 50)
    
    dept_count = DepartmentRegistration.objects.count()
    reg_count = RegistrationRequest.objects.count()
    
    print(f"📊 Existing DepartmentRegistrations: {dept_count}")
    print(f"📊 Existing RegistrationRequests: {reg_count}")
    
    if dept_count > 0:
        print("\n   Recent DepartmentRegistrations:")
        for dept in DepartmentRegistration.objects.all()[:3]:
            print(f"   - {dept.department_name} ({dept.status})")
    
    if reg_count > 0:
        print("\n   Recent RegistrationRequests:")
        for req in RegistrationRequest.objects.all()[:3]:
            print(f"   - {req.full_name} ({req.status})")
    
    # Test 6: API Endpoints
    print("\n6️⃣ API Endpoint Information:")
    print("-" * 50)
    
    print("📡 Department Registration Endpoints:")
    print("   POST /api/devices/departments/register/")
    print("   GET  /api/devices/departments/registrations/")
    print("   POST /api/devices/departments/registrations/<id>/approve/")
    
    print("\n📡 Account Registration Endpoints:")
    print("   POST /api/auth/registration-request/")
    print("   GET  /api/auth/registration-requests/")
    
    print("\n💡 Common 400 Error Causes:")
    print("   1. Missing required fields")
    print("   2. Invalid email format")
    print("   3. Invalid phone number format")
    print("   4. Invalid department_type choice")
    print("   5. File upload issues (if documents required)")
    print("   6. Invalid latitude/longitude values")
    
    return True

if __name__ == "__main__":
    test_department_registration()
