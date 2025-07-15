#!/usr/bin/env python
"""
Script to create a test field officer and verify station-based filtering
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
from geography.models import Station
from alerts.models import Alert

def create_test_field_officer():
    """Create a test field officer assigned to a station with alerts"""
    
    print("👮 CREATING TEST FIELD OFFICER")
    print("=" * 50)
    
    # Find a station that has alerts assigned
    stations_with_alerts = []
    for station in Station.objects.all():
        alert_count = Alert.objects.filter(assigned_station_id=station.station_id).count()
        if alert_count > 0:
            stations_with_alerts.append((station, alert_count))
    
    if not stations_with_alerts:
        print("❌ No stations have alerts assigned")
        return None
    
    # Use the station with the most alerts
    test_station, alert_count = max(stations_with_alerts, key=lambda x: x[1])
    
    print(f"🏥 Selected Station: {test_station.name}")
    print(f"📍 Location: {test_station.address}")
    print(f"🚨 Assigned Alerts: {alert_count}")
    print(f"🆔 Station ID: {test_station.station_id}")
    print()
    
    # Create test field officer
    field_officer, created = User.objects.get_or_create(
        email='test.officer@station.com',
        defaults={
            'username': 'test_field_officer',
            'full_name': 'Test Field Officer',
            'role': 'Field Officer',
            'department': test_station.department,
            'station_id': test_station.station_id,
            'is_active': True,
            'password': 'pbkdf2_sha256$600000$test$hash'  # Dummy hash
        }
    )
    
    if created:
        print(f"✅ Created field officer: {field_officer.full_name}")
    else:
        print(f"📱 Using existing field officer: {field_officer.full_name}")
    
    print(f"📧 Email: {field_officer.email}")
    print(f"🏢 Department: {field_officer.department}")
    print(f"🏥 Station: {field_officer.station_id}")
    print(f"🔑 Password: test1234 (for testing)")
    
    # Update password to test1234 for easy testing
    field_officer.set_password('test1234')
    field_officer.save()
    
    return field_officer, test_station

def show_filtering_results(field_officer, station):
    """Show what alerts the field officer should see"""
    
    print(f"\n🔍 STATION FILTERING RESULTS")
    print("=" * 50)
    
    # Get all alerts
    all_alerts = Alert.objects.all()
    station_alerts = Alert.objects.filter(assigned_station_id=station.station_id)
    
    print(f"📊 Total Alerts in System: {all_alerts.count()}")
    print(f"📊 Station Alerts: {station_alerts.count()}")
    print()
    
    print(f"🎯 FIELD OFFICER SHOULD SEE:")
    print("-" * 30)
    
    if station_alerts.exists():
        for alert in station_alerts:
            print(f"✅ {alert.title}")
            print(f"   🎯 Priority: {alert.priority}")
            print(f"   🏢 Department: {alert.department}")
            print(f"   📍 Location: {alert.location}")
            print()
    else:
        print("❌ No alerts assigned to this station")
    
    print(f"🚫 FIELD OFFICER SHOULD NOT SEE:")
    print("-" * 30)
    
    other_alerts = Alert.objects.exclude(assigned_station_id=station.station_id)
    if other_alerts.exists():
        for alert in other_alerts[:3]:  # Show first 3
            print(f"❌ {alert.title}")
            print(f"   🏥 Assigned to different station")
            print()
        
        if other_alerts.count() > 3:
            print(f"   ... and {other_alerts.count() - 3} more alerts")
    else:
        print("✅ All alerts are assigned to this station")

def main():
    """Main function"""
    
    print("👮 FIELD OFFICER STATION FILTERING TEST")
    print("=" * 70)
    print()
    
    # Create test field officer
    field_officer, station = create_test_field_officer()
    
    if not field_officer:
        print("❌ Could not create test field officer")
        return
    
    # Show filtering results
    show_filtering_results(field_officer, station)
    
    print("\n🧪 TESTING INSTRUCTIONS:")
    print("=" * 50)
    print(f"1. Login as field officer:")
    print(f"   📧 Email: {field_officer.email}")
    print(f"   🔑 Password: test1234")
    print()
    print(f"2. Navigate to: http://localhost:3000/dashboard/alerts")
    print()
    print(f"3. Expected behavior:")
    print(f"   ✅ Should see ONLY {Alert.objects.filter(assigned_station_id=station.station_id).count()} alerts assigned to {station.name}")
    print(f"   ❌ Should NOT see alerts assigned to other stations")
    print(f"   📝 Page should show: 'Showing alerts for your station only'")
    print()
    print(f"4. Compare with admin view:")
    print(f"   👑 Admin sees: {Alert.objects.count()} total alerts")
    print(f"   👮 Field Officer sees: {Alert.objects.filter(assigned_station_id=station.station_id).count()} station alerts")

if __name__ == '__main__':
    main()
