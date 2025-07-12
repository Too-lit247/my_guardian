import 'package:flutter/material.dart';
import 'package:my_guardian/services/device_reading_service.dart';
import 'package:my_guardian/services/postgre_auth.dart';
import 'package:url_launcher/url_launcher.dart';

class Dashboard extends StatefulWidget {
  const Dashboard({super.key});

  @override
  _DashboardState createState() => _DashboardState();
}

class _DashboardState extends State<Dashboard> with TickerProviderStateMixin {
  Map<String, dynamic>? latestData;
  bool deviceNotFound = false;
  bool isEmergency = false;
  late AnimationController _emergencyController;
  late Animation<Color?> _colorAnimation;

  @override
  void initState() {
    super.initState();

    // Initialize emergency animation
    _emergencyController = AnimationController(
      duration: const Duration(milliseconds: 500),
      vsync: this,
    );
    _colorAnimation = ColorTween(
      begin: Colors.red,
      end: Colors.red.shade900,
    ).animate(_emergencyController);

    DeviceReadingService().init();
    DeviceReadingService().latestReading.addListener(() {
      final reading = DeviceReadingService().latestReading.value;

      if (reading != null) {
        final emergencyStatus = reading['is_emergency'] == true;

        setState(() {
          latestData = reading;
          deviceNotFound = false;
          isEmergency = emergencyStatus;
        });

        // Handle emergency state
        if (emergencyStatus) {
          _emergencyController.repeat(reverse: true);
        } else {
          _emergencyController.stop();
          _emergencyController.reset();
        }
      } else {
        setState(() {
          latestData = null;
          deviceNotFound = true;
          isEmergency = false;
        });
      }
    });
  }

  @override
  void dispose() {
    _emergencyController.dispose();
    DeviceReadingService().dispose();
    super.dispose();
  }

  // Battery level widget with color-coded icons
  Widget _buildBatteryLevel(int? batteryLevel) {
    if (batteryLevel == null) {
      return const Row(
        children: [
          Icon(Icons.battery_unknown, color: Colors.grey, size: 24),
          SizedBox(width: 8),
          Text(
            "N/A",
            style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold),
          ),
        ],
      );
    }

    IconData batteryIcon;
    Color batteryColor;

    if (batteryLevel <= 15) {
      batteryIcon = Icons.battery_0_bar;
      batteryColor = Colors.red;
    } else if (batteryLevel <= 30) {
      batteryIcon = Icons.battery_2_bar;
      batteryColor = Colors.orange;
    } else if (batteryLevel <= 50) {
      batteryIcon = Icons.battery_3_bar;
      batteryColor = Colors.yellow.shade700;
    } else if (batteryLevel <= 80) {
      batteryIcon = Icons.battery_5_bar;
      batteryColor = Colors.lightGreen;
    } else {
      batteryIcon = Icons.battery_full;
      batteryColor = Colors.green;
    }

