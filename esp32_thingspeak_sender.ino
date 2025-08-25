// File: esp32_thingspeak_sender.ino

#include <WiFi.h>

// --- Wi-Fi Configuration ---
const char* ssid = "YOUR_WIFI_SSID";         // 👈 Replace with your Wi-Fi network name
const char* password = "YOUR_WIFI_PASSWORD"; // 👈 Replace with your Wi-Fi password

// --- ThingSpeak Configuration ---
const char* server = "api.thingspeak.com";
String writeAPIKey = "YOUR_WRITE_API_KEY"; // 👈 Replace with your Key from ThingSpeak

// ThingSpeak allows updates every 15 seconds on the free plan. 20 seconds is a safe interval.
const int updateInterval = 20000; 

void setup() {
  Serial.begin(115200);
  delay(10);

  // Connect to Wi-Fi
  WiFi.mode(WIFI_STA);
  WiFi.begin(ssid, password);
  Serial.print("Connecting to WiFi..");
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("\nWiFi connected!");
  Serial.print("IP Address: ");
  Serial.println(WiFi.localIP());
}

void loop() {
  // --- Simulate Sensor Readings ---
  // In a real scenario, you would replace these lines with actual sensor reading code.
  // For example:
  // float temperature = dht.readTemperature();
  // int smoke = analogRead(MQ2_PIN);
  float temperature = random(20.0, 35.0); // Normal temperature
  int smoke = random(100, 300);            // Normal smoke level

  // Occasionally simulate a fire event for testing
  if (random(0, 10) > 8) {
    Serial.println("!!! Simulating a fire event !!!");
    temperature = random(60.0, 100.0);
    smoke = random(700, 1000);
  }

  // Use a WiFiClient object to connect to the server
  WiFiClient client;
  
  if (client.connect(server, 80)) {
    // Construct the GET request string for the ThingSpeak API
    String postStr = "GET /update?api_key=" + writeAPIKey;
    postStr += "&field1=";
    postStr += String(temperature);
    postStr += "&field2=";
    postStr += String(smoke);
    postStr += " HTTP/1.1\r\n";
    postStr += "Host: api.thingspeak.com\r\n";
    postStr += "Connection: close\r\n\r\n";

    // Send the request to the server
    client.print(postStr);
    
    Serial.print("Data sent -> ");
    Serial.print("Temperature: ");
    Serial.print(temperature);
    Serial.print(", Smoke: ");
    Serial.println(smoke);
  } else {
    Serial.println("Connection to ThingSpeak failed.");
  }
  
  // Close the connection and wait for the next update
  client.stop();
  Serial.println("------------------------------------");
  delay(updateInterval);
}
