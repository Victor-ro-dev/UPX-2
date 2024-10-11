#include <Arduino.h>
#include <WiFi.h>
#include <ArduinoOTA.h>
#include <Wire.h>

float ArredondarPara(float ValorEntrada, int CasaDecimal);
// Define o pino de Leitura do Sensor
int SensorTurbidez = 34;

// Inicia as variáveis
int i;
float voltagem;
float NTU;

const char *ssid = ""; // Nome da sua Rede
const char *password = ""; // Senha da sua Rede

void setup()
{
  Serial.begin(115200);
  delay(1000);

  Serial.println("Conectando ao WiFi...");
  WiFi.begin(ssid, password);

  while (WiFi.status() != WL_CONNECTED)
  {
    delay(1000);
    Serial.print(".");
  }

  Serial.println();
  Serial.println("Conectado ao WiFi!");
  Serial.println(WiFi.localIP());

  ArduinoOTA.onStart([]()
                     {
        String type;
        if (ArduinoOTA.getCommand() == U_FLASH) {
            type = "sketch";
        } else { // U_SPIFFS
            type = "filesystem";
        }
        Serial.println("Iniciando upload: " + type); });

  ArduinoOTA.onEnd([]()
                   { Serial.println("\nUpload concluído!"); });

  ArduinoOTA.onProgress([](unsigned int progress, unsigned int total)
                        { Serial.printf("Progresso: %u%%\r", (progress / (total / 100))); });

  ArduinoOTA.onError([](ota_error_t error)
                     {
        Serial.printf("Erro [%u]: ", error);
        if (error == OTA_AUTH_ERROR) {
            Serial.println("Falha na autenticação");
        } else if (error == OTA_BEGIN_ERROR) {
            Serial.println("Falha ao começar");
        } else if (error == OTA_CONNECT_ERROR) {
            Serial.println("Falha ao conectar");
        } else if (error == OTA_RECEIVE_ERROR) {
            Serial.println("Falha ao receber");
        } else if (error == OTA_END_ERROR) {
            Serial.println("Falha ao finalizar");
        } });

  ArduinoOTA.begin();
  Serial.println("Pronto para OTA!");
}

void loop()
{
  ArduinoOTA.handle();
  // Inicia a leitura da voltagem em 0
  voltagem = 0;

  // Realiza a soma dos "i" valores de voltagem
  for (i = 0; i < 800; i++)
  {
    voltagem += ((float)analogRead(SensorTurbidez) / 4095) * 3.3;
  }

  // Realiza a média entre os valores lidos na função for acima
  voltagem = voltagem / 800;
  voltagem = ArredondarPara(voltagem, 1);

  // Se Voltagem menor que 2.5 fixa o valor de NTU
  if (voltagem < 0.5)
  {
    NTU = 3000; // Alta turbidez quando a voltagem está abaixo de 0.5V
  }
  else if (voltagem > 3.0)
  {                 // Ajustado para 3.0V
    NTU = 0;        // Baixa turbidez quando a voltagem está acima de 3.0V
    voltagem = 3.0; // Limitar a voltagem a 3.0V para não ultrapassar
  }

  // Senão calcula o valor de NTU através da fórmula
  else
  {
    NTU = -1120.4 * (voltagem * voltagem) + (5742.3 * voltagem) - 4353.8;
  }

  // Imprime as informações na tela do LCD

  Serial.print("Leitura: ");
  Serial.print(voltagem);
  Serial.println(" V");
  Serial.print(" | ");

  // Imprime as informações na tela do LCD

  Serial.print(NTU);
  Serial.print(" NTU");
  delay(1000);
}

// Sistema de arredendamento para Leitura
float ArredondarPara(float ValorEntrada, int CasaDecimal)
{
  float multiplicador = powf(10.0f, CasaDecimal);
  ValorEntrada = roundf(ValorEntrada * multiplicador) / multiplicador;
  return ValorEntrada;
}
