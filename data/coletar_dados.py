import serial
import sqlite3
import time
from datetime import datetime

TABLE_NAME = 'turbidity_data'


ser = serial.Serial('COM6', 115200, timeout=1)
time.sleep(2)  


conn = sqlite3.connect('turbidity_data.db')
cursor = conn.cursor()

cursor.execute(f'''CREATE TABLE IF NOT EXISTS {TABLE_NAME} (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    date TEXT,
                    turbidity REAL
                 )''')

while True:
    if ser.in_waiting > 0:
        line = ser.readline().decode('utf-8').strip()

        if ',' in line:
            try:
                data_str, ntu = line.split(',')

                data_str = data_str.strip()
                ntu = ntu.strip()
                
                data = datetime.strptime(data_str, "%d/%m/%Y").date()

                cursor.execute(f'INSERT INTO {TABLE_NAME} (date, turbidity) VALUES (?, ?)',
                               (data.isoformat(), float(ntu))) 
                conn.commit()

                print(f"Dados salvos no DB: {data}, {ntu} NTU")
            except ValueError as e:
               
                print(f"Erro ao processar a linha: {line} - {e}")
        
        time.sleep(1)  
