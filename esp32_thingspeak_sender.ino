#include <WiFi.h>
#include <HTTPClient.h>
#include "DHT.h"

// ------------ WiFi Setup ------------
const char* ssid = "FALCONE";       
const char* password = "Kushal@7719270241"; 

// ------------ ThingSpeak Setup ------------
String apiKey = "HSHG3JAUXGAOHYBS";
const char* server = "http://api.thingspeak.com/update";

// ------------ Sensor Setup ------------
#define DHTPIN 4
#define DHTTYPE DHT11
DHT dht(DHTPIN, DHTTYPE);

#define MQ135_PIN 34      // Air quality
#define MQ2_PIN 35        // Smoke
#define FLAME_ANALOG_PIN 32 // Flame analog output (AO)
#define FLAME_DIGITAL_PIN 26 // Flame digital output (DO)

#define MQ2_THRESHOLD 1650       // Raw ADC threshold for smoke alert
#define FLAME_THRESHOLD 1000     // Raw ADC threshold for flame alert
#define BUZZER_PIN 25   // Buzzer connected to GPIO 25


unsigned long lastThingSpeak = 0;    // last upload timestamp
const unsigned long intervalTS = 20000; // 20s upload interval

// ------------ Setup ------------
void setup() {
  Serial.begin(115200);
  dht.begin();

  pinMode(FLAME_DIGITAL_PIN, INPUT);
  pinMode(BUZZER_PIN, OUTPUT);
  digitalWrite(BUZZER_PIN, LOW); // buzzer OFF initially


  WiFi.begin(ssid, password);
  Serial.print("Connecting to WiFi");
  int retries = 0;
  while (WiFi.status() != WL_CONNECTED && retries < 20) {
    delay(500);
    Serial.print(".");
    retries++;
  }
  if (WiFi.status() == WL_CONNECTED) {
    Serial.println("\nWiFi Connected!");
  } else {
    Serial.println("\nWiFi Failed!");
  }

}

// ------------ Loop ------------
void loop() {
  // Read sensors
  float temp = dht.readTemperature();
  int airQuality = analogRead(MQ135_PIN);
  int mq2Value = analogRead(MQ2_PIN);
  int flameADC = analogRead(FLAME_ANALOG_PIN);
  int flameDO = digitalRead(FLAME_DIGITAL_PIN); // 0 = Fire detected

  if (isnan(temp)) {
    Serial.println("Failed to read temperature!");
    delay(2000);
    return;
  }

  // Serial output every 2s
  Serial.print("Temp: "); Serial.print(temp); Serial.print(" °C | ");
  Serial.print("Air MQ135: "); Serial.print(airQuality); Serial.print(" | ");
  Serial.print("MQ2: "); Serial.print(mq2Value); 
  if (mq2Value > MQ2_THRESHOLD) Serial.print(" ⚠️ Smoke High!");
  Serial.print(" | Flame ADC: "); Serial.print(flameADC);
  if (flameADC < FLAME_THRESHOLD) Serial.print(" 🔥 Flame Detected!");
  Serial.print(" | Flame DO: "); Serial.println(flameDO == 0 ? "🔥 Fire!" : "No Fire");

  // 🔔 Buzzer control
  if (flameDO == 0) {  
    digitalWrite(BUZZER_PIN, HIGH);   // Fire detected → buzzer ON
  } else {
    digitalWrite(BUZZER_PIN, LOW);    // No fire → buzzer OFF
  }

  // ThingSpeak upload every 20s
  unsigned long now = millis();
  if (now - lastThingSpeak >= intervalTS) {
    lastThingSpeak = now;

    if (WiFi.status() == WL_CONNECTED) {
      HTTPClient http;
      String url = String(server) + "?api_key=" + apiKey;
      url += "&field1=" + String(temp, 2);
      url += "&field2=" + String(airQuality);
      url += "&field3=" + String(mq2Value);
      //url += "&field4=" + String(flameADC);
      url += "&field4=" + String(flameDO);

      http.begin(url.c_str());
      int httpCode = http.GET();
      if (httpCode == 200) {
        Serial.println("Data sent to ThingSpeak!");
      } else {
        Serial.print("Error code: "); Serial.println(httpCode);
      }
      http.end();
    }
  }

  delay(2000); // 2s between Serial prints
}
