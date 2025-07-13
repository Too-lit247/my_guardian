from geography.models import District
from accounts.models import User
from django.utils import timezone

print("Creating Malawian sample data...")

# Create Districts first
districts_data = [
    # Fire Districts
    {
        'name': 'Lilongwe Central Fire District',
        'code': 'LCF01',
        'department': 'fire',
        'address': 'Area 3, Capital City',
        'city': 'Lilongwe',
        'state': 'Central Region',
        'zip_code': '00000',
        'manager': 'James Banda',
        'manager_email': 'j.banda@fire.gov.mw',
        'manager_phone': '+265991234567',
        'description': 'Central Lilongwe fire coverage',
        'population_served': 150000,
    },
    {
        'name': 'Blantyre Fire District',
        'code': 'BFD01',
        'department': 'fire',
        'address': 'Chichiri Industrial Area',
        'city': 'Blantyre',
        'state': 'Southern Region',
        'zip_code': '00000',
        'manager': 'Grace Mwale',
        'manager_email': 'g.mwale@fire.gov.mw',
        'manager_phone': '+265888234567',
        'description': 'Blantyre commercial and industrial fire coverage',
        'population_served': 200000,
    },
    {
        'name': 'Mzuzu Fire District',
        'code': 'MFD01',
        'department': 'fire',
        'address': 'Mzuzu City Centre',
        'city': 'Mzuzu',
        'state': 'Northern Region',
        'zip_code': '00000',
        'manager': 'Peter Phiri',
        'manager_email': 'p.phiri@fire.gov.mw',
        'manager_phone': '+265999234567',
        'description': 'Northern region fire coverage',
        'population_served': 80000,
    },
    # Police Districts
    {
        'name': 'Lilongwe Police District',
        'code': 'LPD01',
        'department': 'police',
        'address': 'Area 30, Police Headquarters',
        'city': 'Lilongwe',
        'state': 'Central Region',
        'zip_code': '00000',
        'manager': 'Inspector Mary Tembo',
        'manager_email': 'm.tembo@police.gov.mw',
        'manager_phone': '+265991345678',
        'description': 'Central Lilongwe police coverage',
        'population_served': 150000,
    },
    {
        'name': 'Blantyre Police District',
        'code': 'BPD01',
        'department': 'police',
        'address': 'Limbe Police Station',
        'city': 'Blantyre',
        'state': 'Southern Region',
        'zip_code': '00000',
        'manager': 'Chief Inspector John Kachale',
        'manager_email': 'j.kachale@police.gov.mw',
        'manager_phone': '+265888345678',
        'description': 'Blantyre metropolitan police coverage',
        'population_served': 200000,
    },
    {
        'name': 'Mzuzu Police District',
        'code': 'MPD01',
        'department': 'police',
        'address': 'Mzuzu Central Police',
        'city': 'Mzuzu',
        'state': 'Northern Region',
        'zip_code': '00000',
        'manager': 'Inspector Alice Nyirenda',
        'manager_email': 'a.nyirenda@police.gov.mw',
        'manager_phone': '+265999345678',
        'description': 'Northern region police coverage',
        'population_served': 80000,
    },
    # Medical Districts
    {
        'name': 'Lilongwe Medical District',
        'code': 'LMD01',
        'department': 'medical',
        'address': 'Kamuzu Central Hospital',
        'city': 'Lilongwe',
        'state': 'Central Region',
        'zip_code': '00000',
        'manager': 'Dr. Francis Makwinja',
        'manager_email': 'f.makwinja@health.gov.mw',
        'manager_phone': '+265991456789',
        'description': 'Central region medical emergency services',
        'population_served': 150000,
    },
    {
        'name': 'Blantyre Medical District',
        'code': 'BMD01',
        'department': 'medical',
        'address': 'Queen Elizabeth Central Hospital',
        'city': 'Blantyre',
        'state': 'Southern Region',
        'zip_code': '00000',
        'manager': 'Dr. Mercy Tsidya',
        'manager_email': 'm.tsidya@health.gov.mw',
        'manager_phone': '+265888456789',
        'description': 'Southern region medical emergency services',
        'population_served': 200000,
    },
    {
        'name': 'Mzuzu Medical District',
        'code': 'MMD01',
        'department': 'medical',
        'address': 'Mzuzu Central Hospital',
        'city': 'Mzuzu',
        'state': 'Northern Region',
        'zip_code': '00000',
        'manager': 'Dr. Patrick Gondwe',
        'manager_email': 'p.gondwe@health.gov.mw',
        'manager_phone': '+265999456789',
        'description': 'Northern region medical emergency services',
        'population_served': 80000,
    },
]

