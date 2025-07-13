import 'package:flutter/material.dart';
import 'package:my_guardian/widgets/logoutTile.dart';
import 'package:my_guardian/widgets/profileHeaderWidget.dart';
import 'package:my_guardian/widgets/settingsHeader.dart';
import 'package:my_guardian/widgets/settingsTile.dart';
import 'package:my_guardian/widgets/registeredDeviceWidget.dart';
import 'package:my_guardian/widgets/emergencyContactsWidget.dart';
import 'package:my_guardian/widgets/tipsTile.dart';

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
  final bool _autoSyncEnabled = true;

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: Colors.white,
      body: SingleChildScrollView(
        child: Column(
          children: [
            const ProfileHeaderWidget(margin: EdgeInsets.all(0)),
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

            TipsTile(),
            // Logout tile
            LogoutTile(),

            const SizedBox(height: 20),

            // Registered device widget
            RegisteredDeviceTile(),
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
