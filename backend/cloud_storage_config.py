"""
Cloud Storage Configuration for Production Deployment
Supports AWS S3, Google Cloud Storage, and Firebase Storage
"""

import os
from decouple import config

def get_storage_settings():
    """
    Get storage settings based on environment variables
    Returns appropriate storage configuration for production
    """
    
    # Check if we're in production (not DEBUG mode)
    DEBUG = config('DEBUG', default=True, cast=bool)
    
    if DEBUG:
        # Development - use local storage
        return {
            'DEFAULT_FILE_STORAGE': 'django.core.files.storage.FileSystemStorage',
            'MEDIA_URL': '/media/',
            'MEDIA_ROOT': 'media',
        }
    
    # Production - use cloud storage
    storage_backend = config('STORAGE_BACKEND', default='s3')
    
    if storage_backend == 's3':
        # AWS S3 Configuration
        return {
            'DEFAULT_FILE_STORAGE': 'storages.backends.s3boto3.S3Boto3Storage',
            'AWS_ACCESS_KEY_ID': config('AWS_ACCESS_KEY_ID'),
            'AWS_SECRET_ACCESS_KEY': config('AWS_SECRET_ACCESS_KEY'),
            'AWS_STORAGE_BUCKET_NAME': config('AWS_STORAGE_BUCKET_NAME'),
            'AWS_S3_REGION_NAME': config('AWS_S3_REGION_NAME', default='us-east-1'),
            'AWS_S3_FILE_OVERWRITE': False,
            'AWS_DEFAULT_ACL': None,
            'AWS_S3_VERIFY': True,
            'AWS_S3_CUSTOM_DOMAIN': f"{config('AWS_STORAGE_BUCKET_NAME')}.s3.amazonaws.com",
            'MEDIA_URL': f"https://{config('AWS_STORAGE_BUCKET_NAME')}.s3.amazonaws.com/",
        }
    
    elif storage_backend == 'gcs':
        # Google Cloud Storage Configuration
        return {
            'DEFAULT_FILE_STORAGE': 'storages.backends.gcloud.GoogleCloudStorage',
            'GS_BUCKET_NAME': config('GS_BUCKET_NAME'),
            'GS_PROJECT_ID': config('GS_PROJECT_ID'),
            'GS_DEFAULT_ACL': 'publicRead',
            'MEDIA_URL': f"https://storage.googleapis.com/{config('GS_BUCKET_NAME')}/",
        }
    
    elif storage_backend == 'firebase':
        # Firebase Storage Configuration
        return {
            'DEFAULT_FILE_STORAGE': 'storages.backends.gcloud.GoogleCloudStorage',
            'GS_BUCKET_NAME': config('FIREBASE_STORAGE_BUCKET', default='guardian-16d00.firebasestorage.app'),
            'GS_PROJECT_ID': config('FIREBASE_PROJECT_ID', default='guardian-16d00'),
            'GS_DEFAULT_ACL': 'publicRead',
            'MEDIA_URL': f"https://firebasestorage.googleapis.com/v0/b/{config('FIREBASE_STORAGE_BUCKET', default='guardian-16d00.firebasestorage.app')}/o/",
        }
    
    else:
        # Fallback to local storage with warning
        print("⚠️  WARNING: No cloud storage configured. Files will be lost on deployment restart!")
        return {
            'DEFAULT_FILE_STORAGE': 'django.core.files.storage.FileSystemStorage',
            'MEDIA_URL': '/media/',
            'MEDIA_ROOT': 'media',
        }

# Environment Variables Guide
REQUIRED_ENV_VARS = {
    's3': [
        'AWS_ACCESS_KEY_ID',
        'AWS_SECRET_ACCESS_KEY', 
        'AWS_STORAGE_BUCKET_NAME',
        'AWS_S3_REGION_NAME'
    ],
    'gcs': [
        'GS_BUCKET_NAME',
        'GS_PROJECT_ID'
    ],
    'firebase': [
        'FIREBASE_STORAGE_BUCKET',
        'FIREBASE_PROJECT_ID'
    ]
}

def check_storage_config():
    """Check if required environment variables are set"""
    storage_backend = config('STORAGE_BACKEND', default='s3')
    debug = config('DEBUG', default=True, cast=bool)
    
    if debug:
        print("✅ Development mode - using local storage")
        return True
    
    required_vars = REQUIRED_ENV_VARS.get(storage_backend, [])
    missing_vars = []
    
    for var in required_vars:
        if not config(var, default=None):
            missing_vars.append(var)
    
    if missing_vars:
        print(f"❌ Missing environment variables for {storage_backend} storage:")
        for var in missing_vars:
            print(f"   - {var}")
        return False
    
    print(f"✅ {storage_backend.upper()} storage configuration complete")
    return True

if __name__ == "__main__":
    print("🔍 Checking Storage Configuration")
    print("=" * 50)
    check_storage_config()
    
    print("\n📋 Current Settings:")
    settings = get_storage_settings()
    for key, value in settings.items():
        if 'SECRET' in key or 'KEY' in key:
            print(f"   {key}: {'*' * 8}")
        else:
            print(f"   {key}: {value}")
