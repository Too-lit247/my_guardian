from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, RegistrationRequest

class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'department', 'role', 'region', 'is_staff')
    list_filter = ('department', 'role', 'region', 'is_staff', 'is_superuser', 'is_active')
    fieldsets = UserAdmin.fieldsets + (
        ('Department Info', {'fields': ('department', 'role', 'region', 'district_id', 'station_id', 'phone_number', 'is_active_user')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Department Info', {'fields': ('department', 'role', 'region', 'district_id', 'station_id', 'phone_number')}),
    )

@admin.register(RegistrationRequest)
class RegistrationRequestAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'organization_name', 'department', 'region', 'status', 'created_at', 'reviewed_by')
    list_filter = ('status', 'department', 'region', 'registration_type', 'created_at')
    search_fields = ('full_name', 'organization_name', 'email')
    readonly_fields = ('request_id', 'created_at', 'updated_at')

    fieldsets = (
        ('Request Information', {
            'fields': ('request_id', 'registration_type', 'organization_name', 'department', 'region')
        }),
        ('Personal Details', {
            'fields': ('full_name', 'email', 'phone_number')
        }),
        ('Location', {
            'fields': ('latitude', 'longitude', 'address')
        }),
        ('Documentation', {
            'fields': ('documentation',)
        }),
        ('Review Status', {
            'fields': ('status', 'reviewed_by_id', 'review_notes', 'reviewed_at')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

admin.site.register(User, CustomUserAdmin)
