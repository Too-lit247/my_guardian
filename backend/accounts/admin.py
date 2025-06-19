from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'department', 'role', 'is_staff')
    list_filter = ('department', 'role', 'is_staff', 'is_superuser', 'is_active')
    fieldsets = UserAdmin.fieldsets + (
        ('Department Info', {'fields': ('department', 'role', 'district', 'phone', 'is_active_user')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Department Info', {'fields': ('department', 'role', 'district', 'phone')}),
    )

admin.site.register(User, CustomUserAdmin)
