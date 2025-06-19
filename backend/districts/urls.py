from django.urls import path
from . import views

urlpatterns = [
    path('', views.DistrictListCreateView.as_view(), name='district_list_create'),
    path('<int:pk>/', views.DistrictDetailView.as_view(), name='district_detail'),
]
