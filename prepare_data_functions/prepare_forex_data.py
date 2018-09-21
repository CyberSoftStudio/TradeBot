import pandas as pd
import numpy as np
from datetime import datetime
import time

data = pd.read_csv('../exchange_data/EURUSD_M5_3.csv', sep='\t')

print(data.head())

closes = data['<CLOSE>'].values

data = pd.DataFrame({'close': closes})
data.to_csv("../train_data/eurusd_m5_3.csv", index=None)