from django.db import models
from django.conf import settings
import uuid

class Device(models.Model):
    """Guardian devices - bracelets, watches, pendants, etc."""
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('inactive', 'Inactive'),
        ('maintenance', 'Maintenance'),
        ('lost', 'Lost/Stolen'),
    ]
    
    DEVICE_TYPE_CHOICES = [
        ('guardian_bracelet', 'Guardian Bracelet'),
        ('guardian_watch', 'Guardian Watch'),
        ('guardian_pendant', 'Guardian Pendant'),
        ('guardian_ring', 'Guardian Ring'),
    ]
    
    # Device Information
    device_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    mac_address = models.CharField(max_length=17, unique=True, help_text="MAC address of the device")
    serial_number = models.CharField(max_length=50, unique=True)
    device_type = models.CharField(max_length=20, choices=DEVICE_TYPE_CHOICES, default='guardian_bracelet')
    
    # User Information
    owner_id = models.UUIDField(null=True, blank=True, help_text="ID of the person wearing the device")
    owner_name = models.CharField(max_length=100, help_text="Name of the person wearing the device")
    owner_phone = models.CharField(max_length=17, help_text="Emergency contact number")
    owner_address = models.TextField(help_text="Home address")
    emergency_contact = models.CharField(max_length=100, blank=True)
    emergency_contact_phone = models.CharField(max_length=17, blank=True)
    
    # Medical Information
    medical_conditions = models.TextField(blank=True, help_text="Known medical conditions")
    medications = models.TextField(blank=True, help_text="Current medications")
    allergies = models.TextField(blank=True, help_text="Known allergies")
    blood_type = models.CharField(max_length=5, blank=True)
    
    # Device Status
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    battery_level = models.IntegerField(default=100, help_text="Battery percentage")
    last_heartbeat = models.DateTimeField(null=True, blank=True)
    firmware_version = models.CharField(max_length=20, default='1.0.0')
    
    # Location Tracking
    last_known_latitude = models.DecimalField(max_digits=10, decimal_places=8, null=True, blank=True)
    last_known_longitude = models.DecimalField(max_digits=11, decimal_places=8, null=True, blank=True)
    last_location_update = models.DateTimeField(null=True, blank=True)
    
    # Monitoring Settings
    audio_monitoring_enabled = models.BooleanField(default=True)
    heart_rate_monitoring_enabled = models.BooleanField(default=True)
    fire_monitoring_enabled = models.BooleanField(default=True)
    fall_detection_enabled = models.BooleanField(default=True)
    monitoring_interval = models.IntegerField(default=300, help_text="Monitoring interval in seconds")
    
    # Timestamps
    registered_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    registered_by_id = models.UUIDField(null=True, blank=True, help_text="ID of user who registered this device")
    
    class Meta:
        db_table = 'devices'
        ordering = ['-registered_at']
    
    def __str__(self):
        return f"Device {self.serial_number} - {self.owner_name}"
    
    @property
    def is_online(self):
        if not self.last_heartbeat:
            return False
        from django.utils import timezone
        return (timezone.now() - self.last_heartbeat).seconds < 600  # 10 minutes
    
    @property
    def registered_by(self):
        """Get the user who registered this device"""
        if self.registered_by_id:
            try:
                from accounts.models import User
                return User.objects.get(id=self.registered_by_id)
            except:
                return None
        return None

class DeviceReading(models.Model):
    """Sensor readings from devices"""
    READING_TYPE_CHOICES = [
        ('audio', 'Audio Analysis'),
        ('heart_rate', 'Heart Rate'),
        ('temperature', 'Temperature'),
        ('smoke', 'Smoke Detection'),
        ('location', 'Location Update'),
        ('battery', 'Battery Status'),
    ]
    
    reading_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    device = models.ForeignKey(Device, on_delete=models.CASCADE, related_name='readings')
    reading_type = models.CharField(max_length=20, choices=READING_TYPE_CHOICES)
    timestamp = models.DateTimeField(auto_now_add=True)
    
    # Sensor Data
    heart_rate = models.IntegerField(null=True, blank=True)
    temperature = models.FloatField(null=True, blank=True)
    smoke_level = models.FloatField(null=True, blank=True)
    battery_level = models.IntegerField(null=True, blank=True)
    
    # Location Data
    latitude = models.DecimalField(max_digits=10, decimal_places=8, null=True, blank=True)
    longitude = models.DecimalField(max_digits=11, decimal_places=8, null=True, blank=True)
    
    # Audio Analysis Results
    audio_file = models.FileField(upload_to='audio_samples/', null=True, blank=True)
    fear_probability = models.FloatField(null=True, blank=True, help_text="Probability of fear detected (0-1)")
    stress_level = models.FloatField(null=True, blank=True, help_text="Stress level detected (0-1)")
    audio_analysis_complete = models.BooleanField(default=False)
    
    # Emergency detection
    is_emergency = models.BooleanField(default=False)
    triggered_by = models.CharField(max_length=100, blank=True)
    
    # Raw sensor data (JSON)
    raw_data = models.JSONField(default=dict, blank=True)
    
    class Meta:
        db_table = 'device_readings'
        ordering = ['-timestamp']
        indexes = [
            models.Index(fields=['device', '-timestamp']),
            models.Index(fields=['reading_type', '-timestamp']),
            models.Index(fields=['is_emergency', '-timestamp']),
        ]
    
    def __str__(self):
        return f"{self.device.serial_number} - {self.reading_type} at {self.timestamp}"

