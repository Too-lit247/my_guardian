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
              tip: 'Tip 1: Use the search bar to find specific features',
              description:
                  'You can use the search bar at the top of the app to quickly find specific features or settings.',
            ),
            TipCard(
              tip: 'Tip 2: Swipe left to delete items',
              description:
                  'You can swipe left on any item in the list to delete it.',
            ),
            TipCard(
              tip: 'Tip 3: Use the filters to narrow down results',
              description:
                  'You can use the filters at the top of the list to narrow down the results based on specific criteria.',
            ),
            TipCard(
              tip: 'Tip 4: Long press to copy text',
              description:
                  'You can long press on any text in the app to copy it to your clipboard.',
            ),
            TipCard(
              tip: 'Tip 5: Use the settings menu to customize the app',
              description:
                  'You can use the settings menu to customize the app\'s appearance and behavior.',
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
