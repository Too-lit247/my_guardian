from rest_framework import generics, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.utils import timezone
from django.db import models
from .models import Alert
from .serializers import AlertSerializer

class AlertListCreateView(generics.ListCreateAPIView):
    serializer_class = AlertSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        user = self.request.user
        queryset = Alert.objects.filter(department=user.department)
        
        # Filter by status if provided
        status_filter = self.request.query_params.get('status', None)
        if status_filter:
            queryset = queryset.filter(status=status_filter)
        
        # Filter by priority if provided
        priority_filter = self.request.query_params.get('priority', None)
        if priority_filter:
            queryset = queryset.filter(priority=priority_filter)
        
        # Search functionality
        search = self.request.query_params.get('search', None)
        if search:
            queryset = queryset.filter(
                models.Q(title__icontains=search) |
                models.Q(location__icontains=search) |
                models.Q(description__icontains=search)
            )
        
        return queryset

class AlertDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = AlertSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return Alert.objects.filter(department=self.request.user.department)
    
    def perform_update(self, serializer):
        # If status is being changed to resolved, set resolved_at
        if serializer.validated_data.get('status') == 'resolved':
            serializer.save(resolved_at=timezone.now())
        else:
            serializer.save()

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def alert_statistics(request):
    user = request.user
    alerts = Alert.objects.filter(department=user.department)
    
    stats = {
        'total_alerts': alerts.count(),
        'active_alerts': alerts.filter(status='active').count(),
        'resolved_alerts': alerts.filter(status='resolved').count(),
        'high_priority': alerts.filter(priority='high').count(),
        'recent_alerts': AlertSerializer(
            alerts.filter(created_at__gte=timezone.now() - timezone.timedelta(days=7))[:5], 
            many=True
        ).data
    }
    
    return Response(stats)
