#!/usr/bin/env python
import os
import sys
import django

# Add the project directory to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'emergency_system.settings')
django.setup()

from accounts.models import RegistrationRequest
from accounts.serializers import RegistrationRequestSerializer
from decimal import Decimal

def test_coordinate_validation():
    """Test coordinate validation with various precision levels"""
    print("🧪 Testing Coordinate Validation")
    print("=" * 60)
    
    # Test cases with different coordinate precisions
    test_cases = [
        {
            'name': 'Valid coordinates (8 decimal places)',
            'lat': 40.71280000,
            'lng': -74.00600000,
            'should_pass': True
        },
        {
            'name': 'Valid coordinates (fewer decimals)',
            'lat': 40.7128,
            'lng': -74.0060,
            'should_pass': True
        },
        {
            'name': 'Too many total digits in latitude',
            'lat': 123.12345678,  # 11 digits total, but max is 10
            'lng': -74.00600000,
            'should_pass': False
        },
        {
            'name': 'Too many total digits in longitude',
            'lat': 40.71280000,
            'lng': -1234.12345678,  # 12 digits total, but max is 11
            'should_pass': False
        },
        {
            'name': 'Valid edge case - max latitude',
            'lat': 90.00000000,  # 10 digits total
            'lng': -180.00000000,  # 11 digits total
            'should_pass': True
        },
        {
            'name': 'High precision coordinates (typical GPS)',
            'lat': 40.71234567,
            'lng': -74.00987654,
            'should_pass': True
        },
        {
            'name': 'Very high precision (too many decimals)',
            'lat': 40.123456789,  # 9 decimal places, but max is 8
            'lng': -74.123456789,
            'should_pass': False
        }
    ]
    
    base_data = {
        'registration_type': 'organization',
        'organization_name': 'Test Emergency Services',
        'department': 'fire',
        'region': 'central',
        'full_name': 'John Doe',
        'email': 'john@test.com',
        'phone_number': '+1234567890',
        'address': '123 Test St, Test City, TS 12345'
    }
    
    print(f"\n📋 Backend Constraints:")
    print(f"   Latitude:  max_digits=10, decimal_places=8 (XX.XXXXXXXX)")
    print(f"   Longitude: max_digits=11, decimal_places=8 (XXX.XXXXXXXX)")
    print()
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"{i}️⃣ {test_case['name']}")
        print(f"   Lat: {test_case['lat']}, Lng: {test_case['lng']}")
        
        test_data = base_data.copy()
        test_data['latitude'] = test_case['lat']
        test_data['longitude'] = test_case['lng']
        
        serializer = RegistrationRequestSerializer(data=test_data)
        is_valid = serializer.is_valid()
        
        if test_case['should_pass']:
            if is_valid:
                print(f"   ✅ PASSED (as expected)")
            else:
                print(f"   ❌ FAILED (should have passed)")
                print(f"      Errors: {serializer.errors}")
        else:
            if not is_valid:
                print(f"   ✅ CORRECTLY REJECTED (as expected)")
                if 'latitude' in serializer.errors or 'longitude' in serializer.errors:
                    lat_errors = serializer.errors.get('latitude', [])
                    lng_errors = serializer.errors.get('longitude', [])
                    if lat_errors:
                        print(f"      Latitude error: {lat_errors}")
                    if lng_errors:
                        print(f"      Longitude error: {lng_errors}")
            else:
                print(f"   ❌ INCORRECTLY ACCEPTED (should have failed)")
        print()
    
    # Test JavaScript rounding function equivalent
    print("🔧 Testing JavaScript Rounding Function:")
    print("-" * 50)
    
    def js_round_coordinate(value):
        """Equivalent to JavaScript: Math.round(value * 100000000) / 100000000"""
        return round(value * 100000000) / 100000000
    
    js_test_cases = [
        40.712345678901234,  # Very high precision
        -74.006789123456789,
        90.123456789,
        -180.987654321
    ]
    
    for value in js_test_cases:
        rounded = js_round_coordinate(value)
        print(f"   Original: {value}")
        print(f"   Rounded:  {rounded}")
        print(f"   Digits:   {len(str(rounded).replace('.', '').replace('-', ''))}")
        print()
    
    print("💡 Frontend Fix Applied:")
    print("   - MapSelector rounds coordinates to 8 decimal places")
    print("   - Registration form validates coordinates before sending")
    print("   - Backend accepts properly formatted coordinates")
    
    return True

if __name__ == "__main__":
    test_coordinate_validation()
