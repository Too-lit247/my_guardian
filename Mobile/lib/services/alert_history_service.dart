import 'dart:async';
import 'package:my_guardian/services/postgre_auth.dart';
import 'package:postgres/postgres.dart';
import 'db_controller.dart';
import 'package:flutter/foundation.dart';

class AlertHistoryService {
  static final AlertHistoryService _instance = AlertHistoryService._internal();
  factory AlertHistoryService() => _instance;
  AlertHistoryService._internal();

  final DBService _dbService = DBService();
  List<Map<String, dynamic>> _alertHistory = [];
  bool _isLoading = false;
  String? _error;

  List<Map<String, dynamic>> get alertHistory => _alertHistory;
  bool get isLoading => _isLoading;
  String? get error => _error;

  Future<void> fetchAlertHistory() async {
    _isLoading = true;
    _error = null;

    try {
      await _dbService.connect();

      // Get current user ID
      String? userId = await _getCurrentUserId();
      if (userId == null) {
        throw Exception('User not authenticated');
      }

      // Get user's device ID
      String? deviceId = await _getUserDeviceId(userId);
      if (deviceId == null) {
        debugPrint(
          "No device found for user, checking for alerts created by user",
        );
        // If no device, check for alerts created by the user directly
        await _fetchUserCreatedAlerts(userId);
        return;
      }

      // Fetch alerts related to the user's device through emergency triggers
      await _fetchDeviceRelatedAlerts(deviceId, userId);
    } catch (e) {
      _error = e.toString();
      debugPrint("Error fetching alert history: $e");
    } finally {
      _isLoading = false;
    }
  }

  Future<String?> _getCurrentUserId() async {
    final auth = PostgreAuth();
    final currentUser = auth.currentUser;
    return currentUser?['id'];
  }

  Future<String?> _getUserDeviceId(String userId) async {
    final conn = _dbService.conn;
    final result = await conn.execute(
      Sql.named(
        "SELECT device_id FROM devices WHERE owner_id = @userId LIMIT 1;",
      ),
      parameters: {'userId': userId},
    );

    if (result.isNotEmpty) {
      return result.first[0] as String;
    }
    return null;
  }

  Future<void> _fetchDeviceRelatedAlerts(String deviceId, String userId) async {
    final conn = _dbService.conn;

    try {
      // First, let's check what tables exist
      debugPrint("Checking available tables...");
      final tablesResult = await conn.execute(
        Sql.named('''
        SELECT table_name
        FROM information_schema.tables
        WHERE table_schema = 'public'
        AND table_name LIKE '%alert%'
        ORDER BY table_name;
        '''),
      );

      debugPrint("Available alert-related tables:");
      for (final row in tablesResult) {
        debugPrint("  - ${row[0]}");
      }

      // Fetch emergency triggers for the user's device
      debugPrint("Fetching emergency triggers for device: $deviceId");
      final result = await conn.execute(
        Sql.named('''
        SELECT
          et.trigger_id,
          et.trigger_type,
          et.severity,
          et.trigger_value,
          et.threshold_value,
          et.triggered_at,
          et.resolved_at,
          et.acknowledged,
          et.acknowledged_by_id,
          et.acknowledged_at,
          et.latitude,
          et.longitude,
          et.alert_created_id,
          et.device_id,
          et.reading_id
        FROM emergency_triggers et
        WHERE et.device_id = @deviceId
        ORDER BY et.triggered_at DESC
        LIMIT 50;
        '''),
        parameters: {'deviceId': deviceId},
      );

      // Convert emergency triggers to alert-like format
      _alertHistory =
          result.map((row) {
            final rowMap = row.toColumnMap();
            return {
              'id': rowMap['trigger_id'],
              'title': _getTriggerTitle(rowMap['trigger_type']),
              'alert_type': rowMap['trigger_type'],
              'description': _getTriggerDescription(
                rowMap['trigger_type'],
                rowMap['trigger_value'],
                rowMap['threshold_value'],
              ),
              'location': _formatLocation(
                rowMap['latitude'],
                rowMap['longitude'],
              ),
              'priority': _mapSeverityToPriority(rowMap['severity']),
              'status': _getStatusFromTrigger(
                rowMap['resolved_at'],
                rowMap['acknowledged'],
              ),
              'department': _getDepartmentForTrigger(rowMap['trigger_type']),
              'assigned_to': '',
              'created_at': rowMap['triggered_at'],
              'updated_at': rowMap['acknowledged_at'] ?? rowMap['triggered_at'],
              'resolved_at': rowMap['resolved_at'],
              'acknowledged_at': rowMap['acknowledged_at'],
              'acknowledged': rowMap['acknowledged'],
              'trigger_value': rowMap['trigger_value'],
              'threshold_value': rowMap['threshold_value'],
              'device_id': rowMap['device_id'],
              'reading_id': rowMap['reading_id'],
              'alert_created_id': rowMap['alert_created_id'],
            };
          }).toList();

      debugPrint(
        "Fetched ${_alertHistory.length} emergency triggers as alerts",
      );
    } catch (e) {
      debugPrint("Error in device-related alerts query: $e");
      // Fallback to user-created alerts
      await _fetchUserCreatedAlerts(userId);
    }
  }

