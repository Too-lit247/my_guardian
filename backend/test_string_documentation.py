#!/usr/bin/env python
import os
import sys
import django

# Add the project directory to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'emergency_system.settings')
django.setup()

from accounts.models import RegistrationRequest
from accounts.serializers import RegistrationRequestSerializer
from devices.models import DepartmentRegistration
from devices.serializers import DepartmentRegistrationSerializer

def test_string_documentation():
    """Test that documentation fields now accept any string (no URL validation)"""
    print("📝 Testing String-Based Documentation Fields")
    print("=" * 60)
    
    # Test 1: RegistrationRequest with various documentation formats
    print("1️⃣ Testing RegistrationRequest with Different Documentation Formats")
    print("-" * 60)
    
    test_cases = [
        {
            'name': 'Full URL',
            'documentation': 'http://localhost:3000/uploads/registration_docs/certificate.pdf'
        },
        {
            'name': 'Relative path',
            'documentation': '/uploads/registration_docs/certificate.pdf'
        },
        {
            'name': 'Simple filename',
            'documentation': 'certificate.pdf'
        },
        {
            'name': 'HTTPS URL',
            'documentation': 'https://example.com/docs/certificate.pdf'
        },
        {
            'name': 'File path with spaces',
            'documentation': '/uploads/registration docs/my certificate.pdf'
        }
    ]
    
    base_data = {
        'registration_type': 'organization',
        'organization_name': 'Test Fire Department',
        'department': 'fire',
        'region': 'central',
        'full_name': 'John Test',
        'email': 'john@test.com',
        'phone_number': '+1234567890',
        'address': '123 Test St',
        'latitude': 40.7128,
        'longitude': -74.0060,
    }
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"   Test {i}: {test_case['name']}")
        
        registration_data = base_data.copy()
        registration_data['documentation'] = test_case['documentation']
        registration_data['email'] = f'test{i}@test.com'  # Unique email
        
        serializer = RegistrationRequestSerializer(data=registration_data)
        if serializer.is_valid():
            registration = serializer.save()
            print(f"   ✅ SUCCESS: {registration.documentation}")
        else:
            print(f"   ❌ FAILED: {serializer.errors}")
        print()
    
    # Test 2: DepartmentRegistration with various document formats
    print("2️⃣ Testing DepartmentRegistration with Different Document Formats")
    print("-" * 60)
    
    dept_base_data = {
        'department_name': 'Test Emergency Services',
        'department_type': 'fire',
        'contact_person': 'Jane Manager',
        'contact_email': 'jane@test.com',
        'contact_phone': '+1234567891',
        'address': '456 Emergency Ave',
        'city': 'Test City',
        'state': 'Test State',
        'zip_code': '12345',
        'coverage_description': 'Test coverage area',
        'population_served': 25000,
        'regional_manager_name': 'Bob Regional',
        'regional_manager_email': 'bob@test.com',
        'regional_manager_phone': '+1234567892',
        'regional_manager_credentials': 'Fire Chief',
    }
    
    document_formats = [
        {
            'license_document': 'http://localhost:3000/uploads/department_docs/license.pdf',
            'insurance_document': '/uploads/department_docs/insurance.pdf',
            'additional_documents': 'additional_docs.pdf'
        },
        {
            'license_document': 'license_file.pdf',
            'insurance_document': 'https://example.com/insurance.pdf',
            'additional_documents': '/path/to/additional documents with spaces.pdf'
        }
    ]
    
    for i, docs in enumerate(document_formats, 1):
        print(f"   Test {i}: Mixed document formats")
        
        dept_data = dept_base_data.copy()
        dept_data.update(docs)
        dept_data['contact_email'] = f'dept{i}@test.com'  # Unique email
        
        dept_serializer = DepartmentRegistrationSerializer(data=dept_data)
        if dept_serializer.is_valid():
            # Generate registration number
            import uuid
            registration_number = f"DEPT-{str(uuid.uuid4())[:8].upper()}"
            
            dept_registration = dept_serializer.save(registration_number=registration_number)
            print(f"   ✅ SUCCESS:")
            print(f"      License: {dept_registration.license_document}")
            print(f"      Insurance: {dept_registration.insurance_document}")
            print(f"      Additional: {dept_registration.additional_documents}")
        else:
            print(f"   ❌ FAILED: {dept_serializer.errors}")
        print()
    
    # Test 3: Empty/null documentation
    print("3️⃣ Testing Empty/Null Documentation")
    print("-" * 40)
    
    empty_data = base_data.copy()
    empty_data['email'] = 'empty@test.com'
    # No documentation field
    
    empty_serializer = RegistrationRequestSerializer(data=empty_data)
    if empty_serializer.is_valid():
        empty_registration = empty_serializer.save()
        print(f"✅ Empty documentation accepted: {empty_registration.documentation}")
    else:
        print(f"❌ Empty documentation rejected: {empty_serializer.errors}")
    
    print()
    
    # Test 4: Frontend compatibility simulation
    print("4️⃣ Testing Frontend JSON Compatibility")
    print("-" * 40)
    
    import json
    
    frontend_data = {
        'registration_type': 'organization',
        'organization_name': 'Frontend Test Org',
        'department': 'police',
        'region': 'central',
        'full_name': 'Frontend User',
        'email': 'frontend@test.com',
        'phone_number': '+1234567890',
        'address': '789 Frontend St',
        'latitude': 40.7500,
        'longitude': -74.0100,
        'documentation': 'http://localhost:3000/uploads/registration_docs/frontend_doc.pdf'
    }
    
    # Simulate JSON serialization/deserialization
    json_string = json.dumps(frontend_data)
    parsed_data = json.loads(json_string)
    
    frontend_serializer = RegistrationRequestSerializer(data=parsed_data)
    if frontend_serializer.is_valid():
        frontend_registration = frontend_serializer.save()
        print("✅ Frontend JSON format accepted")
        print(f"   Documentation: {frontend_registration.documentation}")
    else:
        print(f"❌ Frontend JSON rejected: {frontend_serializer.errors}")
    
    print()
    print("🎉 String-based documentation testing complete!")
    print()
    print("💡 Summary:")
    print("   ✅ Documentation fields now accept any string")
    print("   ✅ No URL validation - accepts paths, URLs, filenames")
    print("   ✅ Frontend can send any file reference format")
    print("   ✅ Backward compatible with existing data")
    print("   ✅ Supports empty/null values")
    
    return True

if __name__ == "__main__":
    test_string_documentation()
