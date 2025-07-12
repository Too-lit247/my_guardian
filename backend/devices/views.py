from rest_framework import generics, status, permissions
from rest_framework.decorators import api_view, permission_classes, parser_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.parsers import MultiPartParser, FormParser
from django.utils import timezone
from django.shortcuts import get_object_or_404
from .models import Device, DeviceReading, EmergencyTrigger, DepartmentRegistration
from .serializers import (
    DeviceSerializer, DeviceReadingSerializer, EmergencyTriggerSerializer,
    DepartmentRegistrationSerializer, DeviceRegistrationSerializer
)
from .ml_models import analyze_audio_for_fear
from alerts.models import Alert
import logging

logger = logging.getLogger(__name__)

# Device Management Views
class DeviceListView(generics.ListAPIView):
    serializer_class = DeviceSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        user = self.request.user
        if user.role == 'System Administrator':
            return Device.objects.all()
        # For now, return all devices - you can add filtering logic
        return Device.objects.all()

@api_view(['POST'])
@permission_classes([AllowAny])  # Mobile app registration
def register_device(request):
    """Register a new device from mobile app"""
    serializer = DeviceRegistrationSerializer(data=request.data)
    if serializer.is_valid():
        # Generate serial number
        import uuid
        serial_number = f"GD-{str(uuid.uuid4())[:8].upper()}"
        
        device = serializer.save(
            serial_number=serial_number,
            status='active'
        )
        
        return Response({
            'message': 'Device registered successfully',
            'device_id': str(device.device_id),
            'serial_number': device.serial_number
        }, status=status.HTTP_201_CREATED)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([AllowAny])
