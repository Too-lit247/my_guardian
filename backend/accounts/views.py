from rest_framework import status, generics, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import logout
from django.utils import timezone
from .models import User, UserLoginHistory, UserSession, EmergencyContact
from .serializers import (
    CustomTokenObtainPairSerializer, UserSerializer, CreateUserSerializer,
    UpdateUserSerializer, ChangePasswordSerializer, UserLoginHistorySerializer,
    RegisterUserSerializer, EmergencyContactSerializer
)



class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

@api_view(['POST'])
@permission_classes([AllowAny])
def register_user(request):
    """Register a new user (self-registration)"""
    serializer = RegisterUserSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        return Response({
            'message': 'User registered successfully',
            'user_id': str(user.id),
            'username': user.username
        }, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout_view(request):
    try:
        # Get the refresh token from request
        refresh_token = request.data.get('refresh_token')
        if refresh_token:
            token = RefreshToken(refresh_token)
            token.blacklist()
        
        # Update login history
        if hasattr(request.user, 'login_history'):
            latest_login = request.user.login_history.filter(
                logout_time__isnull=True
            ).first()
            if latest_login:
                latest_login.logout_time = timezone.now()
                latest_login.save()
        
        # Deactivate user session
        session_key = request.session.session_key
        if session_key:
            UserSession.objects.filter(
                user=request.user,
                session_key=session_key
            ).update(is_active=False)
        
        logout(request)
        return Response({'message': 'Successfully logged out'}, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def current_user(request):
    serializer = UserSerializer(request.user)
    return Response(serializer.data)

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_profile(request):
    serializer = UpdateUserSerializer(request.user, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(UserSerializer(request.user).data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def change_password(request):
    serializer = ChangePasswordSerializer(data=request.data, context={'request': request})
    if serializer.is_valid():
        user = request.user
        user.set_password(serializer.validated_data['new_password'])
        user.save()
        return Response({'message': 'Password changed successfully'})
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserListCreateView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return CreateUserSerializer
        return UserSerializer
    
    def get_queryset(self):
        user = self.request.user
        return user.get_managed_users()
    
    def perform_create(self, serializer):
        user = self.request.user
        if not (user.role.role_name in ['Regional Manager', 'District Manager', 'System Administrator']):
            raise permissions.PermissionDenied("You don't have permission to create users.")
        serializer.save()

class UserDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    
    def get_serializer_class(self):
        if self.request.method in ['PUT', 'PATCH']:
            return UpdateUserSerializer
        return UserSerializer
    
    def get_queryset(self):
        user = self.request.user
        return user.get_managed_users()
    
    def perform_update(self, serializer):
        # Only allow certain fields to be updated by managers
        user = self.request.user
        target_user = self.get_object()
        
        if not user.can_manage_user(target_user):
            raise permissions.PermissionDenied("You don't have permission to update this user.")
        
        serializer.save()
    
    def perform_destroy(self, instance):
        user = self.request.user
        if not user.can_manage_user(instance):
            raise permissions.PermissionDenied("You don't have permission to delete this user.")
        
        # Don't actually delete, just deactivate
        instance.is_active = False
        instance.is_active_user = False
        instance.save()

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_statistics(request):
    user = request.user
    managed_users = user.get_managed_users()
    
    stats = {
        'total_users': managed_users.count(),
        'active_users': managed_users.filter(is_active_user=True).count(),
        'inactive_users': managed_users.filter(is_active_user=False).count(),
        'by_role': {
            'System Administrator': managed_users.filter(role__role_name='System Administrator').count(),
            'Regional Manager': managed_users.filter(role__role_name='Regional Manager').count(),
            'District Manager': managed_users.filter(role__role_name='District Manager').count(),
            'Field User': managed_users.filter(role__role_name='Field User').count(),
        },
        'recent_logins': managed_users.filter(
            last_login__gte=timezone.now() - timezone.timedelta(days=7)
        ).count()
    }
    
    return Response(stats)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def login_history(request):
    user_id = request.query_params.get('user_id')
    
    if user_id:
        # Check if current user can view this user's history
        try:
            target_user = User.objects.get(user_id=user_id)
            if not request.user.can_manage_user(target_user) and request.user != target_user:
                raise permissions.PermissionDenied("You don't have permission to view this user's login history.")
            history = UserLoginHistory.objects.filter(user=target_user)
        except User.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
    else:
        # Return current user's history
        history = UserLoginHistory.objects.filter(user=request.user)
    
    # Paginate results
    page_size = int(request.query_params.get('page_size', 20))
    page = int(request.query_params.get('page', 1))
    start = (page - 1) * page_size
    end = start + page_size
    
    history = history.order_by('-login_time')[start:end]
    serializer = UserLoginHistorySerializer(history, many=True)
    
    return Response({
        'results': serializer.data,
        'page': page,
        'page_size': page_size,
        'has_next': len(serializer.data) == page_size
    })

class EmergencyContactListCreateView(generics.ListCreateAPIView):
    serializer_class = EmergencyContactSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return EmergencyContact.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class EmergencyContactDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = EmergencyContactSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return EmergencyContact.objects.filter(user=self.request.user)
