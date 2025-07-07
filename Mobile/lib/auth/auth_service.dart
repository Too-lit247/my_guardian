// // auth_service.dart
// import 'dart:async';
// import 'dart:convert';
// import 'package:flutter/material.dart';
// import 'package:http/http.dart' as http;
// import 'package:shared_preferences/shared_preferences.dart';
// import 'package:flutter_dotenv/flutter_dotenv.dart';

// // User model
// class AuthUser {
//   final int id;
//   final String email;
//   final String? firstName;
//   final String? lastName;
//   final String? username;
//   final bool isActive;
//   final DateTime? dateJoined;

//   AuthUser({
//     required this.id,
//     required this.email,
//     this.firstName,
//     this.lastName,
//     this.username,
//     required this.isActive,
//     this.dateJoined,
//   });

//   factory AuthUser.fromJson(Map<String, dynamic> json) {
//     return AuthUser(
//       id: json['id'],
//       email: json['email'],
//       firstName: json['first_name'],
//       lastName: json['last_name'],
//       username: json['username'],
//       isActive: json['is_active'] ?? true,
//       dateJoined:
//           json['date_joined'] != null
//               ? DateTime.parse(json['date_joined'])
//               : null,
//     );
//   }

//   Map<String, dynamic> toJson() {
//     return {
//       'id': id,
//       'email': email,
//       'first_name': firstName,
//       'last_name': lastName,
//       'username': username,
//       'is_active': isActive,
//       'date_joined': dateJoined?.toIso8601String(),
//     };
//   }

//   String get displayName {
//     if (firstName != null && lastName != null) {
//       return '$firstName $lastName';
//     }
//     return username ?? email;
//   }
// }

// // Auth exception classes
// class AuthException implements Exception {
//   final String message;
//   final String code;

//   AuthException(this.message, this.code);

//   @override
//   String toString() => 'AuthException: $message';
// }

// class NetworkException extends AuthException {
//   NetworkException(String message) : super(message, 'network-error');
// }

// class InvalidCredentialsException extends AuthException {
//   InvalidCredentialsException()
//     : super('Invalid email or password', 'invalid-credentials');
// }

// class UserNotFoundException extends AuthException {
//   UserNotFoundException() : super('User not found', 'user-not-found');
// }

// class WeakPasswordException extends AuthException {
//   WeakPasswordException() : super('Password is too weak', 'weak-password');
// }

// class EmailAlreadyInUseException extends AuthException {
//   EmailAlreadyInUseException()
//     : super('Email is already in use', 'email-already-in-use');
// }

// // Auth service singleton
// class DjangoAuthService extends ChangeNotifier {
//   static final DjangoAuthService _instance = DjangoAuthService._internal();
//   factory DjangoAuthService() => _instance;
//   DjangoAuthService._internal();

//   // Configuration
//   final _baseUrl =
//       '${dotenv.env['BASE_URL']!}/api/auth'; //  'http://localhost:8000/api/auth';
//   static const String _tokenKey = 'auth_token';
//   static const String _refreshTokenKey = 'refresh_token';
//   static const String _userKey = 'user_data';

//   // State
//   AuthUser? _currentUser;
//   String? _token;
//   String? _refreshToken;
//   bool _isLoading = false;

//   // Getters
//   AuthUser? get currentUser => _currentUser;
//   String? get token => _token;
//   bool get isAuthenticated => _currentUser != null && _token != null;
//   bool get isLoading => _isLoading;

//   // Stream controller for auth state changes
//   final StreamController<AuthUser?> _authStateController =
//       StreamController<AuthUser?>.broadcast();

//   Stream<AuthUser?> get authStateChanges => _authStateController.stream;

//   // Initialize the service
//   Future<void> initialize() async {
//     await _loadStoredAuth();
//     if (_token != null) {
//       await _validateToken();
//     }
//   }

//   // Load stored authentication data
//   Future<void> _loadStoredAuth() async {
//     try {
//       final prefs = await SharedPreferences.getInstance();
//       _token = prefs.getString(_tokenKey);
//       _refreshToken = prefs.getString(_refreshTokenKey);

//       final userJson = prefs.getString(_userKey);
//       if (userJson != null) {
//         final userData = jsonDecode(userJson);
//         _currentUser = AuthUser.fromJson(userData);
//       }
//     } catch (e) {
//       await _clearStoredAuth();
//     }
//   }

