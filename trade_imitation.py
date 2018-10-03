from Predictor import Predictor as Bot
import math
import matplotlib.pyplot as plt
import libs.extremumlib as elib
import numpy as np
import pandas as pd
import json
intervals = []


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
# price_series = np.array(price_series)
window_size = 256

bot = Bot([])
bot.change_config({
    'assurance': 0.9,
    'model_key': 2,
    'scale':50,
    'window_size': 256,
    'mult_const':1
})


limit = len(price_series) - window_size
# limit = 100

init_time = time_series[0]
delta_time = 300

for i in range(0, limit):
    print('{}/{}'.format(i + 1, limit))
    bot.set_data(price_series[i:i + window_size])
    window = price_series[i + bot.config['shift']: i + window_size + bot.config['shift']]
    interval = bot.predict(get_trend=Bot.get_trend_2)
    M = np.zeros((2, 2))

    if len(interval) > 0:
        interval['miny'] = int(interval['miny'])
        interval['maxy'] = int(interval['maxy'])
        interval['center'] = int(interval['center'])
        interval['trend'] = float(interval['trend'])
        interval['amplitude'] = float(interval['amplitude'])

        interval['miny'] += i
        interval['maxy'] += i
        interval['center'] += i

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

with open('./results/eurusd_h1_gt3.txt', 'w') as file:
    intervals_json = {
        'miny':[],
        'maxy':[],
        'center':[],
        'trend' :[],
        'amplitude':[]
    }

    for x in resdata:
        print(init_time + delta_time * x['miny'], init_time + delta_time * x['center'], init_time + delta_time * x['maxy'], file=file)

        for key, val in x.items():
            intervals_json[key].append(val)

resdata = pd.DataFrame(intervals_json)

resdata.to_csv('./results/eurusd_h1_gt3.csv', index=None)

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
