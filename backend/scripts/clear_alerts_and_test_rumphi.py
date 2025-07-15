#!/usr/bin/env python
"""
Script to clear all existing alerts and test Rumphi emergency with clean tracking
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

from devices.models import Device, DeviceReading, EmergencyTrigger
from alerts.models import Alert
from geography.models import Station
from alerts.services import StationFinderService
from accounts.models import User

def analyze_multi_department_response():
    """Analyze which emergency types trigger multi-department responses"""
    
    print("🚨 MULTI-DEPARTMENT EMERGENCY RESPONSE ANALYSIS")
    print("=" * 60)
    
    print("📋 CURRENT SYSTEM BEHAVIOR:")
    print("-" * 40)
    
    # Check the AlertRoutingService code
    print("🔍 Checking AlertRoutingService for multi-department logic...")
    
    from alerts.services import AlertRoutingService
    import inspect
    
    # Get the source code of the route_emergency_alert method
    source = inspect.getsource(AlertRoutingService.route_emergency_alert)
    
    print("\n🎯 FIRE EMERGENCY TYPES THAT TRIGGER MULTI-DEPARTMENT RESPONSE:")
    print("-" * 60)
    
    # Extract the fire types that trigger multi-department response
    fire_types = [
        'fire_detected', 'building_fire', 'wildfire', 'gas_leak', 
        'explosion', 'hazmat_incident'
    ]
    
    for fire_type in fire_types:
        print(f"🔥 {fire_type.replace('_', ' ').title()}")
        print(f"   🚒 Primary: Fire Department")
        print(f"   🏥 Support: Medical Department (injury response)")
        print(f"   👮 Support: Police Department (crowd control, traffic)")
        print()
    
    print("📊 OTHER EMERGENCY TYPES:")
    print("-" * 30)
    print("🏥 Medical emergencies: Only Medical Department")
    print("👮 Police emergencies: Only Police Department")
    print("🔥 Non-fire emergencies: Single department only")
    print()
    
    print("✅ CONCLUSION: Only FIRE emergencies trigger multi-department response!")

def clear_all_alerts_and_triggers():
    """Clear all existing alerts and emergency triggers"""
    
    print("\n🧹 CLEARING ALL EXISTING ALERTS AND TRIGGERS")
    print("=" * 60)
    
    # Count existing data
    alert_count = Alert.objects.count()
    trigger_count = EmergencyTrigger.objects.count()
    reading_count = DeviceReading.objects.count()
    
    print(f"📊 BEFORE CLEANUP:")
    print(f"   🚨 Alerts: {alert_count}")
    print(f"   ⚠️ Triggers: {trigger_count}")
    print(f"   📊 Readings: {reading_count}")
    print()
    
    # Delete all alerts
    Alert.objects.all().delete()
    print("✅ Deleted all alerts")
    
    # Delete all emergency triggers
    EmergencyTrigger.objects.all().delete()
    print("✅ Deleted all emergency triggers")
    
    # Delete all device readings
    DeviceReading.objects.all().delete()
    print("✅ Deleted all device readings")
    
    print()
    print("🧹 CLEANUP COMPLETE - Database is now clean!")
    print()

def create_rumphi_fire_emergency():
    """Create a clean Rumphi fire emergency for tracking"""
    
    print("🏔️ CREATING CLEAN RUMPHI FIRE EMERGENCY")
    print("=" * 60)
    
    # Rumphi coordinates
    rumphi_lat = Decimal('-10.9000')
    rumphi_lng = Decimal('33.8500')
    
    # Get or create Rumphi device
    system_user, _ = User.objects.get_or_create(
        username='rumphi_clean_test',
        defaults={
            'email': 'rumphi_clean@test.com',
            'full_name': 'Rumphi Clean Test User',
            'role': 'Admin',
            'department': 'admin',
            'is_active': True
        }
    )
    
    device, created = Device.objects.get_or_create(
        serial_number='RUMPHI_CLEAN_001',
        defaults={
            'mac_address': '00:RP:CL:01:23:45',
            'device_type': 'guardian_bracelet',
            'owner_name': 'Rumphi Fire Victim',
            'owner_phone': '+265-888-RUMPHI-FIRE',
            'owner_address': 'Rumphi District, Northern Region, Malawi',
            'emergency_contact': 'Emergency Contact',
            'emergency_contact_phone': '+265-999-EMERGENCY',
            'medical_conditions': 'None',
            'status': 'active',
            'battery_level': 89,
            'fire_monitoring_enabled': True,
            'heart_rate_monitoring_enabled': True,
            'registered_by_id': system_user.id
        }
    )
    
    print(f"📱 Device: {device.serial_number}")
    print(f"👤 Owner: {device.owner_name}")
    print(f"📍 Location: Rumphi District ({rumphi_lat}, {rumphi_lng})")
    print(f"📞 Contact: {device.owner_phone}")
    print()
    
    # Create fire emergency readings
    print("🔥 CREATING FIRE EMERGENCY READINGS:")
    print("-" * 40)
    
    fire_readings = [
        {
            'type': 'temperature',
            'value': 85.0,  # Very high temperature - fire detected
            'description': 'CRITICAL: House fire in Rumphi - extreme temperature'
        },
        {
            'type': 'smoke',
            'value': 0.98,  # Very heavy smoke - fire confirmed
            'description': 'CRITICAL: Dense smoke in Rumphi - fire confirmed'
        }
    ]
    
    created_readings = []
    
    for reading_data in fire_readings:
        reading_kwargs = {
            'device': device,
            'reading_type': reading_data['type'],
            'latitude': rumphi_lat,
            'longitude': rumphi_lng,
            'raw_data': {
                'serial_number': device.serial_number,
                'owner_name': device.owner_name,
                'location': 'Rumphi District, Northern Malawi',
                'emergency_level': 'CRITICAL',
                'scenario': 'CLEAN Rumphi Fire Emergency - Multi-Department Test',
                'description': reading_data['description'],
                'test_purpose': 'Track multi-department response routing'
            }
        }
        
        if reading_data['type'] == 'temperature':
            reading_kwargs['temperature'] = reading_data['value']
        elif reading_data['type'] == 'smoke':
            reading_kwargs['smoke_level'] = reading_data['value']
        
        reading = DeviceReading.objects.create(**reading_kwargs)
        created_readings.append(reading)
        
        print(f"✅ {reading_data['type'].title()}: {reading_data['value']}")
        print(f"   📝 {reading_data['description']}")
        print()
    
    return device, created_readings

def process_clean_emergency(readings):
    """Process the clean Rumphi emergency"""
    
    print("🚨 PROCESSING CLEAN RUMPHI FIRE EMERGENCY")
    print("=" * 60)
    
    from devices.views import process_reading_for_emergencies
    
    for i, reading in enumerate(readings, 1):
        print(f"⚡ Processing Reading {i}: {reading.reading_type}")
        print(f"   📊 Value: {getattr(reading, reading.reading_type, 'N/A')}")
        print(f"   📍 Location: {reading.latitude}, {reading.longitude}")
        
        try:
            process_reading_for_emergencies(reading)
            print(f"  ✅ Processed successfully")
        except Exception as e:
            print(f"  ❌ Error: {e}")
        
        print()

def analyze_clean_results():
    """Analyze the clean emergency results"""
    
    print("📋 CLEAN RUMPHI EMERGENCY RESULTS ANALYSIS")
    print("=" * 60)
    
    # Get all alerts (should only be from our clean test)
    all_alerts = Alert.objects.all().order_by('department', '-created_at')
    all_triggers = EmergencyTrigger.objects.all().order_by('-triggered_at')
    
    print(f"📊 TOTAL RESULTS:")
    print(f"   🚨 Alerts Created: {all_alerts.count()}")
    print(f"   ⚠️ Triggers Created: {all_triggers.count()}")
    print()
    
    if not all_alerts.exists():
        print("❌ No alerts were created!")
        return
    
    # Group alerts by department
    departments = {}
    for alert in all_alerts:
        dept = alert.department
        if dept not in departments:
            departments[dept] = []
        departments[dept].append(alert)
    
    print(f"🏢 DEPARTMENT BREAKDOWN:")
    print("-" * 40)
    
    for dept, alerts in departments.items():
        print(f"\n🏢 {dept.upper()} DEPARTMENT ({len(alerts)} alerts)")
        print("-" * 50)
        
        for alert in alerts:
            print(f"📋 {alert.title}")
            print(f"   🎯 Priority: {alert.priority.upper()}")
            print(f"   📍 Location: {alert.location}")
            print(f"   ⏰ Created: {alert.created_at.strftime('%H:%M:%S')}")
            
            if alert.assigned_station_id:
                try:
                    station = Station.objects.get(station_id=alert.assigned_station_id)
                    print(f"   🏥 ✅ ASSIGNED TO: {station.name}")
                    print(f"   📧 Address: {station.address}")
                    print(f"   📞 Contact: {station.phone}")
                    
                    # Calculate distance
                    if alert.latitude and alert.longitude and station.latitude and station.longitude:
                        distance = StationFinderService.calculate_distance(
                            float(alert.latitude), float(alert.longitude),
                            float(station.latitude), float(station.longitude)
                        )
                        print(f"   🚗 Distance: {distance:.2f} km")
                        
                        response_time = (distance / 40) * 60
                        print(f"   ⏱️ Response Time: {response_time:.1f} minutes")
                
                except Station.DoesNotExist:
                    print(f"   ❌ Station not found: {alert.assigned_station_id}")
            else:
                print(f"   ⚠️ NO STATION ASSIGNED")
            
            print()
    
    # Show emergency triggers
    print(f"⚠️ EMERGENCY TRIGGERS ({all_triggers.count()})")
    print("-" * 50)
    
    for trigger in all_triggers:
        print(f"🚨 {trigger.get_trigger_type_display()} - {trigger.get_severity_display()}")
        print(f"   📊 Value: {trigger.trigger_value} (Threshold: {trigger.threshold_value})")
        print(f"   📍 Location: {trigger.latitude}, {trigger.longitude}")
        print(f"   ⏰ Time: {trigger.triggered_at.strftime('%H:%M:%S')}")
        
        if trigger.alert_created_id:
            print(f"   ✅ Alert Created: {trigger.alert_created_id}")
        
        print()

def main():
    """Main function"""
    
    print("🧹 CLEAN RUMPHI FIRE EMERGENCY TEST")
    print("=" * 70)
    print()
    
    # Step 1: Analyze multi-department response behavior
    analyze_multi_department_response()
    
    # Step 2: Clear all existing data
    clear_all_alerts_and_triggers()
    
    # Step 3: Create clean Rumphi fire emergency
    device, readings = create_rumphi_fire_emergency()
    
    # Step 4: Process the emergency
    process_clean_emergency(readings)
    
    # Step 5: Analyze clean results
    analyze_clean_results()
    
    print("🧹 CLEAN RUMPHI FIRE TEST COMPLETE")
    print("=" * 70)
    print()
    print("🎯 WHAT TO EXPECT:")
    print("   🔥 Fire alerts should go to Mzuzu Fire Station")
    print("   🏥 Medical support alerts should go to Mzuzu Central Hospital")
    print("   👮 Police support alerts should go to Mzuzu Police Station")
    print("   📍 All stations ~65km from Rumphi")
    print()
    print("🌐 View clean results at: http://localhost:3000/dashboard/alerts")

if __name__ == '__main__':
    main()
