import 'package:bluetooth_classic/bluetooth_classic.dart';
import 'package:bluetooth_classic/models/device.dart';
import 'package:flutter/material.dart';
import 'package:flutter_blue_plus/flutter_blue_plus.dart';
import 'package:my_guardian/widgets/settingsHeader.dart';
import 'package:my_guardian/widgets/settingsTile.dart';
import 'package:permission_handler/permission_handler.dart';

class Bluetoothscanwidget extends StatefulWidget {
  const Bluetoothscanwidget({super.key});

  @override
  State<Bluetoothscanwidget> createState() => _BluetoothscanwidgetState();
}

class _BluetoothscanwidgetState extends State<Bluetoothscanwidget> {
  final BluetoothClassic _bluetooth = BluetoothClassic();
  final List<Device> _foundDevices = [];
  bool _isScanning = false;

  Device? _connectedDevice;
  BluetoothConnectionEvent? _connection;
  String _receivedData = "";

  @override
  void initState() {
    super.initState();
    _initBluetooth();
  }

  // Bluetooth Functions

  Future<void> _initBluetooth() async {
    // Set up bluetooth event listeners for device discovery
    _bluetooth.onDeviceDiscovered().listen((device) {
      setState(() {
        if (!_foundDevices.any((d) => d.address == device.address)) {
          _foundDevices.add(device);
        }
      });
    });
  }

  Future<void> _scanForBluetoothDevices() async {
    //Request Bluetooth permissions
    var bluetoothStatus = await Permission.bluetooth.request();
    var bluetoothConnectStatus = await Permission.bluetoothConnect.request();
    var bluetoothScanStatus = await Permission.bluetoothScan.request();

    if (!bluetoothStatus.isGranted ||
        !bluetoothConnectStatus.isGranted ||
        !bluetoothScanStatus.isGranted) {
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(content: Text("Bluetooth permissions are required")),
      );
      return;
    }

    setState(() {
      _foundDevices.clear();
      _isScanning = true;
    });

    try {
      // Start discovery to find new devices
      await _bluetooth.startScan();

      // Stop discovery after 30 seconds
      Future.delayed(const Duration(seconds: 20), () {
        if (_isScanning) {
          _bluetooth.stopScan();
          setState(() {
            _isScanning = false;
          });
        }
      });
    } catch (e) {
      ScaffoldMessenger.of(
        context,
      ).showSnackBar(SnackBar(content: Text("Error scanning devices: $e")));
      setState(() {
        _isScanning = false;
      });
    }
  }

  Future<void> _stopScan() async {
    if (_isScanning) {
      await _bluetooth.stopScan();
      setState(() {
        _isScanning = false;
      });
    }
  }

  Future<void> _connectToDevice(Device device) async {
    try {
      final connection = await _bluetooth.connect(device);
      setState(() {
        _connectedDevice = device;
        _connection = connection;
      });

      // Listen to incoming data
      connection.input.listen((data) {
        final incoming = String.fromCharCodes(data);
        setState(() {
          _receivedData += incoming;
        });
        print('Received: $incoming');
      });

      ScaffoldMessenger.of(
        context,
      ).showSnackBar(SnackBar(content: Text('Connected to ${device.name}')));
    } catch (e) {
      ScaffoldMessenger.of(
        context,
      ).showSnackBar(SnackBar(content: Text('Connection failed: $e')));
    }
  }

  @override
  void dispose() {
    _stopScan();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return Column(
      children: [
        const SizedBox(height: 20),
        const SettingsHeader(title: "Bluetooth Devices"),

        SettingsTile(
          icon: Icons.bluetooth_searching,
          title: "Scan for Bluetooth Devices",
          trailing: ElevatedButton(
            style: ElevatedButton.styleFrom(backgroundColor: Colors.green),
            onPressed: _isScanning ? _stopScan : _scanForBluetoothDevices,
            child: Text(
              _isScanning ? "Stop Scan" : "Start Scan",
              style: const TextStyle(color: Colors.white),
            ),
          ),
        ),
        if (_foundDevices.isNotEmpty)
          Column(
            children: [
              Padding(
                padding: const EdgeInsets.all(16.0),
                child: Row(
                  children: const [
                    Icon(Icons.bluetooth, color: Colors.blue),
                    SizedBox(width: 8),
                    Text(
                      "Available Devices",
                      style: TextStyle(
                        fontSize: 16,
                        fontWeight: FontWeight.bold,
                      ),
                    ),
                  ],
                ),
              ),
              ListView.builder(
                shrinkWrap: true,
                physics: const NeverScrollableScrollPhysics(),
                itemCount: _foundDevices.length,
                itemBuilder: (context, index) {
                  final device = _foundDevices[index];
                  return InkWell(
                    onTap: () => _connectToDevice(device),
                    child: Container(
                      margin: const EdgeInsets.symmetric(
                        horizontal: 16,
                        vertical: 5,
                      ),
                      padding: const EdgeInsets.all(12),
                      decoration: BoxDecoration(
                        color: Colors.grey[100],
                        borderRadius: BorderRadius.circular(10),
                        border: Border.all(color: Colors.white),
                      ),
                      child: Row(
                        children: [
                          const Icon(Icons.bluetooth, color: Colors.blue),
                          const SizedBox(width: 10),
                          Expanded(
                            child: Column(
                              crossAxisAlignment: CrossAxisAlignment.start,
                              children: [
                                Text(
                                  device.name ?? "Unknown Device",
                                  style: const TextStyle(
                                    fontWeight: FontWeight.bold,
                                  ),
                                ),
                                Text(device.address),
                              ],
                            ),
                          ),
                        ],
                      ),
                    ),
                  );
                },
              ),
              if (_connectedDevice != null)
                Padding(
                  padding: const EdgeInsets.all(16.0),
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      const Text(
                        "Connected to:",
                        style: TextStyle(fontWeight: FontWeight.bold),
                      ),
                      Text(_connectedDevice!.name ?? _connectedDevice!.address),
                      const SizedBox(height: 10),
                      const Text("Incoming Data:"),
                      Text(
                        _receivedData.isEmpty ? "No data yet." : _receivedData,
                      ),
                    ],
                  ),
                ),
            ],
          ),
        if (_isScanning)
          const Padding(
            padding: EdgeInsets.all(16.0),
            child: Center(
              child: Column(
                children: [
                  CircularProgressIndicator(color: Colors.green),
                  SizedBox(height: 8),
                  Text("Scanning for devices..."),
                ],
              ),
            ),
          ),
      ],
    );
  }
}
