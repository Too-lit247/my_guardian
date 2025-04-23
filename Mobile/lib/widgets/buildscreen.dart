
import 'package:flutter/material.dart';

Widget _buildScreen({
  String title = '',
  required String description,
  required String buttonText,
  required VoidCallback onPressed,
  String image = '',
}) {
  return Padding(
    padding: const EdgeInsets.all(24.0),
    child: Column(
      mainAxisAlignment: MainAxisAlignment.center,
      children: [
        SizedBox(
          width: double.infinity,
          height: 300,
          child: Image.asset(
            image,
            fit: BoxFit.contain,
          ),
        ),
        title != '' ?
        Text(
          title,
          style: const TextStyle(fontSize: 24, fontWeight: FontWeight.bold),
        ): const SizedBox(height: 10),
        const SizedBox(height: 20),
        Text(
          description,
          textAlign: TextAlign.center,
          style: const TextStyle(fontSize: 16),
        ),
        const SizedBox(height: 40),
        ElevatedButton(
          onPressed: onPressed,
          child: Text(buttonText),
        ),
      ],
    ),
  );
}
