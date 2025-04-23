import 'package:flutter/material.dart';
import 'package:get/get.dart';
import 'package:flutter_blue_plus/flutter_blue_plus.dart';
import 'package:my_guardian/controllers/ble_controller.dart';

class DeviceSetupScreen extends StatefulWidget {
  const DeviceSetupScreen({super.key});

  @override
  State<DeviceSetupScreen> createState() => _DeviceSetupScreenState();
}

class _DeviceSetupScreenState extends State<DeviceSetupScreen> {
  final BleController bleController = Get.put(BleController());
  bool isScanning = false;

  void _startScanning() async {
    setState(() {
      isScanning = true;
    });

    await bleController.scanDevices();

    setState(() {
      isScanning = false;
    });
  }

  void _stopScanning() {
    FlutterBluePlus.stopScan();
    setState(() {
      isScanning = false;
    });
  }

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
                  child: StreamBuilder<List<ScanResult>>(
                    stream: bleController.scanResults,
                    builder: (context, snapshot) {
                      if (snapshot.connectionState == ConnectionState.waiting) {
                        return const Center(child: CircularProgressIndicator());
                      }
                      if (snapshot.hasError) {
                        return const Center(child: Text('Error scanning for devices'));
                      }
                      final devices = snapshot.data ?? [];
                      if (devices.isEmpty) {
                        return const Center(child: Text('No devices found.'));
                      }
                      return ListView.builder(
                        itemCount: devices.length,
                        itemBuilder: (context, index) {
                          final device = devices[index].device;
                          return ListTile(
                            leading: const Icon(Icons.watch),
                            title: Text(device.name.isNotEmpty ? device.name : 'Unknown Device'),
                            subtitle: Text(device.id.toString()),
                            onTap: () {
                              FlutterBluePlus.stopScan();
                              Navigator.pop(context);
                              ScaffoldMessenger.of(context).showSnackBar(
                                SnackBar(
                                  content: Text('Connected to ${device.name.isNotEmpty ? device.name : 'Unknown Device'}'),
                                ),
                              );
                            },
                          );
                        },
                      );
                    },
                  ),
                ),
              ],
            ),
          ),
          actions: [
            TextButton(
              onPressed: () {
                if (isScanning) {
                  _stopScanning();
                } else {
                  _startScanning();
                }
                setState(() {});
              },
              child: Text(isScanning ? 'Stop Scanning' : 'Rescan'),
            ),
            TextButton(
              onPressed: () {
                FlutterBluePlus.stopScan();
                Navigator.pop(context);
              },
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
              child: const Text("Connect to My Guardian"),
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
                Navigator.pushReplacementNamed(context, '/home');
              },
              child: const Text("Finish"),
            ),
          ],
        ),
      ),
    );
  }
}