import 'package:flutter/material.dart';
import 'package:my_guardian/auth/auth_service.dart';

class ProfileScreen extends StatelessWidget {
  final AuthUser? user = DjangoAuthService().currentUser;

  ProfileScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: Colors.grey[300],
      body: SingleChildScrollView(
        child: Column(
          children: [
            Column(
              crossAxisAlignment: CrossAxisAlignment.stretch,
              children: [ProfileHeader(user: user)],
            ),
            const SizedBox(height: 20),
            UserInfoSection(user: user),
            const SizedBox(height: 20),
            EmergencyContactsSection(),
          ],
        ),
      ),
    );
  }
}

class ProfileHeader extends StatelessWidget {
  final AuthUser? user;
  const ProfileHeader({required this.user, super.key});

  @override
  Widget build(BuildContext context) {
    return Stack(
      alignment: Alignment.center,
      children: [
        SizedBox(
          width: double.infinity,
          height: 350,
          child: Image.asset(
            "assets/images/user-profile.png",
            fit: BoxFit.cover,
          ),
        ),
        Column(
          children: [
            const CircleAvatar(
              radius: 50,
              backgroundImage: AssetImage("assets/images/user-glasses.jpg"),
            ),
            const SizedBox(height: 10),
            Text(
              user?.displayName ?? "John Doe",
              style: const TextStyle(
                fontSize: 22,
                fontWeight: FontWeight.bold,
                color: Colors.white,
              ),
            ),
            Text(
              user?.email ?? "john.doe@example.com",
              style: const TextStyle(fontSize: 16, color: Colors.white70),
            ),
          ],
        ),
      ],
    );
  }
}

// User Information Section
class UserInfoSection extends StatelessWidget {
  final AuthUser? user;
  const UserInfoSection({required this.user, super.key});

  @override
  Widget build(BuildContext context) {
    return Container(
      margin: const EdgeInsets.symmetric(horizontal: 16),
      padding: const EdgeInsets.all(16),
      decoration: BoxDecoration(
        color: Colors.grey[100],
        borderRadius: BorderRadius.circular(10),
        border: Border.all(color: Colors.white),
      ),
      child: Column(
        children: [
          UserInfoRow(icon: Icons.cake, label: "Age", value: "28"),
          UserInfoRow(
            icon: Icons.email,
            label: "Email",
            value: user?.email ?? "johndoe@email.com",
          ),
          UserInfoRow(
            icon: Icons.phone,
            label: "Phone",
            value: "+123 456 7890",
          ),
        ],
      ),
    );
  }
}

// Row for each user detail
class UserInfoRow extends StatelessWidget {
  final IconData icon;
  final String label;
  final String value;

  const UserInfoRow({
    required this.icon,
    required this.label,
    required this.value,
    super.key,
  });

  @override
  Widget build(BuildContext context) {
    return Padding(
      padding: const EdgeInsets.symmetric(vertical: 8.0),
      child: Row(
        children: [
          Icon(icon, color: Colors.green),
          const SizedBox(width: 10),
          Text(
            label,
            style: const TextStyle(fontSize: 16, fontWeight: FontWeight.bold),
          ),
          const Spacer(),
          Text(value, style: const TextStyle(fontSize: 16, color: Colors.grey)),
        ],
      ),
    );
  }
}

class EmergencyContactsSection extends StatelessWidget {
  final List<Map<String, String>> contacts = [
    {"name": "Alice Banda", "phone": "+123 987 6543"},
    {"name": "Michael Banda", "phone": "+123 654 3210"},
  ];

  EmergencyContactsSection({super.key});

  @override
  Widget build(BuildContext context) {
    return Container(
      margin: const EdgeInsets.symmetric(horizontal: 16),
      padding: const EdgeInsets.all(16),
      decoration: BoxDecoration(
        color: Colors.grey[100],
        borderRadius: BorderRadius.circular(10),
        border: Border.all(color: Colors.white),
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          const Text(
            "Emergency Contacts",
            style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold),
          ),
          const SizedBox(height: 10),
          Column(
            children:
                contacts
                    .map(
                      (contact) => ContactRow(
                        name: contact["name"]!,
                        phone: contact["phone"]!,
                      ),
                    )
                    .toList(),
          ),
          const SizedBox(height: 10),
          ElevatedButton.icon(
            onPressed: () {},
            icon: const Icon(Icons.add, color: Colors.white),
            label: const Text(
              "Add/Edit Contacts",
              style: TextStyle(color: Colors.white),
            ),
            style: ElevatedButton.styleFrom(backgroundColor: Colors.green),
          ),
        ],
      ),
    );
  }
}

// Row for each contact
class ContactRow extends StatelessWidget {
  final String name;
  final String phone;

  const ContactRow({required this.name, required this.phone, super.key});

  @override
  Widget build(BuildContext context) {
    return Padding(
      padding: const EdgeInsets.symmetric(vertical: 8.0),
      child: Row(
        children: [
          const Icon(Icons.person, color: Colors.green),
          const SizedBox(width: 10),
          Text(
            name,
            style: const TextStyle(fontSize: 16, fontWeight: FontWeight.bold),
          ),
          const Spacer(),
          Text(phone, style: const TextStyle(fontSize: 16, color: Colors.grey)),
        ],
      ),
    );
  }
}
