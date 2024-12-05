import sqlite3
import time
import requests
from datetime import datetime
import os
from db_config import DB_PATH, TABLE_NAME

TABLE_NAME = 'turbidity_data'
ESP32_IP = '192.168.4.1'  # Default IP for ESP32 AP




def init_database():
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute(f'''CREATE TABLE IF NOT EXISTS {TABLE_NAME} (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        date TEXT,
                        turbidity REAL
                     )''')
        conn.commit()
        return conn
    except sqlite3.Error as e:
        print(f"Database initialization error: {e}")
        return None

def main():
    conn = init_database()
    if not conn:
        return

    # Connect to ESP32 AP
    os.system('nmcli dev wifi connect ESP32_AP password 12345678')

    try:
        while True:
            try:
                response = requests.get(f'http://{ESP32_IP}')

                if response.status_code == 200:
                    print('Connection Success!')
                    ntu_str = response.text.strip()  

                    try:
                        ntu = float(ntu_str)  
                        data_str = datetime.now().strftime("%d/%m/%Y")

                        cursor = conn.cursor()
                        cursor.execute(f'INSERT INTO {TABLE_NAME} (date, turbidity) VALUES (?, ?)',
                                   (data_str, ntu))
                        conn.commit()  

                        print(f"Dados salvos no DB: {data_str}, {ntu} NTU")
                    except ValueError:
                        print(f"Erro ao converter o valor de NTU: {ntu_str}")
                    except sqlite3.Error as e:
                        print(f"Erro ao inserir dados no banco de dados: {e}")
                else:
                    print(f"Erro ao acessar o ESP32: {response.status_code}")

            except Exception as e:
                print(f"Erro: {e}")

            time.sleep(10)
    finally:
        conn.close()

if __name__ == "__main__":
    main()