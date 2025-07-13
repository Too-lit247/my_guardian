from django.urls import path
from . import views

urlpatterns = [
    path('', views.AlertListCreateView.as_view(), name='alert_list_create'),
    path('<int:pk>/', views.AlertDetailView.as_view(), name='alert_detail'),
    path('statistics/', views.alert_statistics, name='alert_statistics'),

    # Station routing endpoints
    path('find-stations/', views.find_nearest_stations, name='find_nearest_stations'),
    path('emergency/', views.create_emergency_alert, name='create_emergency_alert'),
    path('station-coverage/<uuid:station_id>/', views.get_station_coverage, name='station_coverage'),
]
