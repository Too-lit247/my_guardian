import 'package:flutter/material.dart';
import 'package:my_guardian/services/alert_history_service.dart';

class AlertHistoryPage extends StatefulWidget {
  const AlertHistoryPage({super.key});

  @override
  State<AlertHistoryPage> createState() => _AlertHistoryPageState();
}

class _AlertHistoryPageState extends State<AlertHistoryPage> {
  final AlertHistoryService _alertService = AlertHistoryService();

  @override
  void initState() {
    super.initState();
    _loadAlertHistory();
  }

  Future<void> _loadAlertHistory() async {
    await _alertService.fetchAlertHistory();
    if (mounted) {
      setState(() {});
    }
  }

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
        actions: [
          IconButton(
            icon: const Icon(Icons.refresh, color: Colors.white),
            onPressed: _loadAlertHistory,
          ),
        ],
      ),
      body: Column(
        children: [
          Expanded(
            child: Padding(
              padding: const EdgeInsets.all(16.0),
              child: _buildContent(),
            ),
          ),
        ],
      ),
    );
  }

  Widget _buildContent() {
    if (_alertService.isLoading) {
      return const Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            CircularProgressIndicator(color: Colors.green),
            SizedBox(height: 16),
            Text('Loading alert history...'),
          ],
        ),
      );
    }

    if (_alertService.error != null) {
      return Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            Icon(Icons.error_outline, size: 64, color: Colors.red[300]),
            const SizedBox(height: 16),
            Text(
              'Error loading alerts',
              style: TextStyle(fontSize: 18, color: Colors.red[700]),
            ),
            const SizedBox(height: 8),
            Text(
              _alertService.error!,
              textAlign: TextAlign.center,
              style: const TextStyle(color: Colors.grey),
            ),
            const SizedBox(height: 16),
            ElevatedButton(
              onPressed: _loadAlertHistory,
              child: const Text('Retry'),
            ),
          ],
        ),
      );
    }

    if (_alertService.alertHistory.isEmpty) {
      return Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            Icon(Icons.history, size: 64, color: Colors.grey[400]),
            const SizedBox(height: 16),
            Text(
              'No Alert History',
              style: TextStyle(fontSize: 18, color: Colors.grey[600]),
            ),
            const SizedBox(height: 8),
            const Text(
              'No emergency alerts have been triggered yet.',
              textAlign: TextAlign.center,
              style: TextStyle(color: Colors.grey),
            ),
          ],
        ),
      );
    }

    return RefreshIndicator(
      onRefresh: _loadAlertHistory,
      child: ListView.builder(
        itemCount: _alertService.alertHistory.length,
        itemBuilder: (context, index) {
          final alert = _alertService.alertHistory[index];
          return RealAlertCard(alert: alert);
        },
      ),
    );
  }
}

enum AlertType { manual, general, health, fire, police }

// New widget for real alert data
class RealAlertCard extends StatelessWidget {
  final Map<String, dynamic> alert;

  const RealAlertCard({super.key, required this.alert});

