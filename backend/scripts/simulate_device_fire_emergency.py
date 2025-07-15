#!/usr/bin/env python
"""
Script to simulate fire emergency from specific device data
"""
import os
import sys
import django
import json
from decimal import Decimal
from datetime import datetime

# Add the parent directory to the path so we can import Django modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'emergency_system.settings')
django.setup()

from devices.models import Device, DeviceReading, EmergencyTrigger
from alerts.models import Alert
from accounts.models import User

def create_device_from_json():
    """Create device from the provided JSON data"""
    
    device_data = {
        "device_id": "6ceb1357-771b-4cfb-8edf-0a623e7d5bc3",
        "mac_address": "8C:41:F2:5C:BE:B5",
        "serial_number": "GD-075BDF9E",
        "device_type": "guardian_bracelet",
        "owner_id": "117653b2-ab7e-4bc0-8a04-fcf21b59b7ee",
        "owner_name": "Test Owner",
        "owner_phone": "+265991234567",
        "owner_address": "Mzuzu City",
        "emergency_contact": "",
        "emergency_contact_phone": "",
        "medical_conditions": "",
        "medications": "",
        "allergies": "",
        "blood_type": "",
        "status": "active",
        "battery_level": 34,
        "last_heartbeat": "2025-07-13 08:32:04.896986+00",
        "firmware_version": "1.0.0",
        "last_known_latitude": "-59.89940700",
        "last_known_longitude": "-67.68794700",
        "last_location_update": "2025-07-13 08:32:05.062069+00",
        "audio_monitoring_enabled": True,
        "heart_rate_monitoring_enabled": True,
        "fire_monitoring_enabled": True,
        "fall_detection_enabled": True,
        "monitoring_interval": 300,
        "registered_at": "2025-07-13 08:13:34.274618+00",
        "updated_at": "2025-07-13 08:32:05.062233+00",
        "registered_by_id": None
    }
    
    print("📱 DEVICE INFORMATION")
    print("=" * 50)
    print(f"🆔 Device ID: {device_data['device_id']}")
    print(f"📟 Serial Number: {device_data['serial_number']}")
    print(f"🌐 MAC Address: {device_data['mac_address']}")
    print(f"👤 Owner: {device_data['owner_name']}")
    print(f"📞 Phone: {device_data['owner_phone']}")
    print(f"📍 Address: {device_data['owner_address']}")
    print(f"🗺️ Last Location: {device_data['last_known_latitude']}, {device_data['last_known_longitude']}")
    print(f"🔋 Battery: {device_data['battery_level']}%")
    print(f"🔥 Fire Monitoring: {'✅' if device_data['fire_monitoring_enabled'] else '❌'}")
    print()
    
    # Get or create system user for device registration
    system_user, created = User.objects.get_or_create(
        username='system_device',
        defaults={
            'email': 'system@device.com',
            'full_name': 'System Device User',
            'role': 'Admin',
            'department': 'admin',
            'is_active': True
        }
    )
    
    # Create or get the device
    device, created = Device.objects.get_or_create(
        serial_number=device_data['serial_number'],
        defaults={
            'mac_address': device_data['mac_address'],
            'device_type': device_data['device_type'],
            'owner_name': device_data['owner_name'],
            'owner_phone': device_data['owner_phone'],
            'owner_address': device_data['owner_address'],
            'emergency_contact': device_data['emergency_contact'] or 'Not provided',
            'emergency_contact_phone': device_data['emergency_contact_phone'] or 'Not provided',
            'medical_conditions': device_data['medical_conditions'] or 'None specified',
            'medications': device_data.get('medications', ''),
            'allergies': device_data.get('allergies', ''),
            'blood_type': device_data['blood_type'] or 'Unknown',
            'status': device_data['status'],
            'battery_level': device_data['battery_level'],
            'firmware_version': device_data['firmware_version'],
            'audio_monitoring_enabled': device_data['audio_monitoring_enabled'],
            'heart_rate_monitoring_enabled': device_data['heart_rate_monitoring_enabled'],
            'fire_monitoring_enabled': device_data['fire_monitoring_enabled'],
            'fall_detection_enabled': device_data['fall_detection_enabled'],
            'monitoring_interval': device_data['monitoring_interval'],
            'registered_by': system_user
        }
    )
    
    if created:
        print(f"✅ Created device: {device.serial_number}")
    else:
        print(f"📱 Using existing device: {device.serial_number}")
    
    return device, device_data

