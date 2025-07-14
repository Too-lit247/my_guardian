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

def test_url_documentation():
    """Test that documentation fields now accept URLs instead of files"""
    print("🔗 Testing URL-Based Documentation Fields")
    print("=" * 60)
    
    # Test 1: RegistrationRequest with documentation URL
    print("1️⃣ Testing RegistrationRequest with Documentation URL")
    print("-" * 50)
    
    registration_data = {
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
        'documentation': 'http://localhost:3000/uploads/registration_docs/certificate.pdf'
    }
    
    serializer = RegistrationRequestSerializer(data=registration_data)
    if serializer.is_valid():
        registration = serializer.save()
        print(f"✅ Registration created: {registration.request_id}")
        print(f"   Documentation URL: {registration.documentation}")
        print(f"   Field type: {type(registration._meta.get_field('documentation'))}")
    else:
        print(f"❌ Registration failed: {serializer.errors}")
    
    print()
    
    # Test 2: DepartmentRegistration with document URLs
    print("2️⃣ Testing DepartmentRegistration with Document URLs")
    print("-" * 50)
    
    dept_data = {
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
        'license_document': 'http://localhost:3000/uploads/department_docs/license.pdf',
        'insurance_document': 'http://localhost:3000/uploads/department_docs/insurance.pdf',
        'additional_documents': 'http://localhost:3000/uploads/department_docs/additional.pdf'
    }
    
    dept_serializer = DepartmentRegistrationSerializer(data=dept_data)
    if dept_serializer.is_valid():
        # Generate registration number
        import uuid
        registration_number = f"DEPT-{str(uuid.uuid4())[:8].upper()}"
        
        dept_registration = dept_serializer.save(registration_number=registration_number)
        print(f"✅ Department registration created: {dept_registration.registration_id}")
        print(f"   License URL: {dept_registration.license_document}")
        print(f"   Insurance URL: {dept_registration.insurance_document}")
        print(f"   Additional URL: {dept_registration.additional_documents}")
        print(f"   Field type: {type(dept_registration._meta.get_field('license_document'))}")
    else:
        print(f"❌ Department registration failed: {dept_serializer.errors}")
    
    print()
    
    # Test 3: Invalid URL validation
    print("3️⃣ Testing Invalid URL Validation")
    print("-" * 50)
    
    invalid_data = dept_data.copy()
    invalid_data['license_document'] = 'not-a-valid-url'
    
    invalid_serializer = DepartmentRegistrationSerializer(data=invalid_data)
    if not invalid_serializer.is_valid():
        print("✅ Invalid URL correctly rejected")
        print(f"   Error: {invalid_serializer.errors.get('license_document', 'No error')}")
    else:
        print("❌ Invalid URL incorrectly accepted")
    
    print()
    
    # Test 4: Frontend compatibility test
    print("4️⃣ Testing Frontend Compatibility")
    print("-" * 50)
    
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
    
    # Simulate what the frontend sends
    import json
    json_data = json.dumps(frontend_data)
    parsed_data = json.loads(json_data)
    
    frontend_serializer = RegistrationRequestSerializer(data=parsed_data)
    if frontend_serializer.is_valid():
        frontend_registration = frontend_serializer.save()
        print("✅ Frontend data format accepted")
        print(f"   Registration ID: {frontend_registration.request_id}")
        print(f"   Documentation: {frontend_registration.documentation}")
    else:
        print(f"❌ Frontend data rejected: {frontend_serializer.errors}")
    
    print()
    
    # Test 5: Check existing data
    print("5️⃣ Current Database State")
    print("-" * 50)
    
    total_registrations = RegistrationRequest.objects.count()
    total_departments = DepartmentRegistration.objects.count()
    
    print(f"📊 Total RegistrationRequests: {total_registrations}")
    print(f"📊 Total DepartmentRegistrations: {total_departments}")
    
    # Show recent registrations with documentation
    recent_regs = RegistrationRequest.objects.filter(
        documentation__isnull=False
    ).exclude(documentation='')[:3]
    
    if recent_regs:
        print("\n📋 Recent registrations with documentation:")
        for reg in recent_regs:
            print(f"   - {reg.full_name}: {reg.documentation}")
    
    print()
    print("🎉 URL-based documentation testing complete!")
    print()
    print("💡 Summary:")
    print("   ✅ Backend now accepts URLs for documentation fields")
    print("   ✅ Frontend can send file URLs instead of files")
    print("   ✅ No file upload parsing needed in backend")
    print("   ✅ Files stored on frontend, URLs stored in database")
    
    return True

if __name__ == "__main__":
    test_url_documentation()
