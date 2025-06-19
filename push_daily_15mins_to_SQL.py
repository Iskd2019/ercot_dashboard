import json
import psycopg2
from psycopg2.extras import execute_values
from datetime import datetime

# PostgreSQL connection
# 数据库连接参数
db_conn = psycopg2.connect(
    dbname='postgres',
    user='postgres',
    password='welcome',
    host='localhost',
    port='5432'
)

cursor = db_conn.cursor()

# Load JSON
with open('ercot_15min_aligned_avg.json', 'r') as f:
    data = json.load(f)

# Prepare data
records = [
    (
        datetime.strptime(item['timestamp'], '%Y-%m-%d %H:%M:%S%z'),
        item['demand'],
        item['forecast']
    )
    for item in data
]

# Insert with upsert (to avoid duplicates)
insert_sql = """
INSERT INTO ercot_supply_demand_15min (timestamp, demand, forecast)
VALUES %s
ON CONFLICT (timestamp) DO UPDATE SET
    demand = EXCLUDED.demand,
    forecast = EXCLUDED.forecast;
"""

execute_values(cursor, insert_sql, records)

db_conn.commit()
cursor.close()
db_conn.close()

print("✅ ERCOT 15 mins supply/demand data inserted!")