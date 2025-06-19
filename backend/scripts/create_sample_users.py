from accounts.models import User
from districts.models import District

# First, get the district IDs that were created
fire_districts = District.objects.filter(department='fire')
police_districts = District.objects.filter(department='police')
medical_districts = District.objects.filter(department='medical')

print("Available districts:")
for district in District.objects.all():
    print(f"- {district.name} ({district.department}): {district.id}")

# Create Regional Managers (one per department)
fire_regional = User.objects.create_user(
    username='fire_regional_mw',
    email='regional@fire.gov.mw',
    password='admin123',
    full_name='James Banda',
    department='fire',
    role='Regional Manager',
    employee_id='FR001',
    phone_number='+265991111111',
    badge_number='FR001',
    rank='Fire Chief',
    years_of_service=15
)

police_regional = User.objects.create_user(
    username='police_regional_mw',
    email='regional@police.gov.mw',
    password='admin123',
    full_name='Inspector General Mary Tembo',
    department='police',
    role='Regional Manager',
    employee_id='PR001',
    phone_number='+265991111112',
    badge_number='PR001',
    rank='Inspector General',
    years_of_service=20
)

medical_regional = User.objects.create_user(
    username='medical_regional_mw',
    email='regional@health.gov.mw',
    password='admin123',
    full_name='Dr. Francis Makwinja',
    department='medical',
    role='Regional Manager',
    employee_id='MR001',
    phone_number='+265991111113',
    badge_number='MR001',
    rank='Chief Medical Officer',
    years_of_service=12
)

# Create District Managers
district_managers = []

# Fire District Managers
for i, district in enumerate(fire_districts, 1):
    manager = User.objects.create_user(
        username=f'fire_district_{i}_mw',
        email=f'district{i}@fire.gov.mw',
        full_name=district.manager,
        department='fire',
        role='District Manager',
        district_id=district.id,
        employee_id=f'FD00{i}',
        phone_number=district.manager_phone,
        badge_number=f'FD00{i}',
        rank='District Fire Chief',
        years_of_service=10
    )
    manager.set_password('admin123')
    manager.save()
    district_managers.append(manager)

# Police District Managers
for i, district in enumerate(police_districts, 1):
    manager = User.objects.create_user(
        username=f'police_district_{i}_mw',
        email=f'district{i}@police.gov.mw',
        full_name=district.manager,
        department='police',
        role='District Manager',
        district_id=district.id,
        employee_id=f'PD00{i}',
        phone_number=district.manager_phone,
        badge_number=f'PD00{i}',
        rank='Chief Inspector',
        years_of_service=12
    )
    manager.set_password('admin123')
    manager.save()
    district_managers.append(manager)

# Medical District Managers
for i, district in enumerate(medical_districts, 1):
    manager = User.objects.create_user(
        username=f'medical_district_{i}_mw',
        email=f'district{i}@health.gov.mw',
        full_name=district.manager,
        department='medical',
        role='District Manager',
        district_id=district.id,
        employee_id=f'MD00{i}',
        phone_number=district.manager_phone,
        badge_number=f'MD00{i}',
        rank='District Medical Officer',
        years_of_service=8
    )
    manager.set_password('admin123')
    manager.save()
    district_managers.append(manager)

# Create Field Users
field_users = []

# Fire Department Field Users
lilongwe_fire = fire_districts.filter(name__icontains='Lilongwe').first()
if lilongwe_fire:
    for i in range(1, 4):
        user = User.objects.create_user(
            username=f'firefighter_{i}_lil',
            email=f'ff{i}@fire.gov.mw',
            full_name=f'Firefighter {["Tom Mwanza", "Amy Chirwa", "Chris Mbewe"][i-1]}',
            department='fire',
            role='Field User',
            district_id=lilongwe_fire.id,
            employee_id=f'FF10{i}',
            phone_number=f'+26599333333{i}',
            badge_number=f'FF10{i}',
            rank='Firefighter',
            years_of_service=5
        )
        user.set_password('admin123')
        user.save()
        field_users.append(user)

# Police Department Field Users
lilongwe_police = police_districts.filter(name__icontains='Lilongwe').first()
if lilongwe_police:
    for i in range(1, 4):
        user = User.objects.create_user(
            username=f'officer_{i}_lil',
            email=f'po{i}@police.gov.mw',
            full_name=f'Constable {["David Lungu", "Jessica Mvula", "Michael Banda"][i-1]}',
            department='police',
            role='Field User',
            district_id=lilongwe_police.id,
            employee_id=f'PO20{i}',
            phone_number=f'+26599444444{i}',
            badge_number=f'PO20{i}',
            rank='Police Constable',
            years_of_service=4
        )
        user.set_password('admin123')
        user.save()
        field_users.append(user)

# Medical Department Field Users
lilongwe_medical = medical_districts.filter(name__icontains='Lilongwe').first()
if lilongwe_medical:
    for i in range(1, 4):
        user = User.objects.create_user(
            username=f'medic_{i}_lil',
            email=f'med{i}@health.gov.mw',
            full_name=f'{["Paramedic Anna Gondwe", "EMT James Mwale", "Paramedic Linda Phiri"][i-1]}',
            department='medical',
            role='Field User',
            district_id=lilongwe_medical.id,
            employee_id=f'MD30{i}',
            phone_number=f'+26599555555{i}',
            badge_number=f'MD30{i}',
            rank=['Paramedic', 'EMT', 'Paramedic'][i-1],
            years_of_service=[8, 4, 6][i-1]
        )
        user.set_password('admin123')
        user.save()
        field_users.append(user)

print(f"\nCreated {len(district_managers)} district managers")
print(f"Created {len(field_users)} field users")
print("\nAll users created successfully!")
print("\nSample login credentials:")
print("Regional Manager (Fire): fire_regional_mw / admin123")
print("Regional Manager (Police): police_regional_mw / admin123")
print("Regional Manager (Medical): medical_regional_mw / admin123")
print("District Manager: fire_district_1_mw / admin123")
print("Field User: firefighter_1_lil / admin123")
