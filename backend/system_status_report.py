#!/usr/bin/env python
import os
import sys
import django

# Add the project directory to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'emergency_system.settings')
django.setup()

from django.db import connection
from geography.models import Region, District, Station
from alerts.models import Alert
from alerts.services import AlertRoutingService
from accounts.models import User

def generate_system_status_report():
    """Generate a comprehensive system status report"""
    print("🚨 MyGuardian+ System Status Report 🚨")
    print("=" * 70)
    print(f"Generated on: {django.utils.timezone.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 70)
    
    # Database Connection Status
    print("\n📊 DATABASE CONNECTION STATUS")
    print("-" * 40)
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT version();")
            db_version = cursor.fetchone()[0]
            print(f"✅ Database: Connected")
            print(f"   PostgreSQL Version: {db_version.split(',')[0]}")
            
            # Check table counts
            cursor.execute("""
                SELECT COUNT(*) 
                FROM information_schema.tables 
                WHERE table_schema = 'public';
            """)
            table_count = cursor.fetchone()[0]
            print(f"   Total Tables: {table_count}")
            
    except Exception as e:
        print(f"❌ Database: Connection Failed - {e}")
        return False
    
    # Geography System Status
    print("\n🗺️  GEOGRAPHY SYSTEM STATUS")
    print("-" * 40)
    
    regions = Region.objects.all()
    districts = District.objects.all()
    stations = Station.objects.all()
    
    print(f"✅ Regions: {regions.count()}")
    print(f"✅ Districts: {districts.count()}")
    print(f"✅ Stations: {stations.count()}")
    
    # Show hierarchy
    for region in regions:
        print(f"\n   🌍 {region.display_name}")
        region_districts = region.districts.all()
        for district in region_districts:
            print(f"      🏢 {district.name} ({district.get_department_display()})")
            district_stations = district.stations.all()
            for station in district_stations:
                print(f"         🚒 {station.name} ({station.get_station_type_display()})")
    
    # Alert Routing System Status
    print(f"\n🚨 ALERT ROUTING SYSTEM STATUS")
    print("-" * 40)
    
    alerts = Alert.objects.all()
    assigned_alerts = alerts.filter(assigned_station_id__isnull=False)
    
    print(f"✅ Total Alerts: {alerts.count()}")
    print(f"✅ Assigned Alerts: {assigned_alerts.count()}")
    
    if alerts.count() > 0:
        assignment_rate = (assigned_alerts.count() / alerts.count()) * 100
        print(f"✅ Assignment Rate: {assignment_rate:.1f}%")
        
        # Alert breakdown by department
        fire_alerts = alerts.filter(department='fire').count()
        police_alerts = alerts.filter(department='police').count()
        medical_alerts = alerts.filter(department='medical').count()
        
        print(f"   🔥 Fire Alerts: {fire_alerts}")
        print(f"   👮 Police Alerts: {police_alerts}")
        print(f"   🏥 Medical Alerts: {medical_alerts}")
    
    # User System Status
    print(f"\n👥 USER SYSTEM STATUS")
    print("-" * 40)
    
    users = User.objects.all()
    active_users = users.filter(is_active_user=True)
    
    print(f"✅ Total Users: {users.count()}")
    print(f"✅ Active Users: {active_users.count()}")
    
    # User breakdown by role
    roles = ['System Administrator', 'Regional Manager', 'District Manager', 'Station Manager', 'Responder']
    for role in roles:
        role_count = users.filter(role=role).count()
        if role_count > 0:
            print(f"   {role}: {role_count}")
    
    # System Health Checks
    print(f"\n🔧 SYSTEM HEALTH CHECKS")
    print("-" * 40)
    
    health_checks = []
    
    # Check 1: All districts have regions
    orphaned_districts = District.objects.filter(region__isnull=True).count()
    if orphaned_districts == 0:
        health_checks.append("✅ All districts have regions")
    else:
        health_checks.append(f"⚠️  {orphaned_districts} districts without regions")
    
    # Check 2: All stations have districts
    orphaned_stations = Station.objects.filter(district__isnull=True).count()
    if orphaned_stations == 0:
        health_checks.append("✅ All stations have districts")
    else:
        health_checks.append(f"⚠️  {orphaned_stations} stations without districts")
    
    # Check 3: All stations have coordinates
    stations_without_coords = Station.objects.filter(
        latitude__isnull=True
    ).count() + Station.objects.filter(longitude__isnull=True).count()
    
    if stations_without_coords == 0:
        health_checks.append("✅ All stations have coordinates")
    else:
        health_checks.append(f"⚠️  {stations_without_coords} stations missing coordinates")
    
    # Check 4: Alert routing functionality
    try:
        # Test alert routing
        system_user = User.objects.filter(role='System Administrator').first()
        if system_user:
            test_alert = AlertRoutingService.route_emergency_alert(
                alert_type='test_alert',
                latitude=40.7128,
                longitude=-74.0060,
                severity='low',
                description='System health check test',
                created_by_user=system_user
            )
            if test_alert:
                health_checks.append("✅ Alert routing system functional")
                # Clean up test alert
                test_alert.delete()
            else:
                health_checks.append("❌ Alert routing system failed")
        else:
            health_checks.append("⚠️  No system administrator found for testing")
    except Exception as e:
        health_checks.append(f"❌ Alert routing error: {str(e)[:50]}...")
    
    for check in health_checks:
        print(f"   {check}")
    
    # Summary
    print(f"\n📋 SUMMARY")
    print("-" * 40)
    
    total_checks = len(health_checks)
    passed_checks = len([c for c in health_checks if c.startswith("✅")])
    warning_checks = len([c for c in health_checks if c.startswith("⚠️")])
    failed_checks = len([c for c in health_checks if c.startswith("❌")])
    
    print(f"Health Checks: {passed_checks}/{total_checks} passed")
    if warning_checks > 0:
        print(f"Warnings: {warning_checks}")
    if failed_checks > 0:
        print(f"Failures: {failed_checks}")
    
    if failed_checks == 0 and warning_checks == 0:
        print("\n🎉 System Status: EXCELLENT")
        print("   All systems operational!")
    elif failed_checks == 0:
        print("\n✅ System Status: GOOD")
        print("   Minor warnings detected")
    else:
        print("\n⚠️  System Status: NEEDS ATTENTION")
        print("   Critical issues detected")
    
    print("\n" + "=" * 70)
    return True

if __name__ == "__main__":
    generate_system_status_report()