//   // Save authentication data
//   Future<void> _saveAuthData(
//     String token,
//     String refreshToken,
//     AuthUser user,
//   ) async {
//     final prefs = await SharedPreferences.getInstance();
//     await prefs.setString(_tokenKey, token);
//     await prefs.setString(_refreshTokenKey, refreshToken);
//     await prefs.setString(_userKey, jsonEncode(user.toJson()));

//     _token = token;
//     _refreshToken = refreshToken;
//     _currentUser = user;
//   }

//   // Clear stored authentication data
//   Future<void> _clearStoredAuth() async {
//     final prefs = await SharedPreferences.getInstance();
//     await prefs.remove(_tokenKey);
//     await prefs.remove(_refreshTokenKey);
//     await prefs.remove(_userKey);

//     _token = null;
//     _refreshToken = null;
//     _currentUser = null;
//   }

//   // Set loading state
//   void _setLoading(bool loading) {
//     _isLoading = loading;
//     notifyListeners();
//   }

//   // Validate current token
//   Future<bool> _validateToken() async {
//     if (_token == null) return false;

//     try {
//       final response = await http.get(
//         Uri.parse('$_baseUrl/user/'),
//         headers: {'Authorization': 'Bearer $_token'},
//       );

//       if (response.statusCode == 200) {
//         final userData = jsonDecode(response.body);
//         _currentUser = AuthUser.fromJson(userData);
//         _authStateController.add(_currentUser);
//         notifyListeners();
//         return true;
//       } else if (response.statusCode == 401) {
//         // Token expired, try to refresh
//         return await _refreshAuthToken();
//       }
//     } catch (e) {
//       // Network error or other issues
//     }

//     await signOut();
//     return false;
//   }

//   // Refresh authentication token
//   Future<bool> _refreshAuthToken() async {
//     if (_refreshToken == null) return false;

//     try {
//       final response = await http.post(
//         Uri.parse('$_baseUrl/refresh/'),
//         headers: {'Content-Type': 'application/json'},
//         body: jsonEncode({'refresh': _refreshToken}),
//       );

//       if (response.statusCode == 200) {
//         final data = jsonDecode(response.body);
//         _token = data['access'];

//         final prefs = await SharedPreferences.getInstance();
//         await prefs.setString(_tokenKey, _token!);

//         return true;
//       }
//     } catch (e) {
//       // Refresh failed
//     }

//     return false;
//   }

//   // Sign in with email and password
//   Future<AuthUser> signInWithEmailAndPassword({
//     required String email,
//     required String password,
//   }) async {
//     _setLoading(true);

//     try {
//       final response = await http.post(
//         Uri.parse('$_baseUrl/login/'),
//         headers: {'Content-Type': 'application/json'},
//         body: jsonEncode({'email': email, 'password': password}),
//       );

//       final data = jsonDecode(response.body);

//       if (response.statusCode == 200) {
//         final user = AuthUser.fromJson(data['user']);
//         await _saveAuthData(data['access'], data['refresh'], user);

//         _authStateController.add(_currentUser);
//         notifyListeners();
//         return user;
//       } else {
//         throw _handleAuthError(response.statusCode, data);
//       }
//     } catch (e) {
//       if (e is AuthException) rethrow;
//       throw NetworkException('Network error occurred');
//     } finally {
//       _setLoading(false);
//     }
//   }

//   // Create user with email and password
//   Future<AuthUser> createUserWithEmailAndPassword({
//     required String email,
//     required String password,
//     String? firstName,
//     String? lastName,
//     String? username,
//   }) async {
//     _setLoading(true);

//     try {
//       final response = await http.post(
//         Uri.parse('$_baseUrl/register/'),
//         headers: {'Content-Type': 'application/json'},
//         body: jsonEncode({
//           'email': email,
//           'password': password,
//           'first_name': firstName,
//           'last_name': lastName,
//           'username': username,
//         }),
//       );

//       final data = jsonDecode(response.body);

//       if (response.statusCode == 201) {
//         final user = AuthUser.fromJson(data['user']);
//         await _saveAuthData(data['access'], data['refresh'], user);

//         _authStateController.add(_currentUser);
//         notifyListeners();
//         return user;
//       } else {
//         throw _handleAuthError(response.statusCode, data);
//       }
//     } catch (e) {
//       if (e is AuthException) rethrow;
//       throw NetworkException('Network error occurred');
//     } finally {
//       _setLoading(false);
//     }
//   }

//   // Send password reset email
//   Future<void> sendPasswordResetEmail({required String email}) async {
//     _setLoading(true);

//     try {
//       final response = await http.post(
//         Uri.parse('$_baseUrl/password-reset/'),
//         headers: {'Content-Type': 'application/json'},
//         body: jsonEncode({'email': email}),
//       );

