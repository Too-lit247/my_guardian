# 🚨 Alert Routing to Nearest Station Implementation

## Overview
This implementation automatically routes emergency alerts to the nearest appropriate station based on:
- **Alert Type** → **Department** (Fire/Police/Medical)
- **Location** → **Nearest Station** (using GPS coordinates)

## 🔧 What Was Implemented

### 1. Enhanced Alert Model
**File:** `Backend/alerts/models.py`

**New Fields:**
- `latitude` & `longitude` - GPS coordinates of the alert
- `assigned_station_id` - UUID of the assigned station
- `get_department_for_alert_type()` - Maps alert types to departments

**Alert Type → Department Mapping:**
```python
Fire Alerts: ['building_fire', 'wildfire', 'gas_leak', 'explosion', 'hazmat_incident', 'fire_detected']
Police Alerts: ['robbery', 'assault', 'traffic_violation', 'domestic_dispute', 'suspicious_activity', 'fear_detected', 'panic_button']
Medical Alerts: ['heart_attack', 'traffic_accident', 'overdose', 'fall_injury', 'allergic_reaction', 'high_heart_rate', 'fall_detected']
```

### 2. Station Finder Service
**File:** `Backend/alerts/services.py`

**Key Features:**
- **Distance Calculation:** Uses Haversine formula for accurate GPS distance
- **Nearest Station Finder:** Finds closest station within specified radius
- **Automatic Assignment:** Assigns alerts to nearest appropriate station
- **Coverage Analysis:** Provides station coverage statistics

**Main Functions:**
```python
StationFinderService.find_nearest_station(lat, lng, department, max_distance_km=100)
StationFinderService.assign_alert_to_nearest_station(alert)
AlertRoutingService.route_emergency_alert(alert_type, lat, lng, severity, description)
```

### 3. Updated Emergency Trigger Processing
**File:** `Backend/devices/views.py`

**Changes:**
- Device triggers now automatically route to nearest station
- Uses GPS coordinates from device readings
- Calculates distance and assigns to closest appropriate station

### 4. New API Endpoints
**File:** `Backend/alerts/views.py` & `Backend/alerts/urls.py`

**New Endpoints:**
```
GET  /api/alerts/find-stations/?latitude=X&longitude=Y&department=fire&radius=50
POST /api/alerts/emergency/
GET  /api/alerts/station-coverage/<station_id>/
```

## 🚀 How It Works

### 1. Device Emergency Detection
```
Device Detects Emergency → GPS Coordinates → Alert Type → Department → Nearest Station
```

**Example:**
1. Device detects `fire_detected` at coordinates `(40.7128, -74.0060)`
2. System maps `fire_detected` → `fire` department
3. Finds nearest fire station within 100km radius
4. Assigns alert to that station with distance info

### 2. Manual Alert Creation
```
User Creates Alert → Provides Location → System Routes → Station Assignment
```

### 3. Distance Calculation
Uses **Haversine Formula** for accurate Earth surface distances:
```python
def calculate_distance(lat1, lon1, lat2, lon2):
    # Returns distance in kilometers
```

## 📋 Setup Instructions

### 1. Run Migrations
```bash
cd Backend
python manage.py makemigrations alerts
python manage.py migrate
```

### 2. Create Sample Data
You need to create regions, districts, and stations with GPS coordinates:

```python
# Create regions
central_region = Region.objects.create(
    name='central',
    display_name='Central Region'
)

# Create districts
fire_district = District.objects.create(
    name='Central Fire District',
    code='CFD001',
    department='fire',
    region=central_region,
    latitude=40.7128,
    longitude=-74.0060,
    address='123 Fire Station Rd'
)

# Create stations
fire_station = Station.objects.create(
    name='Fire Station 1',
    code='FS001',
    district=fire_district,
    latitude=40.7128,
    longitude=-74.0060,
    address='100 Main St'
)
```

### 3. Test the System
Run the test script:
```bash
cd Backend
python test_alert_routing.py
```

## 🎯 Usage Examples

### 1. API Usage - Find Nearest Stations
```javascript
// Find nearest fire stations
const response = await fetch('/api/alerts/find-stations/?latitude=40.7128&longitude=-74.0060&department=fire&radius=50');
const data = await response.json();
console.log(data.stations); // Array of nearby stations with distances
```

### 2. API Usage - Create Emergency Alert
```javascript
// Create emergency alert with automatic routing
const response = await fetch('/api/alerts/emergency/', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
        alert_type: 'building_fire',
        latitude: 40.7128,
        longitude: -74.0060,
        severity: 'high',
        description: 'Building fire at downtown location'
    })
});
const alert = await response.json();
console.log(alert.assigned_station); // Automatically assigned station
```

### 3. Device Integration
The system automatically processes device triggers:
```python
# When device reading triggers emergency
create_emergency_trigger(reading, {
    'trigger_type': 'fire_detected',
    'severity': 'high',
    'trigger_value': 85.0,
    'threshold_value': 80.0
})
# → Automatically creates alert and routes to nearest fire station
```

## 🔍 Key Features

### ✅ **Automatic Department Detection**
- Fire alerts → Fire stations
- Police alerts → Police stations  
- Medical alerts → Medical stations

### ✅ **GPS-Based Routing**
- Calculates real distances using GPS coordinates
- Finds stations within configurable radius (default 100km)
- Handles cases where no stations are nearby

### ✅ **Distance Information**
- Shows exact distance to assigned station
- Helps responders understand response time
- Useful for resource allocation

### ✅ **Fallback Handling**
- If no stations found, alert still created
- Manual assignment possible
- System logs routing decisions

## 🎨 Frontend Integration

### Update Alert Creation Forms
Add location picker to alert creation forms:
```javascript
// Add GPS coordinate inputs
<input type="number" name="latitude" placeholder="Latitude" />
<input type="number" name="longitude" placeholder="Longitude" />

// Or integrate with map picker
<MapPicker onLocationSelect={(lat, lng) => setCoordinates({lat, lng})} />
```

### Display Station Assignments
Show assigned station info in alert lists:
```javascript
{alert.assigned_station_name && (
  <Badge>📍 {alert.assigned_station_name} ({alert.assigned_to})</Badge>
)}
```

## 🚨 Important Notes

1. **GPS Coordinates Required:** Alerts need latitude/longitude for routing
2. **Station Data:** Stations must have GPS coordinates to be found
3. **Department Matching:** Alert types must map to existing departments
4. **Distance Limits:** Default 100km radius, configurable per use case
5. **Fallback:** Manual assignment still possible if auto-routing fails

## 🔮 Future Enhancements

- **Real-time Traffic:** Integrate with traffic APIs for actual travel time
- **Station Capacity:** Consider station availability and capacity
- **Multi-Station Alerts:** Route to multiple stations for major emergencies
- **Predictive Routing:** Use historical data to optimize assignments
- **Mobile Integration:** Push notifications to assigned station personnel

---

The alert routing system is now ready to automatically direct emergency alerts to the nearest appropriate stations based on alert type and location! 🎯
