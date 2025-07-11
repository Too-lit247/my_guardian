import 'package:postgres/postgres.dart';
import 'package:flutter_dotenv/flutter_dotenv.dart';

class DBService {
  static final DBService _instance = DBService._internal();
  factory DBService() => _instance;
  DBService._internal();

  late Connection _conn;

  Future<void> connect() async {
    final uri = Uri.parse(dotenv.env['DATABASE_URL']!);
    _conn = await Connection.open(
      Endpoint(
        host: uri.host,
        port: uri.port,
        database: uri.pathSegments.first,
        username: uri.userInfo.split(':').first,
        password: uri.userInfo.split(':').last,
      ),
      settings: ConnectionSettings(
        sslMode:
            uri.queryParameters['sslmode'] == 'require'
                ? SslMode.require
                : SslMode.disable,
      ),
    );
  }

  Connection get conn => _conn;
}
