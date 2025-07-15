from rest_framework import status, generics, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import logout
from django.utils import timezone
from .models import User, UserLoginHistory, UserSession, EmergencyContact, RegistrationRequest
from .serializers import (
    CustomTokenObtainPairSerializer, UserSerializer, CreateUserSerializer,
    UpdateUserSerializer, ChangePasswordSerializer, UserLoginHistorySerializer,
    RegisterUserSerializer, EmergencyContactSerializer, RegistrationRequestSerializer,
    RegistrationRequestDetailSerializer, RegistrationRequestReviewSerializer
)
from utils.email_service import EmailService
import secrets
import string
from django.db import transaction



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
        # Allow all authenticated users to see all users
        return User.objects.filter(is_active=True)

    def perform_create(self, serializer):
        # Allow all authenticated users to create users (less strict)
        serializer.save()

class UserDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    
    def get_serializer_class(self):
        if self.request.method in ['PUT', 'PATCH']:
            return UpdateUserSerializer
        return UserSerializer
    
    def get_queryset(self):
        # Allow all authenticated users to see all users
        return User.objects.filter(is_active=True)

    def perform_update(self, serializer):
        # Allow all authenticated users to update users (less strict)
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


# Registration Request Views
@api_view(['POST'])
@permission_classes([AllowAny])
def submit_registration_request(request):
    """Submit a new registration request"""
    serializer = RegistrationRequestSerializer(data=request.data)
    if serializer.is_valid():
        registration_request = serializer.save()
        return Response({
            'message': 'Registration request submitted successfully',
            'request_id': str(registration_request.request_id)
        }, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def list_registration_requests(request):
    """List all registration requests (Admin only)"""
    if request.user.role != 'Admin':
        return Response({'error': 'Permission denied'}, status=status.HTTP_403_FORBIDDEN)

    # Filter by status if provided
    status_filter = request.query_params.get('status')
    queryset = RegistrationRequest.objects.all()

    if status_filter:
        queryset = queryset.filter(status=status_filter)

    # Pagination
    page_size = int(request.query_params.get('page_size', 20))
    page = int(request.query_params.get('page', 1))
    start = (page - 1) * page_size
    end = start + page_size

    requests = queryset.order_by('-created_at')[start:end]
    serializer = RegistrationRequestDetailSerializer(requests, many=True)

    return Response({
        'results': serializer.data,
        'page': page,
        'page_size': page_size,
        'has_next': len(serializer.data) == page_size
    })


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_registration_request(request, request_id):
    """Get a specific registration request (Admin only)"""
    if request.user.role != 'Admin':
        return Response({'error': 'Permission denied'}, status=status.HTTP_403_FORBIDDEN)

    try:
        registration_request = RegistrationRequest.objects.get(request_id=request_id)
        serializer = RegistrationRequestDetailSerializer(registration_request)
        return Response(serializer.data)
    except RegistrationRequest.DoesNotExist:
        return Response({'error': 'Registration request not found'}, status=status.HTTP_404_NOT_FOUND)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def review_registration_request(request, request_id):
    """Approve or deny a registration request (Admin only)"""
    if request.user.role != 'Admin':
        return Response({'error': 'Permission denied'}, status=status.HTTP_403_FORBIDDEN)

    try:
        registration_request = RegistrationRequest.objects.get(request_id=request_id)

        if registration_request.status != 'pending':
            return Response({'error': 'Request has already been reviewed'}, status=status.HTTP_400_BAD_REQUEST)

        serializer = RegistrationRequestReviewSerializer(data=request.data)
        if serializer.is_valid():
            registration_request.status = serializer.validated_data['status']
            registration_request.review_notes = serializer.validated_data.get('review_notes', '')
            registration_request.reviewed_by_id = request.user.id
            registration_request.reviewed_at = timezone.now()
            registration_request.save()

            # If approved, create the user account and station
            if registration_request.status == 'approved':
                # Check if user with this email already exists
                if User.objects.filter(email=registration_request.email).exists():
                    return Response({
                        'error': f'A user with email {registration_request.email} already exists. Cannot create duplicate account.'
                    }, status=status.HTTP_400_BAD_REQUEST)

                # Check if username already exists (since we use email as username)
                if User.objects.filter(username=registration_request.email).exists():
                    return Response({
                        'error': f'A user with username {registration_request.email} already exists. Cannot create duplicate account.'
                    }, status=status.HTTP_400_BAD_REQUEST)

                try:
                    from geography.models import Station

                    # Create the station directly without district complexity
                    station = Station.objects.create(
                        name=registration_request.station_name,
                        code=f"{registration_request.department.upper()}-{registration_request.station_name.replace(' ', '').upper()[:8]}",
                        station_type='headquarters',
                        department=registration_request.department,
                        region=registration_request.region,
                        address=registration_request.station_address,
                        city='TBD',  # Can be updated later
                        state='TBD',  # Can be updated later
                        zip_code='00000',  # Can be updated later
                        latitude=registration_request.latitude,
                        longitude=registration_request.longitude,
                        description=f'Station registered via registration request',
                        created_by_id=request.user.id
                    )

                    # Create the user as Station Manager with default password
                    user = User.objects.create_user(
                        username=registration_request.email,
                        email=registration_request.email,
                        full_name=registration_request.full_name,
                        phone_number=registration_request.phone_number,
                        department=registration_request.department,
                        role='Station Manager',
                        region=registration_request.region,
                        station_id=station.station_id,
                        password=registration_request.password,
                        is_active=True,  # Activate the user immediately
                        is_active_user=True
                    )

                                # Send welcome email with credentials
                    email_service = EmailService()
                    email_sent, email_result = email_service.send_welcome_email(
                        user_email=user.email,
                        user_name=user.full_name,
                        password="Use the password you used when submitting the request"
                    )

                    if not email_sent:
                        # Log the error but don't fail the user creation
                        print(f"Failed to send welcome email to {user.email}: {email_result}")

                    # Update the station to reference this user as manager
                    station.manager_id = user.id
                    station.save()

                    return Response({
                        'message': 'Registration request approved, station and user created',
                        'user_id': str(user.id),
                        'station_id': str(station.station_id),
                        'station_name': station.name
                    })

                except Exception as e:
                    # If creation fails for any reason, revert the registration status
                    registration_request.status = 'pending'
                    registration_request.reviewed_by_id = None
                    registration_request.reviewed_at = None
                    registration_request.save()

                    return Response({
                        'error': f'Failed to create user account and station: {str(e)}'
                    }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            else:
                return Response({'message': 'Registration request denied'})

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    except RegistrationRequest.DoesNotExist:
        return Response({'error': 'Registration request not found'}, status=status.HTTP_404_NOT_FOUND)


# Admin Management Views
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_admin_user(request):
    """Create a new admin user (System Administrator only)"""
    if request.user.role != 'System Administrator':
        return Response({'error': 'Permission denied'}, status=status.HTTP_403_FORBIDDEN)

    serializer = CreateUserSerializer(data=request.data, context={'request': request})
    if serializer.is_valid():
        # Generate a temporary password
        import secrets
        import string
        temp_password = ''.join(secrets.choice(string.ascii_letters + string.digits) for _ in range(12))

        # Create the user
        user_data = serializer.validated_data.copy()
        user_data.pop('password_confirm', None)
        user_data['password'] = temp_password
        user_data['created_by_id'] = request.user.id

        user = User.objects.create_user(**user_data)

        return Response({
            'message': 'Admin user created successfully',
            'user_id': str(user.id),
            'temporary_password': temp_password,
            'user': UserSerializer(user).data
        }, status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def list_regional_managers(request):
    """List all regional managers - now accessible to all authenticated users"""

    regional_managers = User.objects.filter(role='Regional Manager', is_active=True)

    # Filter by department if provided
    department = request.query_params.get('department')
    if department:
        regional_managers = regional_managers.filter(department=department)

    # Filter by region if provided
    region = request.query_params.get('region')
    if region:
        regional_managers = regional_managers.filter(region=region)

    serializer = UserSerializer(regional_managers, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_user_hierarchy(request):
    """Get the user hierarchy - now accessible to all authenticated users"""
    user = request.user

    # Return all users grouped by role for all authenticated users
    users = User.objects.filter(is_active=True).exclude(id=user.id)

    hierarchy = {
        'admins': UserSerializer(users.filter(role='Admin'), many=True).data,
        'station_managers': UserSerializer(users.filter(role='Station Manager'), many=True).data,
        'field_officers': UserSerializer(users.filter(role='Field Officer'), many=True).data,
    }

    # Note: The above hierarchy is returned for all users regardless of role
    # Frontend will handle role-based display and routing

    return Response(hierarchy)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_subordinate_user(request):
    """Create a subordinate user based on current user's role"""
    user = request.user

    # Check if user can create subordinates
    if user.role not in ['System Administrator', 'Regional Manager', 'District Manager', 'Station Manager']:
        return Response({'error': 'Permission denied'}, status=status.HTTP_403_FORBIDDEN)

    serializer = CreateUserSerializer(data=request.data, context={'request': request})
    if serializer.is_valid():
        # Generate a temporary password
        import secrets
        import string
        temp_password = ''.join(secrets.choice(string.ascii_letters + string.digits) for _ in range(12))

        # Create the user with appropriate hierarchy
        user_data = serializer.validated_data.copy()
        user_data.pop('password_confirm', None)
        user_data['password'] = temp_password
        user_data['created_by_id'] = user.id

        # Set hierarchy based on creator's role
        if user.role == 'Regional Manager':
            user_data['region'] = user.region
            user_data['department'] = user.department
        elif user.role == 'District Manager':
            user_data['region'] = user.region
            user_data['department'] = user.department
            user_data['district_id'] = user.district_id
        elif user.role == 'Station Manager':
            user_data['region'] = user.region
            user_data['department'] = user.department
            user_data['district_id'] = user.district_id
            user_data['station_id'] = user.station_id

        new_user = User.objects.create_user(**user_data)

        return Response({
            'message': 'User created successfully',
            'user_id': str(new_user.id),
            'temporary_password': temp_password,
            'user': UserSerializer(new_user).data
        }, status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


def generate_random_password(length=12):
    """Generate a random password with letters, digits, and special characters"""
    characters = string.ascii_letters + string.digits + "!@#$%^&*"
    password = ''.join(secrets.choice(characters) for _ in range(length))
    return password


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_field_officer(request):
    """Create a new field officer with email notification"""

    # Check if user has permission to create field officers
    if request.user.role not in ['Admin', 'Station Manager']:
        return Response({'error': 'Permission denied'}, status=status.HTTP_403_FORBIDDEN)

    try:
        data = request.data

        # Validate required fields
        required_fields = ['full_name', 'email', 'department', 'region']
        for field in required_fields:
            if not data.get(field):
                return Response({'error': f'{field} is required'}, status=status.HTTP_400_BAD_REQUEST)

        # Check if user with this email already exists
        if User.objects.filter(email=data['email']).exists():
            return Response({'error': 'User with this email already exists'}, status=status.HTTP_400_BAD_REQUEST)

        # Generate random password
        random_password = generate_random_password()

        # Create the field officer
        with transaction.atomic():
            user = User.objects.create_user(
                username=data['email'],
                email=data['email'],
                full_name=data['full_name'],
                phone_number=data.get('phone_number', ''),
                department=data['department'],
                role='Field Officer',
                region=data['region'],
                station_id=data.get('station_id') if data.get('station_id') else None,
                password=random_password,
                is_active=True,
                is_active_user=True
            )

            # Send welcome email with credentials
            email_service = EmailService()
            email_sent, email_result = email_service.send_welcome_email(
                user_email=user.email,
                user_name=user.full_name,
                password=random_password
            )

            if not email_sent:
                # Log the error but don't fail the user creation
                print(f"Failed to send welcome email to {user.email}: {email_result}")

            # Serialize user data for response
            serializer = UserSerializer(user)

            return Response({
                'message': 'Field officer created successfully',
                'user': serializer.data,
                'email_sent': email_sent,
                'temporary_password': random_password if not email_sent else None  # Only return password if email failed
            }, status=status.HTTP_201_CREATED)

    except Exception as e:
        return Response({'error': f'Failed to create field officer: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
