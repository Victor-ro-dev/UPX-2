#include <Arduino.h>
#include <WiFi.h>

#define LED_PIN 2 
const char* ssid = ""; //Nome da sua Rede
const char* password = "";  //Senha da sua Rede


void setup() {

  Serial.begin(115200);         
  delay(1000);

  Serial.println("Conectando ao WiFi...");

  WiFi.begin(ssid, password);   
  
  while (WiFi.status() != WL_CONNECTED) {
    delay(1000);
    Serial.print(".");
  }

  Serial.println();
  Serial.println("Conectado ao WiFi!");

}

void loop() {

  
}
