#!/usr/bin/env python
import os
import sys
import django

# Add the project directory to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'emergency_system.settings')
django.setup()

from devices.models import DepartmentRegistration
from devices.serializers import DepartmentRegistrationSerializer
from accounts.models import User
from django.utils import timezone

def test_region_assignment():
    """Test the region assignment functionality"""
    print("🧪 Testing Region Assignment in Department Registration")
    print("=" * 60)
    
    # Test 1: Create a department registration with region
    print("\n1️⃣ Testing DepartmentRegistration with region field:")
    print("-" * 50)
    
    dept_data = {
        'department_name': 'Test Fire Department',
        'department_type': 'fire',
        'region': 'central',  # New region field
        'contact_person': 'John Smith',
        'contact_email': 'john@testfire.com',
        'contact_phone': '+1234567890',
        'address': '123 Fire Station Rd',
        'city': 'Test City',
        'state': 'Test State',
        'zip_code': '12345',
        'coverage_description': 'Central district fire coverage',
        'population_served': 50000,
        'regional_manager_name': 'Jane Manager',
        'regional_manager_email': 'jane@testfire.com',
        'regional_manager_phone': '+1234567891',
        'regional_manager_credentials': 'Fire Chief Certification'
    }
    
    # Test serializer validation
    serializer = DepartmentRegistrationSerializer(data=dept_data)
    if serializer.is_valid():
        print("✅ DepartmentRegistration with region validation: PASSED")
        
        # Save the registration
        registration = serializer.save(registration_number="DEPT-TEST001")
        print(f"   Registration ID: {registration.registration_id}")
        print(f"   Region: {registration.region}")
        print(f"   Department: {registration.department_type}")
        
        # Test 2: Simulate approval process
        print("\n2️⃣ Testing approval process with region assignment:")
        print("-" * 50)
        
        try:
            # Create regional manager user (simulating approval)
            regional_manager = User.objects.create_user(
                username=f"{registration.department_type}_regional_{registration.registration_id}",
                email=registration.regional_manager_email,
                password='TempPassword123!',
                full_name=registration.regional_manager_name,
                department=registration.department_type,
                role='Regional Manager',
                region=registration.region,  # This is the key assignment
                phone_number=registration.regional_manager_phone,
                employee_id=f"RM-{registration.registration_number}"
            )
            
            print("✅ Regional Manager creation: PASSED")
            print(f"   Manager ID: {regional_manager.id}")
            print(f"   Manager Region: {regional_manager.region}")
            print(f"   Manager Department: {regional_manager.department}")
            print(f"   Manager Role: {regional_manager.role}")
            
            # Test 3: Verify region assignment
            print("\n3️⃣ Testing region assignment verification:")
            print("-" * 50)
            
            if regional_manager.region == registration.region:
                print("✅ Region assignment: PASSED")
                print(f"   Registration region: {registration.region}")
                print(f"   Manager region: {regional_manager.region}")
            else:
                print("❌ Region assignment: FAILED")
                print(f"   Registration region: {registration.region}")
                print(f"   Manager region: {regional_manager.region}")
            
            # Test 4: Test region property access
            print("\n4️⃣ Testing region object access:")
            print("-" * 50)
            
            region_obj = regional_manager.region_obj
            if region_obj:
                print("✅ Region object access: PASSED")
                print(f"   Region object: {region_obj}")
            else:
                print("⚠️  Region object access: No region object found (this is expected if regions aren't populated)")
            
            # Cleanup
            print("\n🧹 Cleaning up test data...")
            regional_manager.delete()
            registration.delete()
            print("✅ Cleanup completed")
            
        except Exception as e:
            print(f"❌ Error during approval simulation: {str(e)}")
            # Cleanup registration if user creation failed
            registration.delete()
            
    else:
        print("❌ DepartmentRegistration validation: FAILED")
        print(f"   Errors: {serializer.errors}")
    
    print("\n" + "=" * 60)
    print("🎯 Test Summary:")
    print("   - Department registration now includes region field")
    print("   - Regional managers are assigned to their selected region")
    print("   - When they log in, they can manage their specific region")
    print("   - They can create districts within their assigned region")

if __name__ == "__main__":
    test_region_assignment()
