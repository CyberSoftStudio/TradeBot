# from Predictor import Predictor as Bot
import math
import matplotlib.pyplot as plt
import libs.extremumlib as elib
import numpy as np
import pandas as pd
import json

'./train_data/eurusd_h1.csv'
FILE = 'eurusd_m5_201808010800_201809282355'

data = pd.read_csv('./train_data/' + FILE + '.csv')

# with open('./train_data/eurusd_h1.txt', 'r') as f:
#     lines = list(f)
#     price_series = [float(x) for x in lines[0][1:-2].split(',')]
#     # price_times = [str(x) for x in lines[1][1:-2].split(",")]
#     # print(line)
#     n = len(price_series)
#     # print(price_series)

price_series = data['close'].values
time_series = data['time'].values
plt.plot(price_series)
plt.show()

data = pd.read_csv('./results/' + FILE + '.csv')
print(data)

csv_data = data.copy()
csv_data[['start', 'miny', 'center', 'maxy']] = csv_data[['start', 'miny', 'center', 'maxy']].applymap(lambda x : time_series[min(x + 30, len(time_series) - 1)])
csv_data.to_csv('./results/{}_datetime.csv'.format(FILE), index=None)

intervals = []

for i in range(data.shape[0]):
    interval = {
        'start': [],
        'miny': [],
        'maxy': [],
        'center' : [],
        'trend': [],
        'amplitude': []
    }

    for key in interval.keys():
        interval[key] = data[key][i]

    intervals.append(interval)

print(intervals)

balance = 0

trade_count = 0
average_balance = 0

bad_attempts = 0
bad_volume = 0

shift = 30
window_size = 256


def get_trend_1(trend):
    return math.atan((trend[-1] - trend[-30]) / 30)

def get_trend_2(trend):
    return math.atan(trend[-1] - trend[-6])

def get_trend_3(trend):
    res = [math.atan(trend[-1] - trend[-i]) for i in range(2, 11)]
    res = sorted(res)
    return res[len(res) // 2 + 1]

def get_trend_4(trend):
    res = [math.atan(trend[-1] - trend[-i]) for i in range(2, 11)]
    res = sorted(res)
    return sum(res) / len(res)


for x in intervals:
    if x['amplitude'] < 0.001:
        continue
    start = x['start'] + 30
    window = price_series[start - window_size : start]
    window = elib.wavedec_filtration(window, [1, 0, 0, 0 , 0 , 0, 0 ,0 ,  0, 0, 0, 0,0 ,0 ,0])

    trend = get_trend_4(window)
    miny = x['miny'] + 30
    center = x['center'] + 30

    # miny, center = center, miny
    trade_count += 1

    try:
        if True:
            additional_balance = price_series[center] - price_series[miny] - 0.0003     #((price_series[x['center']] - fee)/(price_series[x['miny']] + fee) - 1) * balance - 0.00015
        else:
            additional_balance = price_series[miny] - price_series[center] - 0.0003
        average_balance += abs(additional_balance)

        if additional_balance < 0:
            print(x['trend'], x['amplitude'], time_series[miny], time_series[center], price_series[miny], price_series[center], additional_balance, '-')
        else:
            print(x['trend'], x['amplitude'], time_series[miny], time_series[center], price_series[miny], price_series[center], additional_balance, '+')

        if True:

            # fig, ax = plt.subplots()
            # plt.plot(price_series)
            # ax.axvline(x=x['miny'] + shift, color='g')
            # ax.axvline(x=x['maxy'] + shift, color='g')
            # ax.axvline(x=x['center'] + shift, color='r')
            # mng = plt.get_current_fig_manager()
            # mng.resize(*mng.window.maxsize())
            # plt.show()
            pass

        if additional_balance < 0:
            bad_attempts += 1
            bad_volume += abs(additional_balance)

        balance += additional_balance
    except:
        pass
    

    cur_time = x['center']

    print("Current balance is", balance)

print("End balance is", balance)

print("Statistic")
print("Trade count -", trade_count)
# print("Average additional balance -", average_balance/trade_count)
print("Bad attempts count -", bad_attempts)
print("Negative changes -", bad_volume)
plt.show()
