import 'dart:async';
import 'package:my_guardian/services/postgre_auth.dart';
import 'package:postgres/postgres.dart';
import 'db_controller.dart';
import 'package:flutter/foundation.dart';

class DeviceReadingService {
  static final DeviceReadingService _instance =
      DeviceReadingService._internal();
  factory DeviceReadingService() => _instance;
  DeviceReadingService._internal();

  ValueNotifier<Map<String, dynamic>?> latestReading = ValueNotifier(null);

  final DBService _dbService = DBService();
  Timer? _pollingTimer;
  String? _deviceId;

  Future<void> init() async {
    await _dbService.connect();

    try {
      String? userId = await _getCurrentUserId();
      if (userId == null) {
        debugPrint("No user ID found.");
        latestReading.value = null;
        return;
      }

      await _fetchDeviceId(userId);

      if (_deviceId == null) {
        debugPrint("No device found for user.");
        //_deviceId = 'a44bc384-2220-426b-a2e7-c0b4b57a8b3b';
      }

      // Still null? Abort polling.
      if (_deviceId == null) {
        debugPrint("No valid device ID available.");
        latestReading.value = null;
        return;
      }

      // Start polling
      _pollingTimer = Timer.periodic(const Duration(seconds: 1), (_) async {
        await _fetchDeviceReadings();
      });
    } catch (e) {
      debugPrint("Error during init: $e");
      latestReading.value = null;
    }
  }

  Future<String?> _getCurrentUserId() async {
    final auth = PostgreAuth();
    final currentUser = auth.currentUser;
    return currentUser?['id'];
  }

  Future<void> _fetchDeviceId(String userId) async {
    final conn = _dbService.conn;
    final result = await conn.execute(
      Sql.named(
        "SELECT device_id FROM devices WHERE owner_id = @userId LIMIT 1;",
      ),
      parameters: {'userId': userId},
    );

    if (result.isNotEmpty) {
      _deviceId = result.first[0] as String;
      debugPrint("Device ID: $_deviceId");
    }
  }

  Future<void> _fetchDeviceReadings() async {
    final conn = _dbService.conn;

    try {
      final result = await conn.execute(
        Sql.named('''
      SELECT * FROM device_readings 
      WHERE device_id = @deviceId 
      ORDER BY timestamp DESC 
      LIMIT 1;
      '''),
        parameters: {'deviceId': _deviceId},
      );

      if (result.isNotEmpty) {
        final row = result.first.toColumnMap();
        latestReading.value = row;
        debugPrint("Latest Reading fetched!");
      }
    } catch (e) {
      debugPrint("Error fetching readings: $e");
    }
  }

  void dispose() {
    _pollingTimer?.cancel();
  }
}
