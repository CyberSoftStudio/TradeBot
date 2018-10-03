import pandas as pd
import numpy as np
from datetime import datetime
import time

data = pd.read_csv('../exchange_data/EURUSD_M5_201809170000.csv', sep='\t')

print(data.head())

closes = data['<CLOSE>'].values

assert isinstance((data['<DATE>'] + ' ' + data['<TIME>']).values, object)
# times = [int(datetime.strptime(x, "%Y.%m.%d %H:%M:%S").timestamp()) for x in (data['<DATE>'] + ' ' + data['<TIME>']).values]
times = (data['<DATE>'] + ' ' + data['<TIME>']).values


data = {'close':closes, 'time': times}
data = pd.DataFrame(data)

data.to_csv("../train_data/eurusd_m5_5.csv", index=None)