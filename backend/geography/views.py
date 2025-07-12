from rest_framework import status, generics, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from .models import Region, District, Station
from .serializers import (
    RegionSerializer, DistrictSerializer, DistrictCreateSerializer,
    StationSerializer, StationCreateSerializer, StationListSerializer
)
from accounts.models import User


class RegionListView(generics.ListAPIView):
    """List all regions"""
    queryset = Region.objects.filter(is_active=True)
    serializer_class = RegionSerializer
    permission_classes = [IsAuthenticated]


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def list_districts(request):
    """List districts based on user role"""
    user = request.user
    
    if user.role == 'System Administrator':
        districts = District.objects.filter(is_active=True)
    elif user.role == 'Regional Manager':
        districts = District.objects.filter(
            region__name=user.region,
            department=user.department,
            is_active=True
        )
    else:
        return Response({'error': 'Permission denied'}, status=status.HTTP_403_FORBIDDEN)
    
    serializer = DistrictSerializer(districts, many=True)
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_district(request):
    """Create a new district (Regional Manager only)"""
    if request.user.role != 'Regional Manager':
        return Response({'error': 'Permission denied'}, status=status.HTTP_403_FORBIDDEN)
    
    serializer = DistrictCreateSerializer(data=request.data, context={'request': request})
    if serializer.is_valid():
        # Ensure the district is created in the manager's region and department
        district = serializer.save(
            region=Region.objects.get(name=request.user.region),
            department=request.user.department
        )
        return Response(DistrictSerializer(district).data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_district(request, district_id):
    """Get a specific district"""
    user = request.user
    
    try:
        district = District.objects.get(district_id=district_id, is_active=True)
        
        # Check permissions
        if user.role == 'System Administrator':
            pass  # Can view any district
        elif user.role == 'Regional Manager':
            if district.region.name != user.region or district.department != user.department:
                return Response({'error': 'Permission denied'}, status=status.HTTP_403_FORBIDDEN)
        elif user.role == 'District Manager':
            if district.district_id != user.district_id:
                return Response({'error': 'Permission denied'}, status=status.HTTP_403_FORBIDDEN)
        else:
            return Response({'error': 'Permission denied'}, status=status.HTTP_403_FORBIDDEN)
        
        serializer = DistrictSerializer(district)
        return Response(serializer.data)
        
    except District.DoesNotExist:
        return Response({'error': 'District not found'}, status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def list_stations(request):
    """List stations based on user role"""
    user = request.user
    district_id = request.query_params.get('district_id')
    
    if user.role == 'System Administrator':
        stations = Station.objects.filter(is_active=True)
        if district_id:
            stations = stations.filter(district__district_id=district_id)
    elif user.role == 'Regional Manager':
        stations = Station.objects.filter(
            district__region__name=user.region,
            district__department=user.department,
            is_active=True
        )
        if district_id:
            stations = stations.filter(district__district_id=district_id)
    elif user.role == 'District Manager':
        stations = Station.objects.filter(
            district__district_id=user.district_id,
            is_active=True
        )
    elif user.role == 'Station Manager':
        stations = Station.objects.filter(
            station_id=user.station_id,
            is_active=True
        )
    else:
        return Response({'error': 'Permission denied'}, status=status.HTTP_403_FORBIDDEN)
    
    serializer = StationListSerializer(stations, many=True)
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_station(request):
    """Create a new station (District Manager only)"""
    if request.user.role != 'District Manager':
        return Response({'error': 'Permission denied'}, status=status.HTTP_403_FORBIDDEN)
    
    serializer = StationCreateSerializer(data=request.data, context={'request': request})
    if serializer.is_valid():
        # Ensure the station is created in the manager's district
        station = serializer.save(
            district=District.objects.get(district_id=request.user.district_id)
        )
        return Response(StationSerializer(station).data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_station(request, station_id):
    """Get a specific station"""
    user = request.user
    
    try:
        station = Station.objects.get(station_id=station_id, is_active=True)
        
        # Check permissions
        if user.role == 'System Administrator':
            pass  # Can view any station
        elif user.role == 'Regional Manager':
            if (station.district.region.name != user.region or 
                station.district.department != user.department):
                return Response({'error': 'Permission denied'}, status=status.HTTP_403_FORBIDDEN)
        elif user.role == 'District Manager':
            if station.district.district_id != user.district_id:
                return Response({'error': 'Permission denied'}, status=status.HTTP_403_FORBIDDEN)
        elif user.role == 'Station Manager':
            if station.station_id != user.station_id:
                return Response({'error': 'Permission denied'}, status=status.HTTP_403_FORBIDDEN)
        else:
            return Response({'error': 'Permission denied'}, status=status.HTTP_403_FORBIDDEN)
        
        serializer = StationSerializer(station)
        return Response(serializer.data)
        
    except Station.DoesNotExist:
        return Response({'error': 'Station not found'}, status=status.HTTP_404_NOT_FOUND)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def assign_district_manager(request, district_id):
    """Assign a district manager to a district (Regional Manager only)"""
    if request.user.role != 'Regional Manager':
        return Response({'error': 'Permission denied'}, status=status.HTTP_403_FORBIDDEN)
    
    try:
        district = District.objects.get(district_id=district_id)
        
        # Check if district belongs to the regional manager
        if (district.region.name != request.user.region or 
            district.department != request.user.department):
            return Response({'error': 'Permission denied'}, status=status.HTTP_403_FORBIDDEN)
        
        user_id = request.data.get('user_id')
        if not user_id:
            return Response({'error': 'user_id is required'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            user = User.objects.get(id=user_id)
            
            # Update user role and district
            user.role = 'District Manager'
            user.district_id = district_id
            user.save()
            
            # Update district manager
            district.manager_id = user_id
            district.save()
            
            return Response({'message': 'District manager assigned successfully'})
            
        except User.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
            
    except District.DoesNotExist:
        return Response({'error': 'District not found'}, status=status.HTTP_404_NOT_FOUND)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def assign_station_manager(request, station_id):
    """Assign a station manager to a station (District Manager only)"""
    if request.user.role != 'District Manager':
        return Response({'error': 'Permission denied'}, status=status.HTTP_403_FORBIDDEN)
    
    try:
        station = Station.objects.get(station_id=station_id)
        
        # Check if station belongs to the district manager
        if station.district.district_id != request.user.district_id:
            return Response({'error': 'Permission denied'}, status=status.HTTP_403_FORBIDDEN)
        
        user_id = request.data.get('user_id')
        if not user_id:
            return Response({'error': 'user_id is required'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            user = User.objects.get(id=user_id)
            
            # Update user role and station
            user.role = 'Station Manager'
            user.station_id = station_id
            user.save()
            
            # Update station manager
            station.manager_id = user_id
            station.save()
            
            return Response({'message': 'Station manager assigned successfully'})
            
        except User.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
            
    except Station.DoesNotExist:
        return Response({'error': 'Station not found'}, status=status.HTTP_404_NOT_FOUND)
