from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password
from .models import User, UserLoginHistory

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    department = serializers.ChoiceField(choices=User.DEPARTMENT_CHOICES)
    role = serializers.ChoiceField(choices=User.ROLE_CHOICES)
    
    def validate(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password')
        department = attrs.get('department')
        role = attrs.get('role')
        
        if username and password:
            user = authenticate(
                request=self.context.get('request'),
                username=username,
                password=password
            )
            
            if user:
                if not user.is_active:
                    raise serializers.ValidationError('User account is disabled.')
                
                if user.department != department:
                    raise serializers.ValidationError('Invalid department for this user.')
                
                if user.role != role:
                    raise serializers.ValidationError('Invalid role for this user.')
                
                # Log successful login
                request = self.context.get('request')
                if request:
                    UserLoginHistory.objects.create(
                        user=user,
                        ip_address=self.get_client_ip(request),
                        user_agent=request.META.get('HTTP_USER_AGENT', ''),
                        success=True
                    )
                
                # Update last login IP
                user.last_login_ip = self.get_client_ip(request)
                user.save(update_fields=['last_login_ip'])
                
                refresh = self.get_token(user)
                return {
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                    'user': UserSerializer(user).data
                }
            else:
                # Log failed login attempt
                request = self.context.get('request')
                if request:
                    try:
                        user_obj = User.objects.get(username=username)
                        UserLoginHistory.objects.create(
                            user=user_obj,
                            ip_address=self.get_client_ip(request),
                            user_agent=request.META.get('HTTP_USER_AGENT', ''),
                            success=False,
                            failure_reason='Invalid password'
                        )
                    except User.DoesNotExist:
                        pass
                
                raise serializers.ValidationError('Invalid username or password.')
        else:
            raise serializers.ValidationError('Must include username and password.')
    
    def get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip

class UserSerializer(serializers.ModelSerializer):
    district_name = serializers.SerializerMethodField()
    department_display = serializers.CharField(source='get_department_display', read_only=True)
    role_display = serializers.CharField(source='get_role_display', read_only=True)
    
    class Meta:
        model = User
        fields = [
            'id', 'username', 'email', 'full_name', 'phone_number',
            'employee_id', 'department', 'department_display', 'role', 'role_display',
            'district_id', 'district_name', 'badge_number', 'rank', 'years_of_service', 
            'certifications', 'is_active', 'is_active_user', 'date_joined', 
            'last_login', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'date_joined', 'last_login', 'created_at', 'updated_at', 
                           'department_display', 'role_display', 'district_name']
    
    def get_district_name(self, obj):
        district = obj.district
        return district.name if district else None

class CreateUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, validators=[validate_password])
    password_confirm = serializers.CharField(write_only=True)
    
    class Meta:
        model = User
        fields = [
            'username', 'email', 'full_name', 'phone_number', 'employee_id',
            'password', 'password_confirm', 'department', 'role', 'district_id',
            'badge_number', 'rank', 'years_of_service', 'certifications'
        ]
    
    def validate(self, attrs):
        if attrs['password'] != attrs['password_confirm']:
            raise serializers.ValidationError("Password fields didn't match.")
        return attrs
    
    def validate_district_id(self, value):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            user = request.user
            if user.role == 'District Manager' and value != user.district_id:
                raise serializers.ValidationError("You can only assign users to your own district.")
            elif user.role == 'Regional Manager' and value:
                # Check if district belongs to same department
                try:
                    from districts.models import District
                    district = District.objects.get(id=value)
                    if district.department != user.department:
                        raise serializers.ValidationError("You can only assign users to districts in your department.")
                except District.DoesNotExist:
                    raise serializers.ValidationError("District not found.")
        return value
    
    def create(self, validated_data):
        validated_data.pop('password_confirm')
        password = validated_data.pop('password')
        
        # Set department based on creator's department
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            validated_data['department'] = request.user.department
            validated_data['created_by_id'] = request.user.id
        
        user = User.objects.create_user(**validated_data)
        user.set_password(password)
        user.save()
        return user

class RegisterUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, validators=[validate_password])
    
    class Meta:
        model = User
        fields = [
            'username', 'email', 'full_name', 'phone_number', 
            'password', 'department'
        ]
    
    def create(self, validated_data):
        password = validated_data.pop('password')
        
        # Assign Field User role by default for self-registration
        validated_data['role'] = 'Field User'
        
        user = User.objects.create_user(**validated_data)
        user.set_password(password)
        user.save()
        return user

class UpdateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'full_name', 'email', 'phone_number', 'badge_number', 'rank', 
            'years_of_service', 'certifications', 'is_active_user'
        ]

class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True, validators=[validate_password])
    new_password_confirm = serializers.CharField(required=True)
    
    def validate(self, attrs):
        if attrs['new_password'] != attrs['new_password_confirm']:
            raise serializers.ValidationError("New password fields didn't match.")
        return attrs
    
    def validate_old_password(self, value):
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError("Old password is incorrect.")
        return value

class UserLoginHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = UserLoginHistory
        fields = ['ip_address', 'user_agent', 'login_time', 'logout_time', 'success', 'failure_reason']
