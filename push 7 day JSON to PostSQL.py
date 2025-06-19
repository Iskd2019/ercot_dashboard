import json
import psycopg2
from psycopg2.extras import execute_values
from datetime import datetime, timedelta

# PostgreSQL connection info
db_conn = psycopg2.connect(
    dbname='postgres',
    user='postgres',
    password='welcome',
    host='localhost',
    port='5432'
)

cursor = db_conn.cursor()

# Load JSON
with open('7 days ercot_forecast_filtered.json', 'r') as f:
    data = json.load(f)

# Helper to convert DeliveryDate + HourEnding → timestamp
def convert_to_timestamp(delivery_date_str, hour_ending_str):
    # Convert delivery date
    dt_date = datetime.strptime(delivery_date_str, '%m/%d/%Y')
    # Extract hour
    hour = int(hour_ending_str.split(':')[0])
    if hour == 24:
        # Special case: 24:00 → next day at 00:00
        dt_date += timedelta(days=1)
        hour = 0
    dt_datetime = dt_date.replace(hour=hour)
    return dt_datetime

# Prepare data for batch insert
records = [
    (
        convert_to_timestamp(item['DeliveryDate'], item['HourEnding']),
        item['SystemTotal']
    )
    for item in data
]

# Insert — optional: truncate first if you want clean data each time
cursor.execute('TRUNCATE TABLE ercot_seven_day_forecast;')

insert_sql = """
INSERT INTO ercot_seven_day_forecast (timestamp, system_total)
VALUES %s
"""

execute_values(cursor, insert_sql, records)

db_conn.commit()
cursor.close()
db_conn.close()

print("✅ ERCOT 7 Days forecast data inserted into PostgreSQL!")