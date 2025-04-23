import 'package:flutter/material.dart';

class SettingsScreen extends StatefulWidget {
  const SettingsScreen({super.key});

  @override
  State<SettingsScreen> createState() => _SettingsScreenState();
}

class _SettingsScreenState extends State<SettingsScreen> {
  bool _notificationsEnabled = true;
  bool _darkMode = false;
  String _selectedLanguage = "English";
  final bool _bridgeConnected = true;
  final String _firmwareVersion = "v1.2.3";
  bool _autoSyncEnabled = true;

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: Colors.grey[300],
      appBar: AppBar(
        backgroundColor: Colors.green,
        title: const Text(
            "Settings",
            style: TextStyle(color: Colors.white),
            ),
        centerTitle: true,
      ),
      body: SingleChildScrollView(
        child: Column(
          children: [
            SizedBox(
              width: double.infinity,
              height: 270,
              child: Image.asset(
                "assets/images/settings.png",
                fit: BoxFit.contain,
              ),
            ),
            const SizedBox(height: 20),
            const SettingsHeader(title: "User Settings"),
            SettingsTile(
              icon: Icons.notifications,
              title: "Notifications",
              trailing: Switch(
                activeTrackColor: Colors.green,inactiveTrackColor: Colors.green[50],
                value: _notificationsEnabled,
                onChanged: (value) {
                  setState(() {
                    _notificationsEnabled = value;
                  });
                },
              ),
            ),
            SettingsTile(
              icon: Icons.dark_mode,
              title: "Dark Mode",
              trailing: Switch(
                activeTrackColor: Colors.green,inactiveTrackColor: Colors.green[50],
                value: _darkMode,
                onChanged: (value) {
                  setState(() {
                    _darkMode = value;
                  });
                },
              ),
            ),
            SettingsTile(
              icon: Icons.language,
              title: "Language",
              trailing: DropdownButton<String>(
                value: _selectedLanguage,
                onChanged: (String? newValue) {
                  setState(() {
                    _selectedLanguage = newValue!;
                  });
                },
                items: ["English", "Chichewa", "Tumbuka"]
                    .map<DropdownMenuItem<String>>((String value) {
                  return DropdownMenuItem<String>(
                    value: value,
                    child: Text(value),
                  );
                }).toList(),
              ),
            ),
            const SizedBox(height: 20),
            const SettingsHeader(title: "Bridge State Settings"),
            SettingsTile(
              icon: Icons.wifi,
              title: "Connection Status",
              trailing: Text(
                _bridgeConnected ? "Connected" : "Disconnected",
                style: TextStyle(
                  fontWeight: FontWeight.bold,
                  color: _bridgeConnected ? Colors.green : Colors.red,
                ),
              ),
            ),
            SettingsTile(
              icon: Icons.system_update,
              title: "Firmware Version",
              trailing: Text(_firmwareVersion, style: const TextStyle(fontWeight: FontWeight.bold)),
            ),
            SettingsTile(
              icon: Icons.sync,
              title: "Auto Sync",
              trailing: Switch(
                activeTrackColor: Colors.green,inactiveTrackColor: Colors.green[50],
                value: _autoSyncEnabled,
                onChanged: (value) {
                  setState(() {
                    _autoSyncEnabled = value;
                  });
                },
              ),
            ),
            const SizedBox(height: 20),
          ],
        ),
      ),
    );
  }
}

class SettingsHeader extends StatelessWidget {
  final String title;
  const SettingsHeader({required this.title, super.key});

  @override
  Widget build(BuildContext context) {
    return Padding(
      padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 8),
      child: Align(
        alignment: Alignment.centerLeft,
        child: Text(
          title,
          style: const TextStyle(fontSize: 18, fontWeight: FontWeight.bold, color: Colors.blueGrey),
        ),
      ),
    );
  }
}

// General Settings Tile
class SettingsTile extends StatelessWidget {
  final IconData icon;
  final String title;
  final Widget trailing;

  const SettingsTile({required this.icon, required this.title, required this.trailing, super.key});

  @override
  Widget build(BuildContext context) {
    return Container(
      margin: const EdgeInsets.symmetric(horizontal: 16, vertical: 5),
      padding: const EdgeInsets.all(12),
      decoration: BoxDecoration(
        color: Colors.grey[100],
        borderRadius: BorderRadius.circular(10),
        border: Border.all(color: Colors.white),
      ),
      child: Row(
        children: [
          Icon(icon, color: Colors.green),
          const SizedBox(width: 10),
          Expanded(
            child: Text(title, style: const TextStyle(fontSize: 16, fontWeight: FontWeight.bold)),
          ),
          trailing,
        ],
      ),
    );
  }
}
