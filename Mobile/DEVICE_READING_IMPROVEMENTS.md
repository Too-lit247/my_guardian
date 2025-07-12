# Device Reading Improvements

## Problem Statement
The Flutter app was experiencing several issues with device reading display:

1. **Type Conversion Error**: `'String' is not a subtype of 'double'` error when calling `toStringAsFixed()` on database values
2. **Incomplete Data Display**: Only showing the latest single reading, which might only have one field populated (e.g., only heart rate), causing other fields to show "N/A"
3. **Missing Temperature Display**: Temperature sensor data was not displayed in the UI
4. **Data Loss**: When a new reading came in with only one sensor value, all other sensor values would disappear

## Solution Implemented

### 1. Enhanced Data Fetching (`device_reading_service.dart`)

**Before:**
```sql
SELECT * FROM device_readings 
WHERE device_id = @deviceId 
ORDER BY timestamp DESC 
LIMIT 1;
```

**After:**
```sql
SELECT * FROM device_readings 
WHERE device_id = @deviceId 
ORDER BY timestamp DESC 
LIMIT 50;
```

**Key Changes:**
- Fetches the latest 50 readings instead of just 1
- Builds a composite reading with the most recent non-null value for each field
- Stores last known values to prevent data loss
- Uses `_updateFieldIfNotNull()` helper to merge data intelligently

### 2. Safe Type Conversion (`dashboard.dart`)

**Added Helper Functions:**
```dart
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
```

### 3. Enhanced UI Display

**New Features:**
- **Temperature Display**: Added thermometer icon and temperature in Celsius
- **Conditional Rendering**: Only shows sensor cards for fields that have actual values
- **Safe Battery Level**: Updated to handle dynamic types (String, int, double)
- **Improved Stress/Fear Card**: Safe type conversion for mental state data

**Before:**
```dart
"${data['smoke_level']?.toStringAsFixed(2) ?? 'N/A'}"  // Could crash
```

**After:**
```dart
formatDoubleValue(data['smoke_level'], 2)  // Always safe
```

## Testing

### Unit Tests
Run the type conversion tests:
```bash
cd Mobile
flutter test test/type_conversion_test.dart
```

### Manual Testing
1. **Deploy app to device**:
   ```bash
   cd Mobile
   flutter run -d <device_id>
   ```

2. **Simulate device data** (from Backend directory):
   ```bash
   python scripts/simulate_data_upload.py
   ```

3. **Verify the following**:
   - No more type conversion errors in debug console
   - Temperature is displayed when available
   - Sensor values persist even when new readings only contain partial data
   - All numeric values display correctly regardless of database type

## Database Schema Context

The backend stores readings in the `device_readings` table with these relevant fields:
- `heart_rate`: IntegerField (null=True)
- `temperature`: FloatField (null=True)
- `smoke_level`: FloatField (null=True)
- `battery_level`: IntegerField (null=True)
- `latitude`: DecimalField (null=True)
- `longitude`: DecimalField (null=True)
- `fear_probability`: FloatField (null=True)
- `stress_level`: FloatField (null=True)

Each reading typically only populates 1-2 fields based on the `reading_type`, which is why the composite approach is necessary.

## Benefits

1. **Stability**: No more type conversion crashes
2. **Better UX**: Users see all available sensor data, not just the latest reading type
3. **Complete Monitoring**: Temperature monitoring is now visible
4. **Data Persistence**: Sensor values don't disappear when new partial readings arrive
5. **Type Safety**: Robust handling of different data types from PostgreSQL
