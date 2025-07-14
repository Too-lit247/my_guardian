from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import RegexValidator
import uuid

class Role(models.Model):
    role_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    role_name = models.CharField(max_length=50, unique=True)
    
    # Role permissions
    can_manage_users = models.BooleanField(default=False)
    can_manage_devices = models.BooleanField(default=False)
    can_manage_districts = models.BooleanField(default=False)
    can_view_all_alerts = models.BooleanField(default=False)
    can_approve_departments = models.BooleanField(default=False)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'roles'
    
    def __str__(self):
        return self.role_name

class User(AbstractUser):
    DEPARTMENT_CHOICES = [
        ('fire', 'Fire Department'),
        ('police', 'Police Department'),
        ('medical', 'Medical Department'),
        ('admin', 'System Administrator'),
    ]
    
    ROLE_CHOICES = [
        ('System Administrator', 'System Administrator'),
        ('Regional Manager', 'Regional Manager'),
        ('District Manager', 'District Manager'),
        ('Station Manager', 'Station Manager'),
        ('Responder', 'Responder'),
        ('Field User', 'Field User'),
    ]

    REGION_CHOICES = [
        ('central', 'Central Region'),
        ('north', 'Northern Region'),
        ('southern', 'Southern Region'),
    ]
    
    # Override the default id field to use UUID
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    # Basic user information
    full_name = models.CharField(max_length=200)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=17, blank=True)
    
    # Department and role info - using simple CharField to avoid circular dependency
    department = models.CharField(max_length=20, choices=DEPARTMENT_CHOICES)
    role = models.CharField(max_length=50, choices=ROLE_CHOICES, default='Field User')

    # Geographic hierarchy references - using UUIDs to avoid circular dependencies
    region = models.CharField(max_length=20, choices=REGION_CHOICES, null=True, blank=True)
    district_id = models.UUIDField(null=True, blank=True, help_text="Reference to district")
    station_id = models.UUIDField(null=True, blank=True, help_text="Reference to station")
    
    # Additional profile information
    employee_id = models.CharField(max_length=20, unique=True, null=True, blank=True)
    badge_number = models.CharField(max_length=20, blank=True)
    rank = models.CharField(max_length=50, blank=True)
    years_of_service = models.PositiveIntegerField(default=0)
    certifications = models.TextField(blank=True)
    
    # Emergency contact info
    emergency_contact_name = models.CharField(max_length=100, blank=True)
    emergency_contact_phone = models.CharField(max_length=17, blank=True)
    
    # Medical information
    medical_conditions = models.TextField(blank=True)
    medications = models.TextField(blank=True)
    allergies = models.TextField(blank=True)
    blood_type = models.CharField(max_length=5, blank=True)
    
    # Status and metadata
    is_active_user = models.BooleanField(default=False)
    last_login_ip = models.GenericIPAddressField(null=True, blank=True)
    created_by_id = models.UUIDField(null=True, blank=True, help_text="ID of user who created this account")
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'users'
        verbose_name = 'User'
        verbose_name_plural = 'Users'
        ordering = ['department', 'full_name']
    
    def __str__(self):
        return f"{self.full_name} - {self.get_department_display()} ({self.role})"
    
    def can_manage_user(self, target_user):
        """Check if this user can manage the target user"""
        if self.role == 'System Administrator':
            return True
        elif self.role == 'Regional Manager':
            return (target_user.department == self.department and
                   target_user.region == self.region and
                   target_user.role in ['District Manager', 'Station Manager', 'Responder', 'Field User'])
        elif self.role == 'District Manager':
            return (target_user.department == self.department and
                   target_user.district_id == self.district_id and
                   target_user.role in ['Station Manager', 'Responder', 'Field User'])
        elif self.role == 'Station Manager':
            return (target_user.department == self.department and
                   target_user.station_id == self.station_id and
                   target_user.role in ['Responder', 'Field User'])
        return False
    
    def get_managed_users(self):
        """Get users that this user can manage"""
        if self.role == 'System Administrator':
            return User.objects.all().exclude(id=self.id)
        elif self.role == 'Regional Manager':
            return User.objects.filter(
                department=self.department,
                region=self.region,
                role__in=['District Manager', 'Station Manager', 'Responder', 'Field User']
            ).exclude(id=self.id)
        elif self.role == 'District Manager':
            return User.objects.filter(
                department=self.department,
                district_id=self.district_id,
                role__in=['Station Manager', 'Responder', 'Field User']
            ).exclude(id=self.id)
        elif self.role == 'Station Manager':
            return User.objects.filter(
                department=self.department,
                station_id=self.station_id,
                role__in=['Responder', 'Field User']
            ).exclude(id=self.id)
        return User.objects.none()
    
    @property
    def district(self):
        """Get district object if district_id is set"""
        if self.district_id:
            try:
                from geography.models import District
                return District.objects.get(district_id=self.district_id)
            except:
                return None
        return None

    @property
    def station(self):
        """Get station object if station_id is set"""
        if self.station_id:
            try:
                from geography.models import Station
                return Station.objects.get(station_id=self.station_id)
            except:
                return None
        return None

    @property
    def region_obj(self):
        """Get region object if region is set"""
        if self.region:
            try:
                from geography.models import Region
                return Region.objects.get(name=self.region)
            except:
                return None
        return None

