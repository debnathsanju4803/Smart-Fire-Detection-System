# File: local_predictor.py

import requests
import time
import joblib
import numpy as np

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# --- Configuration ---
# Replace with your ThingSpeak Channel ID and Read API Key
READ_API_KEY = 'P43NJGYZP6H53MI4' # 👈 Replace with your Key
CHANNEL_ID = '3048434'     # 👈 Replace with your Channel ID
CHECK_INTERVAL_SECONDS = 20        # Time to wait between checks

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

def send_email_alert(subject, body, to_email):
    sender_email = "debnathsanju4803@gmail.com"
    app_password = "ulkl usvl izwm aoao"

    msg = MIMEMultipart()
    msg["From"] = sender_email
    msg["To"] = to_email
    msg["Subject"] = subject
    
    msg.attach(MIMEText(body, 'plain'))

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(sender_email, app_password)
            server.sendmail(sender_email, to_email, msg.as_string())
        print("📧 Email alert sent successfully.")
    except Exception as e:
        print(f"⚠️ Failed to send email alert. Error: {e}")

def main():
    """
    Main loop to load the model, fetch data from ThingSpeak, and make fire predictions.
    """
    # 1. Load the trained model
    model = load_model()
    if model is None:
        return

    while True:
        try:
            # 2. Fetch the latest data point from ThingSpeak
            print(f"[{time.ctime()}] 🔄 Checking ThingSpeak channel...")
            response = requests.get(THINGSPEAK_URL)
            response.raise_for_status()  # Raise an exception for bad status codes
            data = response.json()

            if 'field1' in data and data['field1'] is not None:
                # Extract the sensor values from the API response
                temp = data['field1']
                air_quality = data['field2']
                smoke = data['field3']
                flame = data['field4']

                # Convert to float for the model
                try:
                    temp_f = float(temp)
                    air_quality_f = float(air_quality)
                    smoke_f = float(smoke)
                    flame_f = float(flame)
                except ValueError:
                    print(f"[{time.ctime()}] ⚠️ Data conversion failed. Skipping this data point.")
                    continue

                print(f"[{time.ctime()}] Data received: Temp={temp_f}, air_quality={air_quality_f}, smoke={smoke_f}, flame={flame_f}")

                # 3. Make a prediction
                features = np.array([[temp_f, air_quality_f, smoke_f, flame_f]])
                prediction = model.predict(features)

                if prediction[0] == 1:
                    print("🚨 PREDICTION: FIRE DETECTED! 🚨\n")
                    # Send alerts
                     send_email_alert(
                         subject="🔥 Fire Alert!",
                         body="Fire has been detected by your IoT system. Please take action immediately!",
                         to_email="recipient@example.com"
                     )
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
