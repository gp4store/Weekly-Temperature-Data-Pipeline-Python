import pandas as pd
from datetime import datetime
import os
import shutil

day_stamp = datetime.today().strftime('%Y%m%d')

try:
    
    # Reads csv file
    df = pd.read_csv("Weekly_temperature.csv")
    
    # We selected rows 0 to 194 which is a complete day in our csv, and step every 4 hours
    # Since our log its recording temperature every 15 minutes
    transformed_log = df.iloc[0:96:4, :]

    # Determine the path where the transformed log is going to be saved
    path = f'/your/path/Weekly-Temperature-Data-Pipeline-Python/Temperature_log_probe1_{day_stamp}.csv'
    
    # The indexer .iloc already creates a new data frame so no need to use pd.DataFrame
    # We set index to False to have a cleaner dataframe without the row indexes
    transformed_log.to_csv(path, index=False)
    
    # Backup directory where cleaned log is going to be saved
    backupdir = '/your/path/Weekly-Temperature-Data-Pipeline-Python/hourly'
    os.makedirs(backupdir, exist_ok=True)
    
    # Copy clean log to hourly folder, backup_s3.py will remove it from main directory
    shutil.copy(path, backupdir)
    
    print(f'Cleaned data was saved to {path}')
    print(f'Cleaned data was copied for backup to {backupdir}')
    print(f'Original log length {len(df)}, Cleaned log length {len(transformed_log)}')
    
except FileNotFoundError:
    print('Weekly_temperature.csv file not found, contact integrator')
except Exception as error:
    print(f'Error:{error}')

