import requests
import random
import json
import time

url = 'https://my-guardian-plus.onrender.com/api/devices/data/'
mac_address = '24:FB:65:99:27:BE'

VALID_READING_TYPES = ['heart_rate', 'temperature', 'smoke', 'location', 'battery']

def generate_mock_data():
    reading_type = random.choice(VALID_READING_TYPES)
    base_data = {
        'mac_address': mac_address,
        'reading_type': reading_type,
        'raw_data': json.dumps({
            'stress_level': round(random.uniform(0.0, 1.0), 2),
            'fear_probability': round(random.uniform(0.0, 1.0), 2)
        }),
    }

    if reading_type == 'heart_rate':
        base_data['heart_rate'] = random.randint(60, 130)
    elif reading_type == 'temperature':
        base_data['temperature'] = round(random.uniform(36.0, 40.0), 2)
    elif reading_type == 'smoke':
        base_data['smoke_level'] = round(random.uniform(0.0, 5.0), 2)
    elif reading_type == 'battery':
        base_data['battery_level'] = random.randint(5, 100)
    elif reading_type == 'location':
        base_data['latitude'] = round(-11.415223026341934, 6) #round(random.uniform(-90.0, 90.0), 6)
        base_data['longitude'] = round(33.99602455950148, 6) #round(random.uniform(-180.0, 180.0), 6)
        # -11.415223026341934, 33.99602455950148

    return base_data

def send_data_loop(interval=0.5):
    while True:
        data = generate_mock_data()

        try:
            response = requests.post(url, data=data)
            print("\n📤 Sent Data:", data)
            print(f"✅ Response [{response.status_code}]:", response.json())
        except Exception as e:
            print("❌ Error sending data:", e)

        time.sleep(interval)

if __name__ == "__main__":
    send_data_loop()
