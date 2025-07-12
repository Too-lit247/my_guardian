from django.urls import path
from . import views

urlpatterns = [
    # Regions
    path('regions/', views.RegionListView.as_view(), name='list_regions'),
    
    # Districts
    path('districts/', views.list_districts, name='list_districts'),
    path('districts/create/', views.create_district, name='create_district'),
    path('districts/<uuid:district_id>/', views.get_district, name='get_district'),
    path('districts/<uuid:district_id>/assign-manager/', views.assign_district_manager, name='assign_district_manager'),
    
    # Stations
    path('stations/', views.list_stations, name='list_stations'),
    path('stations/create/', views.create_station, name='create_station'),
    path('stations/<uuid:station_id>/', views.get_station, name='get_station'),
    path('stations/<uuid:station_id>/assign-manager/', views.assign_station_manager, name='assign_station_manager'),
]
