#!/usr/bin/env python
"""
Script to assign unassigned alerts to their nearest stations
"""
import os
import sys
import django

# Add the parent directory to the path so we can import Django modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'emergency_system.settings')
django.setup()

from alerts.models import Alert
from alerts.services import StationFinderService

def assign_alerts_to_stations():
    """Assign unassigned alerts to their nearest stations"""
    
    print("=== Assigning Alerts to Stations ===\n")
    
    # Get all unassigned alerts
    unassigned_alerts = Alert.objects.filter(assigned_station_id__isnull=True)
    
    print(f"Found {unassigned_alerts.count()} unassigned alerts\n")
    
    assigned_count = 0
    failed_count = 0
    
    for alert in unassigned_alerts:
        print(f"Processing: {alert.title}")
        print(f"  Type: {alert.alert_type} | Department: {alert.department}")
        print(f"  Location: {alert.latitude}, {alert.longitude}")
        
        if alert.latitude and alert.longitude:
            # Find nearest station
            nearest_station = StationFinderService.find_nearest_station(
                float(alert.latitude),
                float(alert.longitude),
                alert.department
            )
            
            if nearest_station:
                # Calculate distance
                distance = StationFinderService.calculate_distance(
                    float(alert.latitude), float(alert.longitude),
                    float(nearest_station.latitude), float(nearest_station.longitude)
                )
                
                # Assign the alert
                alert.assigned_station_id = nearest_station.station_id
                alert.save()
                
                print(f"  ✓ Assigned to: {nearest_station.name} ({distance:.2f} km)")
                assigned_count += 1
            else:
                print(f"  ✗ No {alert.department} stations found nearby")
                failed_count += 1
        else:
            print(f"  ✗ No coordinates available")
            failed_count += 1
        
        print()
    
    print(f"Assignment Summary:")
    print(f"  ✓ Successfully assigned: {assigned_count} alerts")
    print(f"  ✗ Failed to assign: {failed_count} alerts")
    print(f"  📊 Total processed: {unassigned_alerts.count()} alerts")

def show_assignment_summary():
    """Show summary of all alert assignments"""
    
    print("\n=== Alert Assignment Summary ===\n")
    
    # Get all alerts
    all_alerts = Alert.objects.all()
    assigned_alerts = Alert.objects.filter(assigned_station_id__isnull=False)
    unassigned_alerts = Alert.objects.filter(assigned_station_id__isnull=True)
    
    print(f"Total alerts: {all_alerts.count()}")
    print(f"Assigned alerts: {assigned_alerts.count()}")
    print(f"Unassigned alerts: {unassigned_alerts.count()}")
    
    # Show assignments by department
    departments = ['fire', 'police', 'medical']
    
    for dept in departments:
        dept_alerts = Alert.objects.filter(department=dept)
        dept_assigned = dept_alerts.filter(assigned_station_id__isnull=False)
        
        print(f"\n{dept.title()} Department:")
        print(f"  Total alerts: {dept_alerts.count()}")
        print(f"  Assigned: {dept_assigned.count()}")
        print(f"  Unassigned: {dept_alerts.count() - dept_assigned.count()}")
        
        # Show specific assignments
        if dept_assigned.exists():
            print(f"  Assignments:")
            for alert in dept_assigned:
                try:
                    from geography.models import Station
                    station = Station.objects.get(station_id=alert.assigned_station_id)
                    print(f"    - {alert.title[:40]}... → {station.name}")
                except:
                    print(f"    - {alert.title[:40]}... → Unknown station")

if __name__ == '__main__':
    assign_alerts_to_stations()
    show_assignment_summary()
    print("\nAlert assignment complete!")
