import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
import sqlite3

day_stamp = datetime.today().strftime('%Y%m%d')

try:
    
    path  = f"/your/path/Weekly-Temperature-Data-Pipeline-Python/hourly/Temperature_log_probe1_{day_stamp}.csv"
    path_save = f"/your/path/Weekly-Temperature-Data-Pipeline-Python/Dashboards/Daily_temperature_plot_{day_stamp}.png"
    df = pd.read_csv(path)


    plt.figure(figsize=(12, 6))

    # Selecting the columns that have the data we are gonna work with
    plt.plot(df['time'], df['temperatura'])

    # Establishing min a max values to have a better representation on the data plotted
    min_temp = 25
    max_temp = 35
    plt.axhline(y=min_temp, color='blue', linestyle='-', label=f'Min: {min_temp}°C')
    plt.axhline(y=max_temp, color='red', linestyle='-', label=f'Max: {max_temp}°C')

    # Selecting x ticks using the 24 hour period we want in this case the length of our log file
    plt.xticks(range(len(df)), df['time'], rotation=90)
    plt.yticks(range(23, 37))
    plt.grid()
    
    # Add legend to show what the lines mean
    plt.legend() 
    plt.title(f'Daily Temperature Log - {day_stamp}')  
    plt.xlabel('Time')
    plt.ylabel('Temperature (°C)')
    
    plt.tight_layout()
    plt.savefig(path_save)
    plt.show()
    
except FileNotFoundError:
    print('CSV file not found, contact integrator')


