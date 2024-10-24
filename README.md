# Projeto UPX-2: Sensor de Turbidez com Interface Gráfica (GUI)

Este projeto consiste em um script Python que coleta dados de um **sensor de turbidez** e apresenta esses dados por meio de uma **interface gráfica de usuário (GUI)** desenvolvida com Python. O sensor mede a turbidez de um líquido e exibe os resultados em tempo real.

## Funcionalidades

- Leitura em tempo real dos valores do **sensor de turbidez**.
- Apresentação dos dados em uma interface gráfica amigável, permitindo uma visualização clara e acessível das medições.
- Dados são exportados diretamente para um banco de dados **SQLite3**
- Coleta de dados a partir de uma script feito em **Python**

## Tecnologias Usadas

🔹 **Python** para o script de coleta de dados  
🔹 **CustomTkinter** para a criação da GUI  
🔹 **Plataformio** para o ambiente de leitura do senso  
🔹 **SQLite3** para o aramzenamento de dados

## Sensor de Turbidez

O **sensor de turbidez** utilizado neste projeto mede a quantidade de partículas suspensas em um **Fotobiorreator**, retornando um valor que indica o grau de turbidez (0 a 1000 NTU). Os valores são lidos através de uma conexão com o **ESP32**, que envia os dados ao script Python, onde pode ser gerado um gráfico e permite o uso de uma calculadora, que apresenta o dióxido de carbono sequestrado pelo Biorreator.
