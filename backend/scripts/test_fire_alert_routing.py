#!/usr/bin/env python
"""
Script to test fire alert routing from device readings
"""
import os
import sys
import django
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
from geography.models import Station

def create_test_device():
    """Create a test device for fire alert testing"""
    
    # Get or create a system user to register the device
    system_user, created = User.objects.get_or_create(
        username='system_test',
        defaults={
            'email': 'system@test.com',
            'full_name': 'System Test User',
            'role': 'Admin',
            'department': 'admin',
            'is_active': True
        }
    )
    
    # Create test device
    device, created = Device.objects.get_or_create(
        serial_number='TEST_FIRE_001',
        defaults={
            'mac_address': '00:11:22:33:44:55',
            'device_type': 'guardian_bracelet',
            'owner_name': 'John Fire Test',
            'owner_phone': '+1-555-FIRE-001',
            'owner_address': '123 Test Street, Fire District, NYC',
            'emergency_contact': 'Jane Test',
            'emergency_contact_phone': '+1-555-EMERGENCY',
            'medical_conditions': 'None',
            'status': 'active',
            'battery_level': 85,
            'fire_monitoring_enabled': True,
            'registered_by_id': system_user.id
        }
    )
    
    if created:
        print(f"✓ Created test device: {device.serial_number}")
    else:
        print(f"⚠ Using existing device: {device.serial_number}")
    
    return device

def simulate_fire_readings(device):
    """Simulate device readings that would trigger fire alerts"""
    
    print("\n=== Simulating Fire Emergency Readings ===\n")
    
    # Test location coordinates (near our test stations)
    test_locations = [
        {
            'name': 'Downtown Fire Emergency',
            'lat': Decimal('40.7580'),
            'lng': Decimal('-73.9850'),
            'scenario': 'Building fire with high temperature and smoke'
        },
        {
            'name': 'Residential Fire Emergency', 
            'lat': Decimal('40.7550'),
            'lng': Decimal('-73.9830'),
            'scenario': 'House fire with extreme temperature'
        },
        {
            'name': 'Industrial Fire Emergency',
            'lat': Decimal('40.7600'),
            'lng': Decimal('-73.9800'),
            'scenario': 'Factory fire with heavy smoke'
        }
    ]
    
    created_readings = []
    
    for i, location in enumerate(test_locations):
        print(f"Scenario {i+1}: {location['scenario']}")
        print(f"Location: {location['name']} ({location['lat']}, {location['lng']})")
        
        # Create high temperature reading (fire detection)
        temp_reading = DeviceReading.objects.create(
            device=device,
            reading_type='temperature',
            temperature=55.0 + (i * 5),  # 55°C, 60°C, 65°C
            latitude=location['lat'],
            longitude=location['lng'],
            raw_data={
                'sensor_id': f'temp_sensor_{i+1}',
                'ambient_temp': 25.0,
                'device_temp': 55.0 + (i * 5),
                'scenario': location['scenario']
            }
        )
        
        # Create smoke detection reading
        smoke_reading = DeviceReading.objects.create(
            device=device,
            reading_type='smoke',
            smoke_level=0.8 + (i * 0.1),  # 0.8, 0.9, 1.0
            latitude=location['lat'],
            longitude=location['lng'],
            raw_data={
                'sensor_id': f'smoke_sensor_{i+1}',
                'smoke_density': 0.8 + (i * 0.1),
                'air_quality': 'poor',
                'scenario': location['scenario']
            }
        )
        
        created_readings.extend([temp_reading, smoke_reading])
        
        print(f"  ✓ Temperature reading: {temp_reading.temperature}°C (threshold: 40°C)")
        print(f"  ✓ Smoke reading: {smoke_reading.smoke_level} (threshold: 0.3)")
        print()
    
    return created_readings

