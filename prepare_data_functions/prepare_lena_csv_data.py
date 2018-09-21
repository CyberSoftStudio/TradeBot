import requests
import libs.differentiationlib as dlib
import pywt
import matplotlib.pyplot as plt
import numpy as np
import json
import pandas as pd

data = pd.read_csv('./exchange_data/EURUSD_M5_3.csv')

print(len(data))


count = data['<DATE>'].values
volume = data['volume'].values.astype(float)

print(volume.dtype, count.dtype)
print(volume.astype(float))

count = count[1:] - count[:-1]
volume = volume[1:] - volume[:-1]

plt.figure()
plt.plot(count)

print(len(count))
depth = pywt.swt_max_level(len(count))

print(depth)
mod = [1 for i in range(depth)]
mod[-1] = 0
mod[-2] = 0
mod[-3] = 0

count = dlib.swt_filtration(count, mod=mod, wname='db6')
volume = dlib.swt_filtration(volume, mod=mod, wname='db6')

plt.figure()
plt.plot(count)

plt.show()

data = pd.DataFrame({'close': count, 'volume': volume})
data.to_csv("./train_data/eurusd_m5_3.csv", index=None)

# with open("./train_data/eth_weekend.txt", 'w')as file:
#     print(str(list(closes[18:])), file=file)
#     print(str(list(times[18:])), file=file)
