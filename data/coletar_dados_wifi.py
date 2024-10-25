import sqlite3
import time
import requests
from datetime import datetime

TABLE_NAME = 'turbidity_data'
ESP32_IP = ''

conn = sqlite3.connect('turbidity_data.db')
cursor = conn.cursor()

cursor.execute(f'''CREATE TABLE IF NOT EXISTS {TABLE_NAME} (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    date TEXT,
                    turbidity REAL
                 )''')

while True:
    try:
        response = requests.get(ESP32_IP)

        if response.status_code == 200:
            print('Connection Success!')
            ntu_str = response.text.strip()  

            try:
                ntu = float(ntu_str)  
                data_str = datetime.now().strftime("%d/%m/%Y")

                
                cursor.execute(f'INSERT INTO {TABLE_NAME} (date, turbidity) VALUES (?, ?)',
                               (data_str, ntu))
                conn.commit()  

                print(f"Dados salvos no DB: {data_str}, {ntu} NTU")
            except ValueError:
                print(f"Erro ao converter o valor de NTU: {ntu_str}. Certifique-se de que é um número válido.")
            except sqlite3.Error as e:
                print(f"Erro ao inserir dados no banco de dados: {e}")
        else:
            print(f"Erro ao acessar o ESP32: {response.status_code}")

    except Exception as e:
        print(f"Erro: {e}")

    time.sleep(10)
