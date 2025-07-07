import 'dart:convert';
import 'dart:math';
import 'package:shared_preferences/shared_preferences.dart';
import 'package:postgres/postgres.dart';
import 'package:flutter_dotenv/flutter_dotenv.dart';
import 'package:uuid/uuid.dart';
import 'package:bcrypt/bcrypt.dart';

class PostgreAuth {
  static final PostgreAuth _instance = PostgreAuth._internal();
  factory PostgreAuth() => _instance;
  PostgreAuth._internal();

  late Connection _conn;
  Map<String, dynamic>? _currentUser;

  // Add this public getter for the connection
  Connection get connection {
    return _conn;
  }

  Future<void> initialize() async {
    try {
      await _connect();
    } catch (e) {
      print('Database connection failed: $e');
      // Even if DB connection fails, we should still load stored user
    }

    // Always try to load stored user, even if DB connection failed
    await _loadStoredUser();
    print('Loaded user from storage: ${_currentUser != null ? 'Yes' : 'No'}');
    print('Is authenticated: $isAuthenticated');
  }

  Future<void> _connect() async {
    try {
      final host = dotenv.env['DB_HOST']!;
      final port = int.parse(dotenv.env['DB_PORT']!);
      final database = dotenv.env['DB_NAME']!;
      final username = dotenv.env['DB_USER']!;
      final password = dotenv.env['DB_PASSWORD']!;

      print('Connecting to: $host:$port');
      print('Database: $database');

      _conn = await Connection.open(
        Endpoint(
          host: host,
          port: port,
          database: database,
          username: username,
          password: password,
        ),
        settings: ConnectionSettings(sslMode: SslMode.require),
      ).timeout(const Duration(seconds: 10));

      print('Database connection successful');
    } catch (e) {
      print('Database connection failed: $e');
      rethrow;
    }
  }

  Future<void> _loadStoredUser() async {
    try {
      final prefs = await SharedPreferences.getInstance();
      final userJson = prefs.getString('user_data');
      print('Raw user data from SharedPreferences: $userJson');

      if (userJson != null) {
        _currentUser = jsonDecode(userJson);
        print('Successfully loaded user: ${_currentUser?['email']}');
      } else {
        print('No user data found in SharedPreferences');
      }
    } catch (e) {
      print('Error loading stored user: $e');
      _currentUser = null;
    }
  }

  Map<String, dynamic>? get currentUser => _currentUser;
  bool get isAuthenticated => _currentUser != null;

  // FIX: Added 'String' type to the password parameter
  Future<void> login({required String email, required String password}) async {
    try {
      print('Attempting login for email: $email');

      final result = await _conn.execute(
        Sql.named('SELECT * FROM users WHERE email = @email LIMIT 1'),
        parameters: {'email': email},
      );

      if (result.isEmpty) {
        print('Login failed: User not found for email: $email');
        throw Exception('User not found');
      }

      final row = result.first.toColumnMap();
      print('User found: ${row['email']}');

      final hashedPassword = row['password'];
      final isValid = BCrypt.checkpw(password, hashedPassword);
      if (!isValid) {
        print('Login failed: Invalid password for email: $email');
        throw Exception('Invalid password');
      }

      _currentUser = row;

      final jsonSerializableMap = Map<String, dynamic>.from(row);
      jsonSerializableMap.updateAll(
        (key, value) => value is DateTime ? value.toIso8601String() : value,
      );

      final prefs = await SharedPreferences.getInstance();
      await prefs.setString('user_data', jsonEncode(jsonSerializableMap));
      print('Login successful: User data saved to SharedPreferences');
    } catch (e) {
      print('Login error: $e');
      rethrow;
    }
  }

  Future<void> register({
    required String email,
    required String password,
    required String phoneNumber,
    String? username,
    String? firstName,
    String? lastName,
  }) async {
    try {
      print('Attempting registration for email: $email');

      final dpt = "System Administrator";
      final uuid = const Uuid().v4();
      final now = DateTime.now();
      final employeeId = 'EMP${Random().nextInt(999999)}';
      final badgeNumber = 'BDG${Random().nextInt(9999)}';
      final role = 'Field Officer';
      final fullName = '${firstName ?? 'First'} ${lastName ?? 'Last'}';

      print('Generated employee ID: $employeeId');
      print('Generated badge number: $badgeNumber');

      final row = await _conn.execute(
        Sql.named('''
          INSERT INTO users (
            id, email, password, phone_number, department, role,
            username, first_name, last_name, full_name,
            is_superuser, is_staff, is_active, date_joined,
            badge_number, rank, years_of_service, certifications,
            emergency_contact_name, emergency_contact_phone,
            medical_conditions, medications, allergies, blood_type,
            is_active_user, created_at, updated_at, employee_id
          ) VALUES (
            @id, @e, @p, @pn, @dpt, @role,
            @u, @fn, @ln, @full,
            FALSE, FALSE, TRUE, @joined,
            @badge, @rank, 0, 'None',
            'N/A', '0000000000',
            'None', 'None', 'None', 'O+',
            TRUE, @joined, @joined, @emp
          ) RETURNING *;
        '''),
        parameters: {
          'id': uuid,
          'e': email,
          'p': BCrypt.hashpw(password, BCrypt.gensalt()),
          'pn': phoneNumber,
          'dpt': dpt,
          'u': username ?? email.split('@').first,
          'fn': firstName ?? 'First',
          'ln': lastName ?? 'Last',
          'full': fullName,
          'joined': now.toUtc(),
          'badge': badgeNumber,
          'role': role,
          'emp': employeeId,
          'rank': 'Default',
        },
      );

      final rowData = row.first.toColumnMap();
      _currentUser = rowData;

      final jsonSerializableMap = Map<String, dynamic>.from(rowData);
      jsonSerializableMap.updateAll(
        (key, value) => value is DateTime ? value.toIso8601String() : value,
      );

      final prefs = await SharedPreferences.getInstance();
      await prefs.setString('user_data', jsonEncode(jsonSerializableMap));
      print('Registration successful: User data saved to SharedPreferences');
    } catch (e) {
      print('Registration error: $e');
      rethrow;
    }
  }

  Future<void> logout() async {
    try {
      print('Attempting logout...');
      final prefs = await SharedPreferences.getInstance();
      await prefs.remove('user_data');
      _currentUser = null;
      print('Logout successful: User data cleared from SharedPreferences');
    } catch (e) {
      print('Logout error: $e');
      rethrow;
    }
  }
}
