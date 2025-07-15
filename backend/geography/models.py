from django.db import models
from django.core.validators import RegexValidator
import uuid


class Region(models.Model):
    """Model for geographic regions"""
    REGION_CHOICES = [
        ('central', 'Central Region'),
        ('north', 'Northern Region'),
        ('southern', 'Southern Region'),
    ]
    
    # Primary key
    region_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    # Basic information
    name = models.CharField(max_length=20, choices=REGION_CHOICES, unique=True)
    display_name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    
    # Geographic boundaries (optional)
    boundary_coordinates = models.JSONField(null=True, blank=True, help_text="GeoJSON polygon for region boundaries")
    
    # Metadata
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'regions'
        ordering = ['name']
    
    def __str__(self):
        return self.display_name
    
    @property
    def district_count(self):
        return self.districts.filter(is_active=True).count()
    
    @property
    def total_staff_count(self):
        from accounts.models import User
        return User.objects.filter(region=self.name, is_active_user=True).count()


class District(models.Model):
    """Enhanced District model with region relationship"""
    
    # Primary key
    district_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    # Basic Information
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=10, unique=True, help_text="Unique district code")
    department = models.CharField(max_length=20)
    
    # Geographic hierarchy
    region = models.ForeignKey(Region, on_delete=models.CASCADE, related_name='districts')
    
    # Location Information
    address = models.TextField()
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=50)
    zip_code = models.CharField(max_length=10)
    latitude = models.DecimalField(max_digits=10, decimal_places=8, null=True, blank=True)
    longitude = models.DecimalField(max_digits=11, decimal_places=8, null=True, blank=True)
    
    # Management Information
    manager_id = models.UUIDField(null=True, blank=True, help_text="ID of district manager")
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$')
    phone = models.CharField(validators=[phone_regex], max_length=17, blank=True)
    
    # Operational Information
    description = models.TextField(blank=True)
    coverage_area = models.TextField(blank=True, help_text="Description of coverage area")
    population_served = models.PositiveIntegerField(default=0)
    
    # Status and Metadata
    is_active = models.BooleanField(default=True)
    established_date = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by_id = models.UUIDField(null=True, blank=True, help_text="ID of user who created this district")
    
    class Meta:
        db_table = 'geography_districts'
        ordering = ['region__display_name', 'department', 'name']
        unique_together = ['name', 'department', 'region']
    
    def __str__(self):
        return f"{self.name} - {self.department} ({self.region.display_name})"
    
    @property
    def manager(self):
        """Get the district manager"""
        if self.manager_id:
            try:
                from accounts.models import User
                return User.objects.get(id=self.manager_id)
            except User.DoesNotExist:
                return None
        return None
    
    @property
    def station_count(self):
        return self.stations.filter(is_active=True).count()
    
    @property
    def staff_count(self):
        from accounts.models import User
        return User.objects.filter(district_id=self.district_id, is_active_user=True).count()
    
    @property
    def active_alerts_count(self):
        from alerts.models import Alert
        return Alert.objects.filter(
            department=self.department,
            status__in=['active', 'in_progress']
        ).count()
    
    def get_coordinates(self):
        if self.latitude and self.longitude:
            return {'lat': float(self.latitude), 'lng': float(self.longitude)}
        return None


class Station(models.Model):
    """Model for emergency response stations"""
    STATION_TYPE_CHOICES = [
        ('headquarters', 'Headquarters'),
        ('substation', 'Substation'),
        ('outpost', 'Outpost'),
        ('mobile', 'Mobile Unit'),
    ]

    DEPARTMENT_CHOICES = [
        ('fire', 'Fire Department'),
        ('police', 'Police Department'),
        ('medical', 'Medical Department'),
    ]

    # Primary key
    station_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    # Basic Information
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=15, unique=True, help_text="Unique station code")
    station_type = models.CharField(max_length=20, choices=STATION_TYPE_CHOICES, default='substation')

    # Department and Region (simplified)
    department = models.CharField(max_length=20, choices=DEPARTMENT_CHOICES)
    region = models.CharField(max_length=100, help_text="Region name")
    
    # Location Information
    address = models.TextField()
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=50)
    zip_code = models.CharField(max_length=10)
    latitude = models.DecimalField(max_digits=10, decimal_places=8, null=True, blank=True)
    longitude = models.DecimalField(max_digits=11, decimal_places=8, null=True, blank=True)
    
    # Management Information
    manager_id = models.UUIDField(null=True, blank=True, help_text="ID of station manager")
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$')
    phone = models.CharField(validators=[phone_regex], max_length=17, blank=True)
    
    # Operational Information
    description = models.TextField(blank=True)
    capacity = models.PositiveIntegerField(default=0, help_text="Maximum staff capacity")
    operating_hours = models.CharField(max_length=100, blank=True, help_text="e.g., 24/7, 8AM-6PM")
    
    # Status and Metadata
    is_active = models.BooleanField(default=True)
    established_date = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by_id = models.UUIDField(null=True, blank=True, help_text="ID of user who created this station")
    
    class Meta:
        db_table = 'geography_stations'
        ordering = ['region', 'department', 'name']
        unique_together = ['name', 'department', 'region']

    def __str__(self):
        return f"{self.name} - {self.department} ({self.region})"
    
    @property
    def manager(self):
        """Get the station manager"""
        if self.manager_id:
            try:
                from accounts.models import User
                return User.objects.get(id=self.manager_id)
            except User.DoesNotExist:
                return None
        return None
    
    @property
    def staff_count(self):
        from accounts.models import User
        return User.objects.filter(station_id=self.station_id, is_active_user=True).count()
    
    def get_coordinates(self):
        if self.latitude and self.longitude:
            return {'lat': float(self.latitude), 'lng': float(self.longitude)}
        return None
