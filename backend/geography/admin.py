from django.contrib import admin
from .models import Region, District, Station


@admin.register(Region)
class RegionAdmin(admin.ModelAdmin):
    list_display = ('display_name', 'name', 'district_count', 'total_staff_count', 'is_active', 'created_at')
    list_filter = ('is_active', 'created_at')
    search_fields = ('name', 'display_name', 'description')
    readonly_fields = ('region_id', 'created_at', 'updated_at', 'district_count', 'total_staff_count')
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('region_id', 'name', 'display_name', 'description')
        }),
        ('Geographic Data', {
            'fields': ('boundary_coordinates',)
        }),
        ('Status', {
            'fields': ('is_active',)
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at', 'district_count', 'total_staff_count'),
            'classes': ('collapse',)
        }),
    )


@admin.register(District)
class DistrictAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'department', 'region', 'manager', 'station_count', 'staff_count', 'is_active')
    list_filter = ('department', 'region', 'is_active', 'created_at')
    search_fields = ('name', 'code', 'address', 'city')
    readonly_fields = ('district_id', 'created_at', 'updated_at', 'station_count', 'staff_count', 'active_alerts_count')
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('district_id', 'name', 'code', 'department', 'region')
        }),
        ('Location', {
            'fields': ('address', 'city', 'state', 'zip_code', 'latitude', 'longitude')
        }),
        ('Management', {
            'fields': ('manager_id', 'phone')
        }),
        ('Operational Details', {
            'fields': ('description', 'coverage_area', 'population_served', 'established_date')
        }),
        ('Status', {
            'fields': ('is_active',)
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at', 'created_by_id', 'station_count', 'staff_count', 'active_alerts_count'),
            'classes': ('collapse',)
        }),
    )


@admin.register(Station)
class StationAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'station_type', 'department', 'region', 'manager', 'staff_count', 'is_active')
    list_filter = ('station_type', 'department', 'region', 'is_active', 'created_at')
    search_fields = ('name', 'code', 'address', 'city')
    readonly_fields = ('station_id', 'created_at', 'updated_at', 'staff_count')

    fieldsets = (
        ('Basic Information', {
            'fields': ('station_id', 'name', 'code', 'station_type', 'department', 'region')
        }),
        ('Location', {
            'fields': ('address', 'city', 'state', 'zip_code', 'latitude', 'longitude')
        }),
        ('Management', {
            'fields': ('manager_id', 'phone')
        }),
        ('Operational Details', {
            'fields': ('description', 'capacity', 'operating_hours', 'established_date')
        }),
        ('Status', {
            'fields': ('is_active',)
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at', 'created_by_id', 'staff_count'),
            'classes': ('collapse',)
        }),
    )
