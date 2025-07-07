import 'package:flutter/material.dart';
import 'package:my_guardian/controllers/db_controller.dart';
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
            ListTile(
              leading: const Icon(Icons.bluetooth),
              title: Text(
                _deviceName ?? "No registered device",
                style: const TextStyle(fontWeight: FontWeight.bold),
              ),
              subtitle: Text(
                _macAddress ?? "Please scan and register a device",
                style: TextStyle(
                  color:
                      _macAddress != null ? Colors.black : Colors.red.shade600,
                ),
              ),
              trailing: ElevatedButton.icon(
                icon: const Icon(Icons.arrow_forward),
                label: Text(_macAddress == null ? "Scan" : "Change"),
                onPressed: () {
                  Navigator.of(context).pushNamed('/scan_device');
                },
              ),
            ),
          ],
        );
  }
}
