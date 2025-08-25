# File: local_predictor.py

import requests
import time
import joblib
import numpy as np

# --- Configuration ---
# Replace with your ThingSpeak Channel ID and Read API Key
READ_API_KEY = 'YOUR_READ_API_KEY' # 👈 Replace with your Key
CHANNEL_ID = 'YOUR_CHANNEL_ID'     # 👈 Replace with your Channel ID
CHECK_INTERVAL_SECONDS = 30        # Time to wait between checks

# ThingSpeak API URL to fetch the latest data point
THINGSPEAK_URL = f'https://api.thingspeak.com/channels/{CHANNEL_ID}/feeds/last.json?api_key={READ_API_KEY}'

def load_model(model_path='fire_detection_model.joblib'):
    """Loads the trained model from the specified path."""
    try:
        model = joblib.load(model_path)
        print(f"✅ Machine learning model '{model_path}' loaded successfully.")
        return model
    except FileNotFoundError:
        print(f"❌ Error: Model file '{model_path}' not found.")
        print("Please run 'train_model.py' first to create it.")
        return None

def main():
    """
    Main loop to fetch data from ThingSpeak and run predictions.
    """
    model = load_model()
    if model is None:
        return

    print("\n--- Starting Live Fire Prediction ---")
    print(f"Checking ThingSpeak every {CHECK_INTERVAL_SECONDS} seconds. Press Ctrl+C to stop.")
    print("-" * 35)

    while True:
        try:
            # 1. Fetch data from ThingSpeak
            response = requests.get(THINGSPEAK_URL, timeout=10)
            response.raise_for_status()  # Raise an HTTPError for bad responses
            
            data = response.json()
            
            # 2. Process the data
            if data and 'field1' in data and 'field2' in data:
                temp = data.get('field1')
                smoke = data.get('field2')

                if temp is None or smoke is None:
                    print(f"[{time.ctime()}] Waiting for valid data... Last entry was partial.")
                else:
                    temp_f = float(temp)
                    smoke_f = float(smoke)
                    
                    print(f"[{time.ctime()}] Data received: Temp={temp_f}, Smoke={smoke_f}")

                    # 3. Make a prediction
                    features = np.array([[temp_f, smoke_f]])
                    prediction = model.predict(features)

                    if prediction[0] == 1:
                        print("🚨 PREDICTION: FIRE DETECTED! 🚨\n")
                    else:
                        print("✅ PREDICTION: No Fire Detected.\n")
            else:
                print(f"[{time.ctime()}] Channel is empty or data is malformed. Waiting...")

        except requests.exceptions.RequestException as e:
            print(f"⚠️ Network Error: Could not connect to ThingSpeak. Retrying... ({e})")
        except (KeyError, ValueError):
            print("⚠️ Data Error: Received unexpected data format from ThingSpeak. Retrying...")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")

        # Wait before the next check
        time.sleep(CHECK_INTERVAL_SECONDS)

if __name__ == '__main__':
    main()