def simulate_fire_emergency_readings(device, device_data):
    """Simulate fire emergency readings from the device"""
    
    print("\n🔥 SIMULATING FIRE EMERGENCY")
    print("=" * 50)
    
    # Use the device's last known location
    latitude = Decimal(device_data['last_known_latitude'])
    longitude = Decimal(device_data['last_known_longitude'])
    
    print(f"📍 Emergency Location: {latitude}, {longitude}")
    print(f"🏠 Address: {device_data['owner_address']}")
    print(f"👤 Device Owner: {device_data['owner_name']}")
    print()
    
    # Fire emergency scenario
    fire_scenario = {
        'description': f"""
🔥 FIRE EMERGENCY DETECTED - {device_data['owner_address']}

📱 Device: {device_data['serial_number']} ({device_data['owner_name']})
📍 Location: {latitude}, {longitude}
🏠 Address: {device_data['owner_address']}
📞 Contact: {device_data['owner_phone']}

🚨 EMERGENCY READINGS:
- Extreme temperature detected (fire/heat source)
- Heavy smoke concentration
- Elevated heart rate (panic/stress response)

⚠️ IMMEDIATE RESPONSE REQUIRED:
🚒 Fire suppression needed
🏥 Medical attention for smoke inhalation
👮 Emergency coordination and evacuation
        """,
        'readings': [
            {
                'type': 'temperature',
                'value': 72.5,  # Very high temperature indicating fire
                'description': 'Extreme heat detected - possible structure fire'
            },
            {
                'type': 'smoke',
                'value': 0.92,  # Heavy smoke concentration
                'description': 'Dense smoke detected - fire confirmed'
            },
            {
                'type': 'heart_rate',
                'value': 155,  # Very high heart rate - panic response
                'description': 'Extreme stress response - emergency situation'
            }
        ]
    }
    
    print(fire_scenario['description'])
    print()
    
    # Create device readings that will trigger emergency alerts
    created_readings = []
    
    for reading_data in fire_scenario['readings']:
        print(f"📊 Creating {reading_data['type']} reading...")
        
        reading_kwargs = {
            'device': device,
            'reading_type': reading_data['type'],
            'latitude': latitude,
            'longitude': longitude,
            'raw_data': {
                'device_id': device_data['device_id'],
                'serial_number': device_data['serial_number'],
                'owner_name': device_data['owner_name'],
                'owner_address': device_data['owner_address'],
                'emergency_level': 'CRITICAL',
                'scenario': 'Fire Emergency',
                'description': reading_data['description'],
                'battery_level': device_data['battery_level'],
                'firmware_version': device_data['firmware_version']
            }
        }
        
        # Add specific sensor data
        if reading_data['type'] == 'temperature':
            reading_kwargs['temperature'] = reading_data['value']
        elif reading_data['type'] == 'smoke':
            reading_kwargs['smoke_level'] = reading_data['value']
        elif reading_data['type'] == 'heart_rate':
            reading_kwargs['heart_rate'] = reading_data['value']
        
        reading = DeviceReading.objects.create(**reading_kwargs)
        created_readings.append(reading)
        
        print(f"  ✅ {reading_data['type'].title()}: {reading_data['value']}")
        print(f"  📝 {reading_data['description']}")
        print()
    
    return created_readings