    return Row(
      children: [
        Icon(batteryIcon, color: batteryColor, size: 24),
        const SizedBox(width: 8),
        Text(
          "$batteryLevel%",
          style: TextStyle(
            fontSize: 18,
            fontWeight: FontWeight.bold,
            color: batteryColor,
          ),
        ),
      ],
    );
  }

  // GPS location button
  Widget _buildLocationButton(double? latitude, double? longitude) {
    if (latitude == null || longitude == null) {
      return const Text(
        "Location not available",
        style: TextStyle(fontSize: 16, color: Colors.grey),
      );
    }

    return ElevatedButton.icon(
      onPressed: () => _openLocationInMaps(latitude, longitude),
      icon: const Icon(Icons.map, size: 20),
      label: const Text("View in Maps"),
      style: ElevatedButton.styleFrom(
        backgroundColor: Colors.blue,
        foregroundColor: Colors.white,
        padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 8),
      ),
    );
  }

  // Open location in maps
  void _openLocationInMaps(double latitude, double longitude) async {
    final String googleMapsUrl =
        "https://www.google.com/maps/search/?api=1&query=$latitude,$longitude";
    final String appleMapsUrl =
        "https://maps.apple.com/?q=$latitude,$longitude";

    try {
      // Try to open in default maps app
      final Uri mapsUri = Uri.parse(
        "geo:$latitude,$longitude?q=$latitude,$longitude",
      );
      if (await canLaunchUrl(mapsUri)) {
        await launchUrl(mapsUri);
      } else {
        // Fallback to web maps
        final Uri webUri = Uri.parse(googleMapsUrl);
        await launchUrl(webUri);
      }
    } catch (e) {
      // Show error message
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(content: Text("Could not open maps application")),
      );
    }
  }

  Widget _buildSensorCard({
    required IconData icon,
    required String label,
    required Widget valueWidget,
    Color? cardColor,
  }) {
    return Container(
      margin: const EdgeInsets.symmetric(vertical: 8, horizontal: 16),
      padding: const EdgeInsets.all(16),
      decoration: BoxDecoration(
        color: cardColor ?? Colors.grey[200],
        border: Border.all(color: Colors.grey[100]!),
        borderRadius: BorderRadius.circular(10),
      ),
      child: Row(
        children: [
          Icon(icon, size: 30, color: Colors.blueGrey),
          const SizedBox(width: 16),
          Expanded(
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Text(
                  label,
                  style: const TextStyle(
                    fontSize: 16,
                    fontWeight: FontWeight.w500,
                  ),
                ),
                valueWidget,
              ],
            ),
          ),
        ],
      ),
    );
  }

  Widget _buildCombinedStressFearCard() {
    final data = latestData!;
    final stressLevel = data['stress_level']?.toStringAsFixed(2) ?? 'N/A';
    final fearProbability =
        data['fear_probability']?.toStringAsFixed(2) ?? 'N/A';

    return Container(
      margin: const EdgeInsets.symmetric(vertical: 8, horizontal: 16),
      padding: const EdgeInsets.all(16),
      decoration: BoxDecoration(
        color: Colors.grey[200],
        border: Border.all(color: Colors.grey[100]!),
        borderRadius: BorderRadius.circular(10),
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          const Row(
            children: [
              Icon(Icons.psychology, size: 30, color: Colors.blueGrey),
              SizedBox(width: 16),
              Text(
                "Mental State",
                style: TextStyle(fontSize: 16, fontWeight: FontWeight.w500),
              ),
            ],
          ),
          const SizedBox(height: 12),
          Row(
            children: [
              Expanded(
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    const Text(
                      "Stress Level",
                      style: TextStyle(fontSize: 14, color: Colors.grey),
                    ),
                    Text(
                      stressLevel,
                      style: const TextStyle(
                        fontSize: 16,
                        fontWeight: FontWeight.bold,
                      ),
                    ),
                  ],
                ),
              ),
              Expanded(
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    const Text(
                      "Fear Probability",
                      style: TextStyle(fontSize: 14, color: Colors.grey),
                    ),
                    Text(
                      fearProbability,
                      style: const TextStyle(
                        fontSize: 16,
                        fontWeight: FontWeight.bold,
                      ),
                    ),
                  ],
                ),
              ),
            ],
          ),
        ],
      ),
    );
  }

  List<Widget> _buildSensorCards() {
    if (latestData == null) {
      return [
        const Padding(
          padding: EdgeInsets.all(20),
          child: Text("No data available.", style: TextStyle(fontSize: 16)),
        ),
      ];
    }

    final data = latestData!;
    return [
      _buildSensorCard(
        icon: Icons.favorite,
        label: "Heart Rate",
        valueWidget: Text(
          "${data['heart_rate'] ?? 'N/A'} BPM",
          style: const TextStyle(fontSize: 18, fontWeight: FontWeight.bold),
        ),
      ),
      _buildSensorCard(
        icon: Icons.battery_charging_full,
        label: "Battery Level",
        valueWidget: _buildBatteryLevel(data['battery_level']),
      ),
      _buildSensorCard(
        icon: Icons.local_fire_department,
        label: "Smoke Level",
        valueWidget: Text(
          "${data['smoke_level']?.toStringAsFixed(2) ?? 'N/A'}",
          style: const TextStyle(fontSize: 18, fontWeight: FontWeight.bold),
        ),
      ),
      _buildSensorCard(
        icon: Icons.location_on,
        label: "Location",
        valueWidget: _buildLocationButton(data['latitude'], data['longitude']),
      ),
      _buildCombinedStressFearCard(),
      _buildSensorCard(
        icon: Icons.surround_sound,
        label: "Audio Analysis",
        valueWidget: Text(
          data['audio_analysis_complete'] == true ? "Complete" : "In Progress",
          style: const TextStyle(fontSize: 18, fontWeight: FontWeight.bold),
        ),
      ),
    ];
  }

  Widget _buildEmergencyAlert() {
    if (!isEmergency) return const SizedBox.shrink();

    return AnimatedBuilder(
      animation: _colorAnimation,
      builder: (context, child) {
        return Container(
          width: double.infinity,
          padding: const EdgeInsets.all(16),
          margin: const EdgeInsets.all(16),
          decoration: BoxDecoration(
            color: _colorAnimation.value,
            borderRadius: BorderRadius.circular(10),
            boxShadow: [
              BoxShadow(
                color: Colors.red.withOpacity(0.5),
                blurRadius: 10,
                spreadRadius: 2,
              ),
            ],
          ),
          child: Column(
            children: [
              const Icon(Icons.warning, size: 50, color: Colors.white),
              const SizedBox(height: 8),
              const Text(
                "EMERGENCY DETECTED!",
                style: TextStyle(
                  fontSize: 24,
                  fontWeight: FontWeight.bold,
                  color: Colors.white,
                ),
              ),
              const SizedBox(height: 8),
              Text(
                "Triggered by: ${latestData?['triggered_by'] ?? 'Unknown'}",
                style: const TextStyle(fontSize: 16, color: Colors.white),
              ),
              const SizedBox(height: 8),
              const Text(
                "Emergency services have been notified",
                style: TextStyle(fontSize: 14, color: Colors.white70),
              ),
            ],
          ),
        );
      },
    );
  }

  Widget _buildNoDevicePrompt() {
    return Container(
      margin: const EdgeInsets.all(16),
      padding: const EdgeInsets.all(24),
      decoration: BoxDecoration(
        color: Colors.orange.shade50,
        border: Border.all(color: Colors.orange.shade200),
        borderRadius: BorderRadius.circular(10),
      ),
      child: Column(
        children: [
          Icon(Icons.device_unknown, size: 60, color: Colors.orange.shade400),
          const SizedBox(height: 16),
          const Text(
            "No Guardian Device Found",
            style: TextStyle(fontSize: 20, fontWeight: FontWeight.bold),
          ),
          const SizedBox(height: 8),
          const Text(
            "To view device readings, please set up your Guardian device in Settings.",
            textAlign: TextAlign.center,
            style: TextStyle(fontSize: 16, color: Colors.grey),
          ),
          const SizedBox(height: 16),
          ElevatedButton.icon(
            onPressed: () {
              // Navigate to settings
              Navigator.pushNamed(context, '/settings');
            },
            icon: const Icon(Icons.settings),
            label: const Text("Go to Settings"),
            style: ElevatedButton.styleFrom(
              backgroundColor: Colors.orange,
              foregroundColor: Colors.white,
              padding: const EdgeInsets.symmetric(horizontal: 24, vertical: 12),
            ),
          ),
        ],
      ),
    );
  }

  @override
  Widget build(BuildContext context) {
    final user = PostgreAuth().currentUser;

    return Scaffold(
      backgroundColor: isEmergency ? Colors.red.shade50 : Colors.white,
      body: SingleChildScrollView(
        child: Column(
          children: [
            const SizedBox(height: 50),
            SizedBox(
              width: double.infinity,
              height: 300,
              child: Image.asset(
                "assets/images/dashboard.jpg",
                fit: BoxFit.cover,
              ),
            ),
            const SizedBox(height: 16),

            // Emergency alert
            _buildEmergencyAlert(),

            // User welcome section
            if (!isEmergency) ...[
              Padding(
                padding: const EdgeInsets.only(top: 8.0),
                child: Column(
                  children: [
                    Text(
                      "Welcome, ${user?['full_name'] ?? 'User'}",
                      style: const TextStyle(
                        fontSize: 18,
                        fontWeight: FontWeight.bold,
                      ),
                    ),
                    Text(
                      "${user?['email'] ?? ''}",
                      style: const TextStyle(
                        fontSize: 14,
                        color: Colors.black54,
                      ),
                    ),
                  ],
                ),
              ),
              const SizedBox(height: 10),

              // Connection status
              if (!deviceNotFound) ...[
                const Icon(
                  Icons.bluetooth_connected_rounded,
                  size: 50,
                  color: Colors.green,
                ),
                const Text(
                  "Connected to Bracelet",
                  style: TextStyle(fontSize: 16, fontWeight: FontWeight.w500),
                ),
              ],
              const SizedBox(height: 10),
            ],

            // Device readings or no device prompt
            if (deviceNotFound)
              _buildNoDevicePrompt()
            else if (!isEmergency)
              ..._buildSensorCards(),

            const SizedBox(height: 30),
          ],
        ),
      ),
    );
  }
}
