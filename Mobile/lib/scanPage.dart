import 'package:flutter/material.dart';
import 'package:my_guardian/widgets/bluetoothScanWidget.dart';

class DeviceScanPage extends StatelessWidget {
  const DeviceScanPage({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: Colors.white,
      appBar: AppBar(
        title: const Text("Scan for Device"),
        backgroundColor: Colors.green,
        foregroundColor: Colors.white,
      ),
      body: Column(
        children: [
          const SizedBox(height: 32),
          Center(
            child: Stack(
              alignment: Alignment.center,
              children: [
                for (var i = 1; i <= 3; i++)
                  AnimatedCircle(delay: Duration(milliseconds: i * 400)),
                const Icon(Icons.bluetooth, size: 80, color: Colors.green),
              ],
            ),
          ),
          const SizedBox(height: 32),
          const Expanded(child: BluetoothScanWidget()),
        ],
      ),
    );
  }
}

class AnimatedCircle extends StatefulWidget {
  final Duration delay;
  const AnimatedCircle({super.key, required this.delay});

  @override
  State<AnimatedCircle> createState() => _AnimatedCircleState();
}

class _AnimatedCircleState extends State<AnimatedCircle>
    with SingleTickerProviderStateMixin {
  late final AnimationController _controller = AnimationController(
    vsync: this,
    duration: const Duration(seconds: 2),
  )..repeat();

  @override
  Widget build(BuildContext context) {
    return FadeTransition(
      opacity: Tween<double>(begin: 0.3, end: 0).animate(_controller),
      child: ScaleTransition(
        scale: Tween<double>(begin: 0.8, end: 3.0).animate(_controller),
        child: Container(
          width: 80,
          height: 80,
          decoration: BoxDecoration(
            shape: BoxShape.circle,
            color: Colors.green.withOpacity(0.2),
          ),
        ),
      ),
    );
  }

  @override
  void dispose() {
    _controller.dispose();
    super.dispose();
  }
}
