import psycopg2

# Replace with your info:
db_conn = psycopg2.connect(
    dbname='postgres',
    user='postgres',
    password='welcome',
    host='localhost',
    port='5432'
)

cursor = db_conn.cursor()

# Simple test query — count rows in your table
cursor.execute('SELECT COUNT(*) FROM ercot_seven_day_forecast;')
count = cursor.fetchone()[0]

print(f'✅ Connected! Table ercot_seven_day_forecast has {count} rows.')

cursor.close()
db_conn.close()