//       if (response.statusCode != 200) {
//         final data = jsonDecode(response.body);
//         throw _handleAuthError(response.statusCode, data);
//       }
//     } catch (e) {
//       if (e is AuthException) rethrow;
//       throw NetworkException('Network error occurred');
//     } finally {
//       _setLoading(false);
//     }
//   }

//   // Sign out
//   Future<void> signOut() async {
//     _setLoading(true);

//     try {
//       if (_token != null) {
//         // Optional: Call logout endpoint to invalidate token on server
//         await http.post(
//           Uri.parse('$_baseUrl/logout/'),
//           headers: {'Authorization': 'Bearer $_token'},
//         );
//       }
//     } catch (e) {
//       // Ignore network errors during logout
//     }

//     await _clearStoredAuth();
//     _authStateController.add(null);
//     notifyListeners();
//     _setLoading(false);
//   }

//   // Update user profile
//   Future<AuthUser> updateProfile({
//     String? firstName,
//     String? lastName,
//     String? username,
//   }) async {
//     if (!isAuthenticated) {
//       throw AuthException('User not authenticated', 'not-authenticated');
//     }

//     _setLoading(true);

//     try {
//       final response = await http.patch(
//         Uri.parse('$_baseUrl/user/'),
//         headers: {
//           'Authorization': 'Bearer $_token',
//           'Content-Type': 'application/json',
//         },
//         body: jsonEncode({
//           'first_name': firstName,
//           'last_name': lastName,
//           'username': username,
//         }),
//       );

//       if (response.statusCode == 200) {
//         final userData = jsonDecode(response.body);
//         _currentUser = AuthUser.fromJson(userData);

//         // Update stored user data
//         final prefs = await SharedPreferences.getInstance();
//         await prefs.setString(_userKey, jsonEncode(_currentUser!.toJson()));

//         _authStateController.add(_currentUser);
//         notifyListeners();
//         return _currentUser!;
//       } else {
//         final data = jsonDecode(response.body);
//         throw _handleAuthError(response.statusCode, data);
//       }
//     } catch (e) {
//       if (e is AuthException) rethrow;
//       throw NetworkException('Network error occurred');
//     } finally {
//       _setLoading(false);
//     }
//   }

//   // Change password
//   Future<void> changePassword({
//     required String currentPassword,
//     required String newPassword,
//   }) async {
//     if (!isAuthenticated) {
//       throw AuthException('User not authenticated', 'not-authenticated');
//     }

//     _setLoading(true);

//     try {
//       final response = await http.post(
//         Uri.parse('$_baseUrl/change-password/'),
//         headers: {
//           'Authorization': 'Bearer $_token',
//           'Content-Type': 'application/json',
//         },
//         body: jsonEncode({
//           'current_password': currentPassword,
//           'new_password': newPassword,
//         }),
//       );

//       if (response.statusCode != 200) {
//         final data = jsonDecode(response.body);
//         throw _handleAuthError(response.statusCode, data);
//       }
//     } catch (e) {
//       if (e is AuthException) rethrow;
//       throw NetworkException('Network error occurred');
//     } finally {
//       _setLoading(false);
//     }
//   }

//   // Handle authentication errors
//   AuthException _handleAuthError(int statusCode, Map<String, dynamic> data) {
//     switch (statusCode) {
//       case 400:
//         if (data['email'] != null) {
//           return EmailAlreadyInUseException();
//         }
//         if (data['password'] != null) {
//           return WeakPasswordException();
//         }
//         return AuthException(data['message'] ?? 'Bad request', 'bad-request');
//       case 401:
//         return InvalidCredentialsException();
//       case 404:
//         return UserNotFoundException();
//       default:
//         return AuthException(
//           data['message'] ?? 'An error occurred',
//           'unknown-error',
//         );
//     }
//   }

//   // Get authenticated HTTP client
//   Map<String, String> get authHeaders => {
//     'Authorization': 'Bearer $_token',
//     'Content-Type': 'application/json',
//   };

//   @override
//   void dispose() {
//     _authStateController.close();
//     super.dispose();
//   }
// }

// // Auth state wrapper widget
// class AuthStateWrapper extends StatelessWidget {
//   final Widget Function(BuildContext context, AuthUser? user) builder;
//   final Widget? loadingWidget;

//   const AuthStateWrapper({
//     super.key,
//     required this.builder,
//     this.loadingWidget,
//   });

