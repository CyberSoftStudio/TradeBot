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

data = pd.read_csv('./exchange_data/btc_all.csv')
data = data[:1024]

def filtration(data):
    if len(data) > 1024:
        data = data[:1024]
    print(len(data.values))
    depth = 10
    mod = [1 for i in range(depth)]
    mod[-1] = 0
    # mod[-2] = 0
    # mod[-3] = 0

    data = dlib.swt_filtration(data.values, mod=mod, wname='db6')

    return data

for key in data.keys():
    print(key)
    if key != 'time':
        fig = plt.figure()
        fig.add_subplot(211)
        plt.plot(data[key])

        data[key] = filtration(data[key])

        fig.add_subplot(212)
        plt.plot(data[key])
        plt.title(key)

plt.show()

data.to_csv("./train_data/btc_all_1levels.csv", index=None)

# with open("./train_data/eth_weekend.txt", 'w')as file:
#     print(str(list(closes[18:])), file=file)
#     print(str(list(times[18:])), file=file)
