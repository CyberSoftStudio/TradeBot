import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import pywt
from scipy.fftpack import fft, ifft

import libs.extremumlib as elib
import libs.histogramma_lib as hlib
import libs.differentiationlib as dlib



FILE = 'eurusd_m5_201808010800_201809282355'

data = pd.read_csv("./train_data/{}.csv".format(FILE))

data_amount = 8192

price_series = data['close'].values[-data_amount:]

global_trend = hlib.get_trend(price_series)
price_series -= global_trend

plt.plot(price_series)
# plt.show()

global_smoosed = elib.swt_filtration(price_series, [1,1,1,1,1,1,1,1,0,0,0,0,0], wname='dmey')
price_series -= global_smoosed

plt.plot(global_smoosed)

# price_series = elib.swt_filtration(price_series, [1,1,1,1,1,1,1,1,1,0,0,0,0], wname='dmey')
plt.plot(price_series)
# price_series = np.abs(price_series)
# plt.figure()
# plt.plot(price_series)
# plt.show()

image = fft(price_series)
# plt.figure()
# plt.plot(np.abs(image))
# plt.figure()
# plt.plot(np.angle(image))
# plt.show()

image *= -1j
# image[0] = 0
#
# plt.figure()
# plt.plot(np.abs(image))
# plt.figure()
# plt.plot(np.angle(image))
# plt.show()

def hilb(window):
    image = fft(price_series)
    # plt.figure()
    # plt.plot(np.abs(image))
    # plt.figure()
    # plt.plot(np.angle(image))
    # plt.show()

    image *= -1j
    image[0] = 0
    rec_price = ifft(image)

    return rec_price

rec_price = ifft(image)

# plt.figure()
# plt.plot(price_series)
# plt.figure()
plt.plot(np.abs(rec_price))
# plt.show()

win_length = 30
res_price = [sum(np.abs(rec_price[i - win_length: i]))/win_length for i in range(win_length, len(np.abs(rec_price)))]
# res_price = elib.wavedec_filtration(res_price, mod=[1,1,1,1,1,0,0,0,0,0,0,0])
plt.plot(np.arange(win_length, len(rec_price)), res_price)
# plt.show()

scale = 500
wcname='gaus8'
price_map = elib.get_cwt_swt(rec_price,
                        scale=scale,
                        mask=[],
                        wdname="dmey",
                        wcname=wcname,
                        step = 0.1
                        )
plt.figure()
plt.imshow(price_map)
plt.show()

print(price_series.shape)


