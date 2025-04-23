<<<<<<< HEAD
# my_guardian
=======
# 🛡️ Smart Bracelet App
>>>>>>> 87048e5f926f00fca79dade2e6bae245811f887b

A mobile app designed to interact with an Arduino-based bracelet via WiFi or Bluetooth. The bracelet monitors the user's heart rate and voice, sending emergency messages to designated contacts in case of distress.

## 🚀 Features

- 📡 **Wireless Connectivity** (WiFi/Bluetooth)
- ❤️ **Heart Rate Monitoring**
- 🗣️ **Voice Detection & Analysis**
- ⚠️ **Emergency Alert System**
- 🔋 **Low Power Consumption Mode**
- 📊 **Real-time Data Logging & Visualization**
- 🛑 **Manual & Automatic Emergency Triggers**
- 📱 **User-Friendly Mobile Interface**

## 🛠️ Tech Stack

- **Frontend:** Flutter
- **Backend:** Firebase / fastapi
- **Hardware:** Arduino + Heart Rate Sensor + Microphone Module + Bluetooth/WiFi Module
- **Database:** Firebase Firestore (for storing emergency contacts & logs, as well as user information)


## 🔔 Emergency Alert System

- **Automatic Triggers:**
  - Abnormal heart rate detection.
  - Voice recognition for distress words.
  - No movement detected for an extended period.
- **Manual Trigger:**
  - Pressing the emergency button on the bracelet.
  - Triggering an alert via the app.
- **Emergency Actions:**
  - Sends an SMS/Email to emergency contacts.
  - Initiates a call to predefined numbers.
  - Sends GPS location for immediate assistance.
