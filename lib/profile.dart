import 'package:flutter/material.dart';

class ProfileScreen extends StatelessWidget {
  const ProfileScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: Colors.grey[300],/*
      appBar: AppBar(
        backgroundColor: Colors.blue[900],
        title: const Text(
          "Profile",
          style: TextStyle(color: Colors.white),
          ),
        centerTitle: true,
      ),*/
      body: SingleChildScrollView(
        child: Column(
          children: [
            Column(
              crossAxisAlignment: CrossAxisAlignment.stretch,
              children: [ProfileHeader()],
              ),            
            const SizedBox(height: 20),
            const UserInfoSection(),
            const SizedBox(height: 20),
            EmergencyContactsSection(),
          ],
        ),
      ),
    );
  }
}

/* Profile Header with Avatar
class ProfileHeader extends StatelessWidget {
  const ProfileHeader({super.key});

  @override
  Widget build(BuildContext context) {
    return Center(
      child: Container(
        decoration: BoxDecoration(
          image: DecorationImage(
            image: AssetImage(
              "assets/images/user-profile.png",
              ),
            fit: BoxFit.fill,
            )
        ),
        child: Column(
          children: [
            const CircleAvatar(
              radius: 50,
              backgroundImage: AssetImage("assets/images/user-glasses.jpg"),
            ),
            const SizedBox(height: 10),
            Text(
              "John Doe",
              style: TextStyle(fontSize: 22, fontWeight: FontWeight.bold, color: Colors.grey[800]),
            ),
            Text(
              "user@email.com",
              style: TextStyle(fontSize: 16, color: Colors.grey[600]),
            ),
          ],
        ),
      ),
    );
  }
}
*/

class ProfileHeader extends StatelessWidget {
  const ProfileHeader({super.key});

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
              "John Doe",
              style: const TextStyle(fontSize: 22, fontWeight: FontWeight.bold, color: Colors.white),
            ),
            Text(
              "user@email.com",
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
  const UserInfoSection({super.key});

  @override
  Widget build(BuildContext context) {
    return Container(
      margin: const EdgeInsets.symmetric(horizontal: 16),
      padding: const EdgeInsets.all(16),
      decoration: BoxDecoration(
        color: Colors.grey[100],
        borderRadius: BorderRadius.circular(10),
        border: Border.all(color: Colors.white)
      ),
      child: Column(
        children: const [
          UserInfoRow(icon: Icons.cake, label: "Age", value: "28"),
          UserInfoRow(icon: Icons.email, label: "Email", value: "john.doe@example.com"),
          UserInfoRow(icon: Icons.phone, label: "Phone", value: "+123 456 7890"),
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

  const UserInfoRow({required this.icon, required this.label, required this.value, super.key});

  @override
  Widget build(BuildContext context) {
    return Padding(
      padding: const EdgeInsets.symmetric(vertical: 8.0),
      child: Row(
        children: [
          Icon(icon, color: Colors.green),
          const SizedBox(width: 10),
          Text(label, style: const TextStyle(fontSize: 16, fontWeight: FontWeight.bold)),
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
        border: Border.all(color: Colors.white)
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          const Text("Emergency Contacts", style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold)),
          const SizedBox(height: 10),
          Column(
            children: contacts
                .map((contact) => ContactRow(name: contact["name"]!, phone: contact["phone"]!))
                .toList(),
          ),
          const SizedBox(height: 10),
          ElevatedButton.icon(
            onPressed: () {},
            icon: const Icon(Icons.add, color: Colors.white,),
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
          Text(name, style: const TextStyle(fontSize: 16, fontWeight: FontWeight.bold)),
          const Spacer(),
          Text(phone, style: const TextStyle(fontSize: 16, color: Colors.grey)),
        ],
      ),
    );
  }
}