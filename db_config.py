# db_config.py
import os

DB_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'turbidity_data.db')
TABLE_NAME = 'turbidity_data'