//   @override
//   Widget build(BuildContext context) {
//     return StreamBuilder<AuthUser?>(
//       stream: DjangoAuthService().authStateChanges,
//       builder: (context, snapshot) {
//         if (snapshot.connectionState == ConnectionState.waiting) {
//           return loadingWidget ??
//               const Center(child: CircularProgressIndicator());
//         }

//         return builder(context, snapshot.data);
//       },
//     );
//   }
// }

// // Auth guard widget
// class AuthGuard extends StatelessWidget {
//   final Widget child;
//   final Widget? fallback;
//   final VoidCallback? onUnauthenticated;

//   const AuthGuard({
//     super.key,
//     required this.child,
//     this.fallback,
//     this.onUnauthenticated,
//   });

//   @override
//   Widget build(BuildContext context) {
//     return AuthStateWrapper(
//       builder: (context, user) {
//         if (user != null) {
//           return child;
//         } else {
//           if (onUnauthenticated != null) {
//             WidgetsBinding.instance.addPostFrameCallback((_) {
//               onUnauthenticated!();
//             });
//           }
//           return fallback ?? const SizedBox.shrink();
//         }
//       },
//     );
//   }
// }

// // Consumer widget for auth state
// class AuthConsumer extends StatelessWidget {
//   final Widget Function(BuildContext context, AuthUser? user, bool isLoading)
//   builder;

//   const AuthConsumer({super.key, required this.builder});

//   @override
//   Widget build(BuildContext context) {
//     return ListenableBuilder(
//       listenable: DjangoAuthService(),
//       builder: (context, _) {
//         final auth = DjangoAuthService();
//         return builder(context, auth.currentUser, auth.isLoading);
//       },
//     );
//   }
// }

// // Usage example:
// /*
// // In main.dart:
// void main() async {
//   WidgetsFlutterBinding.ensureInitialized();
//   await DjangoAuthService().initialize();
//   runApp(MyApp());
// }

// // In your app:
// class MyApp extends StatelessWidget {
//   @override
//   Widget build(BuildContext context) {
//     return MaterialApp(
//       home: AuthStateWrapper(
//         builder: (context, user) {
//           if (user != null) {
//             return HomeScreen();
//           } else {
//             return LoginScreen();
//           }
//         },
//       ),
//     );
//   }
// }

// // Usage in widgets:
// class LoginScreen extends StatelessWidget {
//   @override
//   Widget build(BuildContext context) {
//     return Scaffold(
//       body: AuthConsumer(
//         builder: (context, user, isLoading) {
//           if (isLoading) {
//             return Center(child: CircularProgressIndicator());
//           }

//           return Column(
//             children: [
//               ElevatedButton(
//                 onPressed: () async {
//                   try {
//                     await DjangoAuthService().signInWithEmailAndPassword(
//                       email: 'user@example.com',
//                       password: 'password123',
//                     );
//                   } catch (e) {
//                     ScaffoldMessenger.of(context).showSnackBar(
//                       SnackBar(content: Text(e.toString())),
//                     );
//                   }
//                 },
//                 child: Text('Sign In'),
//               ),
//             ],
//           );
//         },
//       ),
//     );
//   }
// }
// */


// auth_service.dart
import 'dart:async';
import 'dart:convert';
import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'package:shared_preferences/shared_preferences.dart';
import 'package:flutter_dotenv/flutter_dotenv.dart';

// User model - Updated to match Django backend
class AuthUser {
  final String id; // Django uses UUID strings
  final String username;
  final String email;
  final String? firstName;
  final String? lastName;
  final String fullName;
  final String department;
  final String role;
  final String? phoneNumber;
  final String? employeeId;
  final String? badgeNumber;
  final bool isActive;
  final bool isActiveUser;
  final DateTime? dateJoined;
  final DateTime? lastLogin;

  AuthUser({
    required this.id,
    required this.username,
    required this.email,
    this.firstName,
    this.lastName,
    required this.fullName,
    required this.department,
    required this.role,
    this.phoneNumber,
    this.employeeId,
    this.badgeNumber,
    required this.isActive,
    required this.isActiveUser,
    this.dateJoined,
    this.lastLogin,
  });

  factory AuthUser.fromJson(Map<String, dynamic> json) {
    return AuthUser(
      id: json['id'],
      username: json['username'],
      email: json['email'],
      firstName: json['first_name'],
      lastName: json['last_name'],
      fullName: json['full_name'],
      department: json['department'],
      role: json['role'],
      phoneNumber: json['phone_number'],
      employeeId: json['employee_id'],
      badgeNumber: json['badge_number'],
      isActive: json['is_active'] ?? true,
      isActiveUser: json['is_active_user'] ?? false,
      dateJoined:
          json['date_joined'] != null
              ? DateTime.parse(json['date_joined'])
              : null,
      lastLogin:
          json['last_login'] != null
              ? DateTime.parse(json['last_login'])
              : null,
    );
  }

