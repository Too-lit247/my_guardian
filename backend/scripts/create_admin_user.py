# Create a simple admin user for testing
from accounts.models import User

# Check if admin user exists
admin_user = User.objects.filter(username='admin').first()

if admin_user:
    print(f"Admin user already exists: {admin_user.username}")
    # Reset password to be sure
    admin_user.set_password('admin123')
    admin_user.save()
    print("Password reset to 'admin123'")
else:
    # Create admin user
    admin_user = User.objects.create_user(
        username='admin',
        email='admin@test.com',
        password='admin123',
        full_name='System Administrator',
        department='admin',
        role='System Administrator',
        employee_id='ADMIN001'
    )
    print(f"✅ Created admin user: {admin_user.username}")

print("\n=== LOGIN CREDENTIALS ===")
print("Username: admin")
print("Password: admin123")
print("Department: System Administrator")
print("Role: System Administrator")
