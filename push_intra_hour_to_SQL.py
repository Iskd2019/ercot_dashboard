import json
import psycopg2
from psycopg2.extras import execute_values
from datetime import datetime
from pytz import timezone



# PostgreSQL connection
db_conn = psycopg2.connect(
    dbname='postgres',
    user='postgres',
    password='welcome',
    host='localhost',
    port='5432'
)

cursor = db_conn.cursor()

# Load JSON
with open('Intra Hour ercot_filtered_forecast.json', 'r') as f:
    data = json.load(f)

local_tz = timezone('America/Chicago')
# Parse the string into naive datetime:
#dt = datetime.strptime(item['IntervalEnding'], '%m/%d/%Y %H:%M')

# Localize the naive datetime properly:
#dt_localized = local_tz.localize(dt)
local_tz = timezone('America/Chicago')
# Prepare data
records = [
    (
        local_tz.localize(datetime.strptime(item['IntervalEnding'], '%m/%d/%Y %H:%M')),
        item['SystemTotal'],
        item['Model']
    )
    for item in data
]
'''
records = [
    (
        #local_tz = timezone('America/Chicago'),  # or your local timezone (Central Time / ERCOT is usually CT)
        datetime.strptime(item['IntervalEnding'], '%m/%d/%Y %H:%M').replace(tzinfo=local_tz),
        #datetime.strptime(item['IntervalEnding'], '%m/%d/%Y %H:%M'),
        item['SystemTotal'],
        item['Model']
    )
    for item in data
]
'''

# Insert data
cursor.execute('TRUNCATE TABLE ercot_intra_hour_forecast;')

insert_sql = """
INSERT INTO ercot_intra_hour_forecast (interval_ending, system_total, model)
VALUES %s
"""

execute_values(cursor, insert_sql, records)

db_conn.commit()
cursor.close()
db_conn.close()

print("✅ ERCOT Intra-Hour forecast data inserted!")