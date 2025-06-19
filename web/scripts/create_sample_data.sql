-- Create sample districts
INSERT INTO districts (name, code, department, address, city, state, zip_code, manager, manager_email, manager_phone, description, population_served, is_active, created_at, updated_at) VALUES
('Downtown Fire District', 'DFD01', 'fire', '123 Main Street', 'Metro City', 'CA', '90210', 'John Smith', 'john.smith@fire.gov', '+15551234567', 'Central business district fire coverage', 50000, true, NOW(), NOW()),
('North Police District', 'NPD01', 'police', '456 North Avenue', 'Metro City', 'CA', '90211', 'Sarah Johnson', 'sarah.johnson@police.gov', '+15551234568', 'Northern residential area police coverage', 75000, true, NOW(), NOW()),
('Central Medical District', 'CMD01', 'medical', '789 Health Boulevard', 'Metro City', 'CA', '90212', 'Dr. Mike Davis', 'mike.davis@medical.gov', '+15551234569', 'Central medical emergency services', 100000, true, NOW(), NOW()),
('East Fire District', 'EFD01', 'fire', '321 East Road', 'Metro City', 'CA', '90213', 'Emily Brown', 'emily.brown@fire.gov', '+15551234570', 'Eastern industrial area fire coverage', 30000, true, NOW(), NOW()),
('South Police District', 'SPD01', 'police', '654 South Street', 'Metro City', 'CA', '90214', 'Robert Wilson', 'robert.wilson@police.gov', '+15551234571', 'Southern district police coverage', 60000, true, NOW(), NOW());

-- Create sample users (passwords will need to be set via Django admin or management command)
-- Regional Managers
INSERT INTO auth_user (username, email, first_name, last_name, department, role, employee_id, phone, badge_number, rank, years_of_service, is_active, is_active_user, date_joined) VALUES
('fire_regional', 'regional@fire.gov', 'Jane', 'Doe', 'fire', 'regional', 'FR001', '+15551111111', 'FR001', 'Fire Chief', 15, true, true, NOW()),
('police_regional', 'regional@police.gov', 'Mark', 'Johnson', 'police', 'regional', 'PR001', '+15551111112', 'PR001', 'Police Chief', 20, true, true, NOW()),
('medical_regional', 'regional@medical.gov', 'Dr. Lisa', 'Anderson', 'medical', 'regional', 'MR001', '+15551111113', 'MR001', 'Medical Director', 12, true, true, NOW());

-- District Managers
INSERT INTO auth_user (username, email, first_name, last_name, department, role, district_id, employee_id, phone, badge_number, rank, years_of_service, is_active, is_active_user, date_joined) VALUES
('fire_district_1', 'district1@fire.gov', 'John', 'Smith', 'fire', 'district', 1, 'FD001', '+15552222221', 'FD001', 'District Chief', 10, true, true, NOW()),
('fire_district_4', 'district4@fire.gov', 'Emily', 'Brown', 'fire', 'district', 4, 'FD004', '+15552222224', 'FD004', 'District Chief', 8, true, true, NOW()),
('police_district_2', 'district2@police.gov', 'Sarah', 'Johnson', 'police', 'district', 2, 'PD002', '+15552222222', 'PD002', 'Lieutenant', 12, true, true, NOW()),
('police_district_5', 'district5@police.gov', 'Robert', 'Wilson', 'police', 'district', 5, 'PD005', '+15552222225', 'PD005', 'Lieutenant', 9, true, true, NOW()),
('medical_district_3', 'district3@medical.gov', 'Dr. Mike', 'Davis', 'medical', 'district', 3, 'MD003', '+15552222223', 'MD003', 'Supervisor', 7, true, true, NOW());

