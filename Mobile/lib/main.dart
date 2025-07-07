import 'package:firebase_core/firebase_core.dart';
import 'package:flutter_dotenv/flutter_dotenv.dart';
import 'package:my_guardian/SplashScreen.dart';
import 'package:my_guardian/auth/auth_service.dart';
import 'package:my_guardian/auth/login.dart';
import 'package:my_guardian/auth/register.dart';
import 'package:my_guardian/layouts/layout.dart';
import 'package:flutter/material.dart';
import 'package:my_guardian/scanPage.dart';
import 'services/firebase_options.dart';

void main() async {
  WidgetsFlutterBinding.ensureInitialized();

  await dotenv.load(fileName: ".env");

  await Firebase.initializeApp(options: DefaultFirebaseOptions.currentPlatform);

  // Initialize your auth service (load stored user/token)
  await DjangoAuthService().initialize();
  //await dotenv.load(fileName: ".env");
  runApp(const MyApp());
}

class MyApp extends StatelessWidget {
  const MyApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      debugShowCheckedModeBanner: false,
      title: 'My Guardian Plus',
      theme: ThemeData(primarySwatch: Colors.blue),
      // home: AuthStateWrapper(
      //   builder: (context, user) {
      //     if (user != null) {
      //       return MainScreen(); // Authenticated
      //     } else {
      //       return LoginPage(); // Not authenticated
      //     }
      //   },
      //   loadingWidget: SplashScreen(), // splash screen while waiting
      // ),
      routes: {
        '/': (context) => SplashScreen(),
        '/welcome': (context) => const OnboardingScreen(),
        '/home': (context) => const MainScreen(),
        '/login': (context) => const LoginPage(),
        '/register': (context) => const RegisterPage(),
        '/scan_device': (context) => const DeviceScanPage(),
      },
    );
  }
}

class OnboardingScreen extends StatefulWidget {
  const OnboardingScreen({super.key});

  @override
  _OnboardingScreenState createState() => _OnboardingScreenState();
}

class _OnboardingScreenState extends State<OnboardingScreen> {
  final PageController _pageController = PageController();
  int _currentPage = 0;

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: Colors.white,
      body: Column(
        children: [
          Expanded(
            child: PageView(
              controller: _pageController,
              onPageChanged: (index) {
                setState(() => _currentPage = index);
              },
              children: [
                WelcomeScreen(pageController: _pageController),
                AppDescriptionScreen(pageController: _pageController),
                DashboardInfoScreen(pageController: _pageController),
                const SettingsInfoScreen(),
              ],
            ),
          ),
          _buildIndicator(),
        ],
      ),
    );
  }

  Widget _buildIndicator() {
    return Padding(
      padding: const EdgeInsets.all(16.0),
      child: Row(
        mainAxisAlignment: MainAxisAlignment.center,
        children: List.generate(
          4, // Updated to 5 screens
          (index) => Container(
            margin: const EdgeInsets.symmetric(horizontal: 5),
            width: _currentPage == index ? 12 : 8,
            height: _currentPage == index ? 12 : 8,
            decoration: BoxDecoration(
              shape: BoxShape.circle,
              color: _currentPage == index ? Colors.blue : Colors.grey,
            ),
          ),
        ),
      ),
    );
  }
}

class WelcomeScreen extends StatelessWidget {
  final PageController pageController;

  const WelcomeScreen({super.key, required this.pageController});

  @override
  Widget build(BuildContext context) {
    final user = DjangoAuthService().currentUser;
    final displayName = user?.displayName ?? 'User';
    final email = user?.email ?? '';

    return _buildScreen(
      description:
          "Welcome, $displayName ($email). Your safety is our priority. Let's set up your Guardian+ device.",
      buttonText: "Next",
      image: "assets/images/welcome.jpg",
      onPressed:
          () => pageController.nextPage(
            duration: const Duration(milliseconds: 300),
            curve: Curves.ease,
          ),
    );
  }
}

class AppDescriptionScreen extends StatelessWidget {
  final PageController pageController;

  const AppDescriptionScreen({super.key, required this.pageController});

  @override
  Widget build(BuildContext context) {
    return _buildScreen(
      title: "How It Works",
      description:
          "This app connects to your Guardian+ device to monitor your heart rate voice, as well as if there is a fire in your surrounding"
          "If danger is detected, emergency contacts will be called automatically.",
      buttonText: "Next",
      image: "assets/images/working.jpg",
      onPressed:
          () => pageController.nextPage(
            duration: const Duration(milliseconds: 300),
            curve: Curves.ease,
          ),
    );
  }
}

class DashboardInfoScreen extends StatelessWidget {
  final PageController pageController;

  const DashboardInfoScreen({super.key, required this.pageController});

  @override
  Widget build(BuildContext context) {
    return _buildScreen(
      title: "Live Dashboard",
      description:
          "View real-time updates from your Guardian+ device on the dashboard. "
          "Monitor your heart rate, voice patterns, and environmental conditions "
          "all in one place with live data visualization.",
      buttonText: "Next",
      image: "assets/images/dashboard.jpg", // Add your dashboard image
      onPressed:
          () => pageController.nextPage(
            duration: const Duration(milliseconds: 300),
            curve: Curves.ease,
          ),
    );
  }
}

class SettingsInfoScreen extends StatelessWidget {
  const SettingsInfoScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return _buildScreen(
      title: "Device & Contacts Setup",
      description:
          "Visit the Settings page to connect your Guardian+ device and manage "
          "your emergency contacts. You can add multiple contacts and customize "
          "notification preferences to ensure help reaches you when needed.",
      buttonText: "Get Started",
      image: "assets/images/settings.png", // Add your settings image
      onPressed: () {
        // Navigate to home screen (dashboard) to complete onboarding
        Navigator.pushReplacementNamed(context, '/home');
      },
    );
  }
}

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
          child: Image.asset(image, fit: BoxFit.contain),
        ),
        if (title.isNotEmpty)
          Text(
            title,
            style: const TextStyle(fontSize: 24, fontWeight: FontWeight.bold),
          )
        else
          const SizedBox(height: 10),
        const SizedBox(height: 20),
        Text(
          description,
          textAlign: TextAlign.center,
          style: const TextStyle(fontSize: 16),
        ),
        const SizedBox(height: 40),
        ElevatedButton(
          onPressed: onPressed,
          style: ElevatedButton.styleFrom(
            backgroundColor: Colors.green, // Makes the button green
          ),
          child: Text(buttonText, style: TextStyle(color: Colors.white)),
        ),
      ],
    ),
  );
}