  Map<String, dynamic> toJson() {
    return {
      'id': id,
      'username': username,
      'email': email,
      'first_name': firstName,
      'last_name': lastName,
      'full_name': fullName,
      'department': department,
      'role': role,
      'phone_number': phoneNumber,
      'employee_id': employeeId,
      'badge_number': badgeNumber,
      'is_active': isActive,
      'is_active_user': isActiveUser,
      'date_joined': dateJoined?.toIso8601String(),
      'last_login': lastLogin?.toIso8601String(),
    };
  }

  String get displayName {
    if (firstName != null && lastName != null) {
      return '$firstName $lastName';
    }
    return fullName.isNotEmpty ? fullName : username;
  }
}

// Auth exception classes
class AuthException implements Exception {
  final String message;
  final String code;

  AuthException(this.message, this.code);

  @override
  String toString() => 'AuthException: $message';
}

class NetworkException extends AuthException {
  NetworkException(String message) : super(message, 'network-error');
}

class InvalidCredentialsException extends AuthException {
  InvalidCredentialsException()
    : super('Invalid credentials', 'invalid-credentials');
}

class UserNotFoundException extends AuthException {
  UserNotFoundException() : super('User not found', 'user-not-found');
}

class WeakPasswordException extends AuthException {
  WeakPasswordException() : super('Password is too weak', 'weak-password');
}

class EmailAlreadyInUseException extends AuthException {
  EmailAlreadyInUseException()
    : super('Email is already in use', 'email-already-in-use');
}

class ValidationException extends AuthException {
  final Map<String, dynamic> errors;
  ValidationException(this.errors)
    : super('Validation failed', 'validation-error');
}

// Auth service singleton
class DjangoAuthService extends ChangeNotifier {
  static final DjangoAuthService _instance = DjangoAuthService._internal();
  factory DjangoAuthService() => _instance;
  DjangoAuthService._internal();

  // Configuration
  final _baseUrl = '${dotenv.env['BASE_URL']!}/api/auth';
  static const String _tokenKey = 'auth_token';
  static const String _refreshTokenKey = 'refresh_token';
  static const String _userKey = 'user_data';

  // State
  AuthUser? _currentUser;
  String? _token;
  String? _refreshToken;
  bool _isLoading = false;

  // Getters
  AuthUser? get currentUser => _currentUser;
  String? get token => _token;
  bool get isAuthenticated => _currentUser != null && _token != null;
  bool get isLoading => _isLoading;

  // Stream controller for auth state changes
  final StreamController<AuthUser?> _authStateController =
      StreamController<AuthUser?>.broadcast();

  Stream<AuthUser?> get authStateChanges => _authStateController.stream;

  // Initialize the service
  Future<void> initialize() async {
    await _loadStoredAuth();
    if (_token != null) {
      await _validateToken();
    }
  }

  // Load stored authentication data
  Future<void> _loadStoredAuth() async {
    try {
      final prefs = await SharedPreferences.getInstance();
      _token = prefs.getString(_tokenKey);
      _refreshToken = prefs.getString(_refreshTokenKey);

      final userJson = prefs.getString(_userKey);
      if (userJson != null) {
        final userData = jsonDecode(userJson);
        _currentUser = AuthUser.fromJson(userData);
      }
    } catch (e) {
      await _clearStoredAuth();
    }
  }

  // Save authentication data
  Future<void> _saveAuthData(
    String token,
    String refreshToken,
    AuthUser user,
  ) async {
    final prefs = await SharedPreferences.getInstance();
    await prefs.setString(_tokenKey, token);
    await prefs.setString(_refreshTokenKey, refreshToken);
    await prefs.setString(_userKey, jsonEncode(user.toJson()));

    _token = token;
    _refreshToken = refreshToken;
    _currentUser = user;
  }

  // Clear stored authentication data
  Future<void> _clearStoredAuth() async {
    final prefs = await SharedPreferences.getInstance();
    await prefs.remove(_tokenKey);
    await prefs.remove(_refreshTokenKey);
    await prefs.remove(_userKey);

    _token = null;
    _refreshToken = null;
    _currentUser = null;
  }

  // Set loading state
  void _setLoading(bool loading) {
    _isLoading = loading;
    notifyListeners();
  }