  Future<void> _fetchUserCreatedAlerts(String userId) async {
    final conn = _dbService.conn;

    try {
      // Query to get alerts created by the user
      final result = await conn.execute(
        Sql.named('''
        SELECT
          a.id,
          a.title,
          a.alert_type,
          a.description,
          a.location,
          a.priority,
          a.status,
          a.department,
          a.assigned_to,
          a.created_at,
          a.updated_at,
          a.resolved_at,
          a.response_time,
          a.outcome,
          u.full_name
        FROM alerts_alert a
        LEFT JOIN users u ON a.created_by_id = u.id
        WHERE a.created_by_id = @userId
        ORDER BY a.created_at DESC
        LIMIT 50;
        '''),
        parameters: {'userId': userId},
      );

      _alertHistory = result.map((row) => row.toColumnMap()).toList();
      debugPrint("Fetched ${_alertHistory.length} user-created alerts");
    } catch (e) {
      debugPrint("Error in user-created alerts query: $e");
      rethrow;
    }
  }

  // Helper method to get alert type enum from string
  String getAlertTypeDisplay(String? alertType) {
    if (alertType == null) return 'Unknown';

    switch (alertType) {
      case 'high_heart_rate':
        return 'Health Emergency';
      case 'fire_detected':
        return 'Fire Alert';
      case 'fear_detected':
        return 'Police Alert';
      case 'panic_button':
        return 'Manual Triggered';
      case 'fall_detected':
        return 'Health Emergency';
      case 'building_fire':
        return 'Fire Alert';
      case 'heart_attack':
        return 'Health Emergency';
      case 'robbery':
        return 'Police Alert';
      case 'assault':
        return 'Police Alert';
      default:
        return alertType
            .replaceAll('_', ' ')
            .split(' ')
            .map(
              (word) =>
                  word.isNotEmpty
                      ? word[0].toUpperCase() + word.substring(1)
                      : word,
            )
            .join(' ');
    }
  }

  // Helper method to get priority color
  String getPriorityColor(String? priority) {
    switch (priority?.toLowerCase()) {
      case 'high':
        return 'red';
      case 'medium':
        return 'orange';
      case 'low':
        return 'green';
      default:
        return 'grey';
    }
  }

  // Helper method to get status color
  String getStatusColor(String? status) {
    switch (status?.toLowerCase()) {
      case 'active':
        return 'red';
      case 'in_progress':
        return 'orange';
      case 'resolved':
        return 'green';
      case 'cancelled':
        return 'grey';
      default:
        return 'grey';
    }
  }

