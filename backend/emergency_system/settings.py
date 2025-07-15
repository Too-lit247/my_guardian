import os
from pathlib import Path
from decouple import config, Csv
from datetime import timedelta

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config('SECRET_KEY', default='django-insecure-change-me-in-production')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = config('DEBUG', default=True, cast=bool)

# ALLOWED_HOSTS = config('ALLOWED_HOSTS', default='localhost,127.0.0.1,0.0.0.0,https://my-guardian-plus.onrender.com,*').split(',')
# ALLOWED_HOSTS = config('ALLOWED_HOSTS', default='*', cast=Csv())
ALLOWED_HOSTS = ['*']

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    
    # Third party apps
    'rest_framework',
    'rest_framework_simplejwt',
    'corsheaders',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    
    # Local apps
    'accounts',
    'alerts',
    'devices',  # Consolidated devices app (includes bracelets)
    'geography',  # Geographic hierarchy management
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'allauth.account.middleware.AccountMiddleware',
]

ROOT_URLCONF = 'emergency_system.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'emergency_system.wsgi.application'

# Database - Using Neon PostgreSQL
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': config('DB_NAME', default='emergency_db'),
        'USER': config('DB_USER', default=''),
        'PASSWORD': config('DB_PASSWORD', default=''),
        'HOST': config('DB_HOST', default=''),
        'PORT': config('DB_PORT', default='5432'),
        'OPTIONS': {
            'sslmode': 'require',
        },
    }
}

# If DATABASE_URL is provided (Neon format), parse it manually
DATABASE_URL = config('DATABASE_URL', default=None)
if DATABASE_URL:
    import urllib.parse as urlparse
    url = urlparse.urlparse(DATABASE_URL)
    DATABASES['default'] = {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': url.path[1:],  # Remove leading slash
        'USER': url.username,
        'PASSWORD': url.password,
        'HOST': url.hostname,
        'PORT': url.port or 5432,
        'OPTIONS': {
            'sslmode': 'require',
        },
    }

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    # {
    #     'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    # },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / "staticfiles"

# Only include STATICFILES_DIRS if the directory exists
if (BASE_DIR / "static").exists():
    STATICFILES_DIRS = [BASE_DIR / "static"]

# Media files - Cloud Storage Configuration
if DEBUG:
    # Development - Local storage
    MEDIA_URL = '/media/'
    MEDIA_ROOT = BASE_DIR / "media"
else:
    # Production - Cloud storage (configure via environment variables)
    STORAGE_BACKEND = config('STORAGE_BACKEND', default='s3')

    if STORAGE_BACKEND == 's3':
        # AWS S3 Configuration
        DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
        AWS_ACCESS_KEY_ID = config('AWS_ACCESS_KEY_ID', default='')
        AWS_SECRET_ACCESS_KEY = config('AWS_SECRET_ACCESS_KEY', default='')
        AWS_STORAGE_BUCKET_NAME = config('AWS_STORAGE_BUCKET_NAME', default='')
        AWS_S3_REGION_NAME = config('AWS_S3_REGION_NAME', default='us-east-1')
        AWS_S3_FILE_OVERWRITE = False
        AWS_DEFAULT_ACL = None
        AWS_S3_VERIFY = True
        if AWS_STORAGE_BUCKET_NAME:
            MEDIA_URL = f"https://{AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com/"

    elif STORAGE_BACKEND == 'firebase':
        # Firebase Storage Configuration using existing project
        DEFAULT_FILE_STORAGE = 'storages.backends.gcloud.GoogleCloudStorage'
        GS_BUCKET_NAME = config('FIREBASE_STORAGE_BUCKET', default='guardian-16d00.firebasestorage.app')
        GS_PROJECT_ID = config('FIREBASE_PROJECT_ID', default='guardian-16d00')
        GS_DEFAULT_ACL = 'publicRead'

        # Use service account JSON if provided, otherwise use default credentials
        GOOGLE_APPLICATION_CREDENTIALS_JSON = config('GOOGLE_APPLICATION_CREDENTIALS_JSON', default=None)
        if GOOGLE_APPLICATION_CREDENTIALS_JSON:
            import json
            import tempfile
            # Write JSON to temporary file for Google Cloud Storage
            credentials_dict = json.loads(GOOGLE_APPLICATION_CREDENTIALS_JSON)
            temp_file = tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json')
            json.dump(credentials_dict, temp_file)
            temp_file.close()
            os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = temp_file.name

        MEDIA_URL = f"https://firebasestorage.googleapis.com/v0/b/{GS_BUCKET_NAME}/o/"

    else:
        # Fallback to local (will lose files on restart)
        MEDIA_URL = '/media/'
        MEDIA_ROOT = BASE_DIR / "media"

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# REST Framework settings
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 20,
}