  // Validate current token
  Future<bool> _validateToken() async {
    if (_token == null) return false;

    try {
      final response = await http.get(
        Uri.parse('$_baseUrl/me/'), // Changed from /user/ to /me/
        headers: {'Authorization': 'Bearer $_token'},
      );

      if (response.statusCode == 200) {
        final userData = jsonDecode(response.body);
        _currentUser = AuthUser.fromJson(userData);
        _authStateController.add(_currentUser);
        notifyListeners();
        return true;
      } else if (response.statusCode == 401) {
        // Token expired, try to refresh
        return await _refreshAuthToken();
      }
    } catch (e) {
      // Network error or other issues
    }

    await signOut();
    return false;
  }

  // Refresh authentication token
  Future<bool> _refreshAuthToken() async {
    if (_refreshToken == null) return false;

    try {
      final response = await http.post(
        Uri.parse('$_baseUrl/token/refresh/'), // Updated endpoint
        headers: {'Content-Type': 'application/json'},
        body: jsonEncode({'refresh': _refreshToken}),
      );

      if (response.statusCode == 200) {
        final data = jsonDecode(response.body);
        _token = data['access'];

        final prefs = await SharedPreferences.getInstance();
        await prefs.setString(_tokenKey, _token!);

        return true;
      }
    } catch (e) {
      // Refresh failed
    }

    return false;
  }

  // Sign in with username/email and password
  Future<AuthUser> signInWithCredentials({
    required String username, // Can be username or email
    required String password,
    required String department,
    required String role,
  }) async {
    _setLoading(true);

    try {
      final response = await http.post(
        Uri.parse('$_baseUrl/login/'),
        headers: {'Content-Type': 'application/json'},
        body: jsonEncode({
          'username': username,
          'password': password,
          'department': department,
          'role': role,
        }),
      );

      final data = jsonDecode(response.body);

      if (response.statusCode == 200) {
        final user = AuthUser.fromJson(data['user']);
        await _saveAuthData(data['access'], data['refresh'], user);

        _authStateController.add(_currentUser);
        notifyListeners();
        return user;
      } else {
        throw _handleAuthError(response.statusCode, data);
      }
    } catch (e) {
      if (e is AuthException) rethrow;
      throw NetworkException('Network error occurred');
    } finally {
      _setLoading(false);
    }
  }

  // Convenience method for email/password login
  Future<AuthUser> signInWithEmailAndPassword({
    required String email,
    required String password,
    required String department,
    required String role,
  }) async {
    return signInWithCredentials(
      username: email,
      password: password,
      department: department,
      role: role,
    );
  }

  // Register user (self-registration)
  Future<AuthUser> registerUser({
    required String username,
    required String email,
    required String fullName,
    required String password,
    required String department,
    String? phoneNumber,
  }) async {
    _setLoading(true);

    try {
      final response = await http.post(
        Uri.parse('$_baseUrl/register/'),
        headers: {'Content-Type': 'application/json'},
        body: jsonEncode({
          'username': username,
          'email': email,
          'full_name': fullName,
          'password': password,
          'department': department,
          'phone_number': phoneNumber,
        }),
      );

      final data = jsonDecode(response.body);

      if (response.statusCode == 201) {
        // Registration successful, but user might need to login separately
        return AuthUser.fromJson({
          'id': data['user_id'],
          'username': data['username'],
          'email': email,
          'full_name': fullName,
          'department': department,
          'role': 'Field User', // Default role for self-registration
          'is_active': true,
          'is_active_user': false, // May need admin approval
        });
      } else {
        throw _handleAuthError(response.statusCode, data);
      }
    } catch (e) {
      if (e is AuthException) rethrow;
      throw NetworkException('Network error occurred');
    } finally {
      _setLoading(false);
    }
  }

  // Create user with email and password (admin function)
  Future<AuthUser> createUserWithEmailAndPassword({
    required String email,
    required String password,
    required String fullName,
    required String department,
    required String role,
    String? firstName,
    String? lastName,
    String? username,
    String? phoneNumber,
    String? employeeId,
    String? badgeNumber,
  }) async {
    _setLoading(true);

    try {
      final response = await http.post(
        Uri.parse('$_baseUrl/users/'), // Admin endpoint for creating users
        headers: authHeaders,
        body: jsonEncode({
          'username': username ?? email.split('@')[0],
          'email': email,
          'full_name': fullName,
          'password': password,
          'password_confirm': password,
          'department': department,
          'role': role,
          'first_name': firstName,
          'last_name': lastName,
          'phone_number': phoneNumber,
          'employee_id': employeeId,
          'badge_number': badgeNumber,
        }),
      );

      final data = jsonDecode(response.body);

      if (response.statusCode == 201) {
        return AuthUser.fromJson(data);
      } else {
        throw _handleAuthError(response.statusCode, data);
      }
    } catch (e) {
      if (e is AuthException) rethrow;
      throw NetworkException('Network error occurred');
    } finally {
      _setLoading(false);
    }
  }

