from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from . import views

urlpatterns = [
    # Authentication
    path('login/', views.CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register_user, name='register_user'),  # New registration endpoint
    
    # User Profile
    path('me/', views.current_user, name='current_user'),
    path('profile/update/', views.update_profile, name='update_profile'),
    path('password/change/', views.change_password, name='change_password'),
    
    # User Management
    path('users/', views.UserListCreateView.as_view(), name='user_list_create'),
    path('users/<uuid:pk>/', views.UserDetailView.as_view(), name='user_detail'),
    path('users/statistics/', views.user_statistics, name='user_statistics'),
    
    # Login History
    path('login-history/', views.login_history, name='login_history'),

    # Emergency Contacts
    path('emergency-contacts/', views.EmergencyContactListCreateView.as_view(), name='emergency_contact_list_create'),
    path('emergency-contacts/<uuid:pk>/', views.EmergencyContactDetailView.as_view(), name='emergency_contact_detail'),

    # Registration Requests
    path('registration-request/', views.submit_registration_request, name='submit_registration_request'),
    path('registration-requests/', views.list_registration_requests, name='list_registration_requests'),
    path('registration-requests/<uuid:request_id>/', views.get_registration_request, name='get_registration_request'),
    path('registration-requests/<uuid:request_id>/review/', views.review_registration_request, name='review_registration_request'),

    # Admin Management
    path('admin/create-user/', views.create_admin_user, name='create_admin_user'),
    path('admin/regional-managers/', views.list_regional_managers, name='list_regional_managers'),
    path('admin/hierarchy/', views.get_user_hierarchy, name='get_user_hierarchy'),
    path('admin/create-subordinate/', views.create_subordinate_user, name='create_subordinate_user'),

    # Field Officer Management
    path('field-officers/', views.create_field_officer, name='create_field_officer'),
]