# JWT Settings - Extended token lifetimes for less frequent refreshes
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(hours=config('JWT_ACCESS_TOKEN_LIFETIME', default=24, cast=int)),  # 24 hours instead of 1 hour
    'REFRESH_TOKEN_LIFETIME': timedelta(days=config('JWT_REFRESH_TOKEN_LIFETIME', default=7, cast=int)),  # 7 days instead of 1 day
    'ROTATE_REFRESH_TOKENS': False,  # Disable rotation to reduce complexity
    'BLACKLIST_AFTER_ROTATION': False,  # Disable blacklisting for less strict control
    'UPDATE_LAST_LOGIN': True,
    'ALGORITHM': 'HS256',
    'SIGNING_KEY': config('JWT_SECRET_KEY', default=SECRET_KEY),
    'VERIFYING_KEY': None,
    'AUDIENCE': None,
    'ISSUER': None,
    'JWK_URL': None,
    'LEEWAY': 300,  # 5 minutes leeway for clock skew
    'AUTH_HEADER_TYPES': ('Bearer',),
    'AUTH_HEADER_NAME': 'HTTP_AUTHORIZATION',
    'USER_ID_FIELD': 'id',
    'USER_ID_CLAIM': 'user_id',
    'USER_AUTHENTICATION_RULE': 'rest_framework_simplejwt.authentication.default_user_authentication_rule',
    'AUTH_TOKEN_CLASSES': ('rest_framework_simplejwt.tokens.AccessToken',),
    'TOKEN_TYPE_CLAIM': 'token_type',
    'TOKEN_USER_CLASS': 'rest_framework_simplejwt.models.TokenUser',
    'JTI_CLAIM': 'jti',
}

# CORS settings
CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "https://my-guardian-plus.onrender.com",
]

# Allow all origins for development (can be overridden by environment variable)
CORS_ALLOW_ALL_ORIGINS = config('CORS_ALLOW_ALL_ORIGINS', default=True, cast=bool)

# Security settings for CORS
CORS_ALLOW_CREDENTIALS = True

# Additional CORS settings
CORS_ALLOW_HEADERS = [
    'accept',
    'accept-encoding',
    'authorization',
    'content-type',
    'dnt',
    'origin',
    'user-agent',
    'x-csrftoken',
    'x-requested-with',
    'access-control-allow-origin',
    'access-control-allow-headers',
    'access-control-allow-methods',
]

CORS_ALLOW_METHODS = [
    'DELETE',
    'GET',
    'OPTIONS',
    'PATCH',
    'POST',
    'PUT',
]

# Custom user model
AUTH_USER_MODEL = 'accounts.User'

# Django Allauth settings
SITE_ID = 1
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_USERNAME_REQUIRED = True
ACCOUNT_AUTHENTICATION_METHOD = 'username_email'
ACCOUNT_EMAIL_VERIFICATION = 'none'  # Set to 'mandatory' for production
LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/'

# Email settings (configure for production)
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'  # For development

# File Upload Settings
FILE_UPLOAD_MAX_MEMORY_SIZE = 10 * 1024 * 1024  # 10MB
DATA_UPLOAD_MAX_MEMORY_SIZE = 10 * 1024 * 1024  # 10MB

# ML Model Settings
ML_MODELS_DIR = BASE_DIR / 'ml_models'
os.makedirs(ML_MODELS_DIR, exist_ok=True)

# Logging
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': BASE_DIR / 'logs' / 'django.log',
        },
        'console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
        },
    },
    'root': {
        'handlers': ['console', 'file'],
        'level': 'INFO',
    },
    'loggers': {
        'django': {
            'handlers': ['console', 'file'],
            'level': 'INFO',
            'propagate': False,
        },
        'devices': {
            'handlers': ['console', 'file'],
            'level': 'INFO',
            'propagate': False,
        },
    },
}

# Create logs directory
os.makedirs(BASE_DIR / 'logs', exist_ok=True)

BREVO_API_KEY = config('BREVO_API_KEY')
SENDER_EMAIL = config('SENDER_EMAIL')
SENDER_NAME = config('SENDER_NAME')


