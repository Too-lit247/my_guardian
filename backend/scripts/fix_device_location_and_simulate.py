#!/usr/bin/env python
"""
Script to fix device location to realistic Mzuzu coordinates and re-simulate fire emergency
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

def fix_device_coordinates():
    """Update device coordinates to realistic Mzuzu, Malawi location"""
    
    print("🔧 FIXING DEVICE COORDINATES")
    print("=" * 50)
    
    # Realistic Mzuzu City coordinates
    mzuzu_lat = Decimal('-11.4600')  # Mzuzu latitude
    mzuzu_lng = Decimal('34.0200')   # Mzuzu longitude
    
    try:
        device = Device.objects.get(serial_number='GD-075BDF9E')
        
        print(f"📱 Device: {device.serial_number} ({device.owner_name})")
        print(f"📍 Old Location: {device.last_known_latitude}, {device.last_known_longitude}")
        print(f"📍 New Location: {mzuzu_lat}, {mzuzu_lng}")
        print(f"🏠 Address: {device.owner_address}")
        print()
        
        # Update device coordinates (we don't have these fields in the model, so we'll use them in readings)
        print("✅ Device coordinates will be updated in new readings")
        
        return device, mzuzu_lat, mzuzu_lng
        
    except Device.DoesNotExist:
        print("❌ Device GD-075BDF9E not found")
        return None, None, None

def show_nearby_stations(lat, lng):
    """Show stations near the corrected coordinates"""
    
    print("🏥 NEARBY EMERGENCY STATIONS")
    print("=" * 50)
    
    from alerts.services import StationFinderService
    
    # Find stations for each department
    departments = ['fire', 'police', 'medical']
    
    for dept in departments:
        print(f"\n🏢 {dept.upper()} DEPARTMENT:")
        print("-" * 30)
        
        # Get all stations for this department
        dept_stations = Station.objects.filter(department=dept, is_active=True)
        
        if not dept_stations.exists():
            print(f"   ❌ No {dept} stations found")
            continue
        
        # Calculate distances
        stations_with_distance = []
        for station in dept_stations:
            if station.latitude and station.longitude:
                distance = StationFinderService.calculate_distance(
                    float(lat), float(lng),
                    float(station.latitude), float(station.longitude)
                )
                stations_with_distance.append({
                    'station': station,
                    'distance': distance
                })
        
        # Sort by distance
        stations_with_distance.sort(key=lambda x: x['distance'])
        
        # Show nearest stations
        for i, item in enumerate(stations_with_distance[:3]):  # Show top 3
            station = item['station']
            distance = item['distance']
            
            rank = "🥇" if i == 0 else "🥈" if i == 1 else "🥉"
            
            print(f"   {rank} {station.name}")
            print(f"      📍 Distance: {distance:.2f} km")
            print(f"      📧 Address: {station.address}")
            print(f"      📞 Phone: {station.phone}")
            if station.manager:
                print(f"      👤 Manager: {station.manager.full_name}")
            print()

def simulate_corrected_fire_emergency(device, lat, lng):
    """Simulate fire emergency with corrected coordinates"""
    
    print("🔥 SIMULATING FIRE EMERGENCY - CORRECTED LOCATION")
    print("=" * 60)
    
    print(f"📱 Device: {device.serial_number} ({device.owner_name})")
    print(f"📍 Corrected Location: {lat}, {lng}")
    print(f"🏠 Address: {device.owner_address}")
    print(f"📞 Contact: {device.owner_phone}")
    print()
    
    # Fire emergency scenario for Mzuzu
    fire_scenario = {
        'description': f"""
🔥 HOUSE FIRE EMERGENCY - MZUZU CITY, MALAWI

📱 Device: {device.serial_number} ({device.owner_name})
📍 Location: {lat}, {lng} (Mzuzu City)
🏠 Address: {device.owner_address}
📞 Contact: {device.owner_phone}

🚨 EMERGENCY SITUATION:
- Structure fire in residential area of Mzuzu
- High temperature and smoke detected
- Occupant in distress (elevated heart rate)