class EmergencyTrigger(models.Model):
    """Emergency situations detected by devices"""
    TRIGGER_TYPE_CHOICES = [
        ('fear_detected', 'Fear Detected'),
        ('high_heart_rate', 'High Heart Rate'),
        ('fire_detected', 'Fire Detected'),
        ('panic_button', 'Panic Button'),
        ('device_offline', 'Device Offline'),
        ('fall_detected', 'Fall Detected'),
    ]
    
    SEVERITY_CHOICES = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
        ('critical', 'Critical'),
    ]
    
    trigger_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    device = models.ForeignKey(Device, on_delete=models.CASCADE, related_name='emergency_triggers')
    trigger_type = models.CharField(max_length=20, choices=TRIGGER_TYPE_CHOICES)
    severity = models.CharField(max_length=10, choices=SEVERITY_CHOICES)
    
    # Trigger Data
    reading = models.ForeignKey(DeviceReading, on_delete=models.CASCADE, null=True, blank=True)
    trigger_value = models.FloatField(help_text="The value that triggered the alert")
    threshold_value = models.FloatField(help_text="The threshold that was exceeded")
    
    # Location at time of trigger
    latitude = models.DecimalField(max_digits=10, decimal_places=8, null=True, blank=True)
    longitude = models.DecimalField(max_digits=11, decimal_places=8, null=True, blank=True)
    
    # Alert Management
    alert_created_id = models.UUIDField(null=True, blank=True, help_text="ID of created alert")
    acknowledged = models.BooleanField(default=False)
    acknowledged_by_id = models.UUIDField(null=True, blank=True, help_text="ID of user who acknowledged")
    acknowledged_at = models.DateTimeField(null=True, blank=True)
    
    # Timestamps
    triggered_at = models.DateTimeField(auto_now_add=True)
    resolved_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        db_table = 'emergency_triggers'
        ordering = ['-triggered_at']
    
    def __str__(self):
        return f"{self.device.owner_name} - {self.get_trigger_type_display()} ({self.severity})"
    
    @property
    def alert_created(self):
        """Get the created alert"""
        if self.alert_created_id:
            try:
                from alerts.models import Alert
                return Alert.objects.get(id=self.alert_created_id)
            except:
                return None
        return None
    
    @property
    def acknowledged_by(self):
        """Get the user who acknowledged this trigger"""
        if self.acknowledged_by_id:
            try:
                from accounts.models import User
                return User.objects.get(id=self.acknowledged_by_id)
            except:
                return None
        return None

class DepartmentRegistration(models.Model):
    """Department registration requests"""
    STATUS_CHOICES = [
        ('pending', 'Pending Review'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('suspended', 'Suspended'),
    ]

    DEPARTMENT_TYPE_CHOICES = [
        ('fire', 'Fire Department'),
        ('police', 'Police Department'),
        ('medical', 'Medical Department'),
        ('emergency', 'Emergency Services'),
    ]

    REGION_CHOICES = [
        ('central', 'Central Region'),
        ('north', 'Northern Region'),
        ('southern', 'Southern Region'),
    ]

    registration_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    # Department Information
    department_name = models.CharField(max_length=200)
    department_type = models.CharField(max_length=20, choices=DEPARTMENT_TYPE_CHOICES)
    registration_number = models.CharField(max_length=50, unique=True)

    # Region Assignment
    region = models.CharField(max_length=20, choices=REGION_CHOICES, help_text="Region where this department will operate")
    
    # Contact Information
    contact_person = models.CharField(max_length=100)
    contact_email = models.EmailField()
    contact_phone = models.CharField(max_length=17)
    
    # Address Information
    address = models.TextField()
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=50)
    zip_code = models.CharField(max_length=10)
    country = models.CharField(max_length=50, default='United States')
    
    # Coverage Area
    coverage_description = models.TextField(help_text="Description of the area covered by this department")
    population_served = models.PositiveIntegerField(help_text="Approximate population served")
    
    # Documentation - paths/URLs to uploaded documents (stored on frontend)
    license_document = models.CharField(max_length=500, blank=True, help_text="Path or URL to department license/certification")
    insurance_document = models.CharField(max_length=500, blank=True, help_text="Path or URL to insurance document")
    additional_documents = models.CharField(max_length=500, blank=True, help_text="Path or URL to additional documents")
    
    # Regional Manager Information
    regional_manager_name = models.CharField(max_length=100)
    regional_manager_email = models.EmailField()
    regional_manager_phone = models.CharField(max_length=17)
    regional_manager_credentials = models.TextField(help_text="Qualifications and experience")
    
    # Status and Review
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    reviewed_by_id = models.UUIDField(null=True, blank=True, help_text="ID of user who reviewed")
    review_notes = models.TextField(blank=True)
    reviewed_at = models.DateTimeField(null=True, blank=True)
    
    # Timestamps
    submitted_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'department_registrations'
        ordering = ['-submitted_at']
    
    def __str__(self):
        return f"{self.department_name} - {self.get_status_display()}"
    
    @property
    def reviewed_by(self):
        """Get the user who reviewed this registration"""
        if self.reviewed_by_id:
            try:
                from accounts.models import User
                return User.objects.get(id=self.reviewed_by_id)
            except:
                return None
        return None
