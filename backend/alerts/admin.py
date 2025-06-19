from django.contrib import admin
from .models import Alert

@admin.register(Alert)
class AlertAdmin(admin.ModelAdmin):
    list_display = ('title', 'alert_type', 'department', 'priority', 'status', 'created_by', 'created_at')
    list_filter = ('department', 'priority', 'status', 'alert_type', 'created_at')
    search_fields = ('title', 'location', 'description')
    readonly_fields = ('created_at', 'updated_at')
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(department=request.user.department)
