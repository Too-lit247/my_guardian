from django.urls import path
from . import views

urlpatterns = [
    # Device Management
    path('', views.DeviceListView.as_view(), name='device_list'),
    path('register/', views.register_device, name='register_device'),
    path('data/', views.device_data_upload, name='device_data_upload'),
    
    # Department Registration
    path('departments/register/', views.register_department, name='register_department'),
    path('departments/registrations/', views.DepartmentRegistrationListView.as_view(), name='department_registrations'),
    path('departments/registrations/<uuid:registration_id>/approve/', views.approve_department_registration, name='approve_department'),
    
    # Emergency Triggers
    path('triggers/', views.EmergencyTriggerListView.as_view(), name='emergency_triggers'),
    path('triggers/<uuid:trigger_id>/acknowledge/', views.acknowledge_trigger, name='acknowledge_trigger'),
]
