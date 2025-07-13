from rest_framework import generics, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.utils import timezone
from django.db import models
from .models import Alert
from .serializers import AlertSerializer
from .services import StationFinderService, AlertRoutingService

class AlertListCreateView(generics.ListCreateAPIView):
    serializer_class = AlertSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        user = self.request.user
        queryset = Alert.objects.filter(department=user.department)
        
        # Filter by status if provided
        status_filter = self.request.query_params.get('status', None)
        if status_filter:
            queryset = queryset.filter(status=status_filter)
        
        # Filter by priority if provided
        priority_filter = self.request.query_params.get('priority', None)
        if priority_filter:
            queryset = queryset.filter(priority=priority_filter)
        
        # Search functionality
        search = self.request.query_params.get('search', None)
        if search:
            queryset = queryset.filter(
                models.Q(title__icontains=search) |
                models.Q(location__icontains=search) |
                models.Q(description__icontains=search)
            )
        
        return queryset

class AlertDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = AlertSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return Alert.objects.filter(department=self.request.user.department)
    
    def perform_update(self, serializer):
        # If status is being changed to resolved, set resolved_at
        if serializer.validated_data.get('status') == 'resolved':
            serializer.save(resolved_at=timezone.now())
        else:
            serializer.save()

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def alert_statistics(request):
    user = request.user
    alerts = Alert.objects.filter(department=user.department)
    
    stats = {
        'total_alerts': alerts.count(),
        'active_alerts': alerts.filter(status='active').count(),
        'resolved_alerts': alerts.filter(status='resolved').count(),
        'high_priority': alerts.filter(priority='high').count(),
        'recent_alerts': AlertSerializer(
            alerts.filter(created_at__gte=timezone.now() - timezone.timedelta(days=7))[:5], 
            many=True
        ).data
    }
    
    return Response(stats)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def find_nearest_stations(request):
    """Find nearest stations for a given location and department"""
    try:
        latitude = float(request.query_params.get('latitude'))
        longitude = float(request.query_params.get('longitude'))
        department = request.query_params.get('department', 'police')
        radius_km = float(request.query_params.get('radius', 50))

        stations = StationFinderService.find_stations_in_radius(
            latitude, longitude, department, radius_km
        )

        result = []
        for station_info in stations:
            station = station_info['station']
            result.append({
                'station_id': str(station.station_id),
                'name': station.name,
                'address': station.address,
                'distance_km': station_info['distance_km'],
                'coordinates': station.get_coordinates(),
                'district_name': station.district.name,
                'region_name': station.district.region.display_name,
                'manager_name': station.manager.full_name if station.manager else None,
                'phone': station.phone,
                'operating_hours': station.operating_hours
            })

        return Response({
            'stations': result,
            'search_location': {'latitude': latitude, 'longitude': longitude},
            'department': department,
            'radius_km': radius_km
        })

    except (ValueError, TypeError) as e:
        return Response(
            {'error': 'Invalid latitude, longitude, or radius parameters'},
            status=status.HTTP_400_BAD_REQUEST
        )


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_emergency_alert(request):
    """Create an emergency alert with automatic station assignment"""
    try:
        data = request.data

        # Validate required fields
        required_fields = ['alert_type', 'latitude', 'longitude', 'description']
        for field in required_fields:
            if field not in data:
                return Response(
                    {'error': f'Missing required field: {field}'},
                    status=status.HTTP_400_BAD_REQUEST
                )

        # Create and route the alert
        alert = AlertRoutingService.route_emergency_alert(
            alert_type=data['alert_type'],
            latitude=float(data['latitude']),
            longitude=float(data['longitude']),
            severity=data.get('severity', 'medium'),
            description=data['description'],
            created_by_user=request.user
        )

        # Return the created alert with assignment info
        serializer = AlertSerializer(alert)
        response_data = serializer.data

        if alert.assigned_station:
            response_data['assignment_info'] = {
                'assigned_station': alert.assigned_station.name,
                'station_address': alert.assigned_station.address,
                'distance': alert.assigned_to
            }

        return Response(response_data, status=status.HTTP_201_CREATED)

    except (ValueError, TypeError) as e:
        return Response(
            {'error': 'Invalid coordinate values'},
            status=status.HTTP_400_BAD_REQUEST
        )
    except Exception as e:
        return Response(
            {'error': str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_station_coverage(request, station_id):
    """Get coverage information for a specific station"""
    try:
        from geography.models import Station

        station = Station.objects.get(station_id=station_id)

        # Check permissions
        user = request.user
        if user.role not in ['System Administrator', 'Regional Manager', 'District Manager', 'Station Manager']:
            return Response({'error': 'Permission denied'}, status=status.HTTP_403_FORBIDDEN)

        if user.role == 'Station Manager' and station.station_id != user.station_id:
            return Response({'error': 'Permission denied'}, status=status.HTTP_403_FORBIDDEN)

        coverage_info = StationFinderService.get_station_coverage_info(station)

        return Response({
            'station_id': str(station.station_id),
            'station_name': station.name,
            'department': station.department,
            'coordinates': coverage_info['coordinates'],
            'coverage_radius_km': coverage_info['coverage_radius_km'],
            'active_alerts_count': coverage_info['active_alerts_count'],
            'recent_alerts_count': coverage_info['recent_alerts_count'],
            'staff_count': station.staff_count
        })

    except Station.DoesNotExist:
        return Response({'error': 'Station not found'}, status=status.HTTP_404_NOT_FOUND)
