#!/usr/bin/env python
import os
import sys
import django

# Add the project directory to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'emergency_system.settings')
django.setup()

from accounts.models import User, RegistrationRequest
from devices.models import DepartmentRegistration

def check_user_login_issue():
    """Check the user login issue for strange@gmail.com"""
    print("🔍 Investigating Login Issue for strange@gmail.com")
    print("=" * 60)
    
    email = 'strange@gmail.com'
    
    # Check if user exists
    print("1️⃣ Checking User Account")
    print("-" * 30)
    
    user = User.objects.filter(email=email).first()
    if user:
        print(f"✅ User found!")
        print(f"   Username: {user.username}")
        print(f"   Email: {user.email}")
        print(f"   Full Name: {user.full_name}")
        print(f"   Role: {user.role}")
        print(f"   Department: {user.department}")
        print(f"   Is Active: {user.is_active}")
        print(f"   Date Joined: {user.date_joined}")
        print(f"   Last Login: {user.last_login}")
        print(f"   Has Usable Password: {user.has_usable_password()}")
        
        # Check password
        print(f"\n2️⃣ Testing Passwords")
        print("-" * 30)
        
        passwords_to_test = [
            'admin123',
            'TempPassword123!',
            'password',
            'admin',
            '123456'
        ]
        
        for pwd in passwords_to_test:
            is_valid = user.check_password(pwd)
            print(f"   Password '{pwd}': {'✅ VALID' if is_valid else '❌ Invalid'}")
            
    else:
        print("❌ User not found!")
    
    print()
    
    # Check registration requests
    print("3️⃣ Checking Registration Requests")
    print("-" * 30)
    
    reg_requests = RegistrationRequest.objects.filter(email=email)
    if reg_requests.exists():
        for req in reg_requests:
            print(f"   Registration ID: {req.request_id}")
            print(f"   Type: {req.registration_type}")
            print(f"   Status: {req.status}")
            print(f"   Organization: {req.organization_name}")
            print(f"   Department: {req.department}")
            print(f"   Created: {req.created_at}")
            print()
    else:
        print("   No registration requests found")
    
    print()
    
    # Check department registrations
    print("4️⃣ Checking Department Registrations")
    print("-" * 30)
    
    dept_regs = DepartmentRegistration.objects.filter(regional_manager_email=email)
    if dept_regs.exists():
        for dept in dept_regs:
            print(f"   Registration ID: {dept.registration_id}")
            print(f"   Department: {dept.department_name}")
            print(f"   Status: {dept.status}")
            print(f"   Regional Manager: {dept.regional_manager_name}")
            print(f"   Created: {dept.created_at}")
            print(f"   Reviewed At: {dept.reviewed_at}")
            print()
    else:
        print("   No department registrations found")
    
    print()
    
    # Provide solution
    print("5️⃣ Solution")
    print("-" * 30)
    
    if user:
        if user.role == 'Regional Manager':
            print("   This user was created from department registration approval.")
            print("   The temporary password should be: TempPassword123!")
            print()
            print("   🔧 To fix the login issue:")
            print("   1. Try logging in with: TempPassword123!")
            print("   2. Or reset the password manually:")
            print(f"      user = User.objects.get(email='{email}')")
            print("      user.set_password('admin123')")
            print("      user.save()")
        else:
            print("   This user was created from registration request approval.")
            print("   A random temporary password was generated.")
            print()
            print("   🔧 To fix the login issue:")
            print("   1. Reset the password manually:")
            print(f"      user = User.objects.get(email='{email}')")
            print("      user.set_password('admin123')")
            print("      user.save()")
    
    return user

if __name__ == "__main__":
    check_user_login_issue()
