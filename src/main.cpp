#include <Arduino.h>
#include <WiFi.h>
#include <WebServer.h>
#include <ArduinoOTA.h>

WebServer server(80);

const int sensor = 35;
int analogic;
float voltage = 0.0;
float NTU = 0;

void setup() {
  Serial.begin(115200);
  pinMode(sensor, INPUT);
  delay(100);

  // Set up the ESP32 as an access point
  const char *ssid = "ESP32_AP";
  const char *password = "12345678";
  WiFi.softAP(ssid, password);

  IPAddress IP = WiFi.softAPIP();
  Serial.print("AP IP address: ");
  Serial.println(IP);

  // Configuração OTA
  ArduinoOTA.setHostname("esp32dev");  // Define o hostname para OTA

  ArduinoOTA.onStart([]() {
    String type;
    if (ArduinoOTA.getCommand() == U_FLASH) {
      type = "sketch";
    } else { // U_SPIFFS
      type = "filesystem";
    }
    Serial.println("Start updating " + type);
  });

  ArduinoOTA.onEnd([]() {
    Serial.println("\nEnd");
  });

  ArduinoOTA.onProgress([](unsigned int progress, unsigned int total) {
    Serial.printf("Progress: %u%%\r", (progress / (total / 100)));
  });

  ArduinoOTA.onError([](ota_error_t error) {
    Serial.printf("Error[%u]: ", error);
    if (error == OTA_AUTH_ERROR) {
      Serial.println("Auth Failed");
    } else if (error == OTA_BEGIN_ERROR) {
      Serial.println("Begin Failed");
    } else if (error == OTA_CONNECT_ERROR) {
      Serial.println("Connect Failed");
    } else if (error == OTA_RECEIVE_ERROR) {
      Serial.println("Receive Failed");
    } else if (error == OTA_END_ERROR) {
      Serial.println("End Failed");
    }
  });

  ArduinoOTA.begin();
  Serial.println("OTA iniciado");

  // Inicia o servidor local
  server.on("/", []() {
    analogic = analogRead(sensor);
    voltage = analogic * (3.3 / 4095.0);
    NTU = map(voltage * 1000, 1000, 1530, 200, 0);
    NTU = constrain(NTU, 0, 1000);
    server.send(200, "text/plain", String(NTU));
  });

  server.begin();
  Serial.println("Servidor HTTP iniciado");
}

void loop() {
  ArduinoOTA.handle();  // Processa OTA
  server.handleClient();

  analogic = analogRead(sensor);
  voltage = analogic * (3.3 / 4095.0);
  NTU = map(voltage * 1000, 1000, 1530, 200, 0);
  NTU = constrain(NTU, 0, 1000);

  delay(100); // Reduzir o delay para melhorar a resposta
}