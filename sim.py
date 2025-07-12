import time
import random
import argparse
import requests
import json

# Argument parser
parser = argparse.ArgumentParser(description="Simulate device data upload.")
parser.add_argument('--mac', type=str, default="00:11:22:33:44:55", help="MAC address of the device")
args = parser.parse_args()

# Config
ENDPOINT = "https://dashboard.render.com/api/device/data-upload/"
MAC_ADDRESS = args.mac
UPLOAD_INTERVAL = 5  # seconds

# Initial simulated values
battery_level = 100.0
heart_rate = 75
temperature = 36.5
smoke_level = 0.1
latitude = -11.429
longitude = 34.008

def gradual_change(value, min_val, max_val, step=0.5):
    delta = random.uniform(-step, step)
    value += delta
    return max(min_val, min(max_val, round(value, 2)))

def simulate_upload():
    global battery_level, heart_rate, temperature, smoke_level

    # Gradually change values
    battery_level = max(0, round(battery_level - random.uniform(0.1, 0.5), 2))
    heart_rate = gradual_change(heart_rate, 60, 150)
    temperature = gradual_change(temperature, 35, 45)
    smoke_level = gradual_change(smoke_level, 0.0, 1.0)

    payload = {
        'mac_address': MAC_ADDRESS,
        'reading_type': 'health',
        'heart_rate': heart_rate,
        'temperature': temperature,
        'smoke_level': smoke_level,
        'battery_level': battery_level,
        'latitude': latitude,
        'longitude': longitude,
    }

    try:
        response = requests.post(ENDPOINT, data=payload)
        print("="*50)
        print(f"[{time.strftime('%H:%M:%S')}] Uploading data...")
        print("Payload:")
        print(json.dumps(payload, indent=4))
        print(f"Response [{response.status_code}]:")
        try:
            print(json.dumps(response.json(), indent=4))
        except Exception:
            print(response.text)
        print("="*50)
    except Exception as e:
        print(f"[ERROR] Failed to upload: {e}")

if __name__ == "__main__":
    print(f"Starting data simulation to {ENDPOINT} using MAC: {MAC_ADDRESS} every {UPLOAD_INTERVAL} seconds...")
    while True:
        simulate_upload()
        time.sleep(UPLOAD_INTERVAL)
