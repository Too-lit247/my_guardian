#!/usr/bin/env python
import os
import sys
import django

# Add the project directory to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'emergency_system.settings')
django.setup()

from django.db import connection
from geography.models import Region, District, Station
from alerts.models import Alert

def check_database_tables():
    """Check what tables exist in the database"""
    print("🔍 Checking Database Tables and Data")
    print("=" * 50)
    
    try:
        with connection.cursor() as cursor:
            # Get all tables
            cursor.execute("""
                SELECT table_name 
                FROM information_schema.tables 
                WHERE table_schema = 'public' 
                ORDER BY table_name;
            """)
            tables = cursor.fetchall()
            
            print(f"📊 Found {len(tables)} tables in database:")
            for table in tables:
                print(f"  - {table[0]}")
            
            print("\n" + "=" * 50)
            
            # Check geography tables specifically
            geography_tables = ['regions', 'geography_districts', 'geography_stations']
            print("🗺️  Geography Tables Status:")
            for table_name in geography_tables:
                cursor.execute(f"SELECT COUNT(*) FROM {table_name};")
                count = cursor.fetchone()[0]
                print(f"  - {table_name}: {count} records")
            
            print("\n" + "=" * 50)
            
            # Check model counts
            print("📈 Model Record Counts:")
            print(f"  - Regions: {Region.objects.count()}")
            print(f"  - Districts: {District.objects.count()}")
            print(f"  - Stations: {Station.objects.count()}")
            print(f"  - Alerts: {Alert.objects.count()}")
            
            print("\n" + "=" * 50)
            
            # Show sample data
            print("📋 Sample Data:")
            
            if Region.objects.exists():
                print("\n🌍 Regions:")
                for region in Region.objects.all():
                    print(f"  - {region.display_name} ({region.name})")
            
            if District.objects.exists():
                print("\n🏢 Districts:")
                for district in District.objects.all():
                    print(f"  - {district.name} ({district.department}) - {district.region.display_name}")
            
            if Station.objects.exists():
                print("\n🚒 Stations:")
                for station in Station.objects.all():
                    print(f"  - {station.name} ({station.district.department}) - {station.district.name}")
            
            if Alert.objects.exists():
                print("\n🚨 Recent Alerts:")
                for alert in Alert.objects.all()[:5]:
                    assigned_station = alert.assigned_station.name if alert.assigned_station else "Unassigned"
                    print(f"  - {alert.title} ({alert.department}) - {assigned_station}")
            
            print("\n✅ Database connection and tables verified successfully!")
            
    except Exception as e:
        print(f"❌ Error checking database: {e}")
        return False
    
    return True

if __name__ == "__main__":
    check_database_tables()
