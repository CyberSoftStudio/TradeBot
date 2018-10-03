# from Predictor import Predictor as Bot
import math
import matplotlib.pyplot as plt
import libs.extremumlib as elib
import numpy as np
import pandas as pd
import json

'./train_data/eurusd_h1.csv'

data = pd.read_csv('./train_data/eurusd_h1.csv')

# with open('./train_data/eurusd_h1.txt', 'r') as f:
#     lines = list(f)
#     price_series = [float(x) for x in lines[0][1:-2].split(',')]
#     # price_times = [str(x) for x in lines[1][1:-2].split(",")]
#     # print(line)
#     n = len(price_series)
#     # print(price_series)

price_series = data['close'].values
time_series = data['time'].values

data = pd.read_csv('./results/eurusd_h1.csv')

csv_data = data.copy()
csv_data[['miny', 'center', 'maxy']] = csv_data[['miny', 'center', 'maxy']].applymap(lambda x : time_series[x])
# csv_data.to_csv('./results/eurusd_m5_4_datetime.csv', index=None)

intervals = []

for i in range(data.shape[0]):
    interval = {
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


for x in intervals:
    if x['amplitude'] < 0.001:
        continue
    trade_count += 1
    miny = x['miny']
    center = x['center']
    if x['trend'] >= 0.00001:
        additional_balance = price_series[center] - price_series[miny] - 0.0003     #((price_series[x['center']] - fee)/(price_series[x['miny']] + fee) - 1) * balance - 0.00015
    else:
        additional_balance = price_series[miny] - price_series[center] - 0.0003
    average_balance += abs(additional_balance)

    if additional_balance < 0:
        print(x['trend'], x['amplitude'], time_series[miny], time_series[center], price_series[miny], price_series[center], additional_balance, '-')
    else:
        print(x['trend'], x['amplitude'], time_series[miny], time_series[center], price_series[miny], price_series[center], additional_balance, '+')

        # fig, ax = plt.subplots()
        # plt.plot(price_series)
        # ax.axvline(x=x['miny'], color='g')
        # ax.axvline(x=x['maxy'], color='g')
        # ax.axvline(x=x['center'], color='r')
        # mng = plt.get_current_fig_manager()
        # mng.resize(*mng.window.maxsize())
        # plt.show()


    if additional_balance < 0:
        bad_attempts += 1
        bad_volume += abs(additional_balance)

    balance += additional_balance
    

    cur_time = x['center']

    print("Current balance is", balance)

print("End balance is", balance)

print("Statistic")
print("Trade count -", trade_count)
# print("Average additional balance -", average_balance/trade_count)
print("Bad attempts count -", bad_attempts)
print("Negative changes -", bad_volume)
plt.show()
