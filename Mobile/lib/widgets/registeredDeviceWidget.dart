import 'package:flutter/material.dart';
import 'package:my_guardian/services/db_controller.dart';
import 'package:my_guardian/services/postgre_auth.dart';
import 'package:my_guardian/widgets/settingsHeader.dart';
import 'package:postgres/postgres.dart';

class RegisteredDeviceTile extends StatefulWidget {
  const RegisteredDeviceTile({super.key});

  @override
  State<RegisteredDeviceTile> createState() => _RegisteredDeviceTileState();
}

class _RegisteredDeviceTileState extends State<RegisteredDeviceTile> {
  String? _deviceName;
  String? _macAddress;
  bool _loading = true;

  @override
  void initState() {
    super.initState();
    _fetchDevice();
  }

  Future<void> _fetchDevice() async {
    try {
      final auth = PostgreAuth();
      final currentUser = auth.currentUser;
      if (currentUser == null) {
        throw Exception('User not authenticated');
      }

      await DBService().connect(); // Ensures cached singleton connection

      final result = await DBService().conn.execute(
        Sql.named(
          'SELECT device_type, mac_address FROM devices WHERE owner_id = @owner LIMIT 1',
        ),
        parameters: {'owner': currentUser['id']},
      );

      print('📦 Device query result: $result');

      if (mounted) {
        setState(() {
          if (result.isNotEmpty) {
            _deviceName = result[0].toColumnMap()['device_type'];
            _macAddress = result[0].toColumnMap()['mac_address'];
          }
          _loading = false;
        });
      }
    } catch (e) {
      print('Device fetch error: $e');
      if (mounted) setState(() => _loading = false);
    }
  }

  @override
  Widget build(BuildContext context) {
    return _loading
        ? const Padding(
          padding: EdgeInsets.all(16),
          child: Center(child: CircularProgressIndicator()),
        )
        : Column(
          children: [
            const SettingsHeader(title: "Registered Device"),
            _macAddress == null
                ? ListTile(
                  leading: const Icon(Icons.bluetooth),
                  title: Text(
                    "No registered device Found!",
                    style: const TextStyle(
                      fontWeight: FontWeight.bold,
                      color: Colors.red,
                    ),
                  ),
                  subtitle: Text(
                    "Proceed to Register new device ->",
                    style: const TextStyle(color: Colors.grey),
                  ),

                  trailing: Column(
                    children: [
                      ElevatedButton.icon(
                        icon: const Icon(Icons.arrow_forward),
                        label: const Text("Register Device"),
                        onPressed: () {
                          Navigator.of(context).pushNamed('/scan_device');
                        },
                      ),
                      ElevatedButton.icon(
                        icon: const Icon(Icons.refresh),
                        label: const Text("Refresh"),
                        onPressed: _fetchDevice,
                      ),
                    ],
                  ),
                )
                // ? Column(
                //   children: [
                //     const Icon(
                //       Icons.info_outline,
                //       size: 40,
                //       color: Colors.grey,
                //     ),
                //     const SizedBox(height: 10),
                //     const Text("No device registered."),
                //     const SizedBox(height: 10),
                //     const ElevatedButton.icon(
                //     icon: const Icon(Icons.arrow_forward),
                //     label: const Text("Change"),
                //     onPressed: () {
                //       Navigator.of(context).pushNamed('/scan_device');
                //     },
                //   ),
                //     ElevatedButton.icon(
                //       icon: const Icon(Icons.refresh),
                //       label: const Text("Try Again"),
                //       onPressed: _fetchDevice,
                //     ),
                //   ],
                // )
                : ListTile(
                  leading: const Icon(Icons.bluetooth),
                  title: Text(
                    _deviceName ?? "Unknown device",
                    style: const TextStyle(fontWeight: FontWeight.bold),
                  ),
                  subtitle: Text(
                    _macAddress!,
                    style: const TextStyle(color: Colors.black),
                  ),
                  trailing: ElevatedButton.icon(
                    icon: const Icon(Icons.arrow_forward),
                    label: const Text("Change"),
                    onPressed: () {
                      Navigator.of(context).pushNamed('/scan_device');
                    },
                  ),
                ),
          ],
        );
  }
}
