import 'package:flutter/material.dart';

class DeviceSetupScreen extends StatefulWidget {
  const DeviceSetupScreen({super.key});

  @override
  State<DeviceSetupScreen> createState() => _DeviceSetupScreenState();
}

class _DeviceSetupScreenState extends State<DeviceSetupScreen> {
  bool isScanning = false;
  final List<Map<String, String>> dummyDevices = [
    {'name': 'Safety Bracelet 1', 'id': '00:11:22:33:44:55'},
    {'name': 'Safety Bracelet 2', 'id': '66:77:88:99:AA:BB'},
    {'name': 'Safety Bracelet 3', 'id': 'CC:DD:EE:FF:00:11'},
  ];

  void _showDeviceScanningDialog() {
    showDialog(
      context: context,
      builder: (context) => StatefulBuilder(
        builder: (context, setState) => AlertDialog(
          title: const Text('Connect Device'),
          content: SizedBox(
            width: double.maxFinite,
            child: Column(
              mainAxisSize: MainAxisSize.min,
              children: [
                if (isScanning) ...[
                  const CircularProgressIndicator(),
                  const SizedBox(height: 16),
                  const Text('Scanning for devices...'),
                ],
                const SizedBox(height: 16),
                SizedBox(
                  height: 200,
                  child: ListView.builder(
                    itemCount: dummyDevices.length,
                    itemBuilder: (context, index) => ListTile(
                      leading: const Icon(Icons.watch),
                      title: Text(dummyDevices[index]['name']!),
                      subtitle: Text(dummyDevices[index]['id']!),
                      onTap: () {
                        Navigator.pop(context);
                        // Handle device selection
                      },
                    ),
                  ),
                ),
              ],
            ),
          ),
          actions: [
            TextButton(
              onPressed: () {
                setState(() => isScanning = !isScanning);
              },
              child: Text(isScanning ? 'Stop Scanning' : 'Rescan'),
            ),
            TextButton(
              onPressed: () => Navigator.pop(context),
              child: const Text('Cancel'),
            ),
          ],
        ),
      ),
    );
  }

  @override
  Widget build(BuildContext context) {
    return SafeArea(
      child: Padding(
        padding: const EdgeInsets.symmetric(horizontal: 24.0, vertical: 50.0),
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            const Text(
              "Setup Your Device",
              style: TextStyle(fontSize: 24, fontWeight: FontWeight.bold),
            ),
            const SizedBox(height: 10),
            ElevatedButton(
              onPressed: _showDeviceScanningDialog,
              child: const Text("Connect to Bracelet"),
            ),
            const SizedBox(height: 20),
            const Text(
              "Add Your First Emergency Contact",
              style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold),
            ),
            const SizedBox(height: 10),
            Card(
              child: Padding(
                padding: const EdgeInsets.all(16.0),
                child: Column(
                  children: [
                    const TextField(
                      decoration: InputDecoration(
                        labelText: "Contact Name",
                        prefixIcon: Icon(Icons.person),
                      ),
                    ),
                    const SizedBox(height: 10),
                    const TextField(
                      decoration: InputDecoration(
                        labelText: "Relationship",
                        prefixIcon: Icon(Icons.family_restroom),
                      ),
                    ),
                    const SizedBox(height: 10),
                    const TextField(
                      decoration: InputDecoration(
                        labelText: "Phone Number",
                        prefixIcon: Icon(Icons.phone),
                      ),
                      keyboardType: TextInputType.phone,
                    ),
                    const SizedBox(height: 16),
                    ElevatedButton(
                      onPressed: () {},
                      child: const Text("Add Contact"),
                    ),
                    ElevatedButton(
                      onPressed: () {},
                      child: const Text("Get Existing Contact"),
                    ),
                  ],
                ),
              ),
            ),
            const SizedBox(height: 20),
            const Expanded(
              child: SizedBox(), // Placeholder for contacts list
            ),
            const SizedBox(height: 20),
            ElevatedButton(
              onPressed: () {
                Navigator.pushNamed(context, '/');
              },
              child: const Text("Finish"),
            ),
          ],
        ),
      ),
    );
  }
}