# Create districts
created_districts = []
for district_data in districts_data:
    district, created = District.objects.get_or_create(
        code=district_data['code'],
        defaults=district_data
    )
    if created:
        print(f"Created district: {district.name}")
    else:
        print(f"District already exists: {district.name}")
    created_districts.append(district)

print(f"\nTotal districts: {len(created_districts)}")

# Create Regional Managers
regional_managers = [
    {
        'username': 'fire_regional_mw',
        'email': 'regional@fire.gov.mw',
        'full_name': 'James Banda',
        'department': 'fire',
        'role': 'Regional Manager',
        'employee_id': 'FR001',
        'phone_number': '+265991111111',
        'badge_number': 'FR001',
        'rank': 'Fire Chief',
        'years_of_service': 15
    },
    {
        'username': 'police_regional_mw',
        'email': 'regional@police.gov.mw',
        'full_name': 'Inspector General Mary Tembo',
        'department': 'police',
        'role': 'Regional Manager',
        'employee_id': 'PR001',
        'phone_number': '+265991111112',
        'badge_number': 'PR001',
        'rank': 'Inspector General',
        'years_of_service': 20
    },
    {
        'username': 'medical_regional_mw',
        'email': 'regional@health.gov.mw',
        'full_name': 'Dr. Francis Makwinja',
        'department': 'medical',
        'role': 'Regional Manager',
        'employee_id': 'MR001',
        'phone_number': '+265991111113',
        'badge_number': 'MR001',
        'rank': 'Chief Medical Officer',
        'years_of_service': 12
    }
]

# Create regional managers
for manager_data in regional_managers:
    user, created = User.objects.get_or_create(
        username=manager_data['username'],
        defaults=manager_data
    )
    if created:
        user.set_password('admin123')
        user.save()
        print(f"Created regional manager: {user.full_name}")
    else:
        print(f"Regional manager already exists: {user.full_name}")

# Create District Managers
fire_districts = District.objects.filter(department='fire')
police_districts = District.objects.filter(department='police')
medical_districts = District.objects.filter(department='medical')

district_manager_count = 0

# Fire District Managers
for i, district in enumerate(fire_districts, 1):
    user_data = {
        'username': f'fire_district_{i}_mw',
        'email': f'district{i}@fire.gov.mw',
        'full_name': district.manager,
        'department': 'fire',
        'role': 'District Manager',
        'district_id': district.id,
        'employee_id': f'FD00{i}',
        'phone_number': district.manager_phone,
        'badge_number': f'FD00{i}',
        'rank': 'District Fire Chief',
        'years_of_service': 10
    }
    
    user, created = User.objects.get_or_create(
        username=user_data['username'],
        defaults=user_data
    )
    if created:
        user.set_password('admin123')
        user.save()
        print(f"Created fire district manager: {user.full_name}")
        district_manager_count += 1

# Police District Managers
for i, district in enumerate(police_districts, 1):
    user_data = {
        'username': f'police_district_{i}_mw',
        'email': f'district{i}@police.gov.mw',
        'full_name': district.manager,
        'department': 'police',
        'role': 'District Manager',
        'district_id': district.id,
        'employee_id': f'PD00{i}',
        'phone_number': district.manager_phone,
        'badge_number': f'PD00{i}',
        'rank': 'Chief Inspector',
        'years_of_service': 12
    }
    
    user, created = User.objects.get_or_create(
        username=user_data['username'],
        defaults=user_data
    )
    if created:
        user.set_password('admin123')
        user.save()
        print(f"Created police district manager: {user.full_name}")
        district_manager_count += 1

# Medical District Managers
for i, district in enumerate(medical_districts, 1):
    user_data = {
        'username': f'medical_district_{i}_mw',
        'email': f'district{i}@health.gov.mw',
        'full_name': district.manager,
        'department': 'medical',
        'role': 'District Manager',
        'district_id': district.id,
        'employee_id': f'MD00{i}',
        'phone_number': district.manager_phone,
        'badge_number': f'MD00{i}',
        'rank': 'District Medical Officer',
        'years_of_service': 8
    }
    
    user, created = User.objects.get_or_create(
        username=user_data['username'],
        defaults=user_data
    )
    if created:
        user.set_password('admin123')
        user.save()
        print(f"Created medical district manager: {user.full_name}")
        district_manager_count += 1

