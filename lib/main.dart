import 'package:my_guardian/auth/auth.dart';
import 'package:my_guardian/auth/login.dart';
import 'package:my_guardian/auth/register.dart';
import 'package:my_guardian/layouts/layout.dart';
import 'package:my_guardian/onboarding/devicesetupscreen.dart';
import 'package:firebase_auth/firebase_auth.dart';
import 'package:firebase_core/firebase_core.dart';
import 'package:flutter/material.dart';
import 'firebase_options.dart';

void main() async {
  WidgetsFlutterBinding.ensureInitialized();

  await Firebase.initializeApp(
    options: DefaultFirebaseOptions.currentPlatform,
  );

  runApp(const MyApp());
}

// class MyApp extends StatelessWidget {
//   const MyApp({super.key});

//   @override
//   Widget build(BuildContext context) {
//     return MaterialApp(
//       debugShowCheckedModeBanner: false,
//       home: LoginPage(),
//     );
//   }
// }


class MyApp extends StatelessWidget {
  const MyApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      debugShowCheckedModeBanner: false,
      title: 'my_guardian',
      theme: ThemeData(primarySwatch: Colors.blue),
      routes: {
        '/' : (context) => AuthChecker(),
        '/welcome' : (context) => OnboardingScreen(),
        '/home' : (context) => MainScreen(),
        '/login': (context) => LoginPage(),
        '/register': (context) => RegisterPage(),
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
                const DeviceSetupScreen(),
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
          3,
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

  final user = FirebaseAuth.instance.currentUser;

  WelcomeScreen({super.key, required this.pageController});

  @override
  Widget build(BuildContext context) {
    return _buildScreen(
      description: "Welcome, ${user!.email!} Your safety is our priority. Let's set up your my_guardian.",
      buttonText: "Next",
      image: "assets/images/welcome.jpg",
      onPressed: () => pageController.nextPage(
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
          "This app connects to your my_guardian to monitor your heart rate and voice. "
          "If danger is detected, emergency contacts will be called automatically.",
      buttonText: "Next",
      image: "assets/images/working.jpg",
      onPressed: () => pageController.nextPage(
        duration: const Duration(milliseconds: 300),
        curve: Curves.ease,
      ),
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