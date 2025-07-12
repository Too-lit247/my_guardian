from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/auth/', include('accounts.urls')),
    path('api/alerts/', include('alerts.urls')),
    path('api/devices/', include('devices.urls')),  # Consolidated devices API
    path('api/geography/', include('geography.urls')),  # Geographic hierarchy management
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
