#!/usr/bin/env python
"""
Script to create emergency stations in Mzuzu and re-simulate fire emergency
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

from devices.models import Device, DeviceReading
from alerts.models import Alert
from geography.models import Station
from accounts.models import User

def create_mzuzu_emergency_stations():
    """Create emergency stations in Mzuzu City"""
    
    print("🏥 CREATING MZUZU EMERGENCY STATIONS")
    print("=" * 50)
    
    # Mzuzu City coordinates: -11.4600°S, 34.0200°E
    mzuzu_stations = [
        {
            'name': 'Mzuzu Fire Station',
            'code': 'MFS001',
            'department': 'fire',
            'region': 'Northern Malawi',
            'address': 'Mzuzu City Center, Northern Region, Malawi',
            'latitude': Decimal('-11.4580'),  # Very close to device
            'longitude': Decimal('34.0180'),
            'phone': '+265-1-320-001',
        },
        {
            'name': 'Mzuzu Police Station',
            'code': 'MPS001',
            'department': 'police',
            'region': 'Northern Malawi',
            'address': 'Mzuzu Police Headquarters, Northern Region, Malawi',
            'latitude': Decimal('-11.4620'),  # Very close to device
            'longitude': Decimal('34.0220'),
            'phone': '+265-1-320-002',
        },
        {
            'name': 'Mzuzu Central Hospital',
            'code': 'MCH001',
            'department': 'medical',
            'region': 'Northern Malawi',
            'address': 'Mzuzu Central Hospital, Northern Region, Malawi',
            'latitude': Decimal('-11.4590'),  # Very close to device
            'longitude': Decimal('34.0210'),
            'phone': '+265-1-320-003',
        }
    ]
    
    created_stations = []
    
    for station_data in mzuzu_stations:
        try:
            station, created = Station.objects.get_or_create(
                name=station_data['name'],
                defaults={
                    **station_data,
                    'is_active': True
                }
            )
            
            if created:
                print(f"✅ Created: {station.name}")
            else:
                print(f"⚠️ Already exists: {station.name}")
            
            print(f"   📍 Location: {station.latitude}, {station.longitude}")
            print(f"   🏢 Department: {station.department}")
            print(f"   📞 Phone: {station.phone}")
            
            # Calculate distance to device location
            device_lat = Decimal('-11.4600')
            device_lng = Decimal('34.0200')
            
            from alerts.services import StationFinderService
            distance = StationFinderService.calculate_distance(
                float(device_lat), float(device_lng),
                float(station.latitude), float(station.longitude)
            )
            
            print(f"   🚗 Distance to device: {distance:.2f} km")
            
            created_stations.append(station)
            print()
            
        except Exception as e:
            print(f"❌ Error creating {station_data['name']}: {e}")
    
    return created_stations

def simulate_mzuzu_fire_emergency():
    """Simulate fire emergency in Mzuzu with nearby stations"""
    
    print("🔥 SIMULATING MZUZU FIRE EMERGENCY WITH LOCAL STATIONS")
    print("=" * 60)
    
    # Get the device
    try:
        device = Device.objects.get(serial_number='GD-075BDF9E')
    except Device.DoesNotExist:
        print("❌ Device not found")
        return []
    
    # Mzuzu coordinates
    mzuzu_lat = Decimal('-11.4600')
    mzuzu_lng = Decimal('34.0200')
    
    print(f"📱 Device: {device.serial_number} ({device.owner_name})")
    print(f"📍 Location: {mzuzu_lat}, {mzuzu_lng} (Mzuzu City)")
    print(f"🏠 Address: {device.owner_address}")
    print()
    
    # Fire emergency readings
    fire_readings = [
        {
            'type': 'temperature',
            'value': 78.0,  # Very high temperature
            'description': 'Critical fire temperature in Mzuzu residence'
        },
        {
            'type': 'smoke',
            'value': 0.90,  # Heavy smoke
            'description': 'Dense smoke from house fire in Mzuzu'
        },
        {
            'type': 'heart_rate',
            'value': 165,  # Extreme heart rate
            'description': 'Severe panic response to fire emergency'
        }
    ]
    
    created_readings = []
    
    print("📊 CREATING EMERGENCY READINGS:")
    print("-" * 40)
    
    for reading_data in fire_readings:
        reading_kwargs = {
            'device': device,
            'reading_type': reading_data['type'],
            'latitude': mzuzu_lat,
            'longitude': mzuzu_lng,
            'raw_data': {
                'serial_number': device.serial_number,
                'owner_name': device.owner_name,
                'location': 'Mzuzu City, Northern Malawi',
                'emergency_level': 'CRITICAL',
                'scenario': 'Mzuzu House Fire with Local Stations',
                'description': reading_data['description']
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
        
        print(f"✅ {reading_data['type'].title()}: {reading_data['value']}")
        print(f"   📝 {reading_data['description']}")
        print()
    
    return created_readings

def process_mzuzu_emergency(readings):
    """Process the Mzuzu emergency readings"""
    
    print("🚨 PROCESSING MZUZU EMERGENCY WITH LOCAL STATIONS")
    print("=" * 60)
    
    from devices.views import process_reading_for_emergencies
    
    alerts_before = Alert.objects.count()
    
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
    new_alerts = alerts_after - alerts_before
    
    print(f"📊 EMERGENCY PROCESSING RESULTS:")
    print(f"  🚨 New Alerts Created: {new_alerts}")
    print()

def analyze_mzuzu_response():
    """Analyze the Mzuzu emergency response"""
    
    print("📋 MZUZU EMERGENCY RESPONSE ANALYSIS")
    print("=" * 60)
    
    # Get very recent alerts (last 3 minutes)
    from django.utils import timezone
    recent_alerts = Alert.objects.filter(
        created_at__gte=timezone.now() - timezone.timedelta(minutes=3),
        location__icontains='-11.46'  # Filter for Mzuzu coordinates
    ).order_by('-created_at')
    
    print(f"🚨 Recent Mzuzu Emergency Alerts: {recent_alerts.count()}")
    print()
    
    if not recent_alerts.exists():
        print("❌ No recent alerts found for Mzuzu location")
        return
    
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
                    
                    # Calculate response details
                    if alert.latitude and alert.longitude and station.latitude and station.longitude:
                        from alerts.services import StationFinderService
                        distance = StationFinderService.calculate_distance(
                            float(alert.latitude), float(alert.longitude),
                            float(station.latitude), float(station.longitude)
                        )
                        print(f"   🚗 Response Distance: {distance:.2f} km")
                        
                        # Estimate response time (40 km/h average)
                        response_time_minutes = (distance / 40) * 60
                        print(f"   ⏱️ Estimated Response Time: {response_time_minutes:.1f} minutes")
                        
                        # Response status
                        if distance < 5:
                            print(f"   🟢 EXCELLENT - Very close response")
                        elif distance < 15:
                            print(f"   🟡 GOOD - Reasonable response distance")
                        else:
                            print(f"   🔴 POOR - Long response distance")
                
                except Station.DoesNotExist:
                    print(f"   ❌ Station not found: {alert.assigned_station_id}")
            else:
                print(f"   ⚠️ No station assigned")
            
            print()

def main():
    """Main function"""
    
    print("🏥 MZUZU EMERGENCY STATIONS & FIRE SIMULATION")
    print("=" * 70)
    print()
    
    # Step 1: Create Mzuzu emergency stations
    stations = create_mzuzu_emergency_stations()
    
    # Step 2: Simulate fire emergency in Mzuzu
    readings = simulate_mzuzu_fire_emergency()
    
    # Step 3: Process emergency response
    process_mzuzu_emergency(readings)
    
    # Step 4: Analyze response
    analyze_mzuzu_response()
    
    print("🔥 MZUZU FIRE EMERGENCY SIMULATION COMPLETE 🔥")
    print("=" * 70)
    print(f"🏥 Mzuzu Stations Created: {len(stations)}")
    print(f"📊 Emergency Readings: {len(readings)}")
    print(f"📍 Location: Mzuzu City, Northern Malawi (-11.46°S, 34.02°E)")
    print()
    print("🌐 View alerts at: http://localhost:3000/dashboard/alerts")
    print()
    print("🎯 Expected Results:")
    print("   ✅ Alerts should now be assigned to nearby Mzuzu stations")
    print("   ✅ Response distances should be < 5 km")
    print("   ✅ Response times should be < 10 minutes")

if __name__ == '__main__':
    main()
