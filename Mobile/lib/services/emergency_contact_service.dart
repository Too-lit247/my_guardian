import 'package:postgres/postgres.dart';
import 'package:uuid/uuid.dart';
import 'package:my_guardian/services/postgre_auth.dart'; // Import PostgreAuth

/// A data model class that represents a single emergency contact.
/// This helps in managing the data in a structured and type-safe way.
class EmergencyContact {
  final String contactId;
  final String userId;
  final String name;
  final String phoneNumber;
  final String relation;
  final String preferredMethod;
  final DateTime createdAt;
  final DateTime updatedAt;

  EmergencyContact({
    required this.contactId,
    required this.userId,
    required this.name,
    required this.phoneNumber,
    required this.relation,
    required this.preferredMethod,
    required this.createdAt,
    required this.updatedAt,
  });

  /// A factory constructor to create an EmergencyContact from a database row map.
  factory EmergencyContact.fromMap(Map<String, dynamic> map) {
    return EmergencyContact(
      contactId: map['contact_id'],
      userId: map['user_id'],
      name: map['name'],
      phoneNumber: map['phone_number'],
      relation: map['relation'],
      preferredMethod: map['preferred_method'],
      createdAt: map['created_at'],
      updatedAt: map['updated_at'],
    );
  }

  @override
  String toString() {
    return 'EmergencyContact(name: $name, phone: $phoneNumber, relation: $relation)';
  }
}

/// A service class to handle all CRUD (Create, Read, Update, Delete) operations
/// for the `emergency_contacts` table in the database.
class EmergencyContactService {
  final Connection _conn; // This connection is now passed in
  final PostgreAuth _auth; // This is the singleton instance

  /// The constructor requires a PostgreSQL [Connection] and an instance
  /// of the [PostgreAuth] service to access the current user's ID.
  EmergencyContactService(
    this._conn,
    this._auth,
  ); // Constructor takes the Connection

  /// Retrieves the current user's ID from the auth service.
  /// Throws an exception if the user is not authenticated, preventing any unauthorized access.
  String _getCurrentUserId() {
    if (!_auth.isAuthenticated || _auth.currentUser == null) {
      throw Exception(
        'User is not authenticated. Cannot perform contact operations.',
      );
    }
    // Assuming currentUser['id'] is available and is the user's UUID in the database
    return _auth.currentUser!['id'];
  }

  /// Creates a new emergency contact for the currently logged-in user.
  Future<EmergencyContact> createContact({
    required String name,
    required String phoneNumber,
    required String relation,
    required String preferredMethod,
  }) async {
    final userId = _getCurrentUserId();
    final now = DateTime.now().toUtc();

    final result = await _conn.execute(
      Sql.named('''
        INSERT INTO emergency_contacts (
          contact_id, user_id, name, phone_number, relation,
          preferred_method, created_at, updated_at
        ) VALUES (
          @contactId, @userId, @name, @phoneNumber, @relation,
          @preferredMethod, @now, @now
        ) RETURNING *;
      '''),
      parameters: {
        'contactId': const Uuid().v4(), // Use const Uuid().v4()
        'userId': userId,
        'name': name,
        'phoneNumber': phoneNumber,
        'relation': relation,
        'preferredMethod': preferredMethod,
        'now': now,
      },
    );

    if (result.isEmpty) {
      throw Exception('Failed to create emergency contact.');
    }

    return EmergencyContact.fromMap(result.first.toColumnMap());
  }

  /// Fetches a list of all emergency contacts belonging ONLY to the currently logged-in user.
  Future<List<EmergencyContact>> getContactsForCurrentUser() async {
    final userId = _getCurrentUserId();

    final result = await _conn.execute(
      Sql.named(
        'SELECT * FROM emergency_contacts WHERE user_id = @userId ORDER BY created_at DESC',
      ),
      parameters: {'userId': userId},
    );

    if (result.isEmpty) {
      return []; // Return an empty list if no contacts are found
    }

    // Map each row to an EmergencyContact object and return the list
    return result
        .map((row) => EmergencyContact.fromMap(row.toColumnMap()))
        .toList();
  }

  /// Updates an existing emergency contact.
  /// A user can only update a contact that they own.
  Future<EmergencyContact> updateContact({
    required String contactId,
    String? name,
    String? phoneNumber,
    String? relation,
    String? preferredMethod,
  }) async {
    final userId = _getCurrentUserId();

    // Dynamically build the SET part of the query to only update fields that are provided.
    final updates = <String>[];
    final parameters = <String, dynamic>{
      'contactId': contactId,
      'userId': userId,
      'now': DateTime.now().toUtc(),
    };

    if (name != null) {
      updates.add('name = @name');
      parameters['name'] = name;
    }
    if (phoneNumber != null) {
      updates.add('phone_number = @phoneNumber');
      parameters['phoneNumber'] = phoneNumber;
    }
    if (relation != null) {
      updates.add('relation = @relation');
      parameters['relation'] = relation;
    }
    if (preferredMethod != null) {
      updates.add('preferred_method = @preferredMethod');
      parameters['preferredMethod'] = preferredMethod;
    }

    if (updates.isEmpty) {
      throw Exception('No fields provided to update.');
    }

    updates.add('updated_at = @now');

    final query = '''
      UPDATE emergency_contacts
      SET ${updates.join(', ')}
      WHERE contact_id = @contactId AND user_id = @userId
      RETURNING *;
    ''';

    final result = await _conn.execute(
      Sql.named(query),
      parameters: parameters,
    );

    if (result.isEmpty) {
      throw Exception(
        'Contact not found or user does not have permission to update.',
      );
    }

    return EmergencyContact.fromMap(result.first.toColumnMap());
  }

  /// Deletes an emergency contact.
  /// The WHERE clause ensures a user can only delete their own contacts.
  Future<void> deleteContact({required String contactId}) async {
    final userId = _getCurrentUserId();

    final result = await _conn.execute(
      Sql.named(
        'DELETE FROM emergency_contacts WHERE contact_id = @contactId AND user_id = @userId',
      ),
      parameters: {'contactId': contactId, 'userId': userId},
    );

    // The affectedRows property tells us if a row was actually deleted.
    if (result.affectedRows == 0) {
      throw Exception(
        'Contact not found or user does not have permission to delete.',
      );
    }
  }
}
