from django.contrib import admin
from .models import District

@admin.register(District)
class DistrictAdmin(admin.ModelAdmin):
    list_display = ('name', 'department', 'manager', 'is_active', 'user_count', 'created_at')
    list_filter = ('department', 'is_active', 'created_at')
    search_fields = ('name', 'manager', 'address')
    readonly_fields = ('created_at', 'updated_at')
