#!/usr/bin/env python
"""
Script to fix station departments and create missing stations
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

from geography.models import Station

def fix_stations():
    """Fix station departments and create missing stations"""
    
    print("=== Fixing Station Departments ===\n")
    
    # Fix Police Station 1 department
    try:
        police_station = Station.objects.get(name="Police Station 1")
        print(f"Police Station 1 current department: {police_station.department}")
        police_station.department = "police"
        police_station.save()
        print(f"✓ Updated Police Station 1 department to: {police_station.department}")
    except Station.DoesNotExist:
        print("✗ Police Station 1 not found")
    except Exception as e:
        print(f"✗ Error updating Police Station 1: {e}")
    
    print("\n=== Creating Missing Stations ===\n")
    
    # Create additional stations for testing
    stations_to_create = [
        {
            'name': "Police Station 2",
            'code': "PS002",
            'department': "police",
            'region': "Central Region",
            'address': "456 Police Plaza, NYC",
            'latitude': Decimal('40.7550'),
            'longitude': Decimal('-73.9830'),
            'phone': "+1-555-POLICE2",
        },
        {
            'name': "Central Medical Station",
            'code': "MS001",
            'department': "medical",
            'region': "Central Region", 
            'address': "789 Hospital Ave, NYC",
            'latitude': Decimal('40.7560'),
            'longitude': Decimal('-73.9870'),
            'phone': "+1-555-MEDICAL1",
        },
        {
            'name': "Emergency Medical Center",
            'code': "MS002", 
            'department': "medical",
            'region': "Central Region",
            'address': "321 Emergency Blvd, NYC",
            'latitude': Decimal('40.7580'),
            'longitude': Decimal('-73.9820'),
            'phone': "+1-555-MEDICAL2",
        }
    ]
    
    for station_data in stations_to_create:
        try:
            station, created = Station.objects.get_or_create(
                name=station_data['name'],
                defaults={
                    **station_data,
                    'is_active': True
                }
            )
            if created:
                print(f"✓ Created: {station.name} ({station.department})")
            else:
                print(f"⚠ Already exists: {station.name} ({station.department})")
        except Exception as e:
            print(f"✗ Error creating {station_data['name']}: {e}")
    
    print("\n=== Station Summary ===\n")
    
    # Show all stations by department
    departments = ['fire', 'police', 'medical']
    
    for dept in departments:
        stations = Station.objects.filter(department=dept, is_active=True)
        print(f"{dept.title()} Department ({stations.count()} stations):")
        for station in stations:
            print(f"  - {station.name} at {station.latitude}, {station.longitude}")
        print()
    
    total_stations = Station.objects.filter(is_active=True).count()
    print(f"Total active stations: {total_stations}")

if __name__ == '__main__':
    fix_stations()
    print("Station fixes complete!")
