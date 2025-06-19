from django.contrib import admin
from .models import Device, DeviceReading, EmergencyTrigger, DepartmentRegistration

@admin.register(Device)
class DeviceAdmin(admin.ModelAdmin):
    list_display = ('serial_number', 'owner_name', 'device_type', 'status', 'battery_level', 'is_online', 'registered_at')
    list_filter = ('device_type', 'status', 'registered_at')
    search_fields = ('serial_number', 'owner_name', 'mac_address')
    readonly_fields = ('device_id', 'registered_at', 'updated_at', 'is_online')

@admin.register(DeviceReading)
class DeviceReadingAdmin(admin.ModelAdmin):
    list_display = ('device', 'reading_type', 'timestamp', 'heart_rate', 'temperature', 'fear_probability', 'is_emergency')
    list_filter = ('reading_type', 'timestamp', 'audio_analysis_complete', 'is_emergency')
    search_fields = ('device__serial_number', 'device__owner_name')
    readonly_fields = ('reading_id', 'timestamp')

@admin.register(EmergencyTrigger)
class EmergencyTriggerAdmin(admin.ModelAdmin):
    list_display = ('device', 'trigger_type', 'severity', 'acknowledged', 'triggered_at')
    list_filter = ('trigger_type', 'severity', 'acknowledged', 'triggered_at')
    search_fields = ('device__serial_number', 'device__owner_name')
    readonly_fields = ('trigger_id', 'triggered_at')

@admin.register(DepartmentRegistration)
class DepartmentRegistrationAdmin(admin.ModelAdmin):
    list_display = ('department_name', 'department_type', 'contact_person', 'status', 'submitted_at')
    list_filter = ('department_type', 'status', 'submitted_at')
    search_fields = ('department_name', 'contact_person', 'registration_number')
    readonly_fields = ('registration_id', 'submitted_at', 'updated_at')
