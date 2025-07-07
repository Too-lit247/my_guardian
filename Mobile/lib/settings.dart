import 'package:flutter/material.dart';
import 'package:flutter_contacts/flutter_contacts.dart';
import 'package:my_guardian/widgets/bluetoothScanWidget.dart';
import 'package:my_guardian/widgets/settingsHeader.dart';
import 'package:my_guardian/widgets/settingsTile.dart';
import 'package:permission_handler/permission_handler.dart';

// Import your PostgreSQL services
import 'package:my_guardian/services/emergency_contact_service.dart';
import 'package:my_guardian/services/postgre_auth.dart';

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

  PermissionStatus? _contactPermissionStatus;

  final PostgreAuth _auth = PostgreAuth(); // Get the singleton instance
  late EmergencyContactService _emergencyContactService;

  List<EmergencyContact> _emergencyContacts = [];
  bool _isLoadingContacts = false;
  String? _contactsErrorMessage;

  @override
  void initState() {
    super.initState();
    _checkContactPermission();
    _initializeServices(); // Initialize services here
  }

  Future<void> _initializeServices() async {
    // It's assumed that PostgreAuth().initialize() is called in main.dart
    // and the connection is already open when SettingsScreen is built.
    // However, we still need to check the connection state before using it.

    // If the connection is not yet initialized or is closed, attempt to (re)initialize PostgreAuth.
    // This is a safety measure. The primary initialization should be in main.dart.
    try {
      // Check if the connection property is ready and open.
      // If _auth.connection itself throws (because _conn isn't initialized yet),
      // or if _auth.connection.isClosed is true, then we need to re-initialize.
      // A more robust check might be `if (!_auth.isAuthenticated || _auth.connection.isClosed)`
      // given that `_auth.initialize` also loads the user.
      if (!_auth.isAuthenticated) {
        print(
          'PostgreAuth connection not ready or closed. Attempting to initialize...',
        );
        await _auth.initialize(); // This will connect if not already connected
        print('PostgreAuth connection (re)initialized successfully.');
      }

      // Now that we're sure the connection is available, create the service
      _emergencyContactService = EmergencyContactService(
        _auth.connection,
        _auth,
      );
      _fetchEmergencyContacts(); // Fetch contacts once services are ready
    } catch (e) {
      print('Failed to initialize EmergencyContactService: $e');
      setState(() {
        _contactsErrorMessage =
            'Failed to connect to database for contacts: $e';
        _isLoadingContacts = false;
      });
    }
  }

  Future<void> _checkContactPermission() async {
    final status = await Permission.contacts.status;
    setState(() {
      _contactPermissionStatus = status;
    });
  }

  void _showEmergencyContactOptions() {
    showModalBottomSheet(
      context: context,
      builder: (_) {
        return Column(
          mainAxisSize: MainAxisSize.min,
          children: [
            ListTile(
              leading: const Icon(Icons.contacts),
              title: const Text("Choose from Contacts"),
              onTap: () async {
                Navigator.pop(context);
                await _pickContactFromPhone();
              },
            ),
            ListTile(
              leading: const Icon(Icons.person_add),
              title: const Text("Enter Manually"),
              onTap: () {
                Navigator.pop(context);
                _showManualContactDialog();
              },
            ),
          ],
        );
      },
    );
  }

  Future<void> _pickContactFromPhone() async {
    await _checkContactPermission();

    if (_contactPermissionStatus!.isGranted) {
      try {
        final contact = await FlutterContacts.openExternalPick();
        if (contact != null && contact.phones.isNotEmpty) {
          final name = contact.displayName;
          final phone = contact.phones.first.number;
          await _saveEmergencyContact(name, phone, 'Friend', 'Call');
        }
      } catch (e) {
        ScaffoldMessenger.of(
          context,
        ).showSnackBar(SnackBar(content: Text("Failed to pick contact: $e")));
      }
    } else {
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(
          content: Text("Contacts permission is required"),
          action: SnackBarAction(label: "Settings", onPressed: openAppSettings),
        ),
      );
    }
  }

  void _showManualContactDialog() {
    final nameController = TextEditingController();
    final phoneController = TextEditingController();
    final relationController = TextEditingController();
    String? selectedPreferredMethod = 'Call';

    showDialog(
      context: context,
      builder: (_) {
        return AlertDialog(
          title: const Text("Enter Contact"),
          content: SingleChildScrollView(
            child: Column(
              mainAxisSize: MainAxisSize.min,
              children: [
                TextField(
                  controller: nameController,
                  decoration: const InputDecoration(labelText: "Name"),
                ),
                TextField(
                  controller: phoneController,
                  decoration: const InputDecoration(labelText: "Phone"),
                  keyboardType: TextInputType.phone,
                ),
                TextField(
                  controller: relationController,
                  decoration: const InputDecoration(
                    labelText: "Relation (e.g., Parent, Friend)",
                  ),
                ),
                DropdownButtonFormField<String>(
                  value: selectedPreferredMethod,
                  decoration: const InputDecoration(
                    labelText: "Preferred Method",
                  ),
                  items:
                      <String>['Call', 'SMS'].map((String value) {
                        return DropdownMenuItem<String>(
                          value: value,
                          child: Text(value),
                        );
                      }).toList(),
                  onChanged: (String? newValue) {
                    setState(() {
                      selectedPreferredMethod = newValue;
                    });
                  },
                ),
              ],
            ),
          ),
          actions: [
            TextButton(
              onPressed: () => Navigator.pop(context),
              child: const Text("Cancel"),
            ),
            ElevatedButton(
              onPressed: () async {
                final name = nameController.text.trim();
                final phone = phoneController.text.trim();
                final relation = relationController.text.trim();

                if (name.isNotEmpty &&
                    phone.isNotEmpty &&
                    relation.isNotEmpty &&
                    selectedPreferredMethod != null) {
                  Navigator.pop(context);
                  await _saveEmergencyContact(
                    name,
                    phone,
                    relation,
                    selectedPreferredMethod!,
                  );
                } else {
                  ScaffoldMessenger.of(context).showSnackBar(
                    const SnackBar(content: Text("Please fill all fields.")),
                  );
                }
              },
              child: const Text("Save"),
            ),
          ],
        );
      },
    );
  }

  Future<void> _saveEmergencyContact(
    String name,
    String phoneNumber,
    String relation,
    String preferredMethod,
  ) async {
    // Check if the service is initialized and user is authenticated
    if (!_auth.isAuthenticated || !(_auth.connection.isOpen)) {
      // Use .isOpen now
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(
          content: Text("User not logged in or database not connected."),
        ),
      );
      return;
    }

    try {
      await _emergencyContactService.createContact(
        name: name,
        phoneNumber: phoneNumber,
        relation: relation,
        preferredMethod: preferredMethod,
      );
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(content: Text("Emergency contact saved successfully!")),
      );
      _fetchEmergencyContacts();
    } catch (e) {
      ScaffoldMessenger.of(
        context,
      ).showSnackBar(SnackBar(content: Text("Failed to save contact: $e")));
    }
  }

  Future<void> _fetchEmergencyContacts() async {
    // Check if the service is initialized and user is authenticated
    if (!_auth.isAuthenticated || !(_auth.connection.isOpen)) {
      // Use .isOpen now
      setState(() {
        _contactsErrorMessage = "User not logged in or database not connected.";
        _isLoadingContacts = false;
      });
      return;
    }

    setState(() {
      _isLoadingContacts = true;
      _contactsErrorMessage = null;
    });
    try {
      final contacts =
          await _emergencyContactService.getContactsForCurrentUser();
      setState(() {
        _emergencyContacts = contacts;
        _isLoadingContacts = false;
      });
    } catch (e) {
      setState(() {
        _contactsErrorMessage = "Failed to load contacts: $e";
        _isLoadingContacts = false;
      });
      ScaffoldMessenger.of(
        context,
      ).showSnackBar(SnackBar(content: Text("Error loading contacts: $e")));
    }
  }

  Future<void> _deleteContact(String contactId) async {
    // Check if the service is initialized and user is authenticated
    if (!_auth.isAuthenticated || !(_auth.connection.isOpen)) {
      // Use .isOpen now
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(
          content: Text("User not logged in or database not connected."),
        ),
      );
      return;
    }

    try {
      await _emergencyContactService.deleteContact(contactId: contactId);
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(content: Text("Contact deleted successfully!")),
      );
      _fetchEmergencyContacts();
    } catch (e) {
      ScaffoldMessenger.of(
        context,
      ).showSnackBar(SnackBar(content: Text("Failed to delete contact: $e")));
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: Colors.white,
      appBar: AppBar(
        backgroundColor: Colors.green,
        title: const Text("Settings", style: TextStyle(color: Colors.white)),
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

            //const BluetoothScanWidget(),
            const SizedBox(height: 20),
            const SettingsHeader(title: "Emergency Contact"),
            SettingsTile(
              icon: Icons.contact_phone,
              title: "Manage Emergency Contact",
              trailing: ElevatedButton(
                style: ElevatedButton.styleFrom(
                  backgroundColor: Colors.green,
                  foregroundColor: Colors.white,
                  padding: const EdgeInsets.symmetric(horizontal: 10),
                ),
                onPressed: _showEmergencyContactOptions,
                child: const Text("Add"),
              ),
            ),
            if (_contactPermissionStatus != null)
              Padding(
                padding: const EdgeInsets.symmetric(
                  horizontal: 16.0,
                  vertical: 4,
                ),
                child: Row(
                  children: [
                    const Icon(Icons.privacy_tip, color: Colors.green),
                    const SizedBox(width: 8),
                    Text(
                      "Contact Permission: ${_contactPermissionStatus!.isGranted
                          ? "Granted"
                          : _contactPermissionStatus!.isDenied
                          ? "Denied"
                          : "Restricted"}",
                      style: const TextStyle(fontSize: 14),
                    ),
                  ],
                ),
              ),
            const SizedBox(height: 20),

            // Displaying Emergency Contacts
            if (_isLoadingContacts)
              const CircularProgressIndicator()
            else if (_contactsErrorMessage != null)
              Padding(
                padding: const EdgeInsets.all(16.0),
                child: Text(
                  _contactsErrorMessage!,
                  style: const TextStyle(color: Colors.red),
                ),
              )
            else if (_emergencyContacts.isEmpty)
              const Padding(
                padding: EdgeInsets.all(16),
                child: Text("No emergency contacts added."),
              )
            else
              ListView.builder(
                shrinkWrap: true,
                physics: const NeverScrollableScrollPhysics(),
                itemCount: _emergencyContacts.length,
                itemBuilder: (context, index) {
                  final contact = _emergencyContacts[index];
                  return SettingsTile(
                    icon: Icons.person,
                    title: contact.name,
                    subtitle: Text(contact.phoneNumber),
                    trailing: IconButton(
                      icon: const Icon(Icons.delete, color: Colors.red),
                      onPressed: () => _deleteContact(contact.contactId),
                    ),
                  );
                },
              ),
          ],
        ),
      ),
    );
  }
}