  @override
  Widget build(BuildContext context) {
    final alertService = AlertHistoryService();
    final status = alert['status'] as String?;
    final priority = alert['priority'] as String?;
    final alertType = alert['alert_type'] as String?;
    final title = alert['title'] as String? ?? 'Unknown Alert';
    final createdAt = alert['created_at'];
    final resolvedAt = alert['resolved_at'];
    final description = alert['description'] as String? ?? '';
    final location = alert['location'] as String? ?? 'Unknown location';

    return Card(
      elevation: 2,
      margin: const EdgeInsets.only(bottom: 16),
      child: Padding(
        padding: const EdgeInsets.all(16.0),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Row(
              children: [
                Container(
                  padding: const EdgeInsets.all(8),
                  decoration: BoxDecoration(
                    color: _getAlertTypeColor(alertType),
                    borderRadius: BorderRadius.circular(8),
                  ),
                  child: Icon(
                    _getAlertTypeIcon(alertType),
                    color: Colors.white,
                    size: 20,
                  ),
                ),
                const SizedBox(width: 12),
                Expanded(
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      Text(
                        alertService.getAlertTypeDisplay(alertType),
                        style: TextStyle(
                          fontSize: 16,
                          fontWeight: FontWeight.bold,
                          color: _getAlertTypeColor(alertType),
                        ),
                      ),
                      Text(
                        alertService.formatDate(createdAt),
                        style: const TextStyle(
                          fontSize: 12,
                          color: Colors.grey,
                        ),
                      ),
                    ],
                  ),
                ),
                Container(
                  padding: const EdgeInsets.symmetric(
                    horizontal: 8,
                    vertical: 4,
                  ),
                  decoration: BoxDecoration(
                    color: _getStatusColor(status),
                    borderRadius: BorderRadius.circular(12),
                  ),
                  child: Text(
                    _getStatusDisplay(status),
                    style: const TextStyle(
                      color: Colors.white,
                      fontSize: 12,
                      fontWeight: FontWeight.bold,
                    ),
                  ),
                ),
              ],
            ),
            const SizedBox(height: 12),
            if (title.isNotEmpty && title != 'Unknown Alert')
              Text(
                title,
                style: const TextStyle(
                  fontSize: 14,
                  fontWeight: FontWeight.w500,
                ),
              ),
            if (location.isNotEmpty && location != 'Unknown location')
              Padding(
                padding: const EdgeInsets.only(top: 4),
                child: Row(
                  children: [
                    const Icon(Icons.location_on, size: 14, color: Colors.grey),
                    const SizedBox(width: 4),
                    Expanded(
                      child: Text(
                        location,
                        style: const TextStyle(
                          fontSize: 12,
                          color: Colors.grey,
                        ),
                      ),
                    ),
                  ],
                ),
              ),
            if (priority != null)
              Padding(
                padding: const EdgeInsets.only(top: 8),
                child: Row(
                  children: [
                    Icon(
                      Icons.priority_high,
                      size: 16,
                      color: _getPriorityColor(priority),
                    ),
                    const SizedBox(width: 4),
                    Text(
                      'Priority: ${priority.toUpperCase()}',
                      style: TextStyle(
                        fontSize: 12,
                        color: _getPriorityColor(priority),
                        fontWeight: FontWeight.w500,
                      ),
                    ),
                  ],
                ),
              ),
            if (resolvedAt != null)
              Padding(
                padding: const EdgeInsets.only(top: 4),
                child: Text(
                  'Resolved: ${alertService.formatDate(resolvedAt)}',
                  style: const TextStyle(fontSize: 12, color: Colors.green),
                ),
              ),
            if (alert['acknowledged'] == true &&
                alert['acknowledged_at'] != null)
              Padding(
                padding: const EdgeInsets.only(top: 4),
                child: Text(
                  'Acknowledged: ${alertService.formatDate(alert['acknowledged_at'])}',
                  style: const TextStyle(fontSize: 12, color: Colors.blue),
                ),
              ),
          ],
        ),
      ),
    );
  }

  Color _getAlertTypeColor(String? alertType) {
    switch (alertType) {
      case 'high_heart_rate':
      case 'heart_attack':
      case 'fall_detected':
        return Colors.red[500]!;
      case 'fire_detected':
      case 'building_fire':
        return Colors.orange[500]!;
      case 'fear_detected':
      case 'panic_button':
      case 'robbery':
      case 'assault':
        return Colors.purple[500]!;
      default:
        return Colors.blue[500]!;
    }
  }

  IconData _getAlertTypeIcon(String? alertType) {
    switch (alertType) {
      case 'high_heart_rate':
      case 'heart_attack':
      case 'fall_detected':
        return Icons.medical_services;
      case 'fire_detected':
      case 'building_fire':
        return Icons.local_fire_department;
      case 'fear_detected':
      case 'panic_button':
      case 'robbery':
      case 'assault':
        return Icons.local_police;
      default:
        return Icons.warning;
    }
  }

  Color _getStatusColor(String? status) {
    switch (status?.toLowerCase()) {
      case 'active':
        return Colors.red[600]!;
      case 'in_progress':
        return Colors.orange[600]!;
      case 'resolved':
        return Colors.green[600]!;
      case 'cancelled':
        return Colors.grey[600]!;
      default:
        return Colors.grey[600]!;
    }
  }

  String _getStatusDisplay(String? status) {
    switch (status?.toLowerCase()) {
      case 'active':
        return 'ACTIVE';
      case 'in_progress':
        return 'IN PROGRESS';
      case 'resolved':
        return 'RESOLVED';
      case 'cancelled':
        return 'CANCELLED';
      default:
        return 'UNKNOWN';
    }
  }

  Color _getPriorityColor(String? priority) {
    switch (priority?.toLowerCase()) {
      case 'high':
        return Colors.red[600]!;
      case 'medium':
        return Colors.orange[600]!;
      case 'low':
        return Colors.green[600]!;
      default:
        return Colors.grey[600]!;
    }
  }
}

// Keep the old AlertCard for backward compatibility
class AlertCard extends StatelessWidget {
  final AlertType alertType;
  final String date;
  final bool isResolved;

  const AlertCard({
    super.key,
    required this.alertType,
    required this.date,
    required this.isResolved,
  });

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
