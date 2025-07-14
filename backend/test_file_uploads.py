#!/usr/bin/env python
import os
import sys
import django
from django.core.files.uploadedfile import SimpleUploadedFile

# Add the project directory to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'emergency_system.settings')
django.setup()

from django.conf import settings
from accounts.models import RegistrationRequest
from devices.models import DepartmentRegistration, DeviceReading, Device
from accounts.models import User

def test_file_uploads():
    """Test file upload functionality on localhost"""
    print("📁 Testing File Upload System")
    print("=" * 60)
    
    # Check current settings
    print(f"🔧 Current Configuration:")
    print(f"   DEBUG: {settings.DEBUG}")
    print(f"   MEDIA_URL: {settings.MEDIA_URL}")
    print(f"   MEDIA_ROOT: {settings.MEDIA_ROOT}")
    print()
    
    # Create media directories if they don't exist
    media_dirs = [
        'registration_docs',
        'department_docs', 
        'audio_samples'
    ]
    
    for dir_name in media_dirs:
        dir_path = os.path.join(settings.MEDIA_ROOT, dir_name)
        os.makedirs(dir_path, exist_ok=True)
        print(f"📂 Created directory: {dir_path}")
    
    print()
    
    # Test 1: Registration Request with Document
    print("1️⃣ Testing Registration Request File Upload")
    print("-" * 50)
    
    # Create a test file
    test_content = b"This is a test PDF document content"
    test_file = SimpleUploadedFile(
        "test_certificate.pdf",
        test_content,
        content_type="application/pdf"
    )
    
    try:
        registration = RegistrationRequest.objects.create(
            registration_type='organization',
            organization_name='Test Fire Department',
            department='fire',
            region='central',
            full_name='John Test',
            email='john@test.com',
            phone_number='+1234567890',
            address='123 Test St',
            latitude=40.7128,
            longitude=-74.0060,
            documentation=test_file
        )
        
        print(f"✅ Registration created: {registration.registration_id}")
        print(f"   File path: {registration.documentation.name}")
        print(f"   File URL: http://localhost:8000{registration.documentation.url}")
        print(f"   File exists: {os.path.exists(registration.documentation.path)}")
        
    except Exception as e:
        print(f"❌ Registration failed: {e}")
    
    print()
    
    # Test 2: Department Registration
    print("2️⃣ Testing Department Registration File Upload")
    print("-" * 50)
    
    license_file = SimpleUploadedFile(
        "department_license.pdf",
        b"Department license document content",
        content_type="application/pdf"
    )
    
    try:
        dept_registration = DepartmentRegistration.objects.create(
            department_name='Test Emergency Services',
            department_type='fire',
            registration_number='DEPT-TEST123',
            contact_person='Jane Manager',
            contact_email='jane@test.com',
            contact_phone='+1234567891',
            address='456 Emergency Ave',
            city='Test City',
            state='Test State',
            zip_code='12345',
            coverage_description='Test coverage area',
            population_served=25000,
            regional_manager_name='Bob Regional',
            regional_manager_email='bob@test.com',
            regional_manager_phone='+1234567892',
            regional_manager_credentials='Fire Chief',
            license_document=license_file
        )
        
        print(f"✅ Department registration created: {dept_registration.registration_id}")
        print(f"   License file: {dept_registration.license_document.name}")
        print(f"   License URL: http://localhost:8000{dept_registration.license_document.url}")
        print(f"   File exists: {os.path.exists(dept_registration.license_document.path)}")
        
    except Exception as e:
        print(f"❌ Department registration failed: {e}")
    
    print()
    
    # Test 3: Audio File Upload (Device Reading)
    print("3️⃣ Testing Audio File Upload")
    print("-" * 50)
    
    # Create a test device first
    try:
        user = User.objects.filter(role='System Administrator').first()
        if not user:
            user = User.objects.create(
                username='test_user',
                email='test@test.com',
                full_name='Test User',
                role='System Administrator',
                department='admin'
            )
        
        device, created = Device.objects.get_or_create(
            mac_address='00:11:22:33:44:55',
            defaults={
                'device_name': 'Test Device',
                'device_type': 'bracelet',
                'assigned_user': user,
                'status': 'active'
            }
        )
        
        audio_file = SimpleUploadedFile(
            "test_audio.wav",
            b"Fake audio file content",
            content_type="audio/wav"
        )
        
        reading = DeviceReading.objects.create(
            device=device,
            reading_type='audio',
            heart_rate=75,
            battery_level=85,
            latitude=40.7128,
            longitude=-74.0060,
            audio_file=audio_file
        )
        
        print(f"✅ Audio reading created: {reading.reading_id}")
        print(f"   Audio file: {reading.audio_file.name}")
        print(f"   Audio URL: http://localhost:8000{reading.audio_file.url}")
        print(f"   File exists: {os.path.exists(reading.audio_file.path)}")
        
    except Exception as e:
        print(f"❌ Audio upload failed: {e}")
    
    print()
    
    # Test 4: List all uploaded files
    print("4️⃣ Current Uploaded Files")
    print("-" * 50)
    
    media_root = settings.MEDIA_ROOT
    if os.path.exists(media_root):
        for root, dirs, files in os.walk(media_root):
            for file in files:
                file_path = os.path.join(root, file)
                relative_path = os.path.relpath(file_path, media_root)
                file_url = f"http://localhost:8000/media/{relative_path.replace(os.sep, '/')}"
                file_size = os.path.getsize(file_path)
                print(f"   📄 {relative_path} ({file_size} bytes)")
                print(f"      URL: {file_url}")
    else:
        print("   No media directory found")
    
    print()
    print("🎉 File upload testing complete!")
    print()
    print("💡 To test in browser:")
    print("   1. Start Django server: python manage.py runserver")
    print("   2. Visit file URLs in browser")
    print("   3. Try registration form with file upload")
    
    return True

if __name__ == "__main__":
    test_file_uploads()
