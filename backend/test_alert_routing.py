#!/usr/bin/env python
"""
Test script to demonstrate alert routing to nearest stations
"""
import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'emergency_system.settings')
django.setup()

from alerts.services import StationFinderService, AlertRoutingService
from alerts.models import Alert
from geography.models import Region, District, Station
from accounts.models import User


def create_sample_data():
    """Create sample regions, districts, and stations for testing"""
    print("Creating sample data...")
    
    # Create regions
    central_region, _ = Region.objects.get_or_create(
        name='central',
        defaults={
            'display_name': 'Central Region',
            'description': 'Central metropolitan area'
        }
    )
    
    # Create a fire district
    fire_district, _ = District.objects.get_or_create(
        name='Central Fire District',
        code='CFD001',
        department='fire',
        region=central_region,
        defaults={
            'address': '123 Fire Station Rd',
            'city': 'Central City',
            'state': 'State',
            'zip_code': '12345',
            'latitude': 40.7128,  # NYC coordinates as example
            'longitude': -74.0060,
            'description': 'Main fire district for central region'
        }
    )
    
    # Create fire stations
    station1, _ = Station.objects.get_or_create(
        name='Fire Station 1',
        code='FS001',
        district=fire_district,
        defaults={
            'station_type': 'headquarters',
            'address': '100 Main St',
            'city': 'Central City',
            'state': 'State',
            'zip_code': '12345',
            'latitude': 40.7128,
            'longitude': -74.0060,
            'description': 'Main fire station'
        }
    )
    
    station2, _ = Station.objects.get_or_create(
        name='Fire Station 2',
        code='FS002',
        district=fire_district,
        defaults={
            'station_type': 'substation',
            'address': '200 Oak Ave',
            'city': 'Central City',
            'state': 'State',
            'zip_code': '12346',
            'latitude': 40.7200,  # Slightly north
            'longitude': -74.0100,
            'description': 'North side fire station'
        }
    )
    
    # Create a police district
    police_district, _ = District.objects.get_or_create(
        name='Central Police District',
        code='CPD001',
        department='police',
        region=central_region,
        defaults={
            'address': '456 Police Plaza',
            'city': 'Central City',
            'state': 'State',
            'zip_code': '12345',
            'latitude': 40.7100,
            'longitude': -74.0080,
            'description': 'Main police district for central region'
        }
    )
    
    # Create police station
    police_station, _ = Station.objects.get_or_create(
        name='Police Station 1',
        code='PS001',
        district=police_district,
        defaults={
            'station_type': 'headquarters',
            'address': '300 Police Plaza',
            'city': 'Central City',
            'state': 'State',
            'zip_code': '12345',
            'latitude': 40.7100,
            'longitude': -74.0080,
            'description': 'Main police station'
        }
    )
    
    print(f"Created regions: {Region.objects.count()}")
    print(f"Created districts: {District.objects.count()}")
    print(f"Created stations: {Station.objects.count()}")
    
    return {
        'fire_stations': [station1, station2],
        'police_station': police_station
    }


def test_distance_calculation():
    """Test the distance calculation function"""
    print("\n=== Testing Distance Calculation ===")
    
    # Test distance between NYC and Brooklyn
    nyc_lat, nyc_lng = 40.7128, -74.0060
    brooklyn_lat, brooklyn_lng = 40.6782, -73.9442
    
    distance = StationFinderService.calculate_distance(
        nyc_lat, nyc_lng, brooklyn_lat, brooklyn_lng
    )
    
    print(f"Distance from NYC to Brooklyn: {distance:.2f} km")
    print("Expected: ~8-10 km")


def test_nearest_station_finder():
    """Test finding the nearest station"""
    print("\n=== Testing Nearest Station Finder ===")
    
    # Emergency location (slightly closer to Fire Station 2)
    emergency_lat, emergency_lng = 40.7180, -74.0090
    
    # Find nearest fire station
    nearest_fire = StationFinderService.find_nearest_station(
        emergency_lat, emergency_lng, 'fire'
    )
    
    if nearest_fire:
        distance = StationFinderService.calculate_distance(
            emergency_lat, emergency_lng,
            float(nearest_fire.latitude), float(nearest_fire.longitude)
        )
        print(f"Nearest fire station: {nearest_fire.name}")
        print(f"Distance: {distance:.2f} km")
        print(f"Address: {nearest_fire.address}")
    else:
        print("No fire station found")
    
    # Find nearest police station
    nearest_police = StationFinderService.find_nearest_station(
        emergency_lat, emergency_lng, 'police'
    )
    
    if nearest_police:
        distance = StationFinderService.calculate_distance(
            emergency_lat, emergency_lng,
            float(nearest_police.latitude), float(nearest_police.longitude)
        )
        print(f"Nearest police station: {nearest_police.name}")
        print(f"Distance: {distance:.2f} km")
        print(f"Address: {nearest_police.address}")
    else:
        print("No police station found")


