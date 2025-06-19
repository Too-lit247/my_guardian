from rest_framework import serializers
from .models import District

class DistrictSerializer(serializers.ModelSerializer):
    user_count = serializers.ReadOnlyField()
    
    class Meta:
        model = District
        fields = ['id', 'name', 'code', 'address', 'city', 'state', 'zip_code',
                 'manager', 'manager_email', 'manager_phone', 'description', 
                 'department', 'is_active', 'user_count', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']
