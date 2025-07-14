from rest_framework import serializers
from .models import Device, DeviceReading, EmergencyTrigger, DepartmentRegistration

class DeviceSerializer(serializers.ModelSerializer):
    is_online = serializers.ReadOnlyField()
    
    class Meta:
        model = Device
        fields = [
            'device_id', 'mac_address', 'serial_number', 'device_type',
            'owner_name', 'owner_phone', 'owner_address', 'emergency_contact',
            'emergency_contact_phone', 'medical_conditions', 'medications',
            'allergies', 'blood_type', 'status', 'battery_level', 'last_heartbeat',
            'firmware_version', 'last_known_latitude', 'last_known_longitude',
            'last_location_update', 'audio_monitoring_enabled', 
            'heart_rate_monitoring_enabled', 'fire_monitoring_enabled',
            'fall_detection_enabled', 'monitoring_interval', 'registered_at', 'is_online'
        ]
        read_only_fields = ['device_id', 'registered_at', 'is_online']

class DeviceReadingSerializer(serializers.ModelSerializer):
    device_serial = serializers.CharField(source='device.serial_number', read_only=True)
    
    class Meta:
        model = DeviceReading
        fields = [
            'reading_id', 'device', 'device_serial', 'reading_type', 'timestamp', 
            'heart_rate', 'temperature', 'smoke_level', 'battery_level', 'latitude',
            'longitude', 'audio_file', 'fear_probability', 'stress_level',
            'audio_analysis_complete', 'is_emergency', 'triggered_by', 'raw_data'
        ]
        read_only_fields = ['reading_id', 'timestamp']

class EmergencyTriggerSerializer(serializers.ModelSerializer):
    device_info = serializers.SerializerMethodField()
    
    class Meta:
        model = EmergencyTrigger
        fields = [
            'trigger_id', 'device', 'device_info', 'trigger_type', 'severity',
            'trigger_value', 'threshold_value', 'latitude', 'longitude',
            'alert_created_id', 'acknowledged', 'acknowledged_by_id', 'acknowledged_at',
            'triggered_at', 'resolved_at'
        ]
        read_only_fields = ['trigger_id', 'triggered_at']
    
    def get_device_info(self, obj):
        return {
            'owner_name': obj.device.owner_name,
            'owner_phone': obj.device.owner_phone,
            'serial_number': obj.device.serial_number
        }

class DepartmentRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = DepartmentRegistration
        fields = [
            'registration_id', 'department_name', 'department_type', 'registration_number',
            'contact_person', 'contact_email', 'contact_phone', 'address',
            'city', 'state', 'zip_code', 'country', 'coverage_description',
            'population_served', 'license_document', 'insurance_document',
            'additional_documents', 'regional_manager_name', 'regional_manager_email',
            'regional_manager_phone', 'regional_manager_credentials', 'status',
            'review_notes', 'submitted_at'
        ]
        read_only_fields = ['registration_id', 'registration_number', 'submitted_at', 'status', 'review_notes']



class DeviceRegistrationSerializer(serializers.ModelSerializer):
    """Simplified serializer for mobile app registration"""
    class Meta:
        model = Device
        fields = [
            'mac_address', 'owner_id', 'owner_name', 'owner_phone', 'owner_address',
            'emergency_contact', 'emergency_contact_phone', 'medical_conditions',
            'medications', 'allergies', 'blood_type', 'device_type'
        ]
