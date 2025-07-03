import 'dart:async';
import 'dart:convert';
import 'dart:math';
import 'package:flutter/material.dart';
import 'package:flutter_blue_classic/flutter_blue_classic.dart';
import 'package:permission_handler/permission_handler.dart';
import 'package:http/http.dart' as http;

class BluetoothScanWidget extends StatefulWidget {
  const BluetoothScanWidget({super.key});

  @override
  State<BluetoothScanWidget> createState() => _BluetoothScanWidgetState();
}

class _BluetoothScanWidgetState extends State<BluetoothScanWidget> {
  final FlutterBlueClassic _bt = FlutterBlueClassic();
  final List<BluetoothDevice> _devices = [];
  bool _scanning = false;
  BluetoothConnection? _connection;
  BluetoothDevice? _connected;
  String _received = "";

  // Stream subscriptions to prevent memory leaks
  StreamSubscription<BluetoothDevice>? _scanSubscription;
  StreamSubscription<BluetoothAdapterState>? _adapterSubscription;
  StreamSubscription<List<int>>? _dataSubscription;
  Timer? _scanTimer;

  @override
  void initState() {
    super.initState();
    _initBluetoothAdapter();
  }

  void _initBluetoothAdapter() {
    _adapterSubscription = _bt.adapterState.listen((state) {
      if (state == BluetoothAdapterState.off && mounted) {
        ScaffoldMessenger.of(context).showSnackBar(
          const SnackBar(content: Text('Bluetooth adapter is off')),
        );
      }
    });
  }

  Future<void> _scan() async {
    if (!await _requestPermissions()) return;

    setState(() {
      _devices.clear();
      _scanning = true;
    });

    // Cancel any existing scan subscription
    await _scanSubscription?.cancel();

    // scanResults typically emits List<BluetoothDevice> or List<ScanResult>
    // Based on flutter_blue_classic pattern, it should emit List<BluetoothDevice>
    _scanSubscription = _bt.scanResults.listen(
      (device) {
        // device is a single BluetoothDevice
        if (!_devices.any(
          (existingDevice) => existingDevice.address == device.address,
        )) {
          if (mounted) {
            setState(() => _devices.add(device));
          }
        }
      },
      onError: (error) {
        if (mounted) {
          ScaffoldMessenger.of(
            context,
          ).showSnackBar(SnackBar(content: Text('Scan error: $error')));
        }
      },
    );

    try {
      _bt.startScan();
      // Set a timer to stop scanning after 20 seconds
      _scanTimer = Timer(const Duration(seconds: 20), () {
        if (mounted) {
          _stopScan();
        }
      });
    } catch (e) {
      if (mounted) {
        setState(() => _scanning = false);
        ScaffoldMessenger.of(
          context,
        ).showSnackBar(SnackBar(content: Text('Failed to start scan: $e')));
      }
    }
  }

  Future<void> _stopScan() async {
    _scanTimer?.cancel();
    _scanTimer = null;

    try {
      _bt.stopScan();
    } catch (e) {
      if (mounted) {
        ScaffoldMessenger.of(
          context,
        ).showSnackBar(SnackBar(content: Text('Failed to stop scan: $e')));
      }
    }

    if (mounted) {
      setState(() => _scanning = false);
    }
  }

  Future<bool> _requestPermissions() async {
    try {
      final statuses =
          await [
            Permission.bluetooth,
            Permission.bluetoothScan,
            Permission.bluetoothConnect,
            Permission.locationWhenInUse,
          ].request();

      return statuses.values.every((status) => status.isGranted);
    } catch (e) {
      if (mounted) {
        ScaffoldMessenger.of(
          context,
        ).showSnackBar(SnackBar(content: Text('Permission error: $e')));
      }
      return false;
    }
  }

