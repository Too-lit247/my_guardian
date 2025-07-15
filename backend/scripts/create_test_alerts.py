#!/usr/bin/env python
"""
Script to create test alerts for testing location-based routing
"""
import os
import sys
import django
from decimal import Decimal
from datetime import datetime, timedelta
import random

# Add the parent directory to the path so we can import Django modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'emergency_system.settings')
django.setup()

from alerts.models import Alert
from accounts.models import User
from geography.models import Station

def create_test_alerts():
    """Create test alerts with various locations and types"""
    
    # Get admin user to create alerts
    try:
        admin_user = User.objects.get(username='admin')
    except User.DoesNotExist:
        print("Admin user not found. Please create an admin user first.")
        return
    
    # Get existing stations for reference
    stations = list(Station.objects.filter(is_active=True))
    if not stations:
        print("No active stations found. Please create stations first.")
        return
    
    print(f"Found {len(stations)} active stations")
    for station in stations:
        print(f"  - {station.name} ({station.department}) at {station.latitude}, {station.longitude}")
    
    # Test alert data with coordinates near stations
    test_alerts = [
        # Fire Department Alerts
        {
            'title': 'Building Fire at Downtown Office Complex',
            'alert_type': 'building_fire',
            'description': 'Large fire reported at 5-story office building. Multiple floors affected. Evacuation in progress.',
            'location': '123 Main Street, Downtown',
            'priority': 'high',
            'latitude': Decimal('40.7589'),  # Near NYC coordinates
            'longitude': Decimal('-73.9851'),
            'department': 'fire'
        },
        {
            'title': 'Gas Leak Emergency',
            'alert_type': 'gas_leak',
            'description': 'Natural gas leak reported near residential area. Strong odor detected by multiple residents.',
            'location': '456 Oak Avenue, Residential District',
            'priority': 'high',
            'latitude': Decimal('40.7505'),
            'longitude': Decimal('-73.9934'),
            'department': 'fire'
        },
        {
            'title': 'Wildfire Spreading Near Highway',
            'alert_type': 'wildfire',
            'description': 'Wildfire has jumped containment lines and is approaching Highway 101. Traffic being diverted.',
            'location': 'Highway 101, Mile Marker 45',
            'priority': 'high',
            'latitude': Decimal('40.7614'),
            'longitude': Decimal('-73.9776'),
            'department': 'fire'
        },
        
        # Police Department Alerts
        {
            'title': 'Armed Robbery in Progress',
            'alert_type': 'robbery',
            'description': 'Armed robbery reported at convenience store. Suspect still on scene. Multiple units requested.',
            'location': '789 Elm Street, Commercial District',
            'priority': 'high',
            'latitude': Decimal('40.7549'),
            'longitude': Decimal('-73.9840'),
            'department': 'police'
        },
        {
            'title': 'Domestic Dispute with Weapons',
            'alert_type': 'domestic_dispute',
            'description': 'Domestic violence call with reports of weapons involved. Neighbors report shouting and threats.',
            'location': '321 Pine Street, Apartment 4B',
            'priority': 'high',
            'latitude': Decimal('40.7580'),
            'longitude': Decimal('-73.9855'),
            'department': 'police'
        },
        {
            'title': 'Suspicious Activity at School',
            'alert_type': 'suspicious_activity',
            'description': 'Suspicious individual reported on school grounds after hours. Security cameras show person with large bag.',
            'location': 'Lincoln Elementary School, 555 School Lane',
            'priority': 'medium',
            'latitude': Decimal('40.7595'),
            'longitude': Decimal('-73.9820'),
            'department': 'police'
        },
        
        # Medical Department Alerts
        {
            'title': 'Multi-Vehicle Traffic Accident',
            'alert_type': 'traffic_accident',
            'description': '3-car collision on interstate. Multiple injuries reported. Traffic backed up for miles.',
            'location': 'Interstate 95, Northbound Mile 23',
            'priority': 'high',
            'latitude': Decimal('40.7570'),
            'longitude': Decimal('-73.9890'),
            'department': 'medical'
        },
        {
            'title': 'Heart Attack Emergency',
            'alert_type': 'heart_attack',
            'description': '65-year-old male experiencing chest pain and shortness of breath. Family requesting immediate assistance.',
            'location': '888 Maple Drive, Residential',
            'priority': 'high',
            'latitude': Decimal('40.7560'),
            'longitude': Decimal('-73.9870'),
            'department': 'medical'
        },
        {
            'title': 'Fall Injury at Construction Site',
            'alert_type': 'fall_injury',
            'description': 'Construction worker fell from scaffolding. Conscious but unable to move. Possible spinal injury.',
            'location': 'New Development Site, 999 Construction Blvd',
            'priority': 'high',
            'latitude': Decimal('40.7600'),
            'longitude': Decimal('-73.9800'),
            'department': 'medical'
        },
        
        # Additional alerts for testing
        {
            'title': 'Chemical Spill at Factory',
            'alert_type': 'hazmat_incident',
            'description': 'Unknown chemical spill at manufacturing facility. Workers evacuated. Hazmat team requested.',
            'location': 'Industrial Park, Building C',
            'priority': 'high',
            'latitude': Decimal('40.7520'),
            'longitude': Decimal('-73.9910'),
            'department': 'fire'
        }
    ]
    
    created_alerts = []
    
    for alert_data in test_alerts:
        try:
            # Create the alert
            alert = Alert.objects.create(
                title=alert_data['title'],
                alert_type=alert_data['alert_type'],
                description=alert_data['description'],
                location=alert_data['location'],
                priority=alert_data['priority'],
                latitude=alert_data['latitude'],
                longitude=alert_data['longitude'],
                department=alert_data['department'],
                status='active',
                created_by=admin_user
            )
            
            created_alerts.append(alert)
            print(f"✓ Created alert: {alert.title}")
            
        except Exception as e:
            print(f"✗ Failed to create alert '{alert_data['title']}': {e}")
    
    print(f"\nCreated {len(created_alerts)} test alerts successfully!")
    
    # Show summary by department
    departments = {}
    for alert in created_alerts:
        dept = alert.department
        if dept not in departments:
            departments[dept] = 0
        departments[dept] += 1
    
    print("\nAlerts by department:")
    for dept, count in departments.items():
        print(f"  {dept}: {count} alerts")
    
    return created_alerts

if __name__ == '__main__':
    print("Creating test alerts for location-based routing...")
    create_test_alerts()
    print("Done!")
