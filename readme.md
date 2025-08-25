# Local Fire Detection System with ESP32 and ThingSpeak

This project implements a real-time fire detection system. An ESP32 microcontroller with temperature and smoke sensors sends data to the ThingSpeak cloud platform. A local Python script then fetches this data, processes it through a trained machine learning model, and predicts the likelihood of a fire.

---

## 🏛️ Architecture

The data flows through the system as follows:

**[ESP32 + Sensors]** --- (Wi-Fi) ---> **[ThingSpeak Cloud]** --- (Internet) ---> **[Local Python Script on your PC]** ---> **[Prediction Output]**

---

## 📋 Prerequisites

### Hardware
* An ESP32 development board.
* A temperature sensor (like DHT11 or DHT22).
* A smoke/gas sensor (like MQ-2).
* A breadboard and jumper wires.

### Software
* [Arduino IDE](https://www.arduino.cc/en/software) with the ESP32 board manager installed.
* [Python 3.7+](https://www.python.org/downloads/).
* A free [ThingSpeak](https://thingspeak.com/) account.
* The `fire_data.csv` file in your project directory.

---

## 🚀 Step-by-Step Setup Guide

Follow these four parts in order to get the system running.

### Part 1: Train the Machine Learning Model

This step only needs to be done once. It reads your dataset and creates the `fire_detection_model.joblib` file.

1.  **Install Python Libraries**: Open your terminal or command prompt and run:
    ```bash
    pip install pandas scikit-learn joblib
    ```
2.  **Run the Training Script**: In the same terminal, navigate to your project folder and execute the script:
    ```bash
    python train_model.py
    ```
3.  **Verify the Output**: A new file named `fire_detection_model.joblib` will be created in your folder. This is your trained model.

### Part 2: Configure ThingSpeak

1.  **Create a New Channel**: Log in to ThingSpeak, go to **Channels > My Channels**, and click **New Channel**.
2.  **Configure Fields**:
    * Name the channel (e.g., "Fire Detection Sensor").
    * Enable **Field 1** and name it `Temperature`.
    * Enable **Field 2** and name it `Smoke`.
    * Click **Save Channel**.
3.  **Get API Keys**: Go to the **API Keys** tab of your new channel. You will need to copy three values:
    * **Channel ID**
    * **Write API Key**
    * **Read API Key**

### Part 3: Program the ESP32

This code reads the sensor data and sends it to ThingSpeak.

1.  **Open the Sketch**: Open the `esp32_thingspeak_sender.ino` file in your Arduino IDE.
2.  **Update Credentials**: Modify the following lines at the top of the file with your own credentials:
    ```cpp
    const char* ssid = "YOUR_WIFI_SSID";
    const char* password = "YOUR_WIFI_PASSWORD";
    String writeAPIKey = "YOUR_WRITE_API_KEY"; // From ThingSpeak
    ```
3.  **Connect Hardware**: Wire your temperature and smoke sensors to the ESP32. Make sure the pins you use match the pins in the Arduino code.
4.  **Upload the Code**: Connect your ESP32 to your computer, select the correct board and COM port in the Arduino IDE, and click the "Upload" button.
5.  **Check the Serial Monitor**: Open the Serial Monitor (`Tools > Serial Monitor`) to see the sensor readings and confirm that data is being sent to ThingSpeak.

### Part 4: Run the Local Predictor

This is the final step. This script will run continuously on your PC to check for new data and make predictions.

1.  **Install Python Libraries**: If you haven't already, install the `requests` library:
    ```bash
    pip install requests numpy
    ```
2.  **Update Credentials**: Open the `local_predictor.py` file and modify the following lines with your ThingSpeak channel details:
    ```python
    READ_API_KEY = 'YOUR_READ_API_KEY'
    CHANNEL_ID = 'YOUR_CHANNEL_ID'
    ```
3.  **Run the Predictor**: In your terminal, run the script:
    ```bash
    python local_predictor.py
    ```

You should now see the script fetching the latest data from ThingSpeak every 30 seconds and printing a fire prediction in your terminal. **Success!** 🎉