def test_alert_routing():
    """Test the complete alert routing system"""
    print("\n=== Testing Alert Routing ===")
    
    # Get or create a system user
    system_user, _ = User.objects.get_or_create(
        username='system',
        defaults={
            'email': 'system@myguardian.com',
            'full_name': 'System Administrator',
            'role': 'System Administrator',
            'department': 'admin'
        }
    )
    
    # Test fire alert
    print("\n--- Fire Alert ---")
    fire_alert = AlertRoutingService.route_emergency_alert(
        alert_type='building_fire',
        latitude=40.7180,
        longitude=-74.0090,
        severity='high',
        description='Building fire reported at downtown location',
        created_by_user=system_user
    )
    
    print(f"Fire Alert ID: {fire_alert.id}")
    print(f"Department: {fire_alert.department}")
    print(f"Assigned to: {fire_alert.assigned_to}")
    if fire_alert.assigned_station:
        print(f"Assigned station: {fire_alert.assigned_station.name}")
    
    # Test police alert
    print("\n--- Police Alert ---")
    police_alert = AlertRoutingService.route_emergency_alert(
        alert_type='robbery',
        latitude=40.7150,
        longitude=-74.0070,
        severity='medium',
        description='Robbery in progress',
        created_by_user=system_user
    )
    
    print(f"Police Alert ID: {police_alert.id}")
    print(f"Department: {police_alert.department}")
    print(f"Assigned to: {police_alert.assigned_to}")
    if police_alert.assigned_station:
        print(f"Assigned station: {police_alert.assigned_station.name}")
    
    # Test device trigger simulation
    print("\n--- Device Trigger Simulation ---")
    panic_alert = AlertRoutingService.route_emergency_alert(
        alert_type='panic_button',
        latitude=40.7200,
        longitude=-74.0100,
        severity='critical',
        description='Panic button pressed on device DEV001',
        created_by_user=system_user
    )
    
    print(f"Panic Alert ID: {panic_alert.id}")
    print(f"Department: {panic_alert.department}")
    print(f"Assigned to: {panic_alert.assigned_to}")
    if panic_alert.assigned_station:
        print(f"Assigned station: {panic_alert.assigned_station.name}")


def test_stations_in_radius():
    """Test finding all stations within a radius"""
    print("\n=== Testing Stations in Radius ===")
    
    # Location in central area
    search_lat, search_lng = 40.7150, -74.0070
    
    # Find all fire stations within 10km
    fire_stations = StationFinderService.find_stations_in_radius(
        search_lat, search_lng, 'fire', 10.0
    )
    
    print(f"Fire stations within 10km:")
    for station_info in fire_stations:
        station = station_info['station']
        distance = station_info['distance_km']
        print(f"  - {station.name}: {distance}km away")
    
    # Find all police stations within 10km
    police_stations = StationFinderService.find_stations_in_radius(
        search_lat, search_lng, 'police', 10.0
    )
    
    print(f"Police stations within 10km:")
    for station_info in police_stations:
        station = station_info['station']
        distance = station_info['distance_km']
        print(f"  - {station.name}: {distance}km away")


def main():
    """Run all tests"""
    print("🚨 MyGuardian+ Alert Routing System Test 🚨")
    print("=" * 50)
    
    try:
        # Create sample data
        sample_data = create_sample_data()
        
        # Run tests
        test_distance_calculation()
        test_nearest_station_finder()
        test_alert_routing()
        test_stations_in_radius()
        
        print("\n" + "=" * 50)
        print("✅ All tests completed successfully!")
        print("\nThe alert routing system will now:")
        print("1. Automatically determine department based on alert type")
        print("2. Find the nearest station of that department")
        print("3. Assign the alert to that station")
        print("4. Calculate and display the distance")
        
    except Exception as e:
        print(f"❌ Error during testing: {e}")
        import traceback
        traceback.print_exc()


if __name__ == '__main__':
    main()
