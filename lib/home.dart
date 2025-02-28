import 'package:flutter/material.dart';

class Home extends StatelessWidget {
const Home({ super.key });

  @override
  Widget build(BuildContext context){
    return Scaffold(
      backgroundColor: Colors.grey[300],
      appBar: AppBar(
        title: Text('Bracelet App'),
        centerTitle: true,
        backgroundColor: Colors.green[400],
      ),
      body: Padding(
          padding: EdgeInsets.all(15),
          child: Column(
            children: <Widget>[
              Row(
                mainAxisAlignment: MainAxisAlignment.spaceAround,
                children: [
                  Container(
                    decoration: BoxDecoration(
                      color: Colors.grey[100],
                      border: Border.all(color:  Colors.white),
                      borderRadius: BorderRadius.circular(12),
                    ),
                    padding: EdgeInsets.all(12),
                    child: Column(
                      children: [
                        Container(
                          child: Text(
                              "Heart Rate",
                              style: TextStyle(
                                fontWeight: FontWeight.bold,
                                fontSize: 25,
                              ),
                            ),
                        ),
                        SizedBox(height: 10),
                        Container(
                          child: Text(
                              "Normal (~92 bps)",
                              style: TextStyle(
                                fontWeight: FontWeight.w300,
                                fontSize: 15,
                              ),
                            ),
                        ),
                      ],
                    ),
                  ),
                  Container(
                    decoration: BoxDecoration(
                      color: Colors.grey[100],
                      border: Border.all(color:  Colors.white),
                      borderRadius: BorderRadius.circular(12),
                    ),
                    padding: EdgeInsets.all(12),
                    child: Column(
                      children: [
                        Container(
                          child: Text(
                              "Voice Activity",
                              style: TextStyle(
                                fontWeight: FontWeight.bold,
                                fontSize: 25,
                              ),
                            ),
                        ),
                        SizedBox(height: 10),
                        Container(
                          child: Text(
                              "~92 bps",
                              style: TextStyle(
                                fontWeight: FontWeight.w300,
                                fontSize: 15,
                              ),
                            ),
                        ),
                      ],
                    ),
                  ),
                ],
              )
            ],
          ),
        ),
        bottomNavigationBar: Container(
          decoration: BoxDecoration(
            color: Colors.green[400],
            borderRadius: BorderRadius.circular(12),
          ),
          child: Row(
            mainAxisAlignment: MainAxisAlignment.spaceAround,
            children: [
              IconButton(onPressed: (){}, icon: Icon(Icons.home_outlined)),
              IconButton(onPressed: (){}, icon: Icon(Icons.error_outlined)),
              IconButton(onPressed: (){}, icon: Icon(Icons.settings_outlined)),
              IconButton(onPressed: (){}, icon: Icon(Icons.person_2_outlined)),
            ],
          ),
        ),
      );
  }
}