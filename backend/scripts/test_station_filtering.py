#!/usr/bin/env python
"""
Script to test station-based alert filtering for different user roles
"""
import os
import sys
import django
import requests
import json

# Add the parent directory to the path so we can import Django modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'emergency_system.settings')
django.setup()

from accounts.models import User
from geography.models import Station
from alerts.models import Alert

def test_station_filtering():
    """Test that station-based filtering works correctly"""
    
    print("🔍 TESTING STATION-BASED ALERT FILTERING")
    print("=" * 60)
    
    # Get current alerts
    all_alerts = Alert.objects.all()
    print(f"📊 Total Alerts in System: {all_alerts.count()}")
    
    # Show alert assignments
    print("\n📋 ALERT ASSIGNMENTS:")
    print("-" * 40)
    
    for alert in all_alerts:
        print(f"🚨 {alert.title}")
        print(f"   🏢 Department: {alert.department}")
        print(f"   🎯 Priority: {alert.priority}")
        
        if alert.assigned_station_id:
            try:
                station = Station.objects.get(station_id=alert.assigned_station_id)
                print(f"   🏥 Assigned to: {station.name}")
                print(f"   📍 Station Location: {station.address}")
                
                if station.manager:
                    print(f"   👤 Station Manager: {station.manager.full_name}")
                
                # Find field officers at this station
                field_officers = User.objects.filter(
                    station_id=alert.assigned_station_id,
                    role='Field Officer'
                )
                
                if field_officers.exists():
                    print(f"   👮 Field Officers: {', '.join([fo.full_name for fo in field_officers])}")
                else:
                    print(f"   👮 Field Officers: None assigned")
                
            except Station.DoesNotExist:
                print(f"   ❌ Station not found: {alert.assigned_station_id}")
        else:
            print(f"   ⚠️ No station assigned")
        
        print()
    
    # Test different user roles
    print("\n🎭 TESTING DIFFERENT USER ROLES:")
    print("-" * 50)
    
    # Test Admin access
    admin_users = User.objects.filter(role='Admin')
    if admin_users.exists():
        admin = admin_users.first()
        print(f"👑 ADMIN USER: {admin.full_name}")
        print(f"   📧 Email: {admin.email}")
        print(f"   🏢 Department: {admin.department}")
        print(f"   📊 Should see: ALL alerts ({all_alerts.count()} alerts)")
        print()
    
    # Test Station Manager access
    station_managers = User.objects.filter(role='Station Manager')
    for manager in station_managers:
        print(f"👨‍💼 STATION MANAGER: {manager.full_name}")
        print(f"   📧 Email: {manager.email}")
        print(f"   🏢 Department: {manager.department}")
        print(f"   🏥 Station: {manager.station_id}")
        
        if manager.station_id:
            # Count alerts for this manager's station
            station_alerts = Alert.objects.filter(assigned_station_id=manager.station_id)
            dept_alerts = Alert.objects.filter(department=manager.department)
            
            print(f"   📊 Station Alerts: {station_alerts.count()}")
            print(f"   📊 Department Alerts: {dept_alerts.count()}")
            print(f"   📊 Should see: Station + Department alerts")
            
            if station_alerts.exists():
                print(f"   🚨 Station Alert Examples:")
                for alert in station_alerts[:2]:
                    print(f"      • {alert.title} ({alert.priority})")
        else:
            print(f"   ⚠️ No station assigned")
        
        print()
    
    # Test Field Officer access
    field_officers = User.objects.filter(role='Field Officer')
    for officer in field_officers:
        print(f"👮 FIELD OFFICER: {officer.full_name}")
        print(f"   📧 Email: {officer.email}")
        print(f"   🏢 Department: {officer.department}")
        print(f"   🏥 Station: {officer.station_id}")
        
        if officer.station_id:
            # Count alerts for this officer's station
            station_alerts = Alert.objects.filter(assigned_station_id=officer.station_id)
            
            print(f"   📊 Should see: ONLY station alerts ({station_alerts.count()} alerts)")
            
            if station_alerts.exists():
                print(f"   🚨 Station Alert Examples:")
                for alert in station_alerts[:2]:
                    print(f"      • {alert.title} ({alert.priority})")
            else:
                print(f"   📊 No alerts assigned to their station")
        else:
            print(f"   ⚠️ No station assigned - should see no alerts")
        
        print()

def test_api_filtering():
    """Test the API filtering by making actual requests"""
    
    print("🌐 TESTING API ALERT FILTERING")
    print("=" * 60)
    
    base_url = "http://localhost:8000"
    
    # Test different user logins
    test_users = [
        {"email": "thomhuwa066@gmail.com", "password": "test1234", "expected_role": "Admin"},
    ]
    
    for user_data in test_users:
        print(f"\n🔐 TESTING USER: {user_data['email']}")
        print("-" * 40)
        
        # Login
        login_response = requests.post(f"{base_url}/auth/login/", {
            "email": user_data["email"],
            "password": user_data["password"]
        })
        
        if login_response.status_code == 200:
            tokens = login_response.json()
            access_token = tokens.get("access")
            
            print(f"✅ Login successful")
            
            # Get user profile
            profile_response = requests.get(
                f"{base_url}/auth/profile/",
                headers={"Authorization": f"Bearer {access_token}"}
            )
            
            if profile_response.status_code == 200:
                profile = profile_response.json()
                print(f"👤 Role: {profile.get('role')}")
                print(f"🏢 Department: {profile.get('department')}")
                print(f"🏥 Station: {profile.get('station_id', 'None')}")
                
                # Get alerts
                alerts_response = requests.get(
                    f"{base_url}/alerts/",
                    headers={"Authorization": f"Bearer {access_token}"}
                )
                
                if alerts_response.status_code == 200:
                    alerts_data = alerts_response.json()
                    alerts = alerts_data.get('results', [])
                    
                    print(f"📊 API returned: {len(alerts)} alerts")
                    
                    if alerts:
                        print(f"🚨 Alert Examples:")
                        for alert in alerts[:3]:
                            print(f"   • {alert.get('title')} - {alert.get('department')} - {alert.get('priority')}")
                            if alert.get('assigned_station_id'):
                                print(f"     🏥 Assigned to station: {alert.get('assigned_station_id')}")
                    
                else:
                    print(f"❌ Failed to get alerts: {alerts_response.status_code}")
            
            else:
                print(f"❌ Failed to get profile: {profile_response.status_code}")
        
        else:
            print(f"❌ Login failed: {login_response.status_code}")

def main():
    """Main function"""
    
    print("🧪 STATION-BASED ALERT FILTERING TEST")
    print("=" * 70)
    print()
    
    # Test database filtering
    test_station_filtering()
    
    # Test API filtering
    test_api_filtering()
    
    print("\n✅ STATION FILTERING TEST COMPLETE")
    print("=" * 70)
    print()
    print("🎯 EXPECTED BEHAVIOR:")
    print("   👑 Admins: See ALL alerts")
    print("   👨‍💼 Station Managers: See station + department alerts")
    print("   👮 Field Officers: See ONLY their station's alerts")
    print()
    print("🌐 Frontend should automatically apply these filters")
    print("   based on the authenticated user's role and station")

if __name__ == '__main__':
    main()
