import sqlite3
from datetime import datetime, timedelta
import numpy as np
import matplotlib.pyplot as plt

# Database and table configuration
DB_NAME = "turbidity.db"
TABLE_NAME = "turbidity"

# Connect to SQLite database
conn = sqlite3.connect(DB_NAME)
cursor = conn.cursor()

# Create table
cursor.execute(f'''
    CREATE TABLE IF NOT EXISTS {TABLE_NAME} (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        date TEXT,
        turbidity REAL
    )
''')

# Function to simulate the exponential growth curve
def exponential_growth_curve(day_point, max_turbidity, growth_rate):
    """
    Exponential growth model to simulate bacterial turbidity growth.
    Parameters:
        day_point (float): Time point in days.
        max_turbidity (float): Maximum turbidity (asymptote).
        growth_rate (float): Growth rate.
    Returns:
        float: Turbidity value at the given time point.
    """
    return max_turbidity * (1 - np.exp(-growth_rate * day_point))

# Generate fake data for 20 days starting from 22/11/2024
start_date = datetime.strptime("22/11/2024", "%d/%m/%Y")
end_date = start_date + timedelta(days=19)
time_interval = timedelta(days=1)

max_turbidity = 870  # NTU
growth_rate = 0.3    # Determines the steepness of the curve

current_date = start_date
data = []

day_counter = 0
while current_date <= end_date:
    turbidity = exponential_growth_curve(day_counter, max_turbidity, growth_rate)
    data.append((current_date.strftime("%d/%m/%Y"), turbidity))
    current_date += time_interval
    day_counter += 1

# Insert data into the database
cursor.executemany(f"INSERT INTO {TABLE_NAME} (date, turbidity) VALUES (?, ?)", data)

# Commit changes and close connection
conn.commit()
conn.close()

print(f"Database '{DB_NAME}' created and populated with fake data.")

# Plot the data to visualize the exponential growth
dates, turbidities = zip(*data)
plt.plot(dates, turbidities, marker='o')
plt.xlabel('Date')
plt.ylabel('Turbidity (NTU)')
plt.title('Exponential Growth of Bacterial Turbidity')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()