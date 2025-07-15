#!/usr/bin/env python
"""
Script to test emergency routing for Rumphi (no local stations) and analyze closest station detection
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
from alerts.services import StationFinderService
from accounts.models import User

def analyze_station_detection_algorithm():
    """Analyze how the system detects the closest station"""
    
    print("🔍 STATION DETECTION ALGORITHM ANALYSIS")
    print("=" * 60)
    
    print("📋 HOW THE SYSTEM FINDS THE CLOSEST STATION:")
    print("-" * 50)
    
    print("1. 🎯 DISTANCE CALCULATION:")
    print("   • Uses Haversine formula for great-circle distance")
    print("   • Accounts for Earth's curvature")
    print("   • Formula: d = 2r × arcsin(√(sin²(Δφ/2) + cos(φ1)cos(φ2)sin²(Δλ/2)))")
    print("   • Where: φ = latitude, λ = longitude, r = Earth radius (6371 km)")
    print()
    
    print("2. 🏥 STATION FILTERING:")
    print("   • Filters by department (fire/police/medical)")
    print("   • Only includes active stations (is_active=True)")
    print("   • Requires valid coordinates (lat/lng not null)")
    print()
    
    print("3. 📊 DISTANCE SORTING:")
    print("   • Calculates distance to all matching stations")
    print("   • Sorts by distance (nearest first)")
    print("   • Returns the closest station")
    print()
    
    print("4. ⚠️ DISTANCE LIMITS:")
    print("   • Let's check if there are any distance limits...")
    
    # Check the StationFinderService code
    import inspect
    source = inspect.getsource(StationFinderService.find_nearest_station)
    
    if "distance" in source and (">" in source or "<" in source):
        print("   • ✅ Distance limits may be implemented")
    else:
        print("   • ❌ No obvious distance limits found in code")
    
    print()

def test_rumphi_emergency():
    """Test emergency response for Rumphi district"""
    
    print("🏔️ RUMPHI EMERGENCY RESPONSE TEST")
    print("=" * 60)
    
    # Rumphi coordinates (Northern Malawi, near Mzuzu)
    rumphi_lat = Decimal('-10.9000')  # Rumphi District
    rumphi_lng = Decimal('33.8500')
    
    print(f"📍 Test Location: Rumphi District")
    print(f"🗺️ Coordinates: {rumphi_lat}, {rumphi_lng}")
    print(f"🌍 Region: Northern Malawi")
    print()
    
    # Create test device for Rumphi
    system_user, _ = User.objects.get_or_create(
        username='rumphi_system',
        defaults={
            'email': 'rumphi@test.com',
            'full_name': 'Rumphi Test User',
            'role': 'Admin',
            'department': 'admin',
            'is_active': True
        }
    )
    
    device, created = Device.objects.get_or_create(
        serial_number='RUMPHI_TEST_001',
        defaults={
            'mac_address': '00:RP:HI:01:23:45',
            'device_type': 'guardian_bracelet',
            'owner_name': 'Rumphi Resident',
            'owner_phone': '+265-888-RUMPHI',
            'owner_address': 'Rumphi District, Northern Region, Malawi',
            'emergency_contact': 'Family Member',
            'emergency_contact_phone': '+265-999-FAMILY',
            'medical_conditions': 'None',
            'status': 'active',
            'battery_level': 67,
            'fire_monitoring_enabled': True,
            'heart_rate_monitoring_enabled': True,
            'registered_by_id': system_user.id
        }
    )
    
    if created:
        print(f"✅ Created test device: {device.serial_number}")
    else:
        print(f"📱 Using existing device: {device.serial_number}")
    
    print(f"👤 Owner: {device.owner_name}")
    print(f"📍 Location: {device.owner_address}")
    print()
    
    return device, rumphi_lat, rumphi_lng

def find_closest_stations_to_rumphi(lat, lng):
    """Find the closest stations to Rumphi for each department"""
    
    print("🔍 FINDING CLOSEST STATIONS TO RUMPHI")
    print("=" * 60)
    
    departments = ['fire', 'police', 'medical']
    
    for dept in departments:
        print(f"\n🏢 {dept.upper()} DEPARTMENT:")
        print("-" * 40)
        
        # Get all active stations for this department
        stations = Station.objects.filter(
            department=dept,
            is_active=True,
            latitude__isnull=False,
            longitude__isnull=False
        )
        
        if not stations.exists():
            print(f"   ❌ No {dept} stations found")
            continue
        
        # Calculate distances to all stations
        stations_with_distance = []
        for station in stations:
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
        
        print(f"   📊 Found {len(stations_with_distance)} stations")
        print()
        
        # Show top 3 closest stations
        for i, item in enumerate(stations_with_distance[:3]):
            station = item['station']
            distance = item['distance']
            
            rank = "🥇" if i == 0 else "🥈" if i == 1 else "🥉"
            
            print(f"   {rank} {station.name}")
            print(f"      📍 Distance: {distance:.2f} km")
            print(f"      🗺️ Location: {station.latitude}, {station.longitude}")
            print(f"      📧 Address: {station.address}")
            print(f"      📞 Phone: {station.phone}")
            
            if station.manager:
                print(f"      👤 Manager: {station.manager.full_name}")
            
            # Response time estimate
            response_time = (distance / 40) * 60  # 40 km/h average speed
            print(f"      ⏱️ Est. Response Time: {response_time:.1f} minutes")
            
            # Distance assessment
            if distance < 50:
                status = "🟢 REASONABLE"
            elif distance < 100:
                status = "🟡 DISTANT"
            else:
                status = "🔴 VERY FAR"
            
            print(f"      📊 Assessment: {status}")
            print()
        
        # Test the actual station finder service
        print(f"   🔧 TESTING StationFinderService.find_nearest_station():")
        nearest = StationFinderService.find_nearest_station(
            float(lat), float(lng), dept
        )
        
        if nearest:
            distance = StationFinderService.calculate_distance(
                float(lat), float(lng),
                float(nearest.latitude), float(nearest.longitude)
            )
            print(f"   ✅ Service returned: {nearest.name} ({distance:.2f} km)")
        else:
            print(f"   ❌ Service returned: None (no station found)")
        
        print()

def simulate_rumphi_fire_emergency(device, lat, lng):
    """Simulate a fire emergency in Rumphi"""
    
    print("🔥 SIMULATING RUMPHI FIRE EMERGENCY")
    print("=" * 60)
    
    print(f"📱 Device: {device.serial_number} ({device.owner_name})")
    print(f"📍 Location: {lat}, {lng} (Rumphi District)")
    print(f"🏠 Address: {device.owner_address}")
    print()
    
    # Create fire emergency readings
    fire_readings = [
        {
            'type': 'temperature',
            'value': 82.0,  # Very high temperature
            'description': 'Critical fire in Rumphi - no local stations'
        },
        {
            'type': 'smoke',
            'value': 0.95,  # Heavy smoke
            'description': 'Dense smoke in remote Rumphi location'
        }
    ]
    
    created_readings = []
    
    print("📊 CREATING EMERGENCY READINGS:")
    print("-" * 40)
    
    for reading_data in fire_readings:
        reading_kwargs = {
            'device': device,
            'reading_type': reading_data['type'],
            'latitude': lat,
            'longitude': lng,
            'raw_data': {
                'serial_number': device.serial_number,
                'owner_name': device.owner_name,
                'location': 'Rumphi District, Northern Malawi',
                'emergency_level': 'CRITICAL',
                'scenario': 'Remote Rumphi Fire - Testing Distance Limits',
                'description': reading_data['description']
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
    
    return created_readings

def process_rumphi_emergency(readings):
    """Process the Rumphi emergency and see where alerts get assigned"""
    
    print("🚨 PROCESSING RUMPHI EMERGENCY")
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

def analyze_rumphi_assignments():
    """Analyze where Rumphi alerts were assigned"""
    
    print("📋 RUMPHI ALERT ASSIGNMENT ANALYSIS")
    print("=" * 60)
    
    # Get very recent alerts
    from django.utils import timezone
    recent_alerts = Alert.objects.filter(
        created_at__gte=timezone.now() - timezone.timedelta(minutes=2),
        location__icontains='-10.9'  # Rumphi coordinates
    ).order_by('-created_at')
    
    print(f"🚨 Recent Rumphi Alerts: {recent_alerts.count()}")
    print()
    
    if not recent_alerts.exists():
        print("❌ No recent alerts found for Rumphi")
        return
    
    for alert in recent_alerts:
        print(f"📋 {alert.title}")
        print(f"   🎯 Priority: {alert.priority.upper()}")
        print(f"   🏢 Department: {alert.department.upper()}")
        print(f"   📍 Location: {alert.location}")
        print(f"   ⏰ Created: {alert.created_at.strftime('%H:%M:%S')}")
        
        if alert.assigned_station_id:
            try:
                station = Station.objects.get(station_id=alert.assigned_station_id)
                print(f"   🏥 ✅ ASSIGNED TO: {station.name}")
                print(f"   📧 Station Address: {station.address}")
                print(f"   📞 Contact: {station.phone}")
                
                # Calculate actual distance
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
            print(f"   🤔 Possible reasons:")
            print(f"      • No stations within maximum distance limit")
            print(f"      • Station finder service failed")
            print(f"      • All stations are inactive")
        
        print()

def main():
    """Main function"""
    
    print("🏔️ RUMPHI EMERGENCY ROUTING ANALYSIS")
    print("=" * 70)
    print()
    
    # Step 1: Analyze the station detection algorithm
    analyze_station_detection_algorithm()
    
    # Step 2: Set up Rumphi test
    device, lat, lng = test_rumphi_emergency()
    
    # Step 3: Find closest stations to Rumphi
    find_closest_stations_to_rumphi(lat, lng)
    
    # Step 4: Simulate fire emergency in Rumphi
    readings = simulate_rumphi_fire_emergency(device, lat, lng)
    
    # Step 5: Process emergency
    process_rumphi_emergency(readings)
    
    # Step 6: Analyze assignments
    analyze_rumphi_assignments()
    
    print("🏔️ RUMPHI EMERGENCY ANALYSIS COMPLETE")
    print("=" * 70)
    print()
    print("🎯 KEY FINDINGS:")
    print("   • Shows which stations are closest to Rumphi")
    print("   • Tests if distance limits prevent assignment")
    print("   • Reveals how the system handles remote locations")
    print("   • Demonstrates need for regional emergency coverage")

if __name__ == '__main__':
    main()