def analyze_alert_routing():
    """Analyze how alerts were routed to different departments"""
    
    print("=== Alert Routing Analysis ===\n")
    
    # Get all recent alerts (created in the last hour)
    from django.utils import timezone
    recent_alerts = Alert.objects.filter(
        created_at__gte=timezone.now() - timezone.timedelta(hours=1)
    ).order_by('-created_at')
    
    print(f"Found {recent_alerts.count()} recent alerts\n")
    
    # Group alerts by department
    departments = {}
    for alert in recent_alerts:
        dept = alert.department
        if dept not in departments:
            departments[dept] = []
        departments[dept].append(alert)
    
    # Analyze each department's alerts
    for dept, alerts in departments.items():
        print(f"{dept.upper()} DEPARTMENT ({len(alerts)} alerts):")
        
        for alert in alerts:
            print(f"  📋 {alert.title}")
            print(f"     Type: {alert.alert_type} | Priority: {alert.priority}")
            print(f"     Location: {alert.location}")
            
            if alert.assigned_station_id:
                try:
                    station = Station.objects.get(station_id=alert.assigned_station_id)
                    print(f"     🏢 Assigned to: {station.name}")
                    
                    # Calculate response distance if possible
                    if alert.latitude and alert.longitude and station.latitude and station.longitude:
                        from alerts.services import StationFinderService
                        distance = StationFinderService.calculate_distance(
                            float(alert.latitude), float(alert.longitude),
                            float(station.latitude), float(station.longitude)
                        )
                        print(f"     📍 Distance: {distance:.2f} km")
                except Station.DoesNotExist:
                    print(f"     ❌ Station not found: {alert.assigned_station_id}")
            else:
                print(f"     ⚠ No station assigned")
            
            print()
        
        print("-" * 50)
    
    # Show emergency triggers
    print("\n=== Emergency Triggers ===\n")
    
    recent_triggers = EmergencyTrigger.objects.filter(
        triggered_at__gte=timezone.now() - timezone.timedelta(hours=1)
    ).order_by('-triggered_at')
    
    for trigger in recent_triggers:
        print(f"🚨 {trigger.get_trigger_type_display()} - {trigger.get_severity_display()}")
        print(f"   Device: {trigger.device.serial_number} ({trigger.device.owner_name})")
        print(f"   Value: {trigger.trigger_value} (Threshold: {trigger.threshold_value})")
        print(f"   Location: {trigger.latitude}, {trigger.longitude}")
        
        if trigger.alert_created_id:
            print(f"   ✓ Alert created: {trigger.alert_created_id}")
        else:
            print(f"   ❌ No alert created")
        
        print()

def test_user_access_to_alerts():
    """Test which users can see which alerts"""

    print("=== User Access Control Test ===\n")

    from django.utils import timezone

    users = User.objects.filter(is_active=True)
    recent_alerts = Alert.objects.filter(
        created_at__gte=timezone.now() - timezone.timedelta(hours=1)
    )
    
    for user in users:
        print(f"👤 {user.full_name} ({user.role}) - {user.department}")
        
        # Apply the same filtering logic as in the views
        if user.role == 'Admin':
            user_alerts = recent_alerts
        elif user.role == 'Station Manager':
            if user.station_id:
                user_alerts = recent_alerts.filter(
                    assigned_station_id=user.station_id
                ).union(
                    recent_alerts.filter(department=user.department)
                )
            else:
                user_alerts = recent_alerts.filter(department=user.department)
        elif user.role == 'Field Officer':
            if user.station_id:
                user_alerts = recent_alerts.filter(assigned_station_id=user.station_id)
            else:
                user_alerts = recent_alerts.filter(department=user.department)
        else:
            user_alerts = recent_alerts.none()
        
        print(f"   Can see: {user_alerts.count()} alerts")
        
        if user_alerts.exists():
            for alert in user_alerts[:3]:  # Show first 3
                print(f"     - {alert.title} ({alert.department})")
            if user_alerts.count() > 3:
                print(f"     ... and {user_alerts.count() - 3} more")
        
        print()

def main():
    """Main test function"""
    
    print("🔥 FIRE ALERT ROUTING TEST 🔥\n")
    
    # Create test device
    device = create_test_device()
    
    # Simulate fire readings (this will trigger emergency processing)
    readings = simulate_fire_readings(device)
    
    # Process readings for emergencies (simulate the automatic processing)
    print("=== Processing Readings for Emergencies ===\n")
    
    from devices.views import process_reading_for_emergencies
    
    for reading in readings:
        print(f"Processing {reading.reading_type} reading...")
        process_reading_for_emergencies(reading)
        print(f"✓ Processed reading {reading.reading_id}")
    
    print(f"\nProcessed {len(readings)} readings\n")
    
    # Analyze the results
    analyze_alert_routing()
    
    # Test user access
    test_user_access_to_alerts()
    
    print("🔥 Fire alert routing test complete! 🔥")

if __name__ == '__main__':
    main()