# Create Field Users
field_user_count = 0

# Fire Department Field Users (Lilongwe)
lilongwe_fire = fire_districts.filter(name__icontains='Lilongwe').first()
if lilongwe_fire:
    fire_field_users = [
        {'name': 'Tom Mwanza', 'rank': 'Firefighter'},
        {'name': 'Amy Chirwa', 'rank': 'Firefighter'},
        {'name': 'Chris Mbewe', 'rank': 'Senior Firefighter'}
    ]
    
    for i, user_info in enumerate(fire_field_users, 1):
        user_data = {
            'username': f'firefighter_{i}_lil',
            'email': f'ff{i}@fire.gov.mw',
            'full_name': user_info['name'],
            'department': 'fire',
            'role': 'Field User',
            'district_id': lilongwe_fire.id,
            'employee_id': f'FF10{i}',
            'phone_number': f'+26599333333{i}',
            'badge_number': f'FF10{i}',
            'rank': user_info['rank'],
            'years_of_service': 5
        }
        
        user, created = User.objects.get_or_create(
            username=user_data['username'],
            defaults=user_data
        )
        if created:
            user.set_password('admin123')
            user.save()
            print(f"Created firefighter: {user.full_name}")
            field_user_count += 1

# Police Department Field Users (Lilongwe)
lilongwe_police = police_districts.filter(name__icontains='Lilongwe').first()
if lilongwe_police:
    police_field_users = [
        {'name': 'David Lungu', 'rank': 'Police Constable'},
        {'name': 'Jessica Mvula', 'rank': 'Police Constable'},
        {'name': 'Michael Banda', 'rank': 'Senior Constable'}
    ]
    
    for i, user_info in enumerate(police_field_users, 1):
        user_data = {
            'username': f'officer_{i}_lil',
            'email': f'po{i}@police.gov.mw',
            'full_name': user_info['name'],
            'department': 'police',
            'role': 'Field User',
            'district_id': lilongwe_police.id,
            'employee_id': f'PO20{i}',
            'phone_number': f'+26599444444{i}',
            'badge_number': f'PO20{i}',
            'rank': user_info['rank'],
            'years_of_service': 4
        }
        
        user, created = User.objects.get_or_create(
            username=user_data['username'],
            defaults=user_data
        )
        if created:
            user.set_password('admin123')
            user.save()
            print(f"Created police officer: {user.full_name}")
            field_user_count += 1

# Medical Department Field Users (Lilongwe)
lilongwe_medical = medical_districts.filter(name__icontains='Lilongwe').first()
if lilongwe_medical:
    medical_field_users = [
        {'name': 'Anna Gondwe', 'rank': 'Paramedic', 'years': 8},
        {'name': 'James Mwale', 'rank': 'EMT', 'years': 4},
        {'name': 'Linda Phiri', 'rank': 'Senior Paramedic', 'years': 6}
    ]
    
    for i, user_info in enumerate(medical_field_users, 1):
        user_data = {
            'username': f'medic_{i}_lil',
            'email': f'med{i}@health.gov.mw',
            'full_name': user_info['name'],
            'department': 'medical',
            'role': 'Field User',
            'district_id': lilongwe_medical.id,
            'employee_id': f'MD30{i}',
            'phone_number': f'+26599555555{i}',
            'badge_number': f'MD30{i}',
            'rank': user_info['rank'],
            'years_of_service': user_info['years']
        }
        
        user, created = User.objects.get_or_create(
            username=user_data['username'],
            defaults=user_data
        )
        if created:
            user.set_password('admin123')
            user.save()
            print(f"Created medical staff: {user.full_name}")
            field_user_count += 1

print(f"\n=== SUMMARY ===")
print(f"Districts created: {len(created_districts)}")
print(f"Regional managers: 3")
print(f"District managers: {district_manager_count}")
print(f"Field users: {field_user_count}")
print(f"\n=== SAMPLE LOGIN CREDENTIALS ===")
print("Regional Manager (Fire): fire_regional_mw / admin123")
print("Regional Manager (Police): police_regional_mw / admin123")
print("Regional Manager (Medical): medical_regional_mw / admin123")
print("District Manager (Fire): fire_district_1_mw / admin123")
print("Field User (Fire): firefighter_1_lil / admin123")
print("Field User (Police): officer_1_lil / admin123")
print("Field User (Medical): medic_1_lil / admin123")
print("\nAll sample data created successfully!")
