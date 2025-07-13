#!/usr/bin/env python
"""
Simple test to verify alert routing system functionality
"""
import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'emergency_system.settings')
django.setup()

def test_basic_functionality():
    """Test basic alert routing functionality"""
    print("🚨 Testing MyGuardian+ Alert Routing System")
    print("=" * 50)
    
    try:
        # Test 1: Import services
        print("✓ Testing imports...")
        from alerts.services import StationFinderService, AlertRoutingService
        from alerts.models import Alert
        print("✓ Services imported successfully")
        
        # Test 2: Distance calculation
        print("\n✓ Testing distance calculation...")
        distance = StationFinderService.calculate_distance(
            40.7128, -74.0060,  # NYC
            40.7589, -73.9851   # Times Square
        )
        print(f"✓ Distance NYC to Times Square: {distance:.2f} km")
        
        # Test 3: Alert type mapping
        print("\n✓ Testing alert type mapping...")
        mappings = [
            ('building_fire', 'fire'),
            ('panic_button', 'police'),
            ('heart_attack', 'medical'),
            ('gas_leak', 'fire'),
            ('robbery', 'police'),
            ('fall_detected', 'medical')
        ]
        
        for alert_type, expected_dept in mappings:
            actual_dept = Alert.get_department_for_alert_type(alert_type)
            status = "✓" if actual_dept == expected_dept else "✗"
            print(f"{status} {alert_type} -> {actual_dept} (expected: {expected_dept})")
        
        # Test 4: Check database connectivity
        print("\n✓ Testing database connectivity...")
        from django.db import connection
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
            result = cursor.fetchone()
            print(f"✓ Database connection successful: {result}")
        
        # Test 5: Check if geography models exist
        print("\n✓ Testing geography models...")
        from geography.models import Region, District, Station
        
        region_count = Region.objects.count()
        district_count = District.objects.count()
        station_count = Station.objects.count()
        
        print(f"✓ Regions in database: {region_count}")
        print(f"✓ Districts in database: {district_count}")
        print(f"✓ Stations in database: {station_count}")
        
        if station_count == 0:
            print("⚠️  No stations found - alert routing will not work until stations are created")
        
        # Test 6: Check alert model
        print("\n✓ Testing alert model...")
        alert_count = Alert.objects.count()
        print(f"✓ Alerts in database: {alert_count}")
        
        print("\n" + "=" * 50)
        print("✅ Basic functionality tests completed!")
        
        if station_count > 0:
            print("🎯 Alert routing system is ready to use!")
        else:
            print("📋 Next step: Create regions, districts, and stations with GPS coordinates")
            
    except Exception as e:
        print(f"❌ Error during testing: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    return True

def show_setup_instructions():
    """Show instructions for setting up the system"""
    print("\n📋 Setup Instructions:")
    print("=" * 30)
    print("1. Create regions:")
    print("   python manage.py populate_regions")
    print("\n2. Create sample districts and stations:")
    print("   python manage.py shell")
    print("   >>> from geography.models import *")
    print("   >>> # Create districts and stations with GPS coordinates")
    print("\n3. Test alert routing:")
    print("   python test_alert_routing.py")

if __name__ == '__main__':
    success = test_basic_functionality()
    if success:
        show_setup_instructions()
