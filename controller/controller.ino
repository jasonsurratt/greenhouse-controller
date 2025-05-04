
#include <DHT.h>
#include <HTTPClient.h>
#include <WiFi.h>

// contains local settings such as server URL & wifi settings
#include "config.h"

DHT dht(DHTPIN, DHTTYPE);

void setup() {
  Serial.begin(115200);
  
  // Enable internal pull-up resistor for GPIO4
  // If your chip has 4 pins you may need to use INPUT_PULLUP here.
  pinMode(DHTPIN, INPUT);

  // Connect to WiFi
  WiFi.begin(WIFI_SSID, WIFI_PASSWORD);
  Serial.print("Connecting to WiFi");
  
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  
  Serial.println("");
  Serial.println("WiFi connected!");
  Serial.print("IP address: ");
  Serial.println(WiFi.localIP());
}

int collect_temperature(DHT& dht) {
    // Reading temperature and humidity takes about 250 milliseconds
  float humidity = dht.readHumidity();
  float temperature = dht.readTemperature();
  float temperatureF = dht.readTemperature(true); // Fahrenheit
  
  // Check if any reads failed and exit early (to try again)
  if (isnan(humidity) || isnan(temperature) || isnan(temperatureF)) {
    return -1;
  }
  
  // Compute heat index in Fahrenheit and Celsius
  float heatIndexF = dht.computeHeatIndex(temperatureF, humidity);
  float heatIndexC = dht.computeHeatIndex(temperature, humidity, false);
  
  // Print the results
  Serial.print("Humidity: ");
  Serial.print(humidity);
  Serial.print("%  Temperature: ");
  Serial.print(temperature);
  Serial.print("°C ");
  Serial.print(temperatureF);
  Serial.print("°F  Heat index: ");
  Serial.print(heatIndexC);
  Serial.print("°C ");
  Serial.print(heatIndexF);
  Serial.println("°F");

  return 0;
}

void loop() {

  int err = collect_temperature(dht);
  if (err != 0) {
    Serial.println("Failed to read from DHT sensor.");
  }

  // Send status to server
  if (err == 0 && WiFi.status() == WL_CONNECTED) {
    HTTPClient http;
    
    // Specify the URL
    http.begin(SERVER_URL);
    
    // Specify content-type header
    http.addHeader("Content-Type", "application/json");
    
    // Prepare your data
    String jsonData = "{\"sensor\":\"temperature\",\"value\":25.5,\"unit\":\"celsius\"}";
    
    // Send POST request
    int httpResponseCode = http.POST(jsonData);
    
    // Check response
    if (httpResponseCode > 0) {
      Serial.print("HTTP Response code: ");
      Serial.println(httpResponseCode);
      
      String response = http.getString();
      Serial.println("Response:");
      Serial.println(response);
    } else {
      Serial.print("Error code: ");
      Serial.println(httpResponseCode);
    }
    
    // Free resources
    http.end();
  } else {
    Serial.println("WiFi Disconnected...");
  }
  
  delay(3000);  // Wait before sending again (in ms)
}