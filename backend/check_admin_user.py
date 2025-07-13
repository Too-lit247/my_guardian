#!/usr/bin/env python
import os
import sys
import django

# Add the project directory to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'emergency_system.settings')
django.setup()

from accounts.models import User
from django.contrib.auth.hashers import make_password

def check_admin_users():
    """Check the status of system administrator users"""
    print("🔍 Checking System Administrator Users")
    print("=" * 50)
    
    # Get all system administrators
    admins = User.objects.filter(role='System Administrator')
    
    print(f"Found {admins.count()} System Administrator(s):")
    print()
    
    for i, admin in enumerate(admins, 1):
        print(f"👤 Admin {i}:")
        print(f"   Username: {admin.username}")
        print(f"   Email: {admin.email}")
        print(f"   Full Name: {admin.full_name}")
        print(f"   Password Set: {'✅ Yes' if admin.password else '❌ No (blank)'}")
        print(f"   Is Active: {'✅ Yes' if admin.is_active else '❌ No'}")
        print(f"   Is Staff: {'✅ Yes' if admin.is_staff else '❌ No'}")
        print(f"   Is Superuser: {'✅ Yes' if admin.is_superuser else '❌ No'}")
        print(f"   Can Login: {'✅ Yes' if admin.password and admin.is_active else '❌ No'}")
        print()
    
    # Check if any admin can actually login
    loginable_admins = admins.filter(password__isnull=False, is_active=True).exclude(password='')
    
    print(f"📊 Summary:")
    print(f"   Total Admins: {admins.count()}")
    print(f"   Can Login: {loginable_admins.count()}")
    
    if loginable_admins.count() == 0:
        print("\n⚠️  WARNING: No system administrators can login!")
        print("   You need to set a password for at least one admin user.")
        
        # Offer to create/fix an admin user
        print("\n🔧 Would you like to create a working admin user?")
        print("   Run: python create_admin_user.py")
    else:
        print("\n✅ At least one admin user can login successfully.")
    
    return admins

def create_working_admin():
    """Create or update an admin user with a working password"""
    print("\n🔧 Creating/Updating Admin User")
    print("=" * 40)
    
    # Try to get existing admin or create new one
    admin, created = User.objects.get_or_create(
        username='admin',
        defaults={
            'email': 'admin@myguardian.com',
            'full_name': 'System Administrator',
            'role': 'System Administrator',
            'department': 'admin',
            'is_active': True,
            'is_staff': True,
            'is_superuser': True,
        }
    )
    
    # Set a default password
    default_password = 'admin123'
    admin.password = make_password(default_password)
    admin.is_active = True
    admin.is_staff = True
    admin.is_superuser = True
    admin.save()
    
    if created:
        print(f"✅ Created new admin user: {admin.username}")
    else:
        print(f"✅ Updated existing admin user: {admin.username}")
    
    print(f"   Email: {admin.email}")
    print(f"   Password: {default_password}")
    print(f"   Status: Active and ready to login")
    
    print(f"\n🔐 Login Credentials:")
    print(f"   Username: {admin.username}")
    print(f"   Password: {default_password}")
    print(f"\n⚠️  IMPORTANT: Change this password after first login!")
    
    return admin

if __name__ == "__main__":
    admins = check_admin_users()
    
    # If no working admin, create one
    loginable_admins = admins.filter(password__isnull=False, is_active=True).exclude(password='')
    if loginable_admins.count() == 0:
        print("\n" + "=" * 50)
        create_working_admin()