class EmergencyContact(models.Model):
    contact_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='emergency_contacts')
    name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=17)
    relation = models.CharField(max_length=50)  # spouse, parent, sibling, etc.
    preferred_method = models.CharField(max_length=20, choices=[
        ('call', 'Phone Call'),
        ('sms', 'Text Message'),
        ('email', 'Email'),
    ], default='call')
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'emergency_contacts'
    
    def __str__(self):
        return f"{self.name} - {self.user.full_name}"

class UserSession(models.Model):
    """Track user sessions for security"""
    session_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sessions')
    session_key = models.CharField(max_length=40, unique=True)
    ip_address = models.GenericIPAddressField()
    user_agent = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    last_activity = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        db_table = 'user_sessions'
        ordering = ['-last_activity']
    
    def __str__(self):
        return f"{self.user.username} - {self.ip_address}"

class UserLoginHistory(models.Model):
    """Track user login history"""
    history_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='login_history')
    ip_address = models.GenericIPAddressField()
    user_agent = models.TextField()
    login_time = models.DateTimeField(auto_now_add=True)
    logout_time = models.DateTimeField(null=True, blank=True)
    success = models.BooleanField(default=True)
    failure_reason = models.CharField(max_length=200, blank=True)
    
    class Meta:
        db_table = 'user_login_history'
        ordering = ['-login_time']
    
    def __str__(self):
        status = "Success" if self.success else f"Failed: {self.failure_reason}"
        return f"{self.user.username} - {status} - {self.login_time}"


class RegistrationRequest(models.Model):
    """Model for handling organization registration requests"""
    REGISTRATION_TYPE_CHOICES = [
        ('individual', 'Individual'),
        ('organization', 'Organization'),
    ]

    DEPARTMENT_CHOICES = [
        ('fire', 'Fire Department'),
        ('police', 'Police Department'),
        ('medical', 'Medical Department'),
    ]

    REGION_CHOICES = [
        ('central', 'Central Region'),
        ('north', 'Northern Region'),
        ('southern', 'Southern Region'),
    ]

    STATUS_CHOICES = [
        ('pending', 'Pending Review'),
        ('approved', 'Approved'),
        ('denied', 'Denied'),
        ('under_review', 'Under Review'),
    ]

    # Primary key
    request_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    # Registration type and basic info
    registration_type = models.CharField(max_length=20, choices=REGISTRATION_TYPE_CHOICES)
    organization_name = models.CharField(max_length=200, blank=True)
    department = models.CharField(max_length=20, choices=DEPARTMENT_CHOICES)
    region = models.CharField(max_length=20, choices=REGION_CHOICES)

    # Personal details
    full_name = models.CharField(max_length=200)
    email = models.EmailField()
    phone_number = models.CharField(max_length=17)

    # Location data
    latitude = models.DecimalField(max_digits=10, decimal_places=8, null=True, blank=True)
    longitude = models.DecimalField(max_digits=11, decimal_places=8, null=True, blank=True)
    address = models.TextField(blank=True)

    # Documentation - can be either a file upload or URL to frontend-stored file
    documentation = models.FileField(upload_to='registration_docs/', null=True, blank=True)
    documentation_url = models.URLField(max_length=500, null=True, blank=True, help_text="URL to uploaded document")

    # Status and approval
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    reviewed_by_id = models.UUIDField(null=True, blank=True, help_text="ID of admin who reviewed")
    review_notes = models.TextField(blank=True)
    reviewed_at = models.DateTimeField(null=True, blank=True)

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'registration_requests'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.full_name} - {self.organization_name or 'Individual'} ({self.status})"

    @property
    def reviewed_by(self):
        """Get the admin user who reviewed this request"""
        if self.reviewed_by_id:
            try:
                return User.objects.get(id=self.reviewed_by_id)
            except User.DoesNotExist:
                return None
        return None
