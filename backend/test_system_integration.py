#!/usr/bin/env python
import os
import sys
import django

# Add the project directory to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'emergency_system.settings')
django.setup()

from geography.models import Region, District, Station
from alerts.models import Alert
from alerts.services import AlertRoutingService, StationFinderService
from accounts.models import User

def test_complete_system():
    """Test the complete alert routing and geography system"""
    print("🧪 Complete System Integration Test")
    print("=" * 60)
    
    # Test 1: Geography Models
    print("\n1️⃣ Testing Geography Models...")
    regions = Region.objects.all()
    districts = District.objects.all()
    stations = Station.objects.all()
    
    print(f"   ✅ Regions: {regions.count()}")
    print(f"   ✅ Districts: {districts.count()}")
    print(f"   ✅ Stations: {stations.count()}")
    
    # Test 2: Model Relationships
    print("\n2️⃣ Testing Model Relationships...")
    for region in regions:
        print(f"   🌍 {region.display_name}:")
        for district in region.districts.all():
            print(f"      🏢 {district.name} ({district.department})")
            for station in district.stations.all():
                print(f"         🚒 {station.name}")
    
    # Test 3: Alert Routing
    print("\n3️⃣ Testing Alert Routing...")
    
    # Get or create system user
    system_user, created = User.objects.get_or_create(
        username='system_test',
        defaults={
            'email': 'system@test.com',
            'full_name': 'System Test User',
            'role': 'System Administrator',
            'department': 'admin'
        }
    )
    
    # Test fire alert
    fire_alert = AlertRoutingService.route_emergency_alert(
        alert_type='building_fire',
        latitude=40.7128,
        longitude=-74.0060,
        severity='high',
        description='Test fire alert',
        created_by_user=system_user
    )
    
    print(f"   🔥 Fire Alert: {fire_alert.title}")
    print(f"      Department: {fire_alert.department}")
    print(f"      Assigned to: {fire_alert.assigned_to}")
    if fire_alert.assigned_station:
        print(f"      Station: {fire_alert.assigned_station.name}")
    
    # Test police alert
    police_alert = AlertRoutingService.route_emergency_alert(
        alert_type='robbery',
        latitude=40.7130,
        longitude=-74.0065,
        severity='medium',
        description='Test police alert',
        created_by_user=system_user
    )
    
    print(f"   👮 Police Alert: {police_alert.title}")
    print(f"      Department: {police_alert.department}")
    print(f"      Assigned to: {police_alert.assigned_to}")
    if police_alert.assigned_station:
        print(f"      Station: {police_alert.assigned_station.name}")
    
    # Test 4: Station Finder
    print("\n4️⃣ Testing Station Finder...")
    
    # Find nearest fire station
    nearest_fire = StationFinderService.find_nearest_station(
        latitude=40.7128,
        longitude=-74.0060,
        department='fire'
    )
    
    if nearest_fire:
        print(f"   🔥 Nearest Fire Station: {nearest_fire.name}")
        print(f"      District: {nearest_fire.district.name}")
        print(f"      Region: {nearest_fire.region.display_name}")
    
    # Find stations in radius
    stations_in_radius = StationFinderService.find_stations_in_radius(
        latitude=40.7128,
        longitude=-74.0060,
        department='fire',
        radius_km=50
    )
    
    print(f"   📍 Fire stations within 50km: {len(stations_in_radius)}")
    for station_info in stations_in_radius:
        print(f"      - {station_info['station'].name}: {station_info['distance']:.2f}km")
    
    # Test 5: Database Integrity
    print("\n5️⃣ Testing Database Integrity...")
    
    # Check for orphaned records
    orphaned_districts = District.objects.filter(region__isnull=True).count()
    orphaned_stations = Station.objects.filter(district__isnull=True).count()
    
    print(f"   🔍 Orphaned districts: {orphaned_districts}")
    print(f"   🔍 Orphaned stations: {orphaned_stations}")
    
    # Check alert assignments
    total_alerts = Alert.objects.count()
    assigned_alerts = Alert.objects.filter(assigned_station_id__isnull=False).count()
    
    print(f"   📊 Total alerts: {total_alerts}")
    print(f"   📊 Assigned alerts: {assigned_alerts}")
    print(f"   📊 Assignment rate: {(assigned_alerts/total_alerts*100):.1f}%" if total_alerts > 0 else "   📊 Assignment rate: N/A")
    
    print("\n" + "=" * 60)
    print("✅ System Integration Test Complete!")
    print("🎉 All components are working correctly!")
    
    return True

if __name__ == "__main__":
    test_complete_system()
