#!/usr/bin/env python
"""
Script to simulate a fire emergency in Dowa, Malawi
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

def create_dowa_stations():
    """Create emergency stations in Dowa, Malawi"""
    
    print("🏥 Creating Emergency Stations in Dowa, Malawi...\n")
    
    # Dowa coordinates: approximately -13.6547° S, 33.9353° E
    dowa_stations = [
        {
            'name': 'Dowa Fire Station',
            'code': 'DFS001',
            'department': 'fire',
            'region': 'Central Malawi',
            'address': 'Dowa Boma, Central Region, Malawi',
            'latitude': Decimal('-13.6547'),
            'longitude': Decimal('33.9353'),
            'phone': '+265-1-234-5001',
        },
        {
            'name': 'Dowa Police Station',
            'code': 'DPS001', 
            'department': 'police',
            'region': 'Central Malawi',
            'address': 'Dowa Police Headquarters, Malawi',
            'latitude': Decimal('-13.6560'),
            'longitude': Decimal('33.9340'),
            'phone': '+265-1-234-5002',
        },
        {
            'name': 'Dowa District Hospital',
            'code': 'DDH001',
            'department': 'medical',
            'region': 'Central Malawi', 
            'address': 'Dowa District Hospital, Central Region, Malawi',
            'latitude': Decimal('-13.6530'),
            'longitude': Decimal('33.9370'),
            'phone': '+265-1-234-5003',
        },
        {
            'name': 'Madisi Health Center',
            'code': 'MHC001',
            'department': 'medical',
            'region': 'Central Malawi',
            'address': 'Madisi Trading Center, Dowa, Malawi', 
            'latitude': Decimal('-13.6200'),
            'longitude': Decimal('33.9100'),
            'phone': '+265-1-234-5004',
        }
    ]
    
    created_stations = []
    
    for station_data in dowa_stations:
        try:
            station, created = Station.objects.get_or_create(
                name=station_data['name'],
                defaults={
                    **station_data,
                    'is_active': True
                }
            )
            if created:
                print(f"✓ Created: {station.name}")
                print(f"  📍 Location: {station.latitude}, {station.longitude}")
                print(f"  🏢 Department: {station.department}")
                print(f"  📞 Phone: {station.phone}")
            else:
                print(f"⚠ Already exists: {station.name}")
            
            created_stations.append(station)
            print()
        except Exception as e:
            print(f"✗ Error creating {station_data['name']}: {e}")
    
    return created_stations

def create_dowa_device():
    """Create a test device for Dowa emergency simulation"""
    
    print("📱 Creating Guardian Device in Dowa...\n")
    
    # Get or create system user
    system_user, created = User.objects.get_or_create(
        username='dowa_system',
        defaults={
            'email': 'dowa@myguardian.mw',
            'full_name': 'Dowa Emergency System',
            'role': 'Admin',
            'department': 'admin',
            'is_active': True
        }
    )
    
    # Create device for a resident in Dowa
    device, created = Device.objects.get_or_create(
        serial_number='DOWA_GUARDIAN_001',
        defaults={
            'mac_address': '00:MW:DO:WA:01:23',
            'device_type': 'guardian_bracelet',
            'owner_name': 'Chisomo Banda',
            'owner_phone': '+265-999-123-456',
            'owner_address': 'Chigoneka Village, Traditional Authority Dowa, Dowa District, Central Region, Malawi',
            'emergency_contact': 'Grace Banda (Sister)',
            'emergency_contact_phone': '+265-888-654-321',
            'medical_conditions': 'Diabetes, High Blood Pressure',
            'blood_type': 'O+',
            'status': 'active',
            'battery_level': 78,
            'fire_monitoring_enabled': True,
            'heart_rate_monitoring_enabled': True,
            'registered_by_id': system_user.id
        }
    )
    
    if created:
        print(f"✓ Created Guardian device: {device.serial_number}")
    else:
        print(f"⚠ Using existing device: {device.serial_number}")
    
    print(f"👤 Owner: {device.owner_name}")
    print(f"📍 Location: {device.owner_address}")
    print(f"📞 Contact: {device.owner_phone}")
    print(f"🆘 Emergency Contact: {device.emergency_contact} ({device.emergency_contact_phone})")
    print(f"🩺 Medical Info: {device.medical_conditions}, Blood Type: {device.blood_type}")
    print()
    
    return device

def simulate_dowa_fire_emergency(device):
    """Simulate a realistic fire emergency in Dowa"""
    
    print("🔥 SIMULATING FIRE EMERGENCY IN DOWA, MALAWI 🔥\n")
    
    # Fire scenario: House fire in rural Dowa
    fire_scenario = {
        'location_name': 'Chigoneka Village, Dowa',
        'latitude': Decimal('-13.6580'),  # Near Dowa center
        'longitude': Decimal('33.9380'),  # Near Dowa center
        'scenario_description': '''
        HOUSE FIRE EMERGENCY - CHIGONEKA VILLAGE, DOWA
        
        🏠 Location: Traditional mud-brick house with thatched roof
        🔥 Cause: Cooking fire spread from kitchen area
        ⏰ Time: Evening cooking time (around 6 PM)
        👥 Occupants: Family of 6 (2 adults, 4 children)
        🚨 Status: Fire spreading rapidly due to dry thatch roof
        
        Guardian device detected:
        - Extreme temperature rise (cooking fire spread)
        - Heavy smoke from burning thatch
        - User in distress (elevated heart rate)
        
        IMMEDIATE RESPONSE NEEDED:
        🚒 Fire suppression for thatched roof fire
        🏥 Medical attention for smoke inhalation
        👮 Crowd control and evacuation assistance
        ''',
        'readings': [
            {
                'type': 'temperature',
                'value': 68.5,  # Very high temperature from house fire
                'description': 'Extreme heat from spreading house fire'
            },
            {
                'type': 'smoke',
                'value': 0.95,  # Heavy smoke from burning thatch
                'description': 'Dense smoke from thatched roof fire'
            },
            {
                'type': 'heart_rate', 
                'value': 145,  # Panic/stress response
                'description': 'Elevated heart rate due to emergency stress'
            }
        ]
    }
    
    print(fire_scenario['scenario_description'])
    print(f"📍 GPS Coordinates: {fire_scenario['latitude']}, {fire_scenario['longitude']}")
    print()
    
    # Create device readings that will trigger emergency alerts
    created_readings = []
    
    for reading_data in fire_scenario['readings']:
        print(f"📊 Creating {reading_data['type']} reading...")
        
        reading_kwargs = {
            'device': device,
            'reading_type': reading_data['type'],
            'latitude': fire_scenario['latitude'],
            'longitude': fire_scenario['longitude'],
            'raw_data': {
                'scenario': 'Dowa House Fire Emergency',
                'location': fire_scenario['location_name'],
                'description': reading_data['description'],
                'emergency_level': 'CRITICAL'
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
        
        print(f"  ✓ {reading_data['type'].title()}: {reading_data['value']}")
        print(f"  📝 {reading_data['description']}")
        print()
    
    return created_readings, fire_scenario

def process_emergency_response(readings):
    """Process the emergency readings and create alerts"""
    
    print("🚨 PROCESSING EMERGENCY RESPONSE...\n")
    
    from devices.views import process_reading_for_emergencies
    
    alerts_created = []
    
    for reading in readings:
        print(f"⚡ Processing {reading.reading_type} reading...")
        
        # Get alert count before processing
        alerts_before = Alert.objects.count()
        
        # Process the reading (this will create emergency triggers and alerts)
        process_reading_for_emergencies(reading)
        
        # Get alert count after processing
        alerts_after = Alert.objects.count()
        new_alerts = alerts_after - alerts_before
        
        print(f"  ✓ Created {new_alerts} new alerts")
        
        # Get the latest alerts (the ones just created)
        latest_alerts = Alert.objects.order_by('-created_at')[:new_alerts]
        alerts_created.extend(latest_alerts)
        
        print()
    
    return alerts_created

def analyze_dowa_emergency_response():
    """Analyze the emergency response for Dowa"""
    
    print("📋 DOWA EMERGENCY RESPONSE ANALYSIS\n")
    
    # Get recent alerts (last hour)
    from django.utils import timezone
    recent_alerts = Alert.objects.filter(
        created_at__gte=timezone.now() - timezone.timedelta(hours=1),
        location__icontains='13.658'  # Filter for Dowa coordinates
    ).order_by('-created_at')
    
    print(f"🚨 Emergency Alerts Created: {recent_alerts.count()}\n")
    
    # Group by department
    departments = {}
    for alert in recent_alerts:
        dept = alert.department
        if dept not in departments:
            departments[dept] = []
        departments[dept].append(alert)
    
    # Analyze each department's response
    for dept, alerts in departments.items():
        print(f"🏢 {dept.upper()} DEPARTMENT RESPONSE ({len(alerts)} alerts)")
        print("-" * 50)
        
        for alert in alerts:
            print(f"📋 {alert.title}")
            print(f"   🎯 Priority: {alert.priority.upper()}")
            print(f"   📍 Location: {alert.location}")
            
            if alert.assigned_station_id:
                try:
                    station = Station.objects.get(station_id=alert.assigned_station_id)
                    print(f"   🏥 Assigned Station: {station.name}")
                    print(f"   📞 Contact: {station.phone}")
                    
                    # Calculate response distance
                    if alert.latitude and alert.longitude and station.latitude and station.longitude:
                        from alerts.services import StationFinderService
                        distance = StationFinderService.calculate_distance(
                            float(alert.latitude), float(alert.longitude),
                            float(station.latitude), float(station.longitude)
                        )
                        print(f"   🚗 Response Distance: {distance:.2f} km")
                        
                        # Estimate response time (assuming 40 km/h average speed)
                        response_time_minutes = (distance / 40) * 60
                        print(f"   ⏱️ Estimated Response Time: {response_time_minutes:.1f} minutes")
                
                except Station.DoesNotExist:
                    print(f"   ❌ Station not found")
            else:
                print(f"   ⚠️ No station assigned")
            
            print()
        
        print()
    
    # Show emergency triggers
    recent_triggers = EmergencyTrigger.objects.filter(
        triggered_at__gte=timezone.now() - timezone.timedelta(hours=1),
        device__serial_number='DOWA_GUARDIAN_001'
    ).order_by('-triggered_at')
    
    print(f"🚨 EMERGENCY TRIGGERS ({recent_triggers.count()})")
    print("-" * 50)
    
    for trigger in recent_triggers:
        print(f"⚠️ {trigger.get_trigger_type_display()} - {trigger.get_severity_display()}")
        print(f"   👤 Device Owner: {trigger.device.owner_name}")
        print(f"   📊 Reading: {trigger.trigger_value} (Threshold: {trigger.threshold_value})")
        print(f"   📍 Location: {trigger.latitude}, {trigger.longitude}")
        print(f"   ⏰ Time: {trigger.triggered_at.strftime('%Y-%m-%d %H:%M:%S')}")
        
        if trigger.alert_created_id:
            print(f"   ✅ Alert Created: {trigger.alert_created_id}")
        
        print()

def main():
    """Main simulation function"""
    
    print("🇲🇼 DOWA, MALAWI FIRE EMERGENCY SIMULATION 🇲🇼\n")
    print("=" * 60)
    
    # Step 1: Create Dowa emergency infrastructure
    stations = create_dowa_stations()
    
    # Step 2: Create Guardian device for Dowa resident
    device = create_dowa_device()
    
    # Step 3: Simulate fire emergency
    readings, scenario = simulate_dowa_fire_emergency(device)
    
    # Step 4: Process emergency response
    alerts = process_emergency_response(readings)
    
    # Step 5: Analyze response
    analyze_dowa_emergency_response()
    
    print("🇲🇼 DOWA FIRE EMERGENCY SIMULATION COMPLETE 🇲🇼")
    print("=" * 60)
    print(f"📊 Summary:")
    print(f"   🏥 Stations Created: {len(stations)}")
    print(f"   📱 Device Readings: {len(readings)}")
    print(f"   🚨 Alerts Generated: {len(alerts)}")
    print(f"   🎯 Multi-department response activated for Dowa emergency")

if __name__ == '__main__':
    main()
