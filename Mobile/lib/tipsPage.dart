import 'package:flutter/material.dart';

class TipsPage extends StatelessWidget {
  const TipsPage({Key? key}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        backgroundColor: Colors.green[500],
        foregroundColor: Colors.white,
        leading: IconButton(
          icon: const Icon(Icons.arrow_back),
          onPressed: () {
            Navigator.of(context).pop();
          },
        ),
        title: const Text('Usage Tips'),
      ),
      body: Padding(
        padding: const EdgeInsets.all(16.0),
        child: ListView(
          children: const [
            TipCard(
              tip: 'Tip 1: View Device Readings',
              description:
                  'You can view the latest readings for your device on the main dashboard',
            ),
            TipCard(
              tip: 'Tip 2: Open Location in maps',
              description:
                  'On the dashboard, in the "Location" section, you can select "View in Maps" to view the current location of your device in Google Maps.',
            ),
            TipCard(
              tip: 'Tip 3: View Alert History',
              description:
                  'In the "Alert History" tab, you can view a list of all past alerts and their outcomes.',
            ),
            TipCard(
              tip: 'Tip 4: Device Connection',
              description:
                  'You can connect your device in the "Settings" tab if you don\'t have a registered device',
            ),
            TipCard(
              tip: 'Tip 5: Device Change',
              description:
                  'Register a different device by clicking the "Change" button next to the registered device in the "Settings" tab.',
            ),
            TipCard(
              tip: 'Tip 6: Emergency Contacts',
              description:
                  'In the "Settings" tab, you can add, edit, or remove emergency contacts. You also have the option to select a contact from your phone',
            ),
            TipCard(
              tip: 'Tip 6: Preferences',
              description:
                  'You can use the settings menu to customize the app\'s appearance, language and notifications behavior.',
            ),
          ],
        ),
      ),
    );
  }
}

class TipCard extends StatelessWidget {
  final String tip;
  final String description;

  const TipCard({Key? key, required this.tip, required this.description})
    : super(key: key);

  @override
  Widget build(BuildContext context) {
    return Card(
      elevation: 2,
      margin: const EdgeInsets.only(bottom: 16),
      child: Padding(
        padding: const EdgeInsets.all(16.0),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Text(
              tip,
              style: TextStyle(
                fontSize: 16,
                fontWeight: FontWeight.bold,
                color: Colors.green[500],
              ),
            ),
            const SizedBox(height: 8),
            Text(description),
          ],
        ),
      ),
    );
  }
}
