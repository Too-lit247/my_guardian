import 'package:flutter_blue_plus/flutter_blue_plus.dart';
import 'package:get/get.dart';
import 'package:permission_handler/permission_handler.dart';
import 'package:fluttertoast/fluttertoast.dart';
import 'dart:async';

class BleController extends GetxController {
  // Store subscriptions as class members so they can be properly managed
  StreamSubscription<BluetoothAdapterState>? _adapterStateSubscription;
  StreamSubscription<List<ScanResult>>? _scanResultsSubscription;

  @override
  void onClose() {
    // Clean up subscriptions when controller is closed
    _adapterStateSubscription?.cancel();
    _scanResultsSubscription?.cancel();
    super.onClose();
  }

  Future<void> scanDevices() async {
    try {
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
        // Cancel any existing subscriptions before creating new ones
        _adapterStateSubscription?.cancel();
        _scanResultsSubscription?.cancel();

        // Listen to adapter state
        _adapterStateSubscription = FlutterBluePlus.adapterState.listen((
          BluetoothAdapterState state,
        ) async {
          Fluttertoast.showToast(
            msg: "Adapter State: $state",
            toastLength: Toast.LENGTH_SHORT,
            gravity: ToastGravity.BOTTOM,
          );

          if (state == BluetoothAdapterState.on) {
            // Listen to scan results
            _scanResultsSubscription = FlutterBluePlus.scanResults.listen((
              results,
            ) {
              for (ScanResult result in results) {
                Fluttertoast.showToast(
                  msg:
                      '${result.device.remoteId}: "${result.advertisementData.localName}" found!',
                  toastLength: Toast.LENGTH_SHORT,
                  gravity: ToastGravity.BOTTOM,
                );
              }
            });

            try {
              await FlutterBluePlus.startScan(
                // withServices: [Guid("180D")], // Filter by service UUID
                // withNames: ["Bluno"], // Filter by device name
                timeout: const Duration(seconds: 15),
              );

              // Wait for scanning to stop
              await FlutterBluePlus.isScanning
                  .where((isScanning) => !isScanning)
                  .first;
              // We don't cancel _scanResultsSubscription here to allow accessing the results after scan completes
            } catch (e) {
              Fluttertoast.showToast(
                msg: "Error scanning: ${e.toString()}",
                toastLength: Toast.LENGTH_LONG,
                gravity: ToastGravity.BOTTOM,
              );
            }
          } else {
            Fluttertoast.showToast(
              msg: "Bluetooth is not enabled. Please enable it.",
              toastLength: Toast.LENGTH_LONG,
              gravity: ToastGravity.BOTTOM,
            );
          }
        });
      } else {
        Fluttertoast.showToast(
          msg: "Bluetooth permissions not granted.",
          toastLength: Toast.LENGTH_LONG,
          gravity: ToastGravity.BOTTOM,
        );
      }
    } catch (e) {
      Fluttertoast.showToast(
        msg: "Error: ${e.toString()}",
        toastLength: Toast.LENGTH_LONG,
        gravity: ToastGravity.BOTTOM,
      );
    }
  }

  // Method to stop scanning and clean up scan subscription
  void stopScan() {
    FlutterBluePlus.stopScan();
    _scanResultsSubscription?.cancel();
    _scanResultsSubscription = null;
  }

  // Stream to get scan results
  Stream<List<ScanResult>> get scanResults => FlutterBluePlus.scanResults;
}
