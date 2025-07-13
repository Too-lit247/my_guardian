from rest_framework import serializers
from .models import Alert

class AlertSerializer(serializers.ModelSerializer):
    created_by_name = serializers.CharField(source='created_by.get_full_name', read_only=True)
    assigned_station_name = serializers.CharField(source='assigned_station.name', read_only=True)
    coordinates = serializers.SerializerMethodField()

    class Meta:
        model = Alert
        fields = ['id', 'title', 'alert_type', 'description', 'location',
                 'latitude', 'longitude', 'coordinates', 'priority', 'status',
                 'department', 'assigned_to', 'assigned_station_id', 'assigned_station_name',
                 'created_by', 'created_by_name', 'created_at', 'updated_at',
                 'resolved_at', 'response_time', 'outcome']
        read_only_fields = ['id', 'created_by', 'created_at', 'updated_at']

    def get_coordinates(self, obj):
        return obj.get_coordinates()
    
    def create(self, validated_data):
        validated_data['created_by'] = self.context['request'].user

        # If no department specified, use user's department
        if 'department' not in validated_data:
            validated_data['department'] = self.context['request'].user.department

        # Create the alert
        alert = super().create(validated_data)

        # If coordinates are provided, try to assign to nearest station
        if alert.latitude and alert.longitude:
            from .services import StationFinderService
            StationFinderService.assign_alert_to_nearest_station(alert)

        return alert
