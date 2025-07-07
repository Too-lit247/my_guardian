import 'dart:math';
import 'package:flutter/material.dart';
import 'package:my_guardian/auth/auth_service.dart';
import 'package:my_guardian/services/postgre_auth.dart';

class Dashboard extends StatefulWidget {
  const Dashboard({super.key});

  @override
  _DashboardState createState() => _DashboardState();
}

class _DashboardState extends State<Dashboard> {
  int heartRate = 80;
  String voiceStatus = "Normal";
  bool alertSent = false;

  final List<String> _voiceStates = ["Normal", "Distressed", "Silent"];
  final Random _random = Random();

  void _updateData(
    int newHeartRate,
    String newVoiceStatus,
    bool emergencyAlert,
  ) {
    setState(() {
      heartRate = newHeartRate;
      voiceStatus = newVoiceStatus;
      alertSent = emergencyAlert;
    });
  }

  void _triggerDataManually() {
    final newRate = 60 + _random.nextInt(100);
    final newVoice = _voiceStates[_random.nextInt(_voiceStates.length)];
    final emergency = newRate > 120 || newVoice == "Distressed";

    _updateData(newRate, newVoice, emergency);
  }

  @override
  Widget build(BuildContext context) {
    final user = DjangoAuthService().currentUser;

    return Scaffold(
      backgroundColor: Colors.white,
      // appBar: AppBar(
      //   title: const Text("Dashboard"),
      //   backgroundColor: Colors.green,
      //   foregroundColor: Colors.white,
      //   centerTitle: true,
      // ),
      body: SingleChildScrollView(
        child: Column(
          children: [
            const SizedBox(height: 50),
            SizedBox(
              width: double.infinity,
              height: 350,
              child: Image.asset(
                "assets/images/dashboard.jpg",
                fit: BoxFit.cover,
              ),
            ),
            Padding(
              padding: const EdgeInsets.only(top: 12.0),
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
                ],
              ),
            ),
            if (alertSent)
              Card(
                elevation: 3,
                margin: const EdgeInsets.all(10),
                child: ListTile(
                  leading: const Icon(
                    Icons.warning,
                    color: Colors.orange,
                    size: 30,
                  ),
                  title: const Text("Emergency Alert Sent"),
                  subtitle: const Text(
                    "An emergency SMS has been sent by my_guardian.",
                  ),
                ),
              ),
            const SizedBox(height: 10),
            Card(
              margin: const EdgeInsets.all(10),
              child: Padding(
                padding: const EdgeInsets.symmetric(vertical: 15.0),
                child: ListTile(
                  leading: const Icon(
                    Icons.favorite,
                    color: Colors.red,
                    size: 30,
                  ),
                  title: const Text("Heart Rate"),
                  subtitle: Text(
                    "~$heartRate BPM",
                    style: const TextStyle(
                      fontSize: 20,
                      fontWeight: FontWeight.bold,
                    ),
                  ),
                ),
              ),
            ),
            Card(
              elevation: 2,
              margin: const EdgeInsets.all(10),
              child: Padding(
                padding: const EdgeInsets.symmetric(vertical: 15.0),
                child: ListTile(
                  leading: const Icon(Icons.mic, color: Colors.green, size: 30),
                  title: const Text("Voice Monitoring"),
                  subtitle: Text(
                    voiceStatus,
                    style: const TextStyle(
                      fontSize: 20,
                      fontWeight: FontWeight.bold,
                    ),
                  ),
                ),
              ),
            ),
            const SizedBox(height: 20),
            ElevatedButton.icon(
              onPressed: _triggerDataManually,
              icon: const Icon(Icons.sync),
              label: const Text("Simulate Update"),
              style: ElevatedButton.styleFrom(backgroundColor: Colors.green),
            ),
            const SizedBox(height: 30),
          ],
        ),
      ),
    );
  }
}
