import 'package:flutter/material.dart';
import 'package:my_guardian/widgets/logoutTile.dart';
import 'package:my_guardian/widgets/settingsHeader.dart';
import 'package:my_guardian/widgets/settingsTile.dart';
import 'package:my_guardian/widgets/registeredDeviceWidget.dart';
import 'package:my_guardian/widgets/emergencyContactsWidget.dart';

class SettingsScreen extends StatefulWidget {
  const SettingsScreen({super.key});

  @override
  State<SettingsScreen> createState() => _SettingsScreenState();
}

class _SettingsScreenState extends State<SettingsScreen> {
  bool _notificationsEnabled = true;
  bool _darkMode = false;
  String _selectedLanguage = "English";
  final String _firmwareVersion = "v1.2.3";
  bool _autoSyncEnabled = true;

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: Colors.white,
      // appBar: AppBar(
      //   backgroundColor: Colors.green,
      //   title: const Text("Settings", style: TextStyle(color: Colors.white)),
      //   centerTitle: true,
      // ),
      body: SingleChildScrollView(
        child: Column(
          children: [
            // Header image
            SizedBox(
              width: double.infinity,
              height: 270,
              child: Image.asset(
                "assets/images/settings.png",
                fit: BoxFit.contain,
              ),
            ),
            const SizedBox(height: 20),

            // User Settings Section
            const SettingsHeader(title: "User Settings"),
            SettingsTile(
              icon: Icons.notifications,
              title: "Notifications",
              trailing: Switch(
                activeTrackColor: Colors.green,
                inactiveTrackColor: Colors.green[50],
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
                activeTrackColor: Colors.green,
                inactiveTrackColor: Colors.green[50],
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
                items:
                    [
                      "English",
                      "Chichewa",
                      "Tumbuka",
                    ].map<DropdownMenuItem<String>>((String value) {
                      return DropdownMenuItem<String>(
                        value: value,
                        child: Text(value),
                      );
                    }).toList(),
              ),
            ),

            // Logout tile
            LogoutTile(),
            const SizedBox(height: 20),

            // Registered device widget
            RegisteredDeviceTile(),
            const SizedBox(height: 20),

            // Device Settings Section
            const SettingsHeader(title: "Device Settings"),
            SettingsTile(
              icon: Icons.system_update,
              title: "Firmware Version",
              trailing: Text(
                _firmwareVersion,
                style: const TextStyle(fontWeight: FontWeight.bold),
              ),
            ),
            SettingsTile(
              icon: Icons.sync,
              title: "Auto Sync",
              trailing: Switch(
                activeTrackColor: Colors.green,
                inactiveTrackColor: Colors.green[50],
                value: _autoSyncEnabled,
                onChanged: (value) {
                  setState(() {
                    _autoSyncEnabled = value;
                  });
                },
              ),
            ),
            const SizedBox(height: 20),

            // Emergency Contacts Section (using the new widget)
            const EmergencyContactsWidget(),
            const SizedBox(height: 20),
          ],
        ),
      ),
    );
  }
}
