import 'dart:io';

import 'package:flutter/material.dart';
//import 'package:my_guardian/auth/auth_service.dart';
//import 'package:http/http.dart' as http;
//import 'package:flutter_dotenv/flutter_dotenv.dart';
import 'package:my_guardian/services/postgre_auth.dart';
import 'package:fluttertoast/fluttertoast.dart';

class SplashScreen extends StatefulWidget {
  @override
  State<SplashScreen> createState() => _SplashScreenState();
}

class _SplashScreenState extends State<SplashScreen>
    with SingleTickerProviderStateMixin {
  late AnimationController _controller;
  late Animation<double> _fadeAnimation;
  String? _errorMessage;

  @override
  void initState() {
    super.initState();

    _controller = AnimationController(
      vsync: this,
      duration: const Duration(seconds: 2),
    );

    _fadeAnimation = Tween<double>(
      begin: 0,
      end: 1,
    ).animate(CurvedAnimation(parent: _controller, curve: Curves.easeIn));

    _controller.forward();

    _checkBackendAndAuth();
  }

  Future<bool> _hasInternetConnection() async {
    try {
      final result = await InternetAddress.lookup(
        'google.com',
      ).timeout(const Duration(seconds: 5));
      return result.isNotEmpty && result[0].rawAddress.isNotEmpty;
    } catch (e) {
      return false;
    }
  }

  // Future<void> _checkBackendAndAuth() async {
  //   final baseUrl = '${dotenv.env['BASE_URL']}';

  //   try {
  //     final response = await http.get(Uri.parse(baseUrl)).timeout(const Duration(seconds: 5));

  //     if (response.statusCode != 200 && response.statusCode != 401 && response.statusCode != 404) {
  //       throw Exception('Unexpected server response');
  //     }

  //     await DjangoAuthService().initialize();

  //     final isAuthenticated = DjangoAuthService().isAuthenticated;

  //     await Future.delayed(const Duration(seconds: 2));

  //     SchedulerBinding.instance.addPostFrameCallback((_) {
  //       Navigator.of(context).pushReplacementNamed(isAuthenticated ? '/home' : '/login');
  //     });
  //   } catch (e) {
  //     setState(() {
  //       _errorMessage = e.message;//'Unable to connect to the server. Please check your connection.';
  //     });
  //   }
  // }
  // Add to pubspec.yaml

  Future<void> _checkBackendAndAuth() async {
    try {
      bool hasInternet = await _hasInternetConnection();

      if (!hasInternet) {
        if (!mounted) return;
        Fluttertoast.showToast(
          msg: "No internet connection. Please check your connection.",
          toastLength: Toast.LENGTH_LONG,
        );
        return;
      }

      await PostgreAuth().initialize();
      final isAuthenticated = PostgreAuth().isAuthenticated;
      await Future.delayed(const Duration(seconds: 2));

      if (!mounted) return;
      Navigator.of(
        context,
      ).pushReplacementNamed(isAuthenticated ? '/home' : '/login');
    } catch (e) {
      // Print detailed error information to debug console
      print('Error in _checkBackendAndAuth: $e');
      print('Error type: ${e.runtimeType}');
      print('Stack trace: ${StackTrace.current}');

      if (!mounted) return;
      Fluttertoast.showToast(
        msg: 'Something went wrong while checking authentication.',
        toastLength: Toast.LENGTH_LONG,
      );
    }
  }

  @override
  void dispose() {
    _controller.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: Colors.green,
      body: SafeArea(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            const Spacer(),
            FadeTransition(
              opacity: _fadeAnimation,
              child: Center(
                child: Image.asset(
                  'assets/icon/logo_2.png',
                  width: 120,
                  height: 120,
                ),
              ),
            ),
            const SizedBox(height: 20),
            const Text(
              "My guardian +",
              style: const TextStyle(
                fontSize: 16,
                fontWeight: FontWeight.bold,
                color: Colors.white,
              ),
            ),
            const Spacer(),
            const Padding(
              padding: EdgeInsets.only(bottom: 30),
              child: CircularProgressIndicator(color: Colors.white),
            ),
          ],
        ),
      ),
    );
  }
}
