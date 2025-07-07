// General Settings Tile
import 'package:flutter/material.dart';

class SettingsTile extends StatelessWidget {
  final IconData icon;
  final String title;
  final Widget trailing;
  final Widget? subtitle; // Added optional subtitle
  final VoidCallback? onTap; // Added optional onTap for clickability

  const SettingsTile({
    super.key,
    required this.icon,
    required this.title,
    required this.trailing,
    this.subtitle, // Initialize subtitle
    this.onTap, // Initialize onTap
  });

  @override
  Widget build(BuildContext context) {
    return Padding(
      // Added Padding to create spacing between tiles
      padding: const EdgeInsets.symmetric(
        horizontal: 16.0,
        vertical: 6.0,
      ), // Increased vertical padding
      child: Card(
        // Replaced Container with Card for better visual separation and elevation
        elevation: 2, // Adds a subtle shadow
        shape: RoundedRectangleBorder(
          borderRadius: BorderRadius.circular(12), // Slightly rounded corners
        ),
        clipBehavior:
            Clip.antiAlias, // Ensures content is clipped to rounded corners
        child: InkWell(
          // Use InkWell for tap effects if onTap is provided
          onTap: onTap,
          child: Padding(
            padding: const EdgeInsets.symmetric(
              vertical: 8.0,
              horizontal: 8.0,
            ), // Inner padding for content
            child: Row(
              children: [
                Icon(
                  icon,
                  color: Colors.green[700],
                ), // Slightly darker green for contrast
                const SizedBox(
                  width: 15,
                ), // Increased space between icon and title
                Expanded(
                  child: Column(
                    // Use Column for title and optional subtitle
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      Text(
                        title,
                        style: const TextStyle(
                          fontSize: 16,
                          fontWeight:
                              FontWeight.w600, // Slightly bolder for title
                          color: Colors.black87,
                        ),
                      ),
                      if (subtitle != null) // Display subtitle if provided
                        DefaultTextStyle(
                          style: TextStyle(
                            fontSize: 14,
                            color: Colors.grey[600], // Subtitle color
                            // Removed bold for subtitle
                          ),
                          child: subtitle!,
                        ),
                    ],
                  ),
                ),
                trailing,
              ],
            ),
          ),
        ),
      ),
    );
  }
}
