import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
import sqlite3


day_stamp = datetime.today().strftime('%Y%m%d')
path  = f"/home/gp_/Weekly-Temperature-Data-Pipeline-Python/hourly/Temperature_log_probe1_{day_stamp}.csv"

df = pd.read_csv(path)

df.plot(x = "time", y = "temperatura")
plt.show()