  // Helper method to format date
  String formatDate(dynamic dateValue) {
    if (dateValue == null) return 'N/A';

    try {
      DateTime date;
      if (dateValue is String) {
        date = DateTime.parse(dateValue);
      } else if (dateValue is DateTime) {
        date = dateValue;
      } else {
        return 'N/A';
      }

      return '${date.day}/${date.month}/${date.year} ${date.hour.toString().padLeft(2, '0')}:${date.minute.toString().padLeft(2, '0')}';
    } catch (e) {
      return 'N/A';
    }
  }

  // Helper methods for converting emergency triggers to alert format
  String _getTriggerTitle(dynamic triggerType) {
    if (triggerType == null) return 'Emergency Alert';

    switch (triggerType.toString()) {
      case 'fear_detected':
        return 'Fear Detected';
      case 'high_heart_rate':
        return 'High Heart Rate Alert';
      case 'fire_detected':
        return 'Fire Detected';
      case 'panic_button':
        return 'Panic Button Activated';
      case 'device_offline':
        return 'Device Offline';
      case 'fall_detected':
        return 'Fall Detected';
      default:
        return 'Emergency Alert';
    }
  }

  String _getTriggerDescription(
    dynamic triggerType,
    dynamic triggerValue,
    dynamic thresholdValue,
  ) {
    if (triggerType == null) return 'Emergency situation detected';

    final type = triggerType.toString();
    final value = triggerValue?.toString() ?? '';
    final threshold = thresholdValue?.toString() ?? '';

    switch (type) {
      case 'fear_detected':
        return 'Fear detected through audio analysis${value.isNotEmpty ? ' (confidence: $value)' : ''}';
      case 'high_heart_rate':
        String desc = 'Heart rate exceeded safe threshold';
        if (value.isNotEmpty && threshold.isNotEmpty) {
          desc += ' ($value BPM > $threshold BPM)';
        } else if (value.isNotEmpty) {
          desc += ' ($value BPM)';
        }
        return desc;
      case 'fire_detected':
        String desc = 'Fire or smoke detected by sensors';
        if (value.isNotEmpty && threshold.isNotEmpty) {
          desc += ' (level: $value > $threshold)';
        } else if (value.isNotEmpty) {
          desc += ' (level: $value)';
        }
        return desc;
      case 'panic_button':
        return 'Manual panic button was activated by the user';
      case 'device_offline':
        return 'Guardian device lost connection and went offline';
      case 'fall_detected':
        return 'Fall detected by motion sensors${value.isNotEmpty ? ' (impact: $value)' : ''}';
      default:
        return 'Emergency situation detected${value.isNotEmpty ? ' (value: $value)' : ''}';
    }
  }

  String _formatLocation(dynamic latitude, dynamic longitude) {
    if (latitude == null || longitude == null) return 'Location unavailable';

    try {
      final lat = double.parse(latitude.toString());
      final lng = double.parse(longitude.toString());
      return '${lat.toStringAsFixed(6)}, ${lng.toStringAsFixed(6)}';
    } catch (e) {
      return 'Location unavailable';
    }
  }

  String _mapSeverityToPriority(dynamic severity) {
    if (severity == null) return 'medium';

    switch (severity.toString().toLowerCase()) {
      case 'critical':
        return 'high';
      case 'high':
        return 'high';
      case 'medium':
        return 'medium';
      case 'low':
        return 'low';
      default:
        return 'medium';
    }
  }

  String _getStatusFromTrigger(dynamic resolvedAt, dynamic acknowledged) {
    if (resolvedAt != null) {
      return 'resolved';
    } else if (acknowledged == true) {
      return 'in_progress';
    } else {
      return 'active';
    }
  }

  String _getDepartmentForTrigger(dynamic triggerType) {
    if (triggerType == null) return 'medical';

    switch (triggerType.toString()) {
      case 'fear_detected':
      case 'panic_button':
        return 'police';
      case 'fire_detected':
        return 'fire';
      case 'high_heart_rate':
      case 'fall_detected':
      case 'device_offline':
        return 'medical';
      default:
        return 'medical';
    }
  }

  void dispose() {
    _alertHistory.clear();
  }
}
