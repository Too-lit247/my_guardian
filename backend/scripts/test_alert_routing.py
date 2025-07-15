#!/usr/bin/env python
"""
Script to test alert routing and station assignment
"""
import os
import sys
import django
from decimal import Decimal

# Add the parent directory to the path so we can import Django modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'emergency_system.settings')
django.setup()

from alerts.models import Alert
from alerts.services import StationFinderService
from geography.models import Station
from accounts.models import User

def test_alert_routing():
    """Test alert routing and station assignment"""
    
    print("=== Alert Routing Test ===\n")
    
    # Get all alerts
    alerts = Alert.objects.all().order_by('-created_at')
    stations = Station.objects.filter(is_active=True)
    
    print(f"Found {alerts.count()} alerts and {stations.count()} active stations\n")
    
    # Show station information
    print("Active Stations:")
    for station in stations:
        print(f"  - {station.name} ({station.department})")
        print(f"    Location: {station.latitude}, {station.longitude}")
        print(f"    Region: {station.region}")
        print()
    
    print("Alert Routing Analysis:")
    print("-" * 60)
    
    for alert in alerts:
        print(f"\nAlert: {alert.title}")
        print(f"Type: {alert.alert_type} | Department: {alert.department}")
        print(f"Location: {alert.location}")
        print(f"Coordinates: {alert.latitude}, {alert.longitude}")
        print(f"Priority: {alert.priority} | Status: {alert.status}")
        
        if alert.assigned_station_id:
            try:
                assigned_station = Station.objects.get(station_id=alert.assigned_station_id)
                print(f"✓ Assigned to: {assigned_station.name}")
                
                # Calculate distance
                if alert.latitude and alert.longitude and assigned_station.latitude and assigned_station.longitude:
                    distance = StationFinderService.calculate_distance(
                        float(alert.latitude), float(alert.longitude),
                        float(assigned_station.latitude), float(assigned_station.longitude)
                    )
                    print(f"  Distance: {distance:.2f} km")
                
            except Station.DoesNotExist:
                print(f"✗ Assigned to unknown station: {alert.assigned_station_id}")
        else:
            print("⚠ No station assigned")
            
            # Try to find nearest station
            if alert.latitude and alert.longitude:
                nearest_station = StationFinderService.find_nearest_station(
                    float(alert.latitude),
                    float(alert.longitude),
                    alert.department
                )
                
                if nearest_station:
                    distance = StationFinderService.calculate_distance(
                        float(alert.latitude), float(alert.longitude),
                        float(nearest_station.latitude), float(nearest_station.longitude)
                    )
                    print(f"  Nearest {alert.department} station: {nearest_station.name} ({distance:.2f} km)")
                else:
                    print(f"  No {alert.department} stations found nearby")
        
        print("-" * 40)
    
    # Test user access control
    print("\n=== User Access Control Test ===\n")
    
    users = User.objects.filter(is_active=True)
    
    for user in users:
        print(f"User: {user.full_name} ({user.role})")
        print(f"Department: {user.department}")
        print(f"Station: {user.station_id if user.station_id else 'None'}")
        
        # Simulate alert filtering logic
        if user.role == 'Admin':
            user_alerts = Alert.objects.all()
            print(f"Can see: ALL alerts ({user_alerts.count()} total)")
        elif user.role == 'Station Manager':
            if user.station_id:
                user_alerts = Alert.objects.filter(
                    assigned_station_id=user.station_id
                ).union(
                    Alert.objects.filter(department=user.department)
                )
            else:
                user_alerts = Alert.objects.filter(department=user.department)
            print(f"Can see: {user_alerts.count()} alerts (station + department)")
        elif user.role == 'Field Officer':
            if user.station_id:
                user_alerts = Alert.objects.filter(assigned_station_id=user.station_id)
            else:
                user_alerts = Alert.objects.filter(department=user.department)
            print(f"Can see: {user_alerts.count()} alerts (station only)")
        else:
            user_alerts = Alert.objects.none()
            print(f"Can see: 0 alerts (unknown role)")
        
        # Show specific alerts this user can see
        if user_alerts.exists():
            print("  Visible alerts:")
            for alert in user_alerts[:3]:  # Show first 3
                print(f"    - {alert.title} ({alert.department})")
            if user_alerts.count() > 3:
                print(f"    ... and {user_alerts.count() - 3} more")
        
        print()

def test_station_finder():
    """Test the station finder service"""
    
    print("\n=== Station Finder Service Test ===\n")
    
    # Test coordinates (NYC area)
    test_locations = [
        {'name': 'Downtown NYC', 'lat': 40.7589, 'lng': -73.9851},
        {'name': 'Brooklyn', 'lat': 40.6782, 'lng': -73.9442},
        {'name': 'Queens', 'lat': 40.7282, 'lng': -73.7949},
    ]
    
    departments = ['fire', 'police', 'medical']
    
    for location in test_locations:
        print(f"Testing location: {location['name']} ({location['lat']}, {location['lng']})")
        
        for dept in departments:
            nearest = StationFinderService.find_nearest_station(
                location['lat'], location['lng'], dept
            )
            
            if nearest:
                distance = StationFinderService.calculate_distance(
                    location['lat'], location['lng'],
                    float(nearest.latitude), float(nearest.longitude)
                )
                print(f"  {dept.title()}: {nearest.name} ({distance:.2f} km)")
            else:
                print(f"  {dept.title()}: No stations found")
        
        print()

if __name__ == '__main__':
    test_alert_routing()
    test_station_finder()
    print("Testing complete!")
