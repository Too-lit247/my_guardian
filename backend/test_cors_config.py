#!/usr/bin/env python
import os
import sys
import django

# Add the project directory to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'emergency_system.settings')
django.setup()

from django.conf import settings

def check_cors_configuration():
    """Check the current CORS configuration"""
    print("🌐 CORS Configuration Check")
    print("=" * 50)
    
    # Check if corsheaders is installed
    if 'corsheaders' in settings.INSTALLED_APPS:
        print("✅ corsheaders app: Installed")
    else:
        print("❌ corsheaders app: NOT installed")
    
    # Check if CORS middleware is enabled
    if 'corsheaders.middleware.CorsMiddleware' in settings.MIDDLEWARE:
        print("✅ CORS middleware: Enabled")
        
        # Check position (should be first or near first)
        cors_position = settings.MIDDLEWARE.index('corsheaders.middleware.CorsMiddleware')
        if cors_position <= 2:
            print(f"✅ CORS middleware position: {cors_position} (Good)")
        else:
            print(f"⚠️  CORS middleware position: {cors_position} (Should be earlier)")
    else:
        print("❌ CORS middleware: NOT enabled")
    
    # Check CORS settings
    print(f"\n📋 CORS Settings:")
    
    if hasattr(settings, 'CORS_ALLOW_ALL_ORIGINS'):
        print(f"   CORS_ALLOW_ALL_ORIGINS: {settings.CORS_ALLOW_ALL_ORIGINS}")
    
    if hasattr(settings, 'CORS_ALLOWED_ORIGINS'):
        print(f"   CORS_ALLOWED_ORIGINS: {list(settings.CORS_ALLOWED_ORIGINS)}")
    
    if hasattr(settings, 'CORS_ALLOW_CREDENTIALS'):
        print(f"   CORS_ALLOW_CREDENTIALS: {settings.CORS_ALLOW_CREDENTIALS}")
    
    if hasattr(settings, 'CORS_ALLOW_METHODS'):
        print(f"   CORS_ALLOW_METHODS: {list(settings.CORS_ALLOW_METHODS)}")
    
    if hasattr(settings, 'CORS_ALLOW_HEADERS'):
        print(f"   CORS_ALLOW_HEADERS: {len(settings.CORS_ALLOW_HEADERS)} headers")
    
    # Check other relevant settings
    print(f"\n🔧 Other Settings:")
    print(f"   DEBUG: {settings.DEBUG}")
    print(f"   ALLOWED_HOSTS: {settings.ALLOWED_HOSTS}")
    
    # Recommendations
    print(f"\n💡 Recommendations:")
    
    if not hasattr(settings, 'CORS_ALLOW_ALL_ORIGINS') or not settings.CORS_ALLOW_ALL_ORIGINS:
        if not hasattr(settings, 'CORS_ALLOWED_ORIGINS') or 'http://localhost:3000' not in settings.CORS_ALLOWED_ORIGINS:
            print("   ⚠️  Add 'http://localhost:3000' to CORS_ALLOWED_ORIGINS")
    
    if 'corsheaders.middleware.CorsMiddleware' not in settings.MIDDLEWARE:
        print("   ❌ Add 'corsheaders.middleware.CorsMiddleware' to MIDDLEWARE (at the top)")
    
    if settings.CORS_ALLOW_ALL_ORIGINS:
        print("   ✅ CORS_ALLOW_ALL_ORIGINS is True - should work for development")
    
    print(f"\n🧪 Test URLs:")
    print(f"   Backend: https://my-guardian-plus.onrender.com")
    print(f"   Frontend: http://localhost:3000")
    print(f"   Login API: https://my-guardian-plus.onrender.com/api/auth/login/")
    
    return True

if __name__ == "__main__":
    check_cors_configuration()