-- Field Users
INSERT INTO auth_user (username, email, first_name, last_name, department, role, district_id, employee_id, phone, badge_number, rank, years_of_service, is_active, is_active_user, date_joined) VALUES
-- Fire Department Users
('firefighter_1', 'ff1@fire.gov', 'Tom', 'Wilson', 'fire', 'user', 1, 'FF101', '+15553333331', 'FF101', 'Firefighter', 5, true, true, NOW()),
('firefighter_2', 'ff2@fire.gov', 'Amy', 'Taylor', 'fire', 'user', 1, 'FF102', '+15553333332', 'FF102', 'Firefighter', 3, true, true, NOW()),
('firefighter_3', 'ff3@fire.gov', 'Chris', 'Moore', 'fire', 'user', 4, 'FF401', '+15553333333', 'FF401', 'Firefighter', 6, true, true, NOW()),

-- Police Department Users
('officer_1', 'po1@police.gov', 'David', 'Lee', 'police', 'user', 2, 'PO201', '+15553333334', 'PO201', 'Officer', 4, true, true, NOW()),
('officer_2', 'po2@police.gov', 'Jessica', 'White', 'police', 'user', 2, 'PO202', '+15553333335', 'PO202', 'Officer', 2, true, true, NOW()),
('officer_3', 'po3@police.gov', 'Michael', 'Brown', 'police', 'user', 5, 'PO501', '+15553333336', 'PO501', 'Officer', 7, true, true, NOW()),

-- Medical Department Users
('medic_1', 'med1@medical.gov', 'Dr. Anna', 'Garcia', 'medical', 'user', 3, 'MD301', '+15553333337', 'MD301', 'Paramedic', 8, true, true, NOW()),
('medic_2', 'med2@medical.gov', 'James', 'Martinez', 'medical', 'user', 3, 'MD302', '+15553333338', 'MD302', 'EMT', 4, true, true, NOW()),
('medic_3', 'med3@medical.gov', 'Linda', 'Rodriguez', 'medical', 'user', 3, 'MD303', '+15553333339', 'MD303', 'Paramedic', 6, true, true, NOW());

-- Create sample district resources
INSERT INTO district_resources (district_id, name, resource_type, description, quantity, is_available, last_maintenance, next_maintenance) VALUES
-- Fire District Resources
(1, 'Fire Engine 1', 'vehicle', 'Primary fire suppression vehicle', 1, true, '2024-01-15', '2024-04-15'),
(1, 'Ladder Truck 1', 'vehicle', 'Aerial ladder truck', 1, true, '2024-01-10', '2024-04-10'),
(1, 'Breathing Apparatus', 'equipment', 'Self-contained breathing apparatus', 20, true, '2024-01-20', '2024-07-20'),
(4, 'Fire Engine 4', 'vehicle', 'Primary fire suppression vehicle', 1, true, '2024-01-12', '2024-04-12'),
(4, 'Hazmat Unit', 'vehicle', 'Hazardous materials response unit', 1, true, '2024-01-18', '2024-04-18'),

-- Police District Resources
(2, 'Patrol Car 201', 'vehicle', 'Standard patrol vehicle', 1, true, '2024-01-08', '2024-04-08'),
(2, 'Patrol Car 202', 'vehicle', 'Standard patrol vehicle', 1, true, '2024-01-14', '2024-04-14'),
(2, 'Mobile Command Unit', 'vehicle', 'Mobile command and communication center', 1, true, '2024-01-05', '2024-04-05'),
(5, 'Patrol Car 501', 'vehicle', 'Standard patrol vehicle', 1, true, '2024-01-11', '2024-04-11'),
(5, 'K-9 Unit Vehicle', 'vehicle', 'Specialized K-9 patrol vehicle', 1, true, '2024-01-16', '2024-04-16'),

-- Medical District Resources
(3, 'Ambulance 301', 'vehicle', 'Advanced life support ambulance', 1, true, '2024-01-09', '2024-04-09'),
(3, 'Ambulance 302', 'vehicle', 'Basic life support ambulance', 1, true, '2024-01-13', '2024-04-13'),
(3, 'Mobile ICU', 'vehicle', 'Intensive care transport unit', 1, true, '2024-01-07', '2024-04-07'),
(3, 'Defibrillators', 'equipment', 'Automated external defibrillators', 15, true, '2024-01-21', '2024-07-21'),
(3, 'Oxygen Tanks', 'equipment', 'Portable oxygen supply units', 50, true, '2024-01-19', '2024-04-19');