@parser_classes([MultiPartParser, FormParser])
def device_data_upload(request):
    """Receive data from devices (1 reading per device)"""
    mac_address = request.data.get('mac_address')
    reading_type = request.data.get('reading_type')

    if not mac_address:
        return Response({'error': 'MAC address required'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        device = Device.objects.get(mac_address=mac_address, status='active')
    except Device.DoesNotExist:
        return Response({'error': 'Device not found or inactive'}, status=status.HTTP_404_NOT_FOUND)

    device.last_heartbeat = timezone.now()

    reading_data = {
        'device': device.device_id,
        'reading_type': reading_type,
        'heart_rate': request.data.get('heart_rate'),
        'temperature': request.data.get('temperature'),
        'smoke_level': request.data.get('smoke_level'),
        'battery_level': request.data.get('battery_level'),
        'latitude': request.data.get('latitude'),
        'longitude': request.data.get('longitude'),
        'raw_data': request.data.get('raw_data', {})
    }

    if 'audio_file' in request.FILES:
        reading_data['audio_file'] = request.FILES['audio_file']
        reading_data['reading_type'] = 'audio'

    # Check if a reading already exists for this device
    existing = DeviceReading.objects.filter(device=device).first()

    if existing:
        serializer = DeviceReadingSerializer(existing, data=reading_data, partial=True)
    else:
        serializer = DeviceReadingSerializer(data={**reading_data, 'device': device.device_id})

    if serializer.is_valid():
        reading = serializer.save()

        # Update device coordinates & battery
        if reading.latitude and reading.longitude:
            device.last_known_latitude = reading.latitude
            device.last_known_longitude = reading.longitude
            device.last_location_update = timezone.now()

        if reading.battery_level:
            device.battery_level = reading.battery_level

        device.save()

        process_reading_for_emergencies(reading)

        return Response({
            'message': 'Data received successfully',
            'reading_id': str(reading.reading_id)
        }, status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


def process_reading_for_emergencies(reading):
    """Process device reading to detect emergencies"""
    triggers = []

    # Check heart rate
    if reading.heart_rate and reading.heart_rate > 120:
        triggers.append({
            'trigger_type': 'high_heart_rate',
            'severity': 'high' if reading.heart_rate > 150 else 'medium',
            'trigger_value': reading.heart_rate,
            'threshold_value': 120
        })

    # Check temperature
    if reading.temperature and reading.temperature > 40:
        triggers.append({
            'trigger_type': 'fire_detected',
            'severity': 'critical' if reading.temperature > 50 else 'high',
            'trigger_value': reading.temperature,
            'threshold_value': 40
        })

    # Check smoke level
    if reading.smoke_level and reading.smoke_level > 0.3:
        triggers.append({
            'trigger_type': 'fire_detected',
            'severity': 'critical' if reading.smoke_level > 0.7 else 'high',
            'trigger_value': reading.smoke_level,
            'threshold_value': 0.3
        })

    # Analyze audio
    if reading.audio_file and reading.reading_type == 'audio':
        try:
            analysis = analyze_audio_for_fear(reading.audio_file.path)
            if analysis:
                reading.fear_probability = analysis['fear_probability']
                reading.stress_level = analysis['stress_level']
                reading.audio_analysis_complete = True

                if analysis['fear_probability'] > 0.7:
                    triggers.append({
                        'trigger_type': 'fear_detected',
                        'severity': 'critical' if analysis['fear_probability'] > 0.9 else 'high',
                        'trigger_value': analysis['fear_probability'],
                        'threshold_value': 0.7
                    })
        except Exception as e:
            logger.error(f"Audio analysis error: {e}")

    # If any triggers were found, mark reading as emergency
    if triggers:
        reading.is_emergency = True
        reading.triggered_by = triggers[0]['trigger_type']
        reading.save()

    # Create emergency triggers + alerts
    for trigger_data in triggers:
        create_emergency_trigger(reading, trigger_data)


def create_emergency_trigger(reading, trigger_data):
    """Create emergency trigger and corresponding alert"""
    trigger = EmergencyTrigger.objects.create(
        device=reading.device,
        reading=reading,
        trigger_type=trigger_data['trigger_type'],
        severity=trigger_data['severity'],
        trigger_value=trigger_data['trigger_value'],
        threshold_value=trigger_data['threshold_value'],
        latitude=reading.latitude,
        longitude=reading.longitude
    )
    
    # Determine which department should handle this
    department_mapping = {
        'fear_detected': 'police',
        'high_heart_rate': 'medical',
        'fire_detected': 'fire',
        'panic_button': 'police',
        'fall_detected': 'medical'
    }
    
    department = department_mapping.get(trigger.trigger_type, 'police')
    
    # Create alert
    alert_title = f"Emergency: {trigger.get_trigger_type_display()}"
    alert_description = f"""
    Emergency detected from device {reading.device.serial_number}
    Owner: {reading.device.owner_name}
    Trigger: {trigger.get_trigger_type_display()}
    Severity: {trigger.get_severity_display()}
    Value: {trigger.trigger_value} (Threshold: {trigger.threshold_value})
    """
    
    location = f"Lat: {trigger.latitude}, Lng: {trigger.longitude}" if trigger.latitude else reading.device.owner_address
    
    # Get a system user to create the alert
    from accounts.models import User
    system_user = User.objects.filter(role='System Administrator').first()
    
    if system_user:
        alert = Alert.objects.create(
            title=alert_title,
            alert_type=trigger.trigger_type,
            description=alert_description,
            location=location,
            priority='high' if trigger.severity in ['high', 'critical'] else 'medium',
            status='active',
            department=department,
            created_by=system_user,
            assigned_to=f"Auto-assigned from device {reading.device.serial_number}"
        )
        
        trigger.alert_created_id = alert.id
        trigger.save()
        
        logger.info(f"Emergency alert created: {alert.id} for device {reading.device.serial_number}")

# Department Registration Views
@api_view(['POST'])
@permission_classes([AllowAny])
def register_department(request):
    """Register a new department"""
    serializer = DepartmentRegistrationSerializer(data=request.data)
    if serializer.is_valid():
        # Generate registration number
        import uuid
        registration_number = f"DEPT-{str(uuid.uuid4())[:8].upper()}"
        
        registration = serializer.save(registration_number=registration_number)
        
        return Response({
            'message': 'Department registration submitted successfully',
            'registration_number': registration.registration_number,
            'status': 'pending'
        }, status=status.HTTP_201_CREATED)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class DepartmentRegistrationListView(generics.ListAPIView):
    serializer_class = DepartmentRegistrationSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        user = self.request.user
        if user.role == 'System Administrator':
            return DepartmentRegistration.objects.all()
        return DepartmentRegistration.objects.none()

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def approve_department_registration(request, registration_id):
    """Approve department registration and create regional manager"""
    if request.user.role != 'System Administrator':
        return Response({'error': 'Only system administrators can approve registrations'}, 
                       status=status.HTTP_403_FORBIDDEN)
    
    registration = get_object_or_404(DepartmentRegistration, registration_id=registration_id)
    
    if registration.status != 'pending':
        return Response({'error': 'Registration is not pending'}, status=status.HTTP_400_BAD_REQUEST)
    
    # Create regional manager user
    from accounts.models import User
    
    try:
        regional_manager = User.objects.create_user(
            username=f"{registration.department_type}_regional_{registration.registration_id}",
            email=registration.regional_manager_email,
            password='TempPassword123!',  # They should change this
            full_name=registration.regional_manager_name,
            department=registration.department_type,
            role='Regional Manager',
            phone_number=registration.regional_manager_phone,
            employee_id=f"RM-{registration.registration_number}"
        )
        
        # Update registration status
        registration.status = 'approved'
        registration.reviewed_by_id = request.user.id
        registration.reviewed_at = timezone.now()
        registration.review_notes = request.data.get('review_notes', 'Approved by system administrator')
        registration.save()
        
        return Response({
            'message': 'Department registration approved successfully',
            'regional_manager_username': regional_manager.username,
            'temporary_password': 'TempPassword123!'
        }, status=status.HTTP_200_OK)
        
    except Exception as e:
        return Response({'error': f'Error creating regional manager: {str(e)}'}, 
                       status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# Emergency Trigger Views
class EmergencyTriggerListView(generics.ListAPIView):
    serializer_class = EmergencyTriggerSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        user = self.request.user
        if user.role == 'System Administrator':
            return EmergencyTrigger.objects.all()
        
        # Filter by department - need to get alerts and check department
        return EmergencyTrigger.objects.filter(
            alert_created_id__isnull=False
        ).select_related('device')

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def acknowledge_trigger(request, trigger_id):
    """Acknowledge an emergency trigger"""
    trigger = get_object_or_404(EmergencyTrigger, trigger_id=trigger_id)
    
    trigger.acknowledged = True
    trigger.acknowledged_by_id = request.user.id
    trigger.acknowledged_at = timezone.now()
    trigger.save()
    
    return Response({'message': 'Emergency trigger acknowledged'}, status=status.HTTP_200_OK)
