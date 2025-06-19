from rest_framework import generics, permissions
from rest_framework.permissions import IsAuthenticated
from .models import District
from .serializers import DistrictSerializer

class DistrictListCreateView(generics.ListCreateAPIView):
    serializer_class = DistrictSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        user = self.request.user
        if user.role == 'regional':
            return District.objects.filter(department=user.department)
        else:
            raise permissions.PermissionDenied("Only regional managers can access districts.")
    
    def perform_create(self, serializer):
        user = self.request.user
        if user.role == 'regional':
            serializer.save(department=user.department)
        else:
            raise permissions.PermissionDenied("Only regional managers can create districts.")

class DistrictDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = DistrictSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        user = self.request.user
        if user.role == 'regional':
            return District.objects.filter(department=user.department)
        else:
            raise permissions.PermissionDenied("Only regional managers can access districts.")
