from Predictor import Predictor as Bot
import math
import matplotlib.pyplot as plt
import libs.extremumlib as elib
import numpy as np
import pandas as pd
import libs.histogramma_lib as hlib
import json
intervals = []


FILE = 'eurusd_m5_201808010800_201809282355.csv'


data = pd.read_csv('./train_data/' + FILE)

values = slice(len(data) -6000, len(data))
price_series = data['close'].values[values]
time_series = data['time'].values[values]

print(len(price_series))

window_size = 256

bot = Bot([])
bot.change_config({
    'assurance': 0.9,
    'model_key': 2,
    'scale':50,
    'window_size': 256,
    'mult_const':1
})


limit = len(price_series)
# limit = 10

init_time = time_series[0]
delta_time = 300
shift = bot.config['shift']

for i in range(0, limit):
    print('{}/{}'.format(i + 1, limit))
    try:
        window = price_series[i: i + window_size]
        window = list(window)
        # tmp = window[-shift:]
        # tmp.reverse()
        #
        # for i in range(len(tmp)):
        #     cur = tmp[i] - tmp[0]
        #     tmp[i] = tmp[0] - cur

        # window.extend(tmp)
        # window = np.array(window[shift:])
        bot.set_data(window)
        window = price_series[i + bot.config['shift']: i + window_size + bot.config['shift']]
        interval = bot.predict()
        M = np.zeros((2, 2))
    except:
        break

    if len(interval) > 0:
        interval['miny'] = int(interval['miny'])
        interval['maxy'] = int(interval['maxy'])
        interval['center'] = int(interval['center'])
        interval['trend'] = float(interval['trend'])
        interval['amplitude'] = float(interval['amplitude'])
        interval['start'] = 225

        interval['miny'] += i
        interval['maxy'] += i
        interval['center'] += i
        interval['start'] += i

        # interval['miny'] = init_time + interval['miny'] * delta_time
        # interval['maxy'] = init_time + interval['maxy'] * delta_time
        # interval['center'] = init_time + interval['center'] * delta_time

        print("Interval predicted", interval)
        intervals.append((interval, M, window, i))

balance = 0
cur_time = 0

print("Initial balance is", balance)

intervals = sorted(intervals, key=lambda x: (x[0]['miny'], x[0]['center'] - x[0]['miny']))

resdata = [x[0] for x in intervals]

intervals_json = {
    'start':[],
    'miny':[],
    'maxy':[],
    'center':[],
    'trend' :[],
    'amplitude':[]
}

for x in resdata:

    for key, val in x.items():
        intervals_json[key].append(val)

resdata = pd.DataFrame(intervals_json)

resdata.to_csv('./results/' + FILE, index=None)

trade_count = 0
average_balance = 0

bad_attempts = 0
bad_volume = 0

for x, mat, win, i in intervals:

    trade_count += 1
    #что на самом деле получается balance * (1/(price1 + alpha)) - balance * (price1 - alpha)
    fee = 0.000
    miny = x['miny']
    center = x['center']
    # if x['trend'] >= -0.3:
    additional_balance = price_series[center] - price_series[miny]      #((price_series[x['center']] - fee)/(price_series[x['miny']] + fee) - 1) * balance - 0.00015
    # else :
    #     additional_balance = price_series[miny] - price_series[center]
    print(miny, center, price_series[miny], price_series[center], additional_balance)
    average_balance += abs(additional_balance)

    if additional_balance < 0:
        print(x['amplitude'])
        # scale, wdname, wcname = 50, 'db6', 'gaus8'
        # fig = plt.figure()
        # ax = fig.add_subplot(311)
        # ax.matshow(mat)
        # ax.axvline(x=x['miny'] - i)
        # ax.axvline(x=x['maxy'] - i)
        #
        # true_mat = elib.get_cwt_swt(win,
        #         scale=scale,
        #         mask=[1, 1, 1, 1, 1, 0, 0, 0, 0, 0],
        #         wdname=wdname,
        #         wcname=wcname
        #         )
        #
        # ax = fig.add_subplot(312)
        # ax.matshow(true_mat)
        # ax.axvline(x=x['miny'] - i)
        # ax.axvline(x=x['maxy'] - i)
        #
        # ax = fig.add_subplot(313)
        # ax.plot(win)
        # ax.axvline(x=x['miny'] - i)
        # ax.axvline(x=x['maxy'] - i)
        # ax.axvline(x=x['center'] - i, color='r')
        #
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
