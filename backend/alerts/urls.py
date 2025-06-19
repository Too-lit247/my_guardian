from django.urls import path
from . import views

urlpatterns = [
    path('', views.AlertListCreateView.as_view(), name='alert_list_create'),
    path('<int:pk>/', views.AlertDetailView.as_view(), name='alert_detail'),
    path('statistics/', views.alert_statistics, name='alert_statistics'),
]
