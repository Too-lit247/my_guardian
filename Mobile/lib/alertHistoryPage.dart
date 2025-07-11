import 'package:flutter/material.dart';

class AlertHistoryPage extends StatelessWidget {
  const AlertHistoryPage({Key? key}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        backgroundColor: Colors.green[500],
        title: const Text(
          'Alert History',
          style: TextStyle(
            fontSize: 20,
            fontWeight: FontWeight.bold,
            color: Colors.white,
          ),
        ),
        centerTitle: true,
      ),
      body: Column(
        children: [
          Expanded(
            child: Padding(
              padding: const EdgeInsets.all(16.0),
              child: ListView(
                children: const [
                  AlertCard(
                    alertType: AlertType.manual,
                    date: '2024-09-10 14:30',
                    isResolved: true,
                  ),
                  AlertCard(
                    alertType: AlertType.fire,
                    date: '2024-09-09 02:00',
                    isResolved: false,
                  ),
                  AlertCard(
                    alertType: AlertType.health,
                    date: '2024-09-08 10:00',
                    isResolved: true,
                  ),
                  AlertCard(
                    alertType: AlertType.police,
                    date: '2024-09-07 22:00',
                    isResolved: false,
                  ),
                  AlertCard(
                    alertType: AlertType.general,
                    date: '2024-09-06 12:00',
                    isResolved: true,
                  ),
                ],
              ),
            ),
          ),
        ],
      ),
    );
  }
}

enum AlertType { manual, general, health, fire, police }

class AlertCard extends StatelessWidget {
  final AlertType alertType;
  final String date;
  final bool isResolved;

  const AlertCard({
    Key? key,
    required this.alertType,
    required this.date,
    required this.isResolved,
  }) : super(key: key);

  Color getAlertColor() {
    switch (alertType) {
      case AlertType.manual:
        return Colors.blue[500]!;
      case AlertType.general:
        return Colors.grey[500]!;
      case AlertType.health:
        return Colors.red[500]!;
      case AlertType.fire:
        return Colors.orange[500]!;
      case AlertType.police:
        return Colors.purple[500]!;
    }
  }

  IconData getAlertIcon() {
    switch (alertType) {
      case AlertType.manual:
        return Icons.warning;
      case AlertType.general:
        return Icons.info;
      case AlertType.health:
        return Icons.medical_services;
      case AlertType.fire:
        return Icons.local_fire_department;
      case AlertType.police:
        return Icons.local_police;
    }
  }

  String getAlertTypeString() {
    switch (alertType) {
      case AlertType.manual:
        return 'Manual Triggered';
      case AlertType.general:
        return 'General Alert';
      case AlertType.health:
        return 'Health Emergency';
      case AlertType.fire:
        return 'Fire Alert';
      case AlertType.police:
        return 'Police Alert';
    }
  }

  String formatDate(String date) {
    DateTime dateTime = DateTime.parse(date);
    String amPm = dateTime.hour < 12 ? 'AM' : 'PM';
    int hour = dateTime.hour % 12 == 0 ? 12 : dateTime.hour % 12;
    String formattedDate =
        '${getDayOfWeek(dateTime.weekday)}, ${getMonth(dateTime.month)} ${dateTime.day}, ${dateTime.year} $hour:${dateTime.minute.toString().padLeft(2, '0')} $amPm';
    return formattedDate;
  }

  String getDayOfWeek(int day) {
    switch (day) {
      case 1:
        return 'Mon';
      case 2:
        return 'Tue';
      case 3:
        return 'Wed';
      case 4:
        return 'Thu';
      case 5:
        return 'Fri';
      case 6:
        return 'Sat';
      case 7:
        return 'Sun';
      default:
        return '';
    }
  }

  String getMonth(int month) {
    switch (month) {
      case 1:
        return 'Jan';
      case 2:
        return 'Feb';
      case 3:
        return 'Mar';
      case 4:
        return 'Apr';
      case 5:
        return 'May';
      case 6:
        return 'Jun';
      case 7:
        return 'Jul';
      case 8:
        return 'Aug';
      case 9:
        return 'Sep';
      case 10:
        return 'Oct';
      case 11:
        return 'Nov';
      case 12:
        return 'Dec';
      default:
        return '';
    }
  }

  @override
  Widget build(BuildContext context) {
    String formattedDate = formatDate(date);

    return Card(
      elevation: 2,
      margin: const EdgeInsets.only(bottom: 16),
      child: Padding(
        padding: const EdgeInsets.all(16.0),
        child: Row(
          children: [
            Container(
              padding: const EdgeInsets.all(8),
              decoration: BoxDecoration(
                color: getAlertColor(),
                borderRadius: BorderRadius.circular(8),
              ),
              child: Icon(getAlertIcon(), color: Colors.white),
            ),
            const SizedBox(width: 16),
            Expanded(
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Text(
                    getAlertTypeString(),
                    style: TextStyle(
                      fontSize: 16,
                      fontWeight: FontWeight.bold,
                      color: getAlertColor(),
                    ),
                  ),
                  Text(formattedDate),
                ],
              ),
            ),
            Container(
              padding: const EdgeInsets.all(8),
              decoration: BoxDecoration(
                color: isResolved ? Colors.green[100] : Colors.red[100],
                borderRadius: BorderRadius.circular(8),
              ),
              child: Text(
                isResolved ? 'Resolved' : 'Unresolved',
                style: TextStyle(
                  color: isResolved ? Colors.green[500] : Colors.red[500],
                ),
              ),
            ),
          ],
        ),
      ),
    );
  }
}
