import 'package:flutter/material.dart';
import 'package:my_guardian/auth/auth_service.dart';
import 'package:my_guardian/services/device_reading_service.dart';

class Dashboard extends StatefulWidget {
  const Dashboard({super.key});

  @override
  _DashboardState createState() => _DashboardState();
}

class _DashboardState extends State<Dashboard> {
  Map<String, dynamic>? latestData;
  bool deviceNotFound = false;

  @override
  void initState() {
    super.initState();

    DeviceReadingService().init();
    DeviceReadingService().latestReading.addListener(() {
      final reading = DeviceReadingService().latestReading.value;

      if (reading != null) {
        setState(() {
          latestData = reading;
          deviceNotFound = false;
        });
      } else {
        setState(() {
          latestData = null;
          deviceNotFound = true;
        });
      }
    });
  }

  @override
  void dispose() {
    DeviceReadingService().dispose();
    super.dispose();
  }

  Widget _buildSensorCard({
    required IconData icon,
    required String label,
    required String value,
  }) {
    return Container(
      margin: const EdgeInsets.symmetric(vertical: 8, horizontal: 16),
      padding: const EdgeInsets.all(16),
      decoration: BoxDecoration(
        color: Colors.grey[200],
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
                Text(
                  value,
                  style: const TextStyle(
                    fontSize: 18,
                    fontWeight: FontWeight.bold,
                  ),
                ),
              ],
            ),
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
        value: "${data['heart_rate'] ?? 'N/A'} BPM",
      ),
      _buildSensorCard(
        icon: Icons.thermostat,
        label: "Temperature",
        value: "${data['temperature']?.toStringAsFixed(1) ?? 'N/A'} °C",
      ),
      _buildSensorCard(
        icon: Icons.local_fire_department,
        label: "Smoke Level",
        value: "${data['smoke_level']?.toStringAsFixed(2) ?? 'N/A'}",
      ),
      _buildSensorCard(
        icon: Icons.battery_full,
        label: "Battery Level",
        value: "${data['battery_level'] ?? 'N/A'}%",
      ),
      _buildSensorCard(
        icon: Icons.location_on,
        label: "Location",
        value:
            "${data['latitude']?.toStringAsFixed(4) ?? 'N/A'}, ${data['longitude']?.toStringAsFixed(4) ?? 'N/A'}",
      ),
      _buildSensorCard(
        icon: Icons.analytics,
        label: "Stress Level",
        value: "${data['stress_level']?.toStringAsFixed(2) ?? 'N/A'}",
      ),
      _buildSensorCard(
        icon: Icons.psychology,
        label: "Fear Probability",
        value: "${data['fear_probability']?.toStringAsFixed(2) ?? 'N/A'}",
      ),
      _buildSensorCard(
        icon: Icons.surround_sound,
        label: "Audio Analysis",
        value:
            data['audio_analysis_complete'] == true
                ? "Complete"
                : "In Progress",
      ),
      _buildSensorCard(
        icon: Icons.warning_amber_rounded,
        label: "Emergency Triggered",
        value: data['is_emergency'] == true ? "YES" : "NO",
      ),
      _buildSensorCard(
        icon: Icons.person_pin,
        label: "Triggered By",
        value: data['triggered_by'] ?? "Unknown",
      ),
    ];
  }

  @override
  Widget build(BuildContext context) {
    final user = DjangoAuthService().currentUser;

    return Scaffold(
      backgroundColor: Colors.white,
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
            if (deviceNotFound)
              const Padding(
                padding: EdgeInsets.all(16),
                child: Text(
                  "Device not found for this user.",
                  style: TextStyle(color: Colors.red, fontSize: 16),
                ),
              ),
            Padding(
              padding: const EdgeInsets.only(top: 8.0),
              child: Column(
                children: [
                  Text(
                    "Welcome, ${user?.displayName ?? 'User'}",
                    style: const TextStyle(
                      fontSize: 18,
                      fontWeight: FontWeight.bold,
                    ),
                  ),
                  Text(
                    user?.email ?? '',
                    style: const TextStyle(fontSize: 14, color: Colors.black54),
                  ),
                ],
              ),
            ),
            const SizedBox(height: 10),
            const Icon(
              Icons.bluetooth_connected_rounded,
              size: 50,
              color: Colors.green,
            ),
            const Text(
              "Connected to Bracelet",
              style: TextStyle(fontSize: 16, fontWeight: FontWeight.w500),
            ),
            const SizedBox(height: 10),
            ..._buildSensorCards(),
            const SizedBox(height: 30),
          ],
        ),
      ),
    );
  }
}
