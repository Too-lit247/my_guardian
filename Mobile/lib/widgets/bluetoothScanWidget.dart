import 'dart:async';
import 'dart:convert';
import 'package:flutter/material.dart';
import 'package:flutter_blue_classic/flutter_blue_classic.dart';
import 'package:permission_handler/permission_handler.dart';
import 'package:http/http.dart' as http;
import 'package:my_guardian/services/postgre_auth.dart';

class BluetoothScanWidget extends StatefulWidget {
  final String? baseUrl; // Add baseUrl parameter
  final double? height; // Optional height constraint

  const BluetoothScanWidget({super.key, this.baseUrl, this.height});

  @override
  State<BluetoothScanWidget> createState() => _BluetoothScanWidgetState();
}

class _BluetoothScanWidgetState extends State<BluetoothScanWidget> {
  final FlutterBlueClassic _bt = FlutterBlueClassic();
  final List<BluetoothDevice> _devices = [];
  bool _scanning = false;
  final Set<String> _registeredDevices = {}; // Track registered devices
  final Set<String> _registeringDevices = {}; // Track devices being registered
  BluetoothAdapterState _bluetoothState = BluetoothAdapterState.unknown;

  // Stream subscriptions to prevent memory leaks
  StreamSubscription<BluetoothDevice>? _scanSubscription;
  StreamSubscription<BluetoothAdapterState>? _adapterSubscription;
  Timer? _scanTimer;

  // Get base URL from environment or use default
  String get _baseUrl =>
      widget.baseUrl ?? 'https://my-guardian-plus.onrender.com';

  @override
  void initState() {
    super.initState();
    print('🔧 BluetoothScanWidget: Initializing...');
    _initBluetoothAdapter();
  }

  void _initBluetoothAdapter() {
    print('🔧 BluetoothScanWidget: Initializing Bluetooth adapter...');
    _adapterSubscription = _bt.adapterState.listen((state) {
      print('🔧 BluetoothScanWidget: Adapter state changed to: $state');
      if (mounted) {
        setState(() {
          _bluetoothState = state;
        });

        if (state == BluetoothAdapterState.off) {
          print('⚠️ BluetoothScanWidget: Bluetooth adapter is off');
          ScaffoldMessenger.of(context).showSnackBar(
            const SnackBar(content: Text('Bluetooth adapter is off')),
          );
        }
      }
    });

    // Get initial state
    _checkBluetoothState();
  }

