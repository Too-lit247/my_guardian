#!/usr/bin/env python
"""
Script to clear all alerts and create clean Rumphi fire emergency test
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

def clear_all_emergency_data():
    """Clear all existing alerts, triggers, and readings"""
    
    print("🧹 CLEARING ALL EMERGENCY DATA")
    print("=" * 50)
    
    # Count existing data
    alert_count = Alert.objects.count()
    trigger_count = EmergencyTrigger.objects.count()
    reading_count = DeviceReading.objects.count()
    
    print(f"📊 BEFORE CLEANUP:")
    print(f"   🚨 Alerts: {alert_count}")
    print(f"   ⚠️ Triggers: {trigger_count}")
    print(f"   📊 Readings: {reading_count}")
    print()
    
    # Delete all data
    Alert.objects.all().delete()
    EmergencyTrigger.objects.all().delete()
    DeviceReading.objects.all().delete()
    
    print("✅ All emergency data cleared!")
    print("📊 Database is now clean for testing")
    print()

def create_clean_rumphi_emergency():
    """Create a clean Rumphi fire emergency using existing device"""
    
    print("🏔️ CREATING CLEAN RUMPHI FIRE EMERGENCY")
    print("=" * 50)
    
    # Use existing device GD-075BDF9E
    try:
        device = Device.objects.get(serial_number='GD-075BDF9E')
        print(f"📱 Using existing device: {device.serial_number}")
        print(f"👤 Owner: {device.owner_name}")
        print(f"📞 Contact: {device.owner_phone}")
    except Device.DoesNotExist:
        print("❌ Device GD-075BDF9E not found!")
        return None, []
    
    # Rumphi coordinates (Northern Malawi)
    rumphi_lat = Decimal('-10.9000')
    rumphi_lng = Decimal('33.8500')
    
    print(f"📍 Emergency Location: Rumphi District ({rumphi_lat}, {rumphi_lng})")
    print(f"🌍 Region: Northern Malawi (no local emergency stations)")
    print()
    
    # Create fire emergency readings
    print("🔥 CREATING FIRE EMERGENCY READINGS:")
    print("-" * 40)
    
    fire_readings = [
        {
            'type': 'temperature',
            'value': 88.0,  # Very high temperature - critical fire
            'description': 'CRITICAL: House fire in Rumphi - extreme heat detected'
        },
        {
            'type': 'smoke',
            'value': 0.96,  # Very heavy smoke - fire confirmed
            'description': 'CRITICAL: Dense smoke in Rumphi - fire spreading rapidly'
        }
    ]
    
    created_readings = []
    
    for i, reading_data in enumerate(fire_readings, 1):
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
                'scenario': 'CLEAN Rumphi Fire Emergency - Multi-Department Tracking',
                'description': reading_data['description'],
                'test_id': f'CLEAN_RUMPHI_{i}',
                'purpose': 'Track where alerts get assigned across departments'
            }
        }
        
        if reading_data['type'] == 'temperature':
            reading_kwargs['temperature'] = reading_data['value']
        elif reading_data['type'] == 'smoke':
            reading_kwargs['smoke_level'] = reading_data['value']
        
        reading = DeviceReading.objects.create(**reading_kwargs)
        created_readings.append(reading)
        
        print(f"✅ Reading {i}: {reading_data['type'].title()}")
        print(f"   📊 Value: {reading_data['value']}")
        print(f"   📝 {reading_data['description']}")
        print(f"   🆔 Reading ID: {reading.reading_id}")
        print()
    
    return device, created_readings

def process_rumphi_emergency(readings):
    """Process the Rumphi emergency readings"""
    
    print("🚨 PROCESSING RUMPHI FIRE EMERGENCY")
    print("=" * 50)
    
    from devices.views import process_reading_for_emergencies
    
    for i, reading in enumerate(readings, 1):
        print(f"⚡ Processing Reading {i}: {reading.reading_type}")
        print(f"   📊 Value: {getattr(reading, reading.reading_type, 'N/A')}")
        print(f"   📍 Location: {reading.latitude}, {reading.longitude}")
        print(f"   🆔 Reading ID: {reading.reading_id}")
        
        try:
            process_reading_for_emergencies(reading)
            print(f"  ✅ Processed successfully")
        except Exception as e:
            print(f"  ❌ Error: {e}")
        
        print()

def analyze_rumphi_alert_routing():
    """Analyze where the Rumphi alerts were routed"""
    
    print("📋 RUMPHI ALERT ROUTING ANALYSIS")
    print("=" * 50)
    
    # Get all alerts (should only be from our clean test)
    all_alerts = Alert.objects.all().order_by('department', '-created_at')
    all_triggers = EmergencyTrigger.objects.all().order_by('-triggered_at')
    
    print(f"📊 EMERGENCY RESPONSE SUMMARY:")
    print(f"   🚨 Total Alerts Created: {all_alerts.count()}")
    print(f"   ⚠️ Total Triggers Created: {all_triggers.count()}")
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
    
    print(f"🏢 MULTI-DEPARTMENT RESPONSE BREAKDOWN:")
    print("-" * 50)
    
    for dept, alerts in departments.items():
        print(f"\n🏢 {dept.upper()} DEPARTMENT ({len(alerts)} alerts)")
        print("-" * 40)
        
        for j, alert in enumerate(alerts, 1):
            print(f"📋 Alert {j}: {alert.title}")
            print(f"   🎯 Priority: {alert.priority.upper()}")
            print(f"   📍 Location: {alert.location}")
            print(f"   ⏰ Created: {alert.created_at.strftime('%H:%M:%S')}")
            print(f"   🆔 Alert ID: {alert.alert_id}")
            
            if alert.assigned_station_id:
                try:
                    station = Station.objects.get(station_id=alert.assigned_station_id)
                    print(f"   🏥 ✅ ASSIGNED TO: {station.name}")
                    print(f"   📧 Station Address: {station.address}")
                    print(f"   📞 Station Contact: {station.phone}")
                    
                    if station.manager:
                        print(f"   👤 Station Manager: {station.manager.full_name}")
                    
                    # Calculate response details
                    if alert.latitude and alert.longitude and station.latitude and station.longitude:
                        distance = StationFinderService.calculate_distance(
                            float(alert.latitude), float(alert.longitude),
                            float(station.latitude), float(station.longitude)
                        )
                        print(f"   🚗 Response Distance: {distance:.2f} km")
                        
                        response_time = (distance / 40) * 60
                        print(f"   ⏱️ Est. Response Time: {response_time:.1f} minutes")
                        
                        # Distance assessment
                        if distance < 50:
                            status = "🟢 REASONABLE"
                        elif distance < 100:
                            status = "🟡 DISTANT"
                        else:
                            status = "🔴 VERY FAR"
                        
                        print(f"   📊 Distance Assessment: {status}")
                
                except Station.DoesNotExist:
                    print(f"   ❌ Station not found: {alert.assigned_station_id}")
            else:
                print(f"   ⚠️ NO STATION ASSIGNED")
            
            print()
    
    # Show emergency triggers
    print(f"⚠️ EMERGENCY TRIGGERS CREATED ({all_triggers.count()})")
    print("-" * 50)
    
    for k, trigger in enumerate(all_triggers, 1):
        print(f"🚨 Trigger {k}: {trigger.get_trigger_type_display()} - {trigger.get_severity_display()}")
        print(f"   📊 Reading Value: {trigger.trigger_value}")
        print(f"   🎯 Threshold: {trigger.threshold_value}")
        print(f"   📍 Location: {trigger.latitude}, {trigger.longitude}")
        print(f"   ⏰ Triggered At: {trigger.triggered_at.strftime('%H:%M:%S')}")
        print(f"   🆔 Trigger ID: {trigger.trigger_id}")
        
        if trigger.alert_created_id:
            print(f"   ✅ Created Alert: {trigger.alert_created_id}")
        else:
            print(f"   ❌ No alert created")
        
        print()

def show_expected_vs_actual():
    """Show what we expected vs what actually happened"""
    
    print("🎯 EXPECTED VS ACTUAL RESULTS")
    print("=" * 50)
    
    print("📋 WHAT WE EXPECTED:")
    print("-" * 30)
    print("🔥 Fire Department:")
    print("   • Primary fire alert → Mzuzu Fire Station (~65km)")
    print("🏥 Medical Department:")
    print("   • Medical support alert → Mzuzu Central Hospital (~65km)")
    print("👮 Police Department:")
    print("   • Police support alert → Mzuzu Police Station (~65km)")
    print()
    
    # Count actual results
    fire_alerts = Alert.objects.filter(department='fire').count()
    medical_alerts = Alert.objects.filter(department='medical').count()
    police_alerts = Alert.objects.filter(department='police').count()
    
    print("📊 WHAT ACTUALLY HAPPENED:")
    print("-" * 30)
    print(f"🔥 Fire Department: {fire_alerts} alerts")
    print(f"🏥 Medical Department: {medical_alerts} alerts")
    print(f"👮 Police Department: {police_alerts} alerts")
    print()
    
    total_alerts = fire_alerts + medical_alerts + police_alerts
    
    if total_alerts >= 3:
        print("✅ SUCCESS: Multi-department response activated!")
    else:
        print("⚠️ PARTIAL: Not all departments responded")
    
    print()

def main():
    """Main function"""
    
    print("🧹 CLEAN RUMPHI FIRE EMERGENCY TEST")
    print("=" * 70)
    print("🎯 Purpose: Track exactly where Rumphi fire alerts get assigned")
    print("=" * 70)
    print()
    
    # Step 1: Clear all existing emergency data
    clear_all_emergency_data()
    
    # Step 2: Create clean Rumphi fire emergency
    device, readings = create_clean_rumphi_emergency()
    
    if not device:
        print("❌ Cannot proceed without device")
        return
    
    # Step 3: Process the emergency
    process_rumphi_emergency(readings)
    
    # Step 4: Analyze the routing results
    analyze_rumphi_alert_routing()
    
    # Step 5: Show expected vs actual
    show_expected_vs_actual()
    
    print("🧹 CLEAN RUMPHI TEST COMPLETE")
    print("=" * 70)
    print()
    print("🌐 View clean results at: http://localhost:3000/dashboard/alerts")
    print("🔍 You should now see ONLY the Rumphi fire emergency alerts")
    print("📍 All alerts should be assigned to Mzuzu stations (~65km away)")

if __name__ == '__main__':
    main()