def process_emergency_alerts(readings):
    """Process the emergency readings and create alerts"""
    
    print("🚨 PROCESSING EMERGENCY RESPONSE")
    print("=" * 50)
    
    from devices.views import process_reading_for_emergencies
    
    alerts_before = Alert.objects.count()
    triggers_before = EmergencyTrigger.objects.count()
    
    for reading in readings:
        print(f"⚡ Processing {reading.reading_type} reading (ID: {reading.reading_id})...")
        
        try:
            # Process the reading for emergencies
            process_reading_for_emergencies(reading)
            print(f"  ✅ Processed successfully")
        except Exception as e:
            print(f"  ❌ Error processing: {e}")
        
        print()
    
    alerts_after = Alert.objects.count()
    triggers_after = EmergencyTrigger.objects.count()
    
    new_alerts = alerts_after - alerts_before
    new_triggers = triggers_after - triggers_before
    
    print(f"📊 EMERGENCY PROCESSING RESULTS:")
    print(f"  🚨 New Alerts Created: {new_alerts}")
    print(f"  ⚠️ New Triggers Created: {new_triggers}")
    print()
    
    return new_alerts, new_triggers

def show_emergency_response():
    """Show the emergency response details"""
    
    print("📋 EMERGENCY RESPONSE ANALYSIS")
    print("=" * 50)
    
    # Get recent alerts (last 10 minutes)
    from django.utils import timezone
    recent_alerts = Alert.objects.filter(
        created_at__gte=timezone.now() - timezone.timedelta(minutes=10)
    ).order_by('-created_at')
    
    print(f"🚨 Recent Emergency Alerts: {recent_alerts.count()}")
    print()
    
    for alert in recent_alerts:
        print(f"📋 {alert.title}")
        print(f"   🎯 Priority: {alert.priority.upper()}")
        print(f"   🏢 Department: {alert.department.upper()}")
        print(f"   📍 Location: {alert.location}")
        print(f"   ⏰ Created: {alert.created_at.strftime('%H:%M:%S')}")
        
        if alert.assigned_station_id:
            print(f"   🏥 Assigned Station: {alert.assigned_station_id}")
        else:
            print(f"   ⚠️ No station assigned")
        
        print()
    
    # Show emergency triggers
    recent_triggers = EmergencyTrigger.objects.filter(
        triggered_at__gte=timezone.now() - timezone.timedelta(minutes=10),
        device__serial_number='GD-075BDF9E'
    ).order_by('-triggered_at')
    
    print(f"⚠️ Emergency Triggers: {recent_triggers.count()}")
    print()
    
    for trigger in recent_triggers:
        print(f"🚨 {trigger.get_trigger_type_display()} - {trigger.get_severity_display()}")
        print(f"   📊 Value: {trigger.trigger_value} (Threshold: {trigger.threshold_value})")
        print(f"   📍 Location: {trigger.latitude}, {trigger.longitude}")
        print(f"   ⏰ Time: {trigger.triggered_at.strftime('%H:%M:%S')}")
        
        if trigger.alert_created_id:
            print(f"   ✅ Alert Created: {trigger.alert_created_id}")
        
        print()

def main():
    """Main simulation function"""
    
    print("🔥 DEVICE FIRE EMERGENCY SIMULATION 🔥")
    print("Device: GD-075BDF9E (Test Owner)")
    print("=" * 60)
    print()
    
    # Step 1: Create device from JSON data
    device, device_data = create_device_from_json()
    
    # Step 2: Simulate fire emergency readings
    readings = simulate_fire_emergency_readings(device, device_data)
    
    # Step 3: Process emergency response
    new_alerts, new_triggers = process_emergency_alerts(readings)
    
    # Step 4: Show emergency response
    show_emergency_response()
    
    print("🔥 FIRE EMERGENCY SIMULATION COMPLETE 🔥")
    print("=" * 60)
    print(f"📱 Device: {device.serial_number} ({device.owner_name})")
    print(f"📍 Location: {device_data['last_known_latitude']}, {device_data['last_known_longitude']}")
    print(f"📊 Readings Created: {len(readings)}")
    print(f"🚨 Alerts Generated: {new_alerts}")
    print(f"⚠️ Triggers Created: {new_triggers}")
    print()
    print("🌐 View alerts at: http://localhost:3000/dashboard/alerts")

if __name__ == '__main__':
    main()
