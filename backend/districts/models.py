from django.db import models
from django.core.validators import RegexValidator
import uuid

class District(models.Model):
    DEPARTMENT_CHOICES = [
        ('fire', 'Fire Department'),
        ('police', 'Police Department'),
        ('medical', 'Medical Department'),
    ]
    
    # Use UUID as primary key
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    # Basic Information
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=10, unique=True, help_text="Unique district code")
    department = models.CharField(max_length=20, choices=DEPARTMENT_CHOICES)
    
    # Location Information
    address = models.TextField()
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=50)
    zip_code = models.CharField(max_length=10)
    coordinates = models.CharField(max_length=50, blank=True, help_text="Latitude,Longitude")
    
    # Management Information
    manager = models.CharField(max_length=100)
    manager_email = models.EmailField(blank=True)
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$')
    manager_phone = models.CharField(validators=[phone_regex], max_length=17, blank=True)
    
    # Operational Information
    description = models.TextField(blank=True)
    coverage_area = models.TextField(blank=True, help_text="Description of coverage area")
    population_served = models.PositiveIntegerField(default=0)
    
    # Status and Metadata
    is_active = models.BooleanField(default=True)
    established_date = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # Reference to creator without foreign key to avoid circular dependency
    created_by_id = models.UUIDField(null=True, blank=True, help_text="ID of user who created this district")
    
    class Meta:
        db_table = 'districts'
        ordering = ['department', 'name']
        unique_together = ['name', 'department']
    
    def __str__(self):
        return f"{self.name} - {self.get_department_display()}"
    
    @property
    def user_count(self):
        from accounts.models import User
        return User.objects.filter(district_id=self.id, is_active_user=True).count()
    
    @property
    def active_alerts_count(self):
        from alerts.models import Alert
        return Alert.objects.filter(
            department=self.department,
            status__in=['active', 'in_progress']
        ).count()
    
    def get_coordinates(self):
        if self.coordinates:
            try:
                lat, lng = self.coordinates.split(',')
                return {'lat': float(lat.strip()), 'lng': float(lng.strip())}
            except (ValueError, AttributeError):
                return None
        return None
    
    @property
    def created_by(self):
        """Get the user who created this district"""
        if self.created_by_id:
            try:
                from accounts.models import User
                return User.objects.get(id=self.created_by_id)
            except:
                return None
        return None

class DistrictResource(models.Model):
    """Resources available in each district"""
    RESOURCE_TYPES = [
        ('vehicle', 'Vehicle'),
        ('equipment', 'Equipment'),
        ('personnel', 'Personnel'),
        ('facility', 'Facility'),
    ]
    
    resource_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    district = models.ForeignKey(District, on_delete=models.CASCADE, related_name='resources')
    name = models.CharField(max_length=100)
    resource_type = models.CharField(max_length=20, choices=RESOURCE_TYPES)
    description = models.TextField(blank=True)
    quantity = models.PositiveIntegerField(default=1)
    is_available = models.BooleanField(default=True)
    last_maintenance = models.DateField(null=True, blank=True)
    next_maintenance = models.DateField(null=True, blank=True)
    
    class Meta:
        db_table = 'district_resources'
        ordering = ['district', 'resource_type', 'name']
    
    def __str__(self):
        return f"{self.district.name} - {self.name}"