  // Send password reset email
  Future<void> sendPasswordResetEmail({required String email}) async {
    _setLoading(true);

    try {
      final response = await http.post(
        Uri.parse('$_baseUrl/password-reset/'),
        headers: {'Content-Type': 'application/json'},
        body: jsonEncode({'email': email}),
      );

      if (response.statusCode != 200) {
        final data = jsonDecode(response.body);
        throw _handleAuthError(response.statusCode, data);
      }
    } catch (e) {
      if (e is AuthException) rethrow;
      throw NetworkException('Network error occurred');
    } finally {
      _setLoading(false);
    }
  }

  // Sign out
  Future<void> signOut() async {
    _setLoading(true);

    try {
      if (_token != null && _refreshToken != null) {
        // Call logout endpoint to invalidate token on server
        await http.post(
          Uri.parse('$_baseUrl/logout/'),
          headers: {
            'Authorization': 'Bearer $_token',
            'Content-Type': 'application/json',
          },
          body: jsonEncode({'refresh_token': _refreshToken}),
        );
      }
    } catch (e) {
      // Ignore network errors during logout
    }

    await _clearStoredAuth();
    _authStateController.add(null);
    notifyListeners();
    _setLoading(false);
  }

  // Update user profile
  Future<AuthUser> updateProfile({
    String? firstName,
    String? lastName,
    String? fullName,
    String? email,
    String? phoneNumber,
    String? badgeNumber,
  }) async {
    if (!isAuthenticated) {
      throw AuthException('User not authenticated', 'not-authenticated');
    }

    _setLoading(true);

    try {
      final response = await http.put(
        Uri.parse('$_baseUrl/profile/update/'),
        headers: authHeaders,
        body: jsonEncode({
          'first_name': firstName,
          'last_name': lastName,
          'full_name': fullName,
          'email': email,
          'phone_number': phoneNumber,
          'badge_number': badgeNumber,
        }),
      );

      if (response.statusCode == 200) {
        final userData = jsonDecode(response.body);
        _currentUser = AuthUser.fromJson(userData);

        // Update stored user data
        final prefs = await SharedPreferences.getInstance();
        await prefs.setString(_userKey, jsonEncode(_currentUser!.toJson()));

        _authStateController.add(_currentUser);
        notifyListeners();
        return _currentUser!;
      } else {
        final data = jsonDecode(response.body);
        throw _handleAuthError(response.statusCode, data);
      }
    } catch (e) {
      if (e is AuthException) rethrow;
      throw NetworkException('Network error occurred');
    } finally {
      _setLoading(false);
    }
  }

  // Change password
  Future<void> changePassword({
    required String currentPassword,
    required String newPassword,
  }) async {
    if (!isAuthenticated) {
      throw AuthException('User not authenticated', 'not-authenticated');
    }

    _setLoading(true);

    try {
      final response = await http.post(
        Uri.parse('$_baseUrl/password/change/'),
        headers: authHeaders,
        body: jsonEncode({
          'old_password': currentPassword,
          'new_password': newPassword,
          'new_password_confirm': newPassword,
        }),
      );

      if (response.statusCode != 200) {
        final data = jsonDecode(response.body);
        throw _handleAuthError(response.statusCode, data);
      }
    } catch (e) {
      if (e is AuthException) rethrow;
      throw NetworkException('Network error occurred');
    } finally {
      _setLoading(false);
    }
  }

  // Handle authentication errors
  AuthException _handleAuthError(int statusCode, Map<String, dynamic> data) {
    switch (statusCode) {
      case 400:
        if (data is Map && data.containsKey('non_field_errors')) {
          return ValidationException(data);
        }
        if (data['email'] != null) {
          return EmailAlreadyInUseException();
        }
        if (data['password'] != null) {
          return WeakPasswordException();
        }
        return AuthException(
          data['message'] ?? data['detail'] ?? 'Bad request',
          'bad-request',
        );
      case 401:
        return InvalidCredentialsException();
      case 404:
        return UserNotFoundException();
      default:
        return AuthException(
          data['message'] ?? data['detail'] ?? 'An error occurred',
          'unknown-error',
        );
    }
  }