  Future<void> _checkBluetoothState() async {
    try {
      print('🔧 BluetoothScanWidget: Checking initial Bluetooth state...');
      final state = await _bt.adapterState.first;
      print('🔧 BluetoothScanWidget: Initial Bluetooth state: $state');
      if (mounted) {
        setState(() {
          _bluetoothState = state;
        });
      }
    } catch (e) {
      print('❌ BluetoothScanWidget: Error checking Bluetooth state: $e');
      if (mounted) {
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(content: Text('Error checking Bluetooth state: $e')),
        );
      }
    }
  }

  Future<bool> _ensureBluetoothEnabled() async {
    print('🔧 BluetoothScanWidget: Ensuring Bluetooth is enabled...');
    if (_bluetoothState == BluetoothAdapterState.on) {
      print('✅ BluetoothScanWidget: Bluetooth is already enabled');

      return true;
    }

    print("Adapter State:");
    //print(BluetoothAdapterState.on);

    if (_bluetoothState == BluetoothAdapterState.off) {
      print('⚠️ BluetoothScanWidget: Bluetooth is off, prompting user...');
      final shouldEnable = await showDialog<bool>(
        context: context,
        builder: (BuildContext context) {
          return AlertDialog(
            title: const Text('Bluetooth Required'),
            content: const Text(
              'Bluetooth is currently turned off. Would you like to enable it to scan for devices?',
            ),
            actions: [
              TextButton(
                onPressed: () => Navigator.of(context).pop(false),
                child: const Text('Cancel'),
              ),
              ElevatedButton(
                onPressed: () => Navigator.of(context).pop(true),
                child: const Text('Enable Bluetooth'),
              ),
            ],
          );
        },
      );

      if (shouldEnable == true) {
        try {
          print('🔧 BluetoothScanWidget: Attempting to turn on Bluetooth...');
          _bt.turnOn();
          // Wait a bit for the adapter to turn on
          await Future.delayed(const Duration(seconds: 2));
          await _checkBluetoothState();
          final enabled = _bluetoothState == BluetoothAdapterState.on;
          print('🔧 BluetoothScanWidget: Bluetooth enabled: $enabled');
          return enabled;
        } catch (e) {
          print('❌ BluetoothScanWidget: Failed to enable Bluetooth: $e');
          if (mounted) {
            ScaffoldMessenger.of(context).showSnackBar(
              SnackBar(content: Text('Failed to enable Bluetooth: $e')),
            );
          }
          return false;
        }
      } else {
        print('❌ BluetoothScanWidget: User cancelled Bluetooth enable');
      }
    }

    return false;
  }

  Future<void> _scan() async {
    print('🔍 BluetoothScanWidget: Starting scan...');
    if (!await _requestPermissions()) {
      print('❌ BluetoothScanWidget: Permissions not granted');
      return;
    }

    // Check and enable Bluetooth if needed
    if (await _ensureBluetoothEnabled()) {
      print('❌ BluetoothScanWidget: Bluetooth not enabled');
      return;
    }

    setState(() {
      _devices.clear();
      _scanning = true;
    });

    // Cancel any existing scan subscription
    await _scanSubscription?.cancel();

    print('🔍 BluetoothScanWidget: Setting up scan subscription...');
    // scanResults typically emits List<BluetoothDevice> or List<ScanResult>
    // Based on flutter_blue_classic pattern, it should emit List<BluetoothDevice>
    _scanSubscription = _bt.scanResults.listen(
      (device) {
        print(
          '📱 BluetoothScanWidget: Found device: ${device.name ?? 'Unknown'} (${device.address})',
        );
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
        print('❌ BluetoothScanWidget: Scan error: $error');
        if (mounted) {
          ScaffoldMessenger.of(
            context,
          ).showSnackBar(SnackBar(content: Text('Scan error: $error')));
        }
      },
    );

    try {
      print('🔍 BluetoothScanWidget: Starting Bluetooth scan...');
      _bt.startScan();
      // Set a timer to stop scanning after 20 seconds
      _scanTimer = Timer(const Duration(seconds: 20), () {
        print('⏰ BluetoothScanWidget: Scan timeout reached (20s)');
        if (mounted) {
          _stopScan();
        }
      });
    } catch (e) {
      print('❌ BluetoothScanWidget: Failed to start scan: $e');
      if (mounted) {
        setState(() => _scanning = false);
        ScaffoldMessenger.of(
          context,
        ).showSnackBar(SnackBar(content: Text('Failed to start scan: $e')));
      }
    }
  }

  Future<void> _stopScan() async {
    print('🔍 BluetoothScanWidget: Stopping scan...');
    _scanTimer?.cancel();
    _scanTimer = null;

    try {
      _bt.stopScan();
      print('✅ BluetoothScanWidget: Scan stopped successfully');
    } catch (e) {
      print('❌ BluetoothScanWidget: Failed to stop scan: $e');
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
    print('🔒 BluetoothScanWidget: Requesting permissions...');
    try {
      final statuses =
          await [
            Permission.bluetooth,
            Permission.bluetoothScan,
            Permission.bluetoothConnect,
            Permission.locationWhenInUse,
          ].request();

      final allGranted = statuses.values.every((status) => status.isGranted);
      print('🔒 BluetoothScanWidget: Permissions granted: $allGranted');
      print('🔒 BluetoothScanWidget: Permission statuses: $statuses');
      return allGranted;
    } catch (e) {
      print('❌ BluetoothScanWidget: Permission error: $e');
      if (mounted) {
        ScaffoldMessenger.of(
          context,
        ).showSnackBar(SnackBar(content: Text('Permission error: $e')));
      }
      return false;
    }
  }

  Future<void> _promptRegisterDevice(BluetoothDevice device) async {
    final deviceName = _getDeviceDisplayName(device);
    print(
      '📝 BluetoothScanWidget: Prompting to register device: $deviceName (${device.address})',
    );

    final shouldRegister = await showDialog<bool>(
      context: context,
      builder: (BuildContext context) {
        return AlertDialog(
          title: const Text('Register Device'),
          content: Column(
            mainAxisSize: MainAxisSize.min,
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              Text('Do you want to register this device?'),
              const SizedBox(height: 16),
              Text(
                'Device: $deviceName',
                style: const TextStyle(fontWeight: FontWeight.bold),
              ),
              Text(
                'Address: ${device.address}',
                style: TextStyle(color: Colors.grey.shade600),
              ),
            ],
          ),
          actions: [
            TextButton(
              onPressed: () => Navigator.of(context).pop(false),
              child: const Text('Cancel'),
            ),
            ElevatedButton(
              onPressed: () => Navigator.of(context).pop(true),
              child: const Text('Register'),
            ),
          ],
        );
      },
    );

    if (shouldRegister == true) {
      print(
        '✅ BluetoothScanWidget: User confirmed registration for: $deviceName',
      );
      await _registerDevice(device);
    } else {
      print(
        '❌ BluetoothScanWidget: User cancelled registration for: $deviceName',
      );
    }
  }

  Future<void> _registerDevice(BluetoothDevice device) async {
    final deviceName = _getDeviceDisplayName(device);
    print(
      '🚀 BluetoothScanWidget: Starting device registration for: $deviceName (${device.address})',
    );

    // Mark device as being registered
    setState(() {
      _registeringDevices.add(device.address);
    });

    try {
      // Get user ID from PostgreAuth service
      final auth = PostgreAuth();
      final currentUser = auth.currentUser;

      if (currentUser == null) {
        throw Exception('User not authenticated. Please login first.');
      }

      final userId = currentUser['id'];
      print('📤 BluetoothScanWidget: Using user ID: $userId');

      final mac = device.address;
      final name = deviceName;

      final payload = {
        "mac_address": mac,
        "name": name,
        "owner_id": userId,
        "owner_name": currentUser['full_name'] ?? "Test Owner",
        "owner_phone": currentUser['phone_number'] ?? "+265991234567",
        "owner_address": "Malawi",
        "is_active": true,
      };

      print('📤 BluetoothScanWidget: Sending registration request...');
      print('📤 BluetoothScanWidget: Base URL: $_baseUrl');
      print('📤 BluetoothScanWidget: Payload: $payload');

      // Prepare headers with authentication
      final headers = {'Content-Type': 'application/json'};

      // Add authentication header if available
      // For Django, we might need to use session-based auth or token auth
      // Check if we have any authentication token or session info
      if (currentUser.containsKey('token')) {
        headers['Authorization'] = 'Token ${currentUser['token']}';
        print('📤 BluetoothScanWidget: Using token authentication');
      } else if (currentUser.containsKey('session_id')) {
        headers['Cookie'] = 'sessionid=${currentUser['session_id']}';
        print('📤 BluetoothScanWidget: Using session authentication');
      } else {
        print(
          '⚠️ BluetoothScanWidget: No authentication token found, proceeding without auth header',
        );
      }

      print('📤 BluetoothScanWidget: Request headers: $headers');

      // Use the configurable base URL
      final uri = Uri.parse('$_baseUrl/api/devices/register/');
      final response = await http.post(
        uri,
        headers: headers,
        body: jsonEncode(payload),
      );

      print(
        '📥 BluetoothScanWidget: Registration response status: ${response.statusCode}',
      );
      print(
        '📥 BluetoothScanWidget: Registration response body: ${response.body}',
      );

      if (response.statusCode == 201) {
        // Success - device registered
        print(
          '✅ BluetoothScanWidget: Device registered successfully: $deviceName',
        );
        if (mounted) {
          setState(() {
            _registeredDevices.add(device.address);
            _registeringDevices.remove(device.address);
          });
          ScaffoldMessenger.of(context).showSnackBar(
            SnackBar(
              content: Text('✅ Device registered successfully: $deviceName'),
              backgroundColor: Colors.green,
              duration: const Duration(seconds: 3),
            ),
          );
        }
        return;
      } else if (response.statusCode == 400 &&
          response.body.contains('unique')) {
        // Device already registered
        print('⚠️ BluetoothScanWidget: Device already registered: $deviceName');
        if (mounted) {
          setState(() {
            _registeredDevices.add(device.address);
            _registeringDevices.remove(device.address);
          });
          ScaffoldMessenger.of(context).showSnackBar(
            SnackBar(
              content: Text('⚠️ Device already registered: $deviceName'),
              backgroundColor: Colors.orange,
              duration: const Duration(seconds: 3),
            ),
          );
        }
        return;
      } else {
        throw Exception('HTTP ${response.statusCode}: ${response.body}');
      }
    } catch (e) {
      print('❌ BluetoothScanWidget: Registration failed for $deviceName: $e');
      if (mounted) {
        setState(() {
          _registeringDevices.remove(device.address);
        });

        String errorMessage = 'Registration failed: ';
        if (e.toString().contains('User not authenticated')) {
          errorMessage += 'Please login first to register devices.';
        } else if (e.toString().contains('SocketException') ||
            e.toString().contains('Connection refused')) {
          errorMessage +=
              'Unable to connect to server. Please check your connection.';
        } else if (e.toString().contains('TimeoutException')) {
          errorMessage += 'Request timed out. Please try again.';
        } else if (e.toString().contains('403') ||
            e.toString().contains('401')) {
          errorMessage += 'Authentication failed. Please login again.';
        } else {
          errorMessage += e.toString();
        }

        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(
            content: Text('❌ $errorMessage'),
            backgroundColor: Colors.red,
            duration: const Duration(seconds: 5),
            action: SnackBarAction(
              label: 'Retry',
              textColor: Colors.white,
              onPressed: () => _registerDevice(device),
            ),
          ),
        );
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

  @override
  void dispose() {
    print('🔧 BluetoothScanWidget: Disposing...');
    // Cancel all subscriptions and timers
    _scanTimer?.cancel();
    _adapterSubscription?.cancel();
    _scanSubscription?.cancel();

    // Stop scanning if in progress
    if (_scanning) {
      print('🔍 BluetoothScanWidget: Stopping scan on dispose...');
      _bt.stopScan();
    }

    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    // Remove Scaffold and return the content directly
    return SizedBox(
      height: widget.height ?? 600, // Always provide a default height
      child: Column(
        mainAxisSize:
            MainAxisSize.min, // Important: don't take all available space
        children: [
          // Header with scan button and Bluetooth status
          Padding(
            padding: const EdgeInsets.all(16.0),
            child: Column(
              children: [
                // Bluetooth status indicator
                Container(
                  width: double.infinity,
                  padding: const EdgeInsets.all(12.0),
                  decoration: BoxDecoration(
                    color:
                        _bluetoothState == BluetoothAdapterState.on
                            ? Colors.green.shade50
                            : Colors.red.shade50,
                    border: Border.all(
                      color:
                          _bluetoothState == BluetoothAdapterState.on
                              ? Colors.green
                              : Colors.red,
                    ),
                    borderRadius: BorderRadius.circular(8),
                  ),
                  child: Row(
                    children: [
                      Icon(
                        _bluetoothState == BluetoothAdapterState.on
                            ? Icons.bluetooth
                            : Icons.bluetooth_disabled,
                        color:
                            _bluetoothState == BluetoothAdapterState.on
                                ? Colors.green.shade700
                                : Colors.red.shade700,
                      ),
                      const SizedBox(width: 8),
                      Text(
                        _bluetoothState == BluetoothAdapterState.on
                            ? 'Bluetooth is ON'
                            : _bluetoothState == BluetoothAdapterState.off
                            ? 'Bluetooth is OFF'
                            : 'Bluetooth status unknown',
                        style: TextStyle(
                          color:
                              _bluetoothState == BluetoothAdapterState.on
                                  ? Colors.green.shade700
                                  : Colors.red.shade700,
                          fontWeight: FontWeight.w500,
                        ),
                      ),
                    ],
                  ),
                ),
                const SizedBox(height: 16),
                // Scan button
                Row(
                  children: [
                    Expanded(
                      child: ElevatedButton.icon(
                        onPressed: _scanning ? _stopScan : _scan,
                        icon: Icon(_scanning ? Icons.stop : Icons.search),
                        label: Text(_scanning ? "Stop Scanning" : "Start Scan"),
                      ),
                    ),
                    const SizedBox(width: 16),
                    if (_scanning)
                      Column(
                        children: [
                          const SizedBox(
                            width: 20,
                            height: 20,
                            child: CircularProgressIndicator(strokeWidth: 2),
                          ),
                          const SizedBox(height: 4),
                          Text(
                            'Scanning...',
                            style: Theme.of(context).textTheme.bodySmall,
                          ),
                        ],
                      ),
                  ],
                ),
              ],
            ),
          ),

          // Device list - wrap in Flexible instead of Expanded to prevent overflow
          Flexible(
            child:
                _devices.isEmpty
                    ? Center(
                      child: Padding(
                        padding: const EdgeInsets.all(16.0),
                        child: Column(
                          mainAxisAlignment: MainAxisAlignment.center,
                          children: [
                            Icon(
                              _scanning
                                  ? Icons.search
                                  : Icons.bluetooth_searching,
                              size: 48,
                              color: Colors.grey.shade400,
                            ),
                            const SizedBox(height: 16),
                            Text(
                              _scanning
                                  ? 'Scanning for devices...'
                                  : 'No devices found. Tap "Start Scan" to search.',
                              style: Theme.of(context).textTheme.bodyLarge,
                              textAlign: TextAlign.center,
                            ),
                          ],
                        ),
                      ),
                    )
                    : ListView.builder(
                      shrinkWrap:
                          true, // Important: don't expand to fill available space
                      itemCount: _devices.length,
                      itemBuilder: (context, index) {
                        final device = _devices[index];
                        final isRegistered = _registeredDevices.contains(
                          device.address,
                        );
                        final isRegistering = _registeringDevices.contains(
                          device.address,
                        );

                        return Card(
                          margin: const EdgeInsets.symmetric(
                            horizontal: 16,
                            vertical: 4,
                          ),
                          child: ListTile(
                            leading: _buildDeviceIcon(
                              isRegistered,
                              isRegistering,
                            ),
                            title: Text(
                              _getDeviceDisplayName(device),
                              style: TextStyle(
                                fontWeight:
                                    isRegistered
                                        ? FontWeight.bold
                                        : FontWeight.normal,
                              ),
                            ),
                            subtitle: Column(
                              crossAxisAlignment: CrossAxisAlignment.start,
                              children: [
                                Text(
                                  'Address: ${device.address}',
                                  style: TextStyle(color: Colors.grey.shade600),
                                ),
                                if (isRegistered)
                                  Text(
                                    'Registered',
                                    style: TextStyle(
                                      color: Colors.green.shade700,
                                      fontWeight: FontWeight.w500,
                                    ),
                                  )
                                else if (isRegistering)
                                  Text(
                                    'Registering...',
                                    style: TextStyle(
                                      color: Colors.orange.shade700,
                                      fontWeight: FontWeight.w500,
                                    ),
                                  ),
                              ],
                            ),
                            trailing: _buildTrailingWidget(
                              isRegistered,
                              isRegistering,
                            ),
                            onTap:
                                (isRegistered || isRegistering)
                                    ? null
                                    : () => _promptRegisterDevice(device),
                          ),
                        );
                      },
                    ),
          ),
        ],
      ),
    );
  }

  Widget _buildDeviceIcon(bool isRegistered, bool isRegistering) {
    if (isRegistering) {
      return SizedBox(
        width: 24,
        height: 24,
        child: CircularProgressIndicator(
          strokeWidth: 2,
          valueColor: AlwaysStoppedAnimation<Color>(Colors.orange.shade700),
        ),
      );
    } else if (isRegistered) {
      return Icon(Icons.check_circle, color: Colors.green);
    } else {
      return Icon(Icons.bluetooth, color: Colors.blue);
    }
  }

  Widget _buildTrailingWidget(bool isRegistered, bool isRegistering) {
    if (isRegistering) {
      return SizedBox(
        width: 24,
        height: 24,
        child: CircularProgressIndicator(
          strokeWidth: 2,
          valueColor: AlwaysStoppedAnimation<Color>(Colors.orange.shade700),
        ),
      );
    } else if (isRegistered) {
      return const Icon(Icons.check_circle, color: Colors.green);
    } else {
      return const Icon(Icons.add_circle_outline);
    }
  }
}