⚠️ IMMEDIATE RESPONSE REQUIRED:
🚒 Fire suppression for residential fire
🏥 Medical attention for smoke inhalation
👮 Emergency coordination and traffic control
        """,
        'readings': [
            {
                'type': 'temperature',
                'value': 75.0,  # Very high temperature
                'description': 'Extreme heat from house fire in Mzuzu'
            },
            {
                'type': 'smoke',
                'value': 0.88,  # Heavy smoke
                'description': 'Dense smoke from residential fire'
            },
            {
                'type': 'heart_rate',
                'value': 160,  # Very high heart rate
                'description': 'Extreme panic response to fire emergency'
            }
        ]
    }
    
    print(fire_scenario['description'])
    print()
    
    # Create device readings with corrected coordinates
    created_readings = []
    
    for reading_data in fire_scenario['readings']:
        print(f"📊 Creating {reading_data['type']} reading...")
        
        reading_kwargs = {
            'device': device,
            'reading_type': reading_data['type'],
            'latitude': lat,
            'longitude': lng,
            'raw_data': {
                'device_id': str(device.device_id) if hasattr(device, 'device_id') else 'N/A',
                'serial_number': device.serial_number,
                'owner_name': device.owner_name,
                'owner_address': device.owner_address,
                'emergency_level': 'CRITICAL',
                'scenario': 'Mzuzu House Fire Emergency',
                'description': reading_data['description'],
                'corrected_location': True,
                'original_location': 'Fixed from -59.89, -67.68'
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

def process_corrected_emergency(readings):
    """Process the emergency with corrected coordinates"""
    
    print("🚨 PROCESSING CORRECTED EMERGENCY RESPONSE")
    print("=" * 60)
    
    from devices.views import process_reading_for_emergencies
    
    alerts_before = Alert.objects.count()
    triggers_before = EmergencyTrigger.objects.count()
    
    for reading in readings:
        print(f"⚡ Processing {reading.reading_type} reading...")
        print(f"   📍 Location: {reading.latitude}, {reading.longitude}")
        
        try:
            process_reading_for_emergencies(reading)
            print(f"  ✅ Processed successfully")
        except Exception as e:
            print(f"  ❌ Error: {e}")
        
        print()
    
    alerts_after = Alert.objects.count()
    triggers_after = EmergencyTrigger.objects.count()
    
    new_alerts = alerts_after - alerts_before
    new_triggers = triggers_after - triggers_before
    
    print(f"📊 EMERGENCY PROCESSING RESULTS:")
    print(f"  🚨 New Alerts Created: {new_alerts}")
    print(f"  ⚠️ New Triggers Created: {new_triggers}")
    print()

def analyze_corrected_response():
    """Analyze the emergency response with corrected coordinates"""
    
    print("📋 CORRECTED EMERGENCY RESPONSE ANALYSIS")
    print("=" * 60)
    
    # Get very recent alerts (last 5 minutes)
    from django.utils import timezone
    recent_alerts = Alert.objects.filter(
        created_at__gte=timezone.now() - timezone.timedelta(minutes=5)
    ).order_by('-created_at')
    
    print(f"🚨 Recent Emergency Alerts: {recent_alerts.count()}")
    print()
    
    # Group by department
    departments = {}
    for alert in recent_alerts:
        dept = alert.department
        if dept not in departments:
            departments[dept] = []
        departments[dept].append(alert)
    
    # Analyze each department's response
    for dept, alerts in departments.items():
        print(f"🏢 {dept.upper()} DEPARTMENT ({len(alerts)} alerts)")
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
                    print(f"   📞 Contact: {station.phone}")
                    
                    if station.manager:
                        print(f"   👤 Manager: {station.manager.full_name}")
                    
                    # Calculate response distance
                    if alert.latitude and alert.longitude and station.latitude and station.longitude:
                        from alerts.services import StationFinderService
                        distance = StationFinderService.calculate_distance(
                            float(alert.latitude), float(alert.longitude),
                            float(station.latitude), float(station.longitude)
                        )
                        print(f"   🚗 Response Distance: {distance:.2f} km")
                        
                        # Estimate response time
                        response_time_minutes = (distance / 40) * 60
                        print(f"   ⏱️ Estimated Response Time: {response_time_minutes:.1f} minutes")
                
                except Station.DoesNotExist:
                    print(f"   ❌ Station not found: {alert.assigned_station_id}")
            else:
                print(f"   ⚠️ No station assigned")
            
            print()

def main():
    """Main function"""
    
    print("🔧 DEVICE LOCATION FIX & FIRE EMERGENCY RE-SIMULATION")
    print("=" * 70)
    print()
    
    # Step 1: Fix device coordinates
    device, lat, lng = fix_device_coordinates()
    
    if not device:
        print("❌ Cannot proceed without device")
        return
    
    # Step 2: Show nearby stations
    show_nearby_stations(lat, lng)
    
    # Step 3: Simulate fire emergency with corrected coordinates
    readings = simulate_corrected_fire_emergency(device, lat, lng)
    
    # Step 4: Process emergency response
    process_corrected_emergency(readings)
    
    # Step 5: Analyze response
    analyze_corrected_response()
    
    print("🔥 CORRECTED FIRE EMERGENCY SIMULATION COMPLETE 🔥")
    print("=" * 70)
    print(f"📱 Device: {device.serial_number} ({device.owner_name})")
    print(f"📍 Corrected Location: {lat}, {lng} (Mzuzu City, Malawi)")
    print(f"📊 Readings Created: {len(readings)}")
    print()
    print("🌐 View updated alerts at: http://localhost:3000/dashboard/alerts")

if __name__ == '__main__':
    main()