  // Get authenticated HTTP client headers
  Map<String, String> get authHeaders => {
    'Authorization': 'Bearer $_token',
    'Content-Type': 'application/json',
  };

  @override
  void dispose() {
    _authStateController.close();
    super.dispose();
  }
}

// Auth state wrapper widget
class AuthStateWrapper extends StatelessWidget {
  final Widget Function(BuildContext context, AuthUser? user) builder;
  final Widget? loadingWidget;

  const AuthStateWrapper({
    super.key,
    required this.builder,
    this.loadingWidget,
  });

  @override
  Widget build(BuildContext context) {
    return StreamBuilder<AuthUser?>(
      stream: DjangoAuthService().authStateChanges,
      builder: (context, snapshot) {
        if (snapshot.connectionState == ConnectionState.waiting) {
          return loadingWidget ??
              const Center(child: CircularProgressIndicator());
        }

        return builder(context, snapshot.data);
      },
    );
  }
}

// Auth guard widget
class AuthGuard extends StatelessWidget {
  final Widget child;
  final Widget? fallback;
  final VoidCallback? onUnauthenticated;

  const AuthGuard({
    super.key,
    required this.child,
    this.fallback,
    this.onUnauthenticated,
  });

  @override
  Widget build(BuildContext context) {
    return AuthStateWrapper(
      builder: (context, user) {
        if (user != null) {
          return child;
        } else {
          if (onUnauthenticated != null) {
            WidgetsBinding.instance.addPostFrameCallback((_) {
              onUnauthenticated!();
            });
          }
          return fallback ?? const SizedBox.shrink();
        }
      },
    );
  }
}

// Consumer widget for auth state
class AuthConsumer extends StatelessWidget {
  final Widget Function(BuildContext context, AuthUser? user, bool isLoading)
  builder;

  const AuthConsumer({super.key, required this.builder});

  @override
  Widget build(BuildContext context) {
    return ListenableBuilder(
      listenable: DjangoAuthService(),
      builder: (context, _) {
        final auth = DjangoAuthService();
        return builder(context, auth.currentUser, auth.isLoading);
      },
    );
  }
}

// Usage example:
/*
// In main.dart:
void main() async {
  WidgetsFlutterBinding.ensureInitialized();
  await DjangoAuthService().initialize();
  runApp(MyApp());
}

// Login example:
class LoginScreen extends StatefulWidget {
  @override
  _LoginScreenState createState() => _LoginScreenState();
}

class _LoginScreenState extends State<LoginScreen> {
  final _usernameController = TextEditingController();
  final _passwordController = TextEditingController();
  String _selectedDepartment = 'fire';
  String _selectedRole = 'Field User';

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: AuthConsumer(
        builder: (context, user, isLoading) {
          if (isLoading) {
            return Center(child: CircularProgressIndicator());
          }
          
          return Column(
            children: [
              TextField(
                controller: _usernameController,
                decoration: InputDecoration(labelText: 'Username/Email'),
              ),
              TextField(
                controller: _passwordController,
                decoration: InputDecoration(labelText: 'Password'),
                obscureText: true,
              ),
              DropdownButton<String>(
                value: _selectedDepartment,
                onChanged: (String? newValue) {
                  setState(() {
                    _selectedDepartment = newValue!;
                  });
                },
                items: <String>['fire', 'police', 'medical', 'admin']
                    .map<DropdownMenuItem<String>>((String value) {
                  return DropdownMenuItem<String>(
                    value: value,
                    child: Text(value),
                  );
                }).toList(),
              ),
              DropdownButton<String>(
                value: _selectedRole,
                onChanged: (String? newValue) {
                  setState(() {
                    _selectedRole = newValue!;
                  });
                },
                items: <String>['System Administrator', 'Regional Manager', 'District Manager', 'Field User']
                    .map<DropdownMenuItem<String>>((String value) {
                  return DropdownMenuItem<String>(
                    value: value,
                    child: Text(value),
                  );
                }).toList(),
              ),
              ElevatedButton(
                onPressed: () async {
                  try {
                    await DjangoAuthService().signInWithCredentials(
                      username: _usernameController.text,
                      password: _passwordController.text,
                      department: _selectedDepartment,
                      role: _selectedRole,
                    );
                  } catch (e) {
                    ScaffoldMessenger.of(context).showSnackBar(
                      SnackBar(content: Text(e.toString())),
                    );
                  }
                },
                child: Text('Sign In'),
              ),
            ],
          );
        },
      ),
    );
  }
}
*/
