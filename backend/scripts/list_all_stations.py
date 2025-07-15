#!/usr/bin/env python
"""
Script to list all available stations in the system
"""
import os
import sys
import django

# Add the parent directory to the path so we can import Django modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'emergency_system.settings')
django.setup()

from geography.models import Station

def list_all_stations():
    """List all stations in the system"""
    
    print("🏥 ALL EMERGENCY STATIONS IN SYSTEM")
    print("=" * 60)
    
    stations = Station.objects.all().order_by('department', 'name')
    
    if not stations.exists():
        print("❌ No stations found in the system")
        return
    
    # Group by department
    departments = {}
    for station in stations:
        dept = station.department
        if dept not in departments:
            departments[dept] = []
        departments[dept].append(station)
    
    total_stations = 0
    
    for dept, dept_stations in departments.items():
        print(f"\n🏢 {dept.upper()} DEPARTMENT ({len(dept_stations)} stations)")
        print("-" * 50)
        
        for station in dept_stations:
            status = "✅ ACTIVE" if station.is_active else "❌ INACTIVE"
            
            print(f"🏥 {station.name}")
            print(f"   📋 Code: {station.code}")
            print(f"   📍 Location: {station.latitude}, {station.longitude}")
            print(f"   🌍 Region: {station.region}")
            print(f"   📧 Address: {station.address}")
            print(f"   📞 Phone: {station.phone}")
            print(f"   📊 Status: {status}")
            
            if station.manager:
                print(f"   👤 Manager: {station.manager.full_name}")
            else:
                print(f"   👤 Manager: Not assigned")
            
            print(f"   🆔 Station ID: {station.station_id}")
            print()
        
        total_stations += len(dept_stations)
    
    print(f"📊 TOTAL STATIONS: {total_stations}")
    
    # Show active vs inactive
    active_count = Station.objects.filter(is_active=True).count()
    inactive_count = Station.objects.filter(is_active=False).count()
    
    print(f"✅ Active Stations: {active_count}")
    print(f"❌ Inactive Stations: {inactive_count}")
    
    return stations

if __name__ == '__main__':
    list_all_stations()
