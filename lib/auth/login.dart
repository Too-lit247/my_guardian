import 'package:flutter/material.dart';

class LoginPage extends StatefulWidget {
  const LoginPage({super.key});

  @override
  State<LoginPage> createState() => _LoginPageState();
}

class _LoginPageState extends State<LoginPage>{

  final _emailController = TextEditingController();
  final _passwordController = TextEditingController();

  Future login() async {
    print("logging in...");
    Navigator.pushReplacementNamed(context, '/welcome');
  }
  
  @override
  Widget build(BuildContext context){
    return Scaffold(
      backgroundColor: Colors.white,
      body: SafeArea(
        child: Center(
          child: SingleChildScrollView(
            child: Column(
              mainAxisAlignment: MainAxisAlignment.center,
              children: [
                Center(
                  child: Image(
                      image: AssetImage('assets/images/login.jpg'),
                      height: 300,
                      width: 300,
                    ),
                ),
            
                SizedBox(height: 10,),
            
                SizedBox(height: 10,),
                Text(
                  'Welcome back to MyGuardian App',
                  style: TextStyle(
                    fontSize: 18,
                  ),
                ),
                SizedBox(height: 30,),
            
                Padding(
                  padding: const EdgeInsets.symmetric(horizontal: 25.0),
                  child: Container(
                    decoration: BoxDecoration(
                      color: Colors.grey[200],
                      border: Border.all(color: Colors.white),
                      borderRadius: BorderRadius.circular(12),
                    ),
                    child: Padding(
                      padding: const EdgeInsets.only(left: 8.0),
                      child: TextField(
                        controller: _emailController,
                        decoration: InputDecoration(
                          border: InputBorder.none,
                          hintText: 'Email',
                        ),
                      ),
                    ),
                  ),
                ),
            
                SizedBox(height: 10,),
            
                Padding(
                  padding: const EdgeInsets.symmetric(horizontal: 25.0),
                  child: Container(
                    decoration: BoxDecoration(
                      color: Colors.grey[200],
                      border: Border.all(color:  Colors.white),
                      borderRadius: BorderRadius.circular(12),
                    ),
                    child: Padding(
                      padding: const EdgeInsets.only(left: 8.0),
                      child: TextField(
                        controller: _passwordController,
                        decoration: InputDecoration(
                          border: InputBorder.none,
                          hintText: 'Password',
                        ),
                        obscureText: true,
                      ),
                    ),
                  ),
                ),
            
                SizedBox(height: 10,),
            
                Padding(
                  padding: const EdgeInsets.symmetric(horizontal: 25.0),
                  child: GestureDetector(
                    onTap: login,
                    child: Container(
                      decoration: BoxDecoration(
                        borderRadius: BorderRadius.circular(12),
                        color: const Color.fromARGB(255, 21, 209, 30),
                      ),
                      padding: EdgeInsets.all(15),
                      child: Center(
                        child: Text(
                          'Login',
                          style: TextStyle(
                            color: Colors.white,
                            fontWeight: FontWeight.bold,
                            fontSize: 18,
                          ),
                        ),
                      ),
                    ),
                  ),
                ),
            
                SizedBox(height: 25,),
            
                Row(
                  mainAxisAlignment: MainAxisAlignment.center,
                  children: [
                    Text(
                      'Not a member?',
                      style: TextStyle(
                        fontWeight: FontWeight.bold,
                      ),
                    ),
                    Text(
                      'Register Now',
                      style: TextStyle(
                        fontWeight: FontWeight.bold,
                        color: Colors.blue
                      ),
                    ),
                  ],
                )
            
            
              ],
            
              //email textfield
            
              //password textfield
            
              //signin button
            
              //not a member yet? register
            ),
          ),
        ),
      ),
    );
  }
}