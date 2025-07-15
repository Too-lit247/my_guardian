#!/usr/bin/env python
"""
Script to show available users for login
"""
import os
import sys
import django

# Add the parent directory to the path so we can import Django modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'emergency_system.settings')
django.setup()

from accounts.models import User

def show_users():
    """Show available users for login"""
    
    print("🔑 AVAILABLE USERS FOR LOGIN")
    print("=" * 50)
    
    users = User.objects.filter(is_active=True).order_by('role', 'full_name')
    
    for user in users:
        print(f"👤 {user.full_name}")
        print(f"   📧 Email: {user.email}")
        print(f"   🏢 Role: {user.role}")
        print(f"   🏥 Department: {user.department}")
        if user.station_id:
            print(f"   🏢 Station ID: {user.station_id}")
        print(f"   🔑 Password: test1234")
        print()
    
    print("🌐 LOGIN INSTRUCTIONS:")
    print("1. Open: http://localhost:3000")
    print("2. Use any email above with password: test1234")
    print("3. Navigate to: /dashboard/alerts")
    print()
    
    print("📊 ALERT VIEWING BY ROLE:")
    print("• Admin: Can see ALL alerts")
    print("• Station Manager: Can see station + department alerts")
    print("• Field Officer: Can see only their station's alerts")
    print()
    
    print("🔥 RECENT DOWA ALERTS:")
    print("The system has alerts from the Dowa fire emergency simulation")
    print("including fire, medical, and police response alerts.")

if __name__ == '__main__':
    show_users()
