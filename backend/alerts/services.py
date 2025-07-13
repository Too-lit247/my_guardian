import math
from typing import Optional, Tuple, List, Dict
from geography.models import Station, District, Region
from .models import Alert


class StationFinderService:
    """Service to find the nearest station for emergency alerts"""
    
    @staticmethod
    def calculate_distance(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
        """
        Calculate the great circle distance between two points on Earth
        using the Haversine formula. Returns distance in kilometers.
        """
        # Convert latitude and longitude from degrees to radians
        lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])
        
        # Haversine formula
        dlat = lat2 - lat1
        dlon = lon2 - lon1
        a = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2)**2
        c = 2 * math.asin(math.sqrt(a))
        
        # Radius of Earth in kilometers
        r = 6371
        
        return c * r
    
    @classmethod
    def find_nearest_station(
        cls, 
        latitude: float, 
        longitude: float, 
        department: str,
        max_distance_km: float = 100.0
    ) -> Optional[Station]:
        """
        Find the nearest station of the specified department to the given coordinates.
        
        Args:
            latitude: Alert latitude
            longitude: Alert longitude
            department: Department type ('fire', 'police', 'medical')
            max_distance_km: Maximum search radius in kilometers
            
        Returns:
            Nearest Station object or None if no station found within range
        """
        # Get all active stations of the specified department with coordinates
        stations = Station.objects.filter(
            district__department=department,
            district__is_active=True,
            is_active=True,
            latitude__isnull=False,
            longitude__isnull=False
        ).select_related('district', 'district__region')
        
        if not stations.exists():
            return None
        
        nearest_station = None
        min_distance = float('inf')
        
        for station in stations:
            distance = cls.calculate_distance(
                latitude, longitude,
                float(station.latitude), float(station.longitude)
            )
            
            if distance < min_distance and distance <= max_distance_km:
                min_distance = distance
                nearest_station = station
        
        return nearest_station
    
    @classmethod
    def find_stations_in_radius(
        cls,
        latitude: float,
        longitude: float,
        department: str,
        radius_km: float = 50.0
    ) -> List[Dict]:
        """
        Find all stations of the specified department within a given radius.
        
        Returns:
            List of dictionaries with station info and distance
        """
        stations = Station.objects.filter(
            district__department=department,
            district__is_active=True,
            is_active=True,
            latitude__isnull=False,
            longitude__isnull=False
        ).select_related('district', 'district__region')
        
        stations_with_distance = []
        
        for station in stations:
            distance = cls.calculate_distance(
                latitude, longitude,
                float(station.latitude), float(station.longitude)
            )
            
            if distance <= radius_km:
                stations_with_distance.append({
                    'station': station,
                    'distance_km': round(distance, 2),
                    'district': station.district,
                    'region': station.district.region
                })
        
        # Sort by distance
        stations_with_distance.sort(key=lambda x: x['distance_km'])
        
        return stations_with_distance
    
    @classmethod
    def assign_alert_to_nearest_station(
        cls,
        alert: Alert,
        latitude: float = None,
        longitude: float = None
    ) -> bool:
        """
        Assign an alert to the nearest appropriate station.
        
        Args:
            alert: Alert object to assign
            latitude: Override alert latitude
            longitude: Override alert longitude
            
        Returns:
            True if assignment was successful, False otherwise
        """
        # Use provided coordinates or alert coordinates
        lat = latitude or alert.latitude
        lng = longitude or alert.longitude
        
        if not lat or not lng:
            return False
        
        # Determine department based on alert type
        department = Alert.get_department_for_alert_type(alert.alert_type)
        
        # Find nearest station
        nearest_station = cls.find_nearest_station(
            float(lat), float(lng), department
        )
        
        if nearest_station:
            # Update alert with station assignment
            alert.assigned_station_id = nearest_station.station_id
            alert.department = department
            
            # Calculate distance for assignment info
            distance = cls.calculate_distance(
                float(lat), float(lng),
                float(nearest_station.latitude), float(nearest_station.longitude)
            )
            
            alert.assigned_to = f"{nearest_station.name} ({distance:.1f}km away)"
            alert.save()
            
            return True
        
        return False
    
    @classmethod
    def get_station_coverage_info(cls, station: Station) -> Dict:
        """
        Get coverage information for a station including nearby alerts.
        
        Returns:
            Dictionary with station coverage statistics
        """
        if not station.latitude or not station.longitude:
            return {
                'station': station,
                'coverage_radius_km': 0,
                'active_alerts_count': 0,
                'recent_alerts_count': 0
            }
        
        # Count active alerts assigned to this station
        active_alerts = Alert.objects.filter(
            assigned_station_id=station.station_id,
            status__in=['active', 'in_progress']
        ).count()
        
        # Count recent alerts (last 24 hours)
        from django.utils import timezone
        from datetime import timedelta
        
        recent_alerts = Alert.objects.filter(
            assigned_station_id=station.station_id,
            created_at__gte=timezone.now() - timedelta(hours=24)
        ).count()
        
        return {
            'station': station,
            'coverage_radius_km': 50,  # Default coverage radius
            'active_alerts_count': active_alerts,
            'recent_alerts_count': recent_alerts,
            'coordinates': station.get_coordinates()
        }


class AlertRoutingService:
    """Service for routing alerts to appropriate stations and personnel"""
    
    @classmethod
    def route_emergency_alert(
        cls,
        alert_type: str,
        latitude: float,
        longitude: float,
        severity: str = 'medium',
        description: str = '',
        created_by_user=None
    ) -> Alert:
        """
        Create and route an emergency alert to the nearest appropriate station.
        
        Args:
            alert_type: Type of emergency
            latitude: Emergency location latitude
            longitude: Emergency location longitude
            severity: Alert severity level
            description: Alert description
            created_by_user: User creating the alert
            
        Returns:
            Created Alert object
        """
        from accounts.models import User
        
        # Get system user if no user provided
        if not created_by_user:
            created_by_user = User.objects.filter(role='System Administrator').first()
        
        # Determine department and priority
        department = Alert.get_department_for_alert_type(alert_type)
        priority_mapping = {
            'low': 'low',
            'medium': 'medium', 
            'high': 'high',
            'critical': 'high'
        }
        priority = priority_mapping.get(severity, 'medium')
        
        # Create alert
        alert = Alert.objects.create(
            title=f"Emergency: {alert_type.replace('_', ' ').title()}",
            alert_type=alert_type,
            description=description,
            location=f"Lat: {latitude}, Lng: {longitude}",
            latitude=latitude,
            longitude=longitude,
            priority=priority,
            status='active',
            department=department,
            created_by=created_by_user
        )
        
        # Assign to nearest station
        StationFinderService.assign_alert_to_nearest_station(alert)
        
        return alert
