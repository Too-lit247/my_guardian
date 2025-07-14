from rest_framework import serializers
from .models import Region, District, Station


class RegionSerializer(serializers.ModelSerializer):
    district_count = serializers.ReadOnlyField()
    total_staff_count = serializers.ReadOnlyField()
    
    class Meta:
        model = Region
        fields = [
            'region_id', 'name', 'display_name', 'description', 
            'boundary_coordinates', 'is_active', 'district_count', 
            'total_staff_count', 'created_at', 'updated_at'
        ]
        read_only_fields = ['region_id', 'created_at', 'updated_at']


class DistrictSerializer(serializers.ModelSerializer):
    region_name = serializers.CharField(source='region.display_name', read_only=True)
    manager_name = serializers.CharField(source='manager.full_name', read_only=True)
    station_count = serializers.ReadOnlyField()
    staff_count = serializers.ReadOnlyField()
    active_alerts_count = serializers.ReadOnlyField()
    coordinates = serializers.SerializerMethodField()
    
    class Meta:
        model = District
        fields = [
            'district_id', 'name', 'code', 'department', 'region', 'region_name',
            'address', 'city', 'state', 'zip_code', 'latitude', 'longitude',
            'coordinates', 'manager_id', 'manager_name', 'phone', 'description',
            'coverage_area', 'population_served', 'is_active', 'established_date',
            'station_count', 'staff_count', 'active_alerts_count', 'created_at', 'updated_at'
        ]
        read_only_fields = ['district_id', 'created_at', 'updated_at']
    
    def get_coordinates(self, obj):
        return obj.get_coordinates()


class DistrictCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating districts"""
    class Meta:
        model = District
        fields = [
            'name', 'code', 'address', 'city', 
            'state', 'zip_code', 'latitude', 'longitude', 'phone', 
            'description', 'coverage_area', 'population_served', 'established_date'
        ]
    
    def create(self, validated_data):
        # Set the creator
        validated_data['created_by_id'] = self.context['request'].user.id
        return super().create(validated_data)


class StationSerializer(serializers.ModelSerializer):
    district_name = serializers.CharField(source='district.name', read_only=True)
    region_name = serializers.CharField(source='district.region.display_name', read_only=True)
    manager_name = serializers.CharField(source='manager.full_name', read_only=True)
    staff_count = serializers.ReadOnlyField()
    department = serializers.ReadOnlyField()
    coordinates = serializers.SerializerMethodField()
    
    class Meta:
        model = Station
        fields = [
            'station_id', 'name', 'code', 'station_type', 'district', 'district_name',
            'region_name', 'address', 'city', 'state', 'zip_code', 'latitude', 
            'longitude', 'coordinates', 'manager_id', 'manager_name', 'phone',
            'description', 'capacity', 'operating_hours', 'is_active', 
            'established_date', 'staff_count', 'department', 'created_at', 'updated_at'
        ]
        read_only_fields = ['station_id', 'created_at', 'updated_at']
    
    def get_coordinates(self, obj):
        return obj.get_coordinates()


class StationCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating stations"""
    class Meta:
        model = Station
        fields = [
            'name', 'code', 'station_type', 'district', 'address', 'city',
            'state', 'zip_code', 'latitude', 'longitude', 'phone',
            'description', 'capacity', 'operating_hours', 'established_date'
        ]
    
    def create(self, validated_data):
        # Set the creator
        validated_data['created_by_id'] = self.context['request'].user.id
        return super().create(validated_data)


class StationListSerializer(serializers.ModelSerializer):
    """Simplified serializer for listing stations"""
    district_name = serializers.CharField(source='district.name', read_only=True)
    manager_name = serializers.CharField(source='manager.full_name', read_only=True)
    staff_count = serializers.ReadOnlyField()
    
    class Meta:
        model = Station
        fields = [
            'station_id', 'name', 'code', 'station_type', 'district_name',
            'manager_name', 'staff_count', 'is_active'
        ]
