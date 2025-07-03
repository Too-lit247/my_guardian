import requests
import random
import time

# List of MAC addresses for devices to simulate
DEVICE_MACS = [
    "00:11:22:33:44:55",
    "AA:BB:CC:DD:EE:FF",
    "12:34:56:78:9A:BC"
]

ENDPOINT = "http://localhost:8000/api/devices/data-upload/"

def random_reading(mac):
    return {
        "mac_address": mac,
        "reading_type": random.choice(["heart_rate", "temperature", "smoke", "battery", "location"]),
        "heart_rate": random.randint(60, 180),
        "temperature": round(random.uniform(36.0, 55.0), 1),
        "smoke_level": round(random.uniform(0.0, 1.0), 2),
        "battery_level": random.randint(10, 100),
        "latitude": round(random.uniform(-13.98, -13.95), 6),
        "longitude": round(random.uniform(33.75, 33.80), 6),
        "raw_data": {}
    }

def simulate_uploads(num=10, delay=2):
    for _ in range(num):
        mac = random.choice(DEVICE_MACS)
        data = random_reading(mac)
        print(f"Uploading data for {mac}: {data}")
        try:
            resp = requests.post(ENDPOINT, data=data)
            print(f"Status: {resp.status_code} | Response: {resp.text}")
        except Exception as e:
            print(f"Error uploading data: {e}")
        time.sleep(delay)

if __name__ == "__main__":
    simulate_uploads(num=20, delay=1)