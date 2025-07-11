// import 'package:flutter/material.dart';
// import 'package:my_guardian/services/postgre_auth.dart';

// class ProfileHeaderWidget extends StatelessWidget {
//   final AuthUser? user;
//   final double? height;
//   final EdgeInsets? margin;

//   const ProfileHeaderWidget({this.user, this.height, this.margin, super.key});

//   @override
//   Widget build(BuildContext context) {
//     final currentUser = user ?? PostgreAuth().currentUser;

//     return Container(
//       margin: margin ?? const EdgeInsets.symmetric(horizontal: 16),
//       child: Column(
//         children: [
//           // Profile Header with background image
//           _buildProfileHeader(currentUser),
//         ],
//       ),
//     );
//   }

//   Widget _buildProfileHeader(AuthUser? currentUser) {
//     return Stack(
//       alignment: Alignment.center,
//       children: [
//         Container(
//           width: double.infinity,
//           height: height ?? 350,
//           decoration: BoxDecoration(
//             borderRadius: BorderRadius.circular(10),
//             image: const DecorationImage(
//               image: AssetImage("assets/images/user-profile.png"),
//               fit: BoxFit.cover,
//             ),
//           ),
//         ),
//         Column(
//           children: [
//             const SizedBox(height: 40),
//             const CircleAvatar(
//               radius: 50,
//               backgroundImage: AssetImage("assets/images/user-glasses.jpg"),
//             ),
//             const SizedBox(height: 10),
//             Text(
//               currentUser?.displayName ?? "John Doe",
//               style: const TextStyle(
//                 fontSize: 22,
//                 fontWeight: FontWeight.bold,
//                 color: Colors.white,
//                 shadows: [
//                   Shadow(
//                     offset: Offset(0, 1),
//                     blurRadius: 3,
//                     color: Colors.black54,
//                   ),
//                 ],
//               ),
//             ),
//             const SizedBox(height: 20),
//             Text(
//               currentUser?.email ?? "john.doe@example.com",
//               style: const TextStyle(
//                 fontSize: 16,
//                 color: Colors.white70,
//                 shadows: [
//                   Shadow(
//                     offset: Offset(0, 1),
//                     blurRadius: 3,
//                     color: Colors.black54,
//                   ),
//                 ],
//               ),
//             ),
//             Text(
//               currentUser?.phoneNumber ?? "+123 456 7890",
//               style: const TextStyle(
//                 fontSize: 16,
//                 color: Colors.white70,
//                 shadows: [
//                   Shadow(
//                     offset: Offset(0, 1),
//                     blurRadius: 3,
//                     color: Colors.black54,
//                   ),
//                 ],
//               ),
//             ),
//           ],
//         ),
//       ],
//     );
//   }
// }

import 'package:flutter/material.dart';
import 'package:my_guardian/services/postgre_auth.dart';

class ProfileHeaderWidget extends StatelessWidget {
  final Map<String, dynamic>? user;
  final double? height;
  final EdgeInsets? margin;

  const ProfileHeaderWidget({this.user, this.height, this.margin, super.key});

  @override
  Widget build(BuildContext context) {
    final currentUser = user ?? PostgreAuth().currentUser;

    return Container(
      margin: margin ?? const EdgeInsets.symmetric(horizontal: 16),
      child: Column(children: [_buildProfileHeader(currentUser)]),
    );
  }

  Widget _buildProfileHeader(Map<String, dynamic>? currentUser) {
    return Stack(
      alignment: Alignment.center,
      children: [
        Container(
          width: double.infinity,
          height: height ?? 350,
          decoration: BoxDecoration(
            borderRadius: BorderRadius.circular(10),
            image: const DecorationImage(
              image: AssetImage("assets/images/user-profile.png"),
              fit: BoxFit.cover,
            ),
          ),
        ),
        Column(
          children: [
            const SizedBox(height: 40),
            const CircleAvatar(
              radius: 50,
              backgroundImage: AssetImage("assets/images/user-glasses.jpg"),
            ),
            const SizedBox(height: 10),
            Text(
              currentUser?['full_name'] ?? "John Doe",
              style: const TextStyle(
                fontSize: 22,
                fontWeight: FontWeight.bold,
                color: Colors.white,
                shadows: [
                  Shadow(
                    offset: Offset(0, 1),
                    blurRadius: 3,
                    color: Colors.black54,
                  ),
                ],
              ),
            ),
            const SizedBox(height: 20),
            Text(
              currentUser?['email'] ?? "john.doe@example.com",
              style: const TextStyle(
                fontSize: 16,
                color: Colors.white70,
                shadows: [
                  Shadow(
                    offset: Offset(0, 1),
                    blurRadius: 3,
                    color: Colors.black54,
                  ),
                ],
              ),
            ),
            Text(
              currentUser?['phone_number'] ?? "+123 456 7890",
              style: const TextStyle(
                fontSize: 16,
                color: Colors.white70,
                shadows: [
                  Shadow(
                    offset: Offset(0, 1),
                    blurRadius: 3,
                    color: Colors.black54,
                  ),
                ],
              ),
            ),
          ],
        ),
      ],
    );
  }
}

// Row for each user detail
class UserInfoRow extends StatelessWidget {
  final IconData icon;
  final String label;
  final String value;

  const UserInfoRow({
    required this.icon,
    required this.label,
    required this.value,
    super.key,
  });

  @override
  Widget build(BuildContext context) {
    return Padding(
      padding: const EdgeInsets.symmetric(vertical: 8.0),
      child: Row(
        children: [
          Icon(icon, color: Colors.green),
          const SizedBox(width: 10),
          Text(
            label,
            style: const TextStyle(fontSize: 16, fontWeight: FontWeight.bold),
          ),
          const Spacer(),
          Text(value, style: const TextStyle(fontSize: 16, color: Colors.grey)),
        ],
      ),
    );
  }
}
