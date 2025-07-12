import 'package:flutter_test/flutter_test.dart';

void main() {
  group('Type Conversion Tests', () {
    // Helper function to safely convert to double and format
    String formatDoubleValue(dynamic value, int decimals) {
      if (value == null) return 'N/A';
      try {
        if (value is String) {
          final parsed = double.tryParse(value);
          return parsed?.toStringAsFixed(decimals) ?? 'N/A';
        } else if (value is num) {
          return value.toStringAsFixed(decimals);
        }
        return 'N/A';
      } catch (e) {
        return 'N/A';
      }
    }

    // Helper function to safely get integer value
    String formatIntValue(dynamic value, String unit) {
      if (value == null) return 'N/A';
      try {
        if (value is String) {
          final parsed = int.tryParse(value);
          return parsed != null ? '$parsed $unit' : 'N/A';
        } else if (value is num) {
          return '${value.toInt()} $unit';
        }
        return 'N/A';
      } catch (e) {
        return 'N/A';
      }
    }

    test('formatDoubleValue handles different types correctly', () {
      expect(formatDoubleValue(null, 2), 'N/A');
      expect(formatDoubleValue(3.14159, 2), '3.14');
      expect(formatDoubleValue('3.14159', 2), '3.14');
      expect(formatDoubleValue('invalid', 2), 'N/A');
      expect(formatDoubleValue(42, 1), '42.0');
      expect(formatDoubleValue('42.5', 1), '42.5');
    });

    test('formatIntValue handles different types correctly', () {
      expect(formatIntValue(null, 'BPM'), 'N/A');
      expect(formatIntValue(75, 'BPM'), '75 BPM');
      expect(formatIntValue('75', 'BPM'), '75 BPM');
      expect(formatIntValue('invalid', 'BPM'), 'N/A');
      expect(formatIntValue(75.8, 'BPM'), '75 BPM');
      expect(formatIntValue('75.8', 'BPM'), 'N/A'); // int.tryParse fails on decimals
    });

    test('battery level conversion', () {
      int? convertBatteryLevel(dynamic batteryLevelValue) {
        if (batteryLevelValue == null) {
          return null;
        } else if (batteryLevelValue is int) {
          return batteryLevelValue;
        } else if (batteryLevelValue is String) {
          return int.tryParse(batteryLevelValue);
        } else if (batteryLevelValue is num) {
          return batteryLevelValue.toInt();
        }
        return null;
      }

      expect(convertBatteryLevel(null), null);
      expect(convertBatteryLevel(85), 85);
      expect(convertBatteryLevel('85'), 85);
      expect(convertBatteryLevel(85.7), 85);
      expect(convertBatteryLevel('invalid'), null);
    });
  });
}
