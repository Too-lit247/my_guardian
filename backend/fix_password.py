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

def fix_user_password():
    """Fix the password for strange@gmail.com"""
    print("🔧 Fixing Password for strange@gmail.com")
    print("=" * 50)
    
    email = 'strange@gmail.com'
    new_password = 'admin123'
    
    try:
        user = User.objects.get(email=email)
        print(f"✅ User found: {user.full_name}")
        print(f"   Current role: {user.role}")
        print(f"   Current department: {user.department}")
        
        # Set the new password
        user.set_password(new_password)
        user.save()
        
        print(f"✅ Password updated successfully!")
        print(f"   New password: {new_password}")
        
        # Verify the password works
        if user.check_password(new_password):
            print("✅ Password verification successful!")
        else:
            print("❌ Password verification failed!")
            
        print()
        print("🎉 Login credentials:")
        print(f"   Email: {email}")
        print(f"   Password: {new_password}")
        print()
        print("You can now log in to the web dashboard!")
        
    except User.DoesNotExist:
        print(f"❌ User with email {email} not found!")
    except Exception as e:
        print(f"❌ Error fixing password: {e}")

if __name__ == "__main__":
    fix_user_password()
