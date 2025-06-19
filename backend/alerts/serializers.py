from rest_framework import serializers
from .models import Alert

class AlertSerializer(serializers.ModelSerializer):
    created_by_name = serializers.CharField(source='created_by.get_full_name', read_only=True)
    
    class Meta:
        model = Alert
        fields = ['id', 'title', 'alert_type', 'description', 'location', 
                 'priority', 'status', 'department', 'assigned_to', 
                 'created_by', 'created_by_name', 'created_at', 'updated_at', 
                 'resolved_at', 'response_time', 'outcome']
        read_only_fields = ['id', 'created_by', 'created_at', 'updated_at']
    
    def create(self, validated_data):
        validated_data['created_by'] = self.context['request'].user
        validated_data['department'] = self.context['request'].user.department
        return super().create(validated_data)
