import 'package:firebase_auth/firebase_auth.dart';
import 'package:flutter/material.dart';

class Dashboard extends StatefulWidget {
  const Dashboard({super.key});

  @override
  _DashboardState createState() => _DashboardState();
}

class _DashboardState extends State<Dashboard> {
  int heartRate = 80;
  String voiceStatus = "Normal";
  bool alertSent = false;

  void _updateData(int newHeartRate, String newVoiceStatus, bool emergencyAlert) {
    setState(() {
      heartRate = newHeartRate;
      voiceStatus = newVoiceStatus;
      alertSent = emergencyAlert;
    });
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: Colors.grey[200],
      appBar: AppBar(
        title: const Text("Home"),
        backgroundColor: Colors.green,
        foregroundColor: Colors.white,
        centerTitle: true,
        actions: [
          IconButton(
        icon: const Icon(Icons.logout),
        onPressed: () async {
          await FirebaseAuth.instance.signOut();
          Navigator.of(context).pushReplacementNamed('/login');
        },
          ),
        ],
      ),
      body: SingleChildScrollView(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            SizedBox(
              width: double.infinity,
              height: 350,
              child: Image.asset(
                "assets/images/dashboard.jpg",
                fit: BoxFit.cover,
              ),
            ),
            const Text("Connected to Bracelet", style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold)),
            const Icon(Icons.bluetooth_connected_rounded, size: 50, color: Colors.green),
            alertSent
              ? Card(
                  elevation: 3,
                  margin: const EdgeInsets.all(10),
                  child: ListTile(
                    leading: const Icon(Icons.warning, color: Colors.orange, size: 30),
                    title: const Text("Emergency Alert Sent"),
                    subtitle: const Text("An emergency SMS has been sent by the my_guardian."),
                  ),
                )
              : const SizedBox.shrink(),
            const SizedBox(height: 10),
            Card(
              elevation: 2,
              margin: const EdgeInsets.all(10),
              child: Padding(
                padding: const EdgeInsets.symmetric(vertical: 15.0),
                child: ListTile(
                  leading: const Icon(Icons.favorite, color: Colors.red, size: 30),
                  title: const Text("Heart Rate"),
                  subtitle: Text("~$heartRate BPM", style: const TextStyle(fontSize: 20, fontWeight: FontWeight.bold)),
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
                  subtitle: Text(voiceStatus, style: const TextStyle(fontSize: 20, fontWeight: FontWeight.bold)),
                ),
              ),
            ),
          ],
        ),
      ),
    );
  }
}
