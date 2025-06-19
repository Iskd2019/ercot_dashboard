import json
import psycopg2
from psycopg2.extras import execute_values
from datetime import datetime

# Load the JSON result
with open("ercot_demand_plus_totalCharging.json", "r") as f:
    records = json.load(f)

# Prepare data for insert
data_to_insert = [
    (
        datetime.strptime(row['timestamp'], '%Y-%m-%d %H:%M:%S%z'),
        row['demand'],
        row['forecast']
    )
    for row in records
]

# Connect to PostgreSQL
conn = psycopg2.connect(
    dbname='postgres',
    user='postgres',
    password='welcome',
    host='localhost',
    port='5432'
)

cur = conn.cursor()

# Insert with UPSERT
sql = """
INSERT INTO ercot_demand_plus_totalcharging (timestamp, demand, forecast)
VALUES %s
ON CONFLICT (timestamp) DO UPDATE
SET demand = EXCLUDED.demand,
    forecast = EXCLUDED.forecast;
"""

execute_values(cur, sql, data_to_insert)
conn.commit()
cur.close()
conn.close()

print("✅ ercot_demand_plus_totalcharging Data pushed to PostgreSQL")