  Future<void> _connect(BluetoothDevice device) async {
    try {
      // Close existing connection if any
      await _connection?.close();
      await _dataSubscription?.cancel();

      _connection = await _bt.connect(device.address);

      if (mounted) {
        setState(() => _connected = device);
      }

      // Listen for incoming data
      _dataSubscription = _connection!.input?.listen(
        (data) {
          if (mounted) {
            setState(() => _received += String.fromCharCodes(data));
          }
        },
        onError: (error) {
          if (mounted) {
            ScaffoldMessenger.of(context).showSnackBar(
              SnackBar(content: Text('Data reception error: $error')),
            );
          }
        },
      );

      // Register the device
      await _registerDevice(device);

      if (mounted) {
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(
            content: Text(
              'Connected & registered: ${_getDeviceDisplayName(device)}',
            ),
          ),
        );
      }
    } catch (e) {
      if (mounted) {
        ScaffoldMessenger.of(
          context,
        ).showSnackBar(SnackBar(content: Text('Connection failed: $e')));
      }
    }
  }

  Future<void> _registerDevice(BluetoothDevice device) async {
    try {
      final mac = device.address;
      final name = _getDeviceDisplayName(device);
      final owner = Random().nextInt(5) + 1;

      final payload = {
        "mac_address": mac,
        "name": name,
        "owner": owner,
        "is_active": true,
      };

      final uri = Uri.parse('http://localhost:8000/api/devices/');
      final response = await http.post(
        uri,
        headers: {'Content-Type': 'application/json'},
        body: jsonEncode(payload),
      );

      if (response.statusCode == 201) {
        // Success - device registered
        return;
      } else if (response.statusCode == 400 &&
          response.body.contains('unique')) {
        // Device already registered
        if (mounted) {
          ScaffoldMessenger.of(context).showSnackBar(
            const SnackBar(content: Text('Device already registered')),
          );
        }
        return;
      } else {
        throw Exception(
          'Failed to register device: ${response.statusCode} - ${response.body}',
        );
      }
    } catch (e) {
      if (mounted) {
        ScaffoldMessenger.of(
          context,
        ).showSnackBar(SnackBar(content: Text('Registration failed: $e')));
      }
      // Re-throw to let the caller handle it
      rethrow;
    }
  }

  String _getDeviceDisplayName(BluetoothDevice device) {
    final name = device.name;
    if (name != null && name.isNotEmpty) {
      return name;
    }
    return device.address;
  }

  Future<void> _disconnect() async {
    try {
      await _dataSubscription?.cancel();
      await _connection?.close();

      if (mounted) {
        setState(() {
          _connected = null;
          _connection = null;
          _received = "";
        });

        ScaffoldMessenger.of(
          context,
        ).showSnackBar(const SnackBar(content: Text('Disconnected')));
      }
    } catch (e) {
      if (mounted) {
        ScaffoldMessenger.of(
          context,
        ).showSnackBar(SnackBar(content: Text('Disconnect error: $e')));
      }
    }
  }

  @override
  void dispose() {
    // Cancel all subscriptions and timers
    _scanTimer?.cancel();
    _adapterSubscription?.cancel();
    _scanSubscription?.cancel();
    _dataSubscription?.cancel();

    // Stop scanning if in progress
    if (_scanning) {
      _bt.stopScan();
    }

    // Close connection
    _connection?.close();

    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Bluetooth Scanner'),
        actions: [
          if (_connected != null)
            IconButton(
              icon: const Icon(Icons.bluetooth_disabled),
              onPressed: _disconnect,
              tooltip: 'Disconnect',
            ),
        ],
      ),
      body: Column(
        children: [
          Padding(
            padding: const EdgeInsets.all(16.0),
            child: Row(
              children: [
                Expanded(
                  child: ElevatedButton.icon(
                    onPressed: _scanning ? _stopScan : _scan,
                    icon: Icon(_scanning ? Icons.stop : Icons.search),
                    label: Text(_scanning ? "Stop Scanning" : "Start Scan"),
                  ),
                ),
                const SizedBox(width: 16),
                if (_scanning) const CircularProgressIndicator(),
              ],
            ),
          ),

          if (_connected != null)
            Container(
              margin: const EdgeInsets.all(16.0),
              padding: const EdgeInsets.all(16.0),
              decoration: BoxDecoration(
                color: Colors.green.shade50,
                border: Border.all(color: Colors.green),
                borderRadius: BorderRadius.circular(8),
              ),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Text(
                    'Connected: ${_getDeviceDisplayName(_connected!)}',
                    style: Theme.of(context).textTheme.titleMedium?.copyWith(
                      fontWeight: FontWeight.bold,
                      color: Colors.green.shade700,
                    ),
                  ),
                  const SizedBox(height: 8),
                  Text(
                    'Received: ${_received.isEmpty ? "No data" : _received}',
                    style: Theme.of(context).textTheme.bodyMedium,
                  ),
                ],
              ),
            ),

          Expanded(
            child:
                _devices.isEmpty
                    ? Center(
                      child: Text(
                        _scanning
                            ? 'Scanning for devices...'
                            : 'No devices found. Tap "Start Scan" to search.',
                        style: Theme.of(context).textTheme.bodyLarge,
                        textAlign: TextAlign.center,
                      ),
                    )
                    : ListView.builder(
                      itemCount: _devices.length,
                      itemBuilder: (context, index) {
                        final device = _devices[index];
                        final isConnected =
                            _connected?.address == device.address;

                        return Card(
                          margin: const EdgeInsets.symmetric(
                            horizontal: 16,
                            vertical: 4,
                          ),
                          child: ListTile(
                            leading: Icon(
                              isConnected
                                  ? Icons.bluetooth_connected
                                  : Icons.bluetooth,
                              color: isConnected ? Colors.green : Colors.blue,
                            ),
                            title: Text(
                              _getDeviceDisplayName(device),
                              style: TextStyle(
                                fontWeight:
                                    isConnected
                                        ? FontWeight.bold
                                        : FontWeight.normal,
                              ),
                            ),
                            subtitle: Text(
                              'Address: ${device.address}',
                              style: TextStyle(color: Colors.grey.shade600),
                            ),
                            trailing:
                                isConnected
                                    ? const Icon(
                                      Icons.check_circle,
                                      color: Colors.green,
                                    )
                                    : const Icon(Icons.arrow_forward_ios),
                            onTap: isConnected ? null : () => _connect(device),
                          ),
                        );
                      },
                    ),
          ),
        ],
      ),
    );
  }
}
