// filepath: c:\Users\TJ\Desktop\dev\flutter\holla\bracelet\lib\controllers\ble_controller.dart
import 'package:flutter_blue_plus/flutter_blue_plus.dart';
import 'package:get/get.dart';
import 'package:permission_handler/permission_handler.dart';
import 'package:fluttertoast/fluttertoast.dart';

class BleController extends GetxController {
  Future<void> scanDevices() async {
    if (await FlutterBluePlus.isSupported == false) {
      Fluttertoast.showToast(
        msg: "Bluetooth not supported by this device",
        toastLength: Toast.LENGTH_LONG,
        gravity: ToastGravity.BOTTOM,
      );
      return;
    }

    // Request necessary permissions
    if (await Permission.bluetoothScan.request().isGranted &&
        await Permission.bluetoothConnect.request().isGranted) {
      // Listen to adapter state
      var subscription = FlutterBluePlus.adapterState.listen((BluetoothAdapterState state) async {
        Fluttertoast.showToast(
          msg: "Adapter State: $state",
          toastLength: Toast.LENGTH_SHORT,
          gravity: ToastGravity.BOTTOM,
        );

        if (state == BluetoothAdapterState.on) {
          // Listen to scan results
          var scanSubscription = FlutterBluePlus.scanResults.listen((results) {
            for (ScanResult result in results) {
              Fluttertoast.showToast(
                msg: '${result.device.remoteId}: "${result.advertisementData.localName}" found!',
                toastLength: Toast.LENGTH_SHORT,
                gravity: ToastGravity.BOTTOM,
              );
            }
          });

          await FlutterBluePlus.startScan(
            // withServices: [Guid("180D")], // Filter by service UUID
            // withNames: ["Bluno"], // Filter by device name
            timeout: const Duration(seconds: 15),
          );

          // Wait for scanning to stop
          await FlutterBluePlus.isScanning.where((isScanning) => !isScanning).first;

          
        } else {
          Fluttertoast.showToast(
            msg: "Bluetooth is not enabled. Please enable it.",
            toastLength: Toast.LENGTH_LONG,
            gravity: ToastGravity.BOTTOM,
          );
        }
      });

      scanSubscription.cancel();
    } else {
      Fluttertoast.showToast(
        msg: "Bluetooth permissions not granted.",
        toastLength: Toast.LENGTH_LONG,
        gravity: ToastGravity.BOTTOM,
      );
    }
  }

  // Stream to get scan results
  Stream<List<ScanResult>> get scanResults => FlutterBluePlus.scanResults;
}