#include <Arduino.h>
#include <WiFi.h>
#include <ESPmDNS.h>
#include <WiFiUdp.h>
#include <ArduinoOTA.h>
#include <time.h>
#include "credentials.h"

const int sensor = 35;
int analogic;
float voltage = 0.0;
float NTU = 0;
const long gmtOffset_sec = -10800;

void setup()
{
  Serial.begin(115200);
  pinMode(sensor, INPUT);
  delay(100);

  Serial.println("Booting ESP32-1- OTA");
  WiFi.mode(WIFI_STA);
  WiFi.begin(ssid, password);
  while (WiFi.waitForConnectResult() != WL_CONNECTED)
  {
    Serial.println("Connection Failed! Rebooting...");
    delay(5000);
    ESP.restart();
  }

  ArduinoOTA.setHostname("ESP32-1");

  ArduinoOTA
      .onStart([]()
               {
      String type;
      if (ArduinoOTA.getCommand() == U_FLASH)
        type = "sketch";
      else // U_SPIFFS
        type = "filesystem";

      Serial.println("Start updating " + type); })
      .onEnd([]()
             { Serial.println("\nEnd"); })
      .onProgress([](unsigned int progress, unsigned int total)
                  { Serial.printf("Progress: %u%%\r", (progress / (total / 100))); })
      .onError([](ota_error_t error)
               {
      Serial.printf("Error[%u]: ", error);
      if (error == OTA_AUTH_ERROR) Serial.println("Auth Failed");
      else if (error == OTA_BEGIN_ERROR) Serial.println("Begin Failed");
      else if (error == OTA_CONNECT_ERROR) Serial.println("Connect Failed");
      else if (error == OTA_RECEIVE_ERROR) Serial.println("Receive Failed");
      else if (error == OTA_END_ERROR) Serial.println("End Failed"); });

  ArduinoOTA.begin();

  configTime(gmtOffset_sec, 0, "pool.ntp.org", "time.nist.gov");
  delay(2000);

  Serial.println("Ready");
  Serial.print("IP address: ");
  Serial.println(WiFi.localIP());
}

void loop()
{
  ArduinoOTA.handle();

  analogic = analogRead(sensor);
  voltage = analogic * (3.3 / 4095.0);

  NTU = map(voltage * 1000, 1000, 1530, 200, 0);
  NTU = constrain(NTU, 0, 1000);

  struct tm timeinfo;
  if (!getLocalTime(&timeinfo))
  {
    Serial.println("Falha ao obter a data");
    return;
  }

  char dateString[11];
  strftime(dateString, sizeof(dateString), "%d/%m/%Y", &timeinfo);

  Serial.print(dateString);
  Serial.print(", ");
  Serial.println(NTU);

  delay(10000);
}
