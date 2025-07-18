import sqlite3
from datetime import datetime
import pandas as pd

day_stamp = datetime.today().strftime('%Y%m%d')
table_name = f'Temperature_log_probe1_{day_stamp}'
path = f'/your/path/Weekly-Temperature-Data-Pipeline-Python/hourly/Temperature_log_probe1_{day_stamp}.csv'


# filename to form database
local_db = "local_db_analytics.db"
df = pd.read_csv(path)

try:
  conn = sqlite3.connect(local_db)
  cursor = conn.cursor()
  print("Database Sqlite3.db formed.")
except FileExistsError:
    print("Database already formed")
except:
  print("Database Sqlite3.db not formed.")

df.to_sql(table_name, conn, if_exists='replace', index=False)
print(f'Log file was added to your database {table_name}')

cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
tables = cursor.fetchall()
print("Tables:", tables)  
conn.close()
