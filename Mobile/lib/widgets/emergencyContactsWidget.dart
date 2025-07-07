import 'package:flutter/material.dart';
import 'package:flutter_contacts/flutter_contacts.dart';
import 'package:my_guardian/widgets/settingsHeader.dart';
import 'package:my_guardian/widgets/settingsTile.dart';
import 'package:permission_handler/permission_handler.dart';
import 'package:my_guardian/services/emergency_contact_service.dart';
import 'package:my_guardian/services/postgre_auth.dart';

class EmergencyContactsWidget extends StatefulWidget {
  const EmergencyContactsWidget({super.key});

  @override
  State<EmergencyContactsWidget> createState() =>
      _EmergencyContactsWidgetState();
}

class _EmergencyContactsWidgetState extends State<EmergencyContactsWidget> {
  final PostgreAuth _auth = PostgreAuth();
  late EmergencyContactService _emergencyContactService;

  List<EmergencyContact> _emergencyContacts = [];
  bool _isLoadingContacts = false;
  String? _contactsErrorMessage;
  PermissionStatus? _contactPermissionStatus;
  bool _isInitialized = false;

  @override
  void initState() {
    super.initState();
    _initializeServices();
    _checkContactPermission();
  }

  Future<void> _initializeServices() async {
    try {
      if (!_auth.isAuthenticated) {
        await _auth.initialize();
      }

      _emergencyContactService = EmergencyContactService(
        _auth.connection,
        _auth,
      );

      setState(() {
        _isInitialized = true;
      });

      await _fetchEmergencyContacts();
    } catch (e) {
      setState(() {
        _contactsErrorMessage =
            'Failed to connect to database for contacts: $e';
        _isLoadingContacts = false;
        _isInitialized = false;
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
        if (mounted) {
          ScaffoldMessenger.of(
            context,
          ).showSnackBar(SnackBar(content: Text("Failed to pick contact: $e")));
        }
      }
    } else {
      if (mounted) {
        ScaffoldMessenger.of(context).showSnackBar(
          const SnackBar(
            content: Text("Contacts permission is required"),
            action: SnackBarAction(
              label: "Settings",
              onPressed: openAppSettings,
            ),
          ),
        );
      }
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
        return StatefulBuilder(
          builder: (context, setDialogState) {
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
                    const SizedBox(height: 16),
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
                        setDialogState(() {
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
                        const SnackBar(
                          content: Text("Please fill all fields."),
                        ),
                      );
                    }
                  },
                  child: const Text("Save"),
                ),
              ],
            );
          },
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
    if (!_isInitialized || !_auth.isAuthenticated || !_auth.connection.isOpen) {
      if (mounted) {
        ScaffoldMessenger.of(context).showSnackBar(
          const SnackBar(
            content: Text("User not logged in or database not connected."),
          ),
        );
      }
      return;
    }

    try {
      await _emergencyContactService.createContact(
        name: name,
        phoneNumber: phoneNumber,
        relation: relation,
        preferredMethod: preferredMethod,
      );

      if (mounted) {
        ScaffoldMessenger.of(context).showSnackBar(
          const SnackBar(
            content: Text("Emergency contact saved successfully!"),
          ),
        );
      }

      await _fetchEmergencyContacts();
    } catch (e) {
      if (mounted) {
        ScaffoldMessenger.of(
          context,
        ).showSnackBar(SnackBar(content: Text("Failed to save contact: $e")));
      }
    }
  }

  Future<void> _fetchEmergencyContacts() async {
    if (!_isInitialized || !_auth.isAuthenticated || !_auth.connection.isOpen) {
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

      if (mounted) {
        ScaffoldMessenger.of(
          context,
        ).showSnackBar(SnackBar(content: Text("Error loading contacts: $e")));
      }
    }
  }

  Future<void> _deleteContact(String contactId) async {
    if (!_isInitialized || !_auth.isAuthenticated || !_auth.connection.isOpen) {
      if (mounted) {
        ScaffoldMessenger.of(context).showSnackBar(
          const SnackBar(
            content: Text("User not logged in or database not connected."),
          ),
        );
      }
      return;
    }

    try {
      await _emergencyContactService.deleteContact(contactId: contactId);

      if (mounted) {
        ScaffoldMessenger.of(context).showSnackBar(
          const SnackBar(content: Text("Contact deleted successfully!")),
        );
      }

      await _fetchEmergencyContacts();
    } catch (e) {
      if (mounted) {
        ScaffoldMessenger.of(
          context,
        ).showSnackBar(SnackBar(content: Text("Failed to delete contact: $e")));
      }
    }
  }

  Widget _buildContactsList() {
    if (_isLoadingContacts) {
      return const Center(
        child: Padding(
          padding: EdgeInsets.all(16.0),
          child: CircularProgressIndicator(),
        ),
      );
    }

    if (_contactsErrorMessage != null) {
      return Padding(
        padding: const EdgeInsets.all(16.0),
        child: Column(
          children: [
            Text(
              _contactsErrorMessage!,
              style: const TextStyle(color: Colors.red),
              textAlign: TextAlign.center,
            ),
            const SizedBox(height: 8),
            ElevatedButton(
              onPressed: _fetchEmergencyContacts,
              child: const Text("Retry"),
            ),
          ],
        ),
      );
    }

    if (_emergencyContacts.isEmpty) {
      return const Padding(
        padding: EdgeInsets.all(16),
        child: Text(
          "No emergency contacts added.",
          style: TextStyle(fontSize: 16, color: Colors.grey),
          textAlign: TextAlign.center,
        ),
      );
    }

    return ListView.builder(
      shrinkWrap: true,
      physics: const NeverScrollableScrollPhysics(),
      itemCount: _emergencyContacts.length,
      itemBuilder: (context, index) {
        final contact = _emergencyContacts[index];
        return SettingsTile(
          icon: Icons.person,
          title: contact.name,
          subtitle: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              Text(contact.phoneNumber),
              Text(
                "${contact.relation} • ${contact.preferredMethod}",
                style: const TextStyle(fontSize: 12, color: Colors.grey),
              ),
            ],
          ),
          trailing: IconButton(
            icon: const Icon(Icons.delete, color: Colors.red),
            onPressed: () => _showDeleteConfirmation(contact),
          ),
        );
      },
    );
  }

  void _showDeleteConfirmation(EmergencyContact contact) {
    showDialog(
      context: context,
      builder:
          (context) => AlertDialog(
            title: const Text("Delete Contact"),
            content: Text("Are you sure you want to delete ${contact.name}?"),
            actions: [
              TextButton(
                onPressed: () => Navigator.pop(context),
                child: const Text("Cancel"),
              ),
              ElevatedButton(
                onPressed: () {
                  Navigator.pop(context);
                  _deleteContact(contact.contactId);
                },
                style: ElevatedButton.styleFrom(backgroundColor: Colors.red),
                child: const Text(
                  "Delete",
                  style: TextStyle(color: Colors.white),
                ),
              ),
            ],
          ),
    );
  }

  @override
  Widget build(BuildContext context) {
    return Column(
      children: [
        const SettingsHeader(title: "Emergency Contacts"),

        // Add contact button
        SettingsTile(
          icon: Icons.contact_phone,
          title: "Manage Emergency Contacts",
          trailing: ElevatedButton(
            style: ElevatedButton.styleFrom(
              backgroundColor: Colors.green,
              foregroundColor: Colors.white,
              padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 8),
            ),
            onPressed: _showEmergencyContactOptions,
            child: const Text("Add Contact"),
          ),
        ),

        // Permission status
        if (_contactPermissionStatus != null)
          Padding(
            padding: const EdgeInsets.symmetric(horizontal: 16.0, vertical: 8),
            child: Row(
              children: [
                Icon(
                  _contactPermissionStatus!.isGranted
                      ? Icons.check_circle
                      : Icons.warning,
                  color:
                      _contactPermissionStatus!.isGranted
                          ? Colors.green
                          : Colors.orange,
                ),
                const SizedBox(width: 8),
                Expanded(
                  child: Text(
                    "Contact Permission: ${_contactPermissionStatus!.isGranted
                        ? "Granted"
                        : _contactPermissionStatus!.isDenied
                        ? "Denied"
                        : "Restricted"}",
                    style: const TextStyle(fontSize: 14),
                  ),
                ),
                if (!_contactPermissionStatus!.isGranted)
                  TextButton(
                    onPressed: () => openAppSettings(),
                    child: const Text("Settings"),
                  ),
              ],
            ),
          ),

        const SizedBox(height: 16),

        // Contacts list
        _buildContactsList(),
      ],
    );
  }
}
