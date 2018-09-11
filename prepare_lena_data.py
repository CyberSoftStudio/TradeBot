import requests
import libs.differentiationlib as dlib
import pywt
import matplotlib.pyplot as plt
import numpy as np
import json
import pandas as pd

# candles = json.load(open('./exchange_data/eth_weekend.json', 'r'))
# closes = np.array([x['close'] for x in candles])
# times = np.array([x['date'] for x in candles])

data = pd.read_csv('./exchange_data/btc_15_close.csv')
closes = data['close'].values[:-1]
times = data['time'].values[:-1]

plt.figure()
plt.plot(closes)

print(len(closes))
depth = pywt.swt_max_level(len(closes))

print(depth)
mod = [1 for i in range(depth)]
mod[-1] = 0
mod[-2] = 0
mod[-3] = 0

closes = dlib.swt_filtration(closes, mod=mod, wname='db6')

plt.figure()
plt.plot(closes)

plt.show()

data = pd.DataFrame({'close':closes[18:], 'time':times[18:]})
data.to_csv("./train_data/btc_15_close_3levels.csv", index=None)

# with open("./train_data/eth_weekend.txt", 'w')as file:
#     print(str(list(closes[18:])), file=file)
#     print(str(list(times[18:])), file=file)
