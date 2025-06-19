from django.db import models
from django.conf import settings

class Alert(models.Model):
    PRIORITY_CHOICES = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
    ]
    
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('in_progress', 'In Progress'),
        ('resolved', 'Resolved'),
        ('cancelled', 'Cancelled'),
    ]
    
    ALERT_TYPE_CHOICES = [
        # Fire Department
        ('building_fire', 'Building Fire'),
        ('wildfire', 'Wildfire'),
        ('gas_leak', 'Gas Leak'),
        ('explosion', 'Explosion'),
        ('hazmat_incident', 'Hazmat Incident'),
        
        # Police Department
        ('robbery', 'Robbery'),
        ('assault', 'Assault'),
        ('traffic_violation', 'Traffic Violation'),
        ('domestic_dispute', 'Domestic Dispute'),
        ('suspicious_activity', 'Suspicious Activity'),
        
        # Medical Department
        ('heart_attack', 'Heart Attack'),
        ('traffic_accident', 'Traffic Accident'),
        ('overdose', 'Overdose'),
        ('fall_injury', 'Fall Injury'),
        ('allergic_reaction', 'Allergic Reaction'),
    ]
    
    title = models.CharField(max_length=200)
    alert_type = models.CharField(max_length=50, choices=ALERT_TYPE_CHOICES)
    description = models.TextField()
    location = models.CharField(max_length=300)
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    department = models.CharField(max_length=20, choices=[
        ('fire', 'Fire Department'),
        ('police', 'Police Department'),
        ('medical', 'Medical Department'),
    ])
    
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='created_alerts')
    assigned_to = models.CharField(max_length=100, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    resolved_at = models.DateTimeField(null=True, blank=True)
    
    # Additional fields for history tracking
    response_time = models.CharField(max_length=50, blank=True)
    outcome = models.TextField(blank=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.title} - {self.get_status_display()}"
