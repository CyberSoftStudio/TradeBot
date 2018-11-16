
from BotTest.Predictor import Predictor as Bot
import math
import matplotlib.pyplot as plt
import libs.extremumlib as elib
import numpy as np
import pandas as pd
import libs.histogramma_lib as hlib
import json
import math
intervals = []

def hist_predict(window, min_prob = 0.01, max_prob = 0.01, mod = (1, 1, 1, 1, 1, 1, 1, 1, 0 , 0 , 0 , 0), wname = 'db1'):
    miny, maxy, trend = hlib.get_bound_by_hist(window=window, pref_prob=min_prob,
                                               suff_prob=max_prob, mod=mod,
                                               wname=wname)
    if window[-1] > trend[-1] + maxy:
        return True, 1
    elif window[-1] < trend[-1] + miny:
        return True, -1
    return False, 0

HIST_CONFIG = {
    "pref_prob" : 0.1, # min probability
    "suff_prob" : 0.1  # max probability
}

FILE = 'eurusd_m5_201808010800_201809282355.csv'


data = pd.read_csv('./train_data/' + FILE)

values = slice(len(data) - 1000, len(data))
price_series = data['close'].values[values]
time_series = data['time'].values[values]

print(len(price_series))

window_size = 256

predictor = Bot([])
predictor.change_config({
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
shift = predictor.config['shift']

tmp_array = []
tmp = []
tmp_min = []
tmp_max = []

pattern_min_center = []

window_size = 256
trend_window_size = 8
limit = len(price_series) - window_size
intervals = []
for i in range(0, limit):
    print("i == ", i)
    interval = {}
    print('{}/{}'.format(i, limit))
    try:
        window = price_series[i:i + window_size]
        predictor.set_data(window)
        interval = predictor.predict()
        M = np.zeros((2, 2))
    except Exception as e:
        print(e)
        break
    print("##############################################################################")

    mina, maxa, trend = hlib.get_bound_by_hist_linear_approx(window[-trend_window_size:], **HIST_CONFIG)

    interval['minmaxamplitude'] = maxa - mina
    interval['mina'] = mina
    interval['maxa'] = maxa
    interval['last_point'] = trend[-1]
    interval['trend'] = math.atan((trend[-1] - trend[0]))

    tmp_array.append((list(range(i, i + window_size))[-trend_window_size:], trend))
    tmp.append(trend[-1])
    tmp_min.append(trend[-1] + mina)
    tmp_max.append(trend[-1] + maxa)

    if window[-1] > trend[-1] + maxa:
        interval['isgood'], interval['state'] = True, 1
    elif window[-1] < trend[-1] + mina:
        interval['isgood'], interval['state'] = True, -1
    else:
        interval['isgood'], interval['state'] = False, 0

    if len(interval) > 7:
        interval['miny'] = int(interval['miny'])
        interval['maxy'] = int(interval['maxy'])
        interval['center'] = int(interval['center'])
        # interval['trend'] = float(interval['trend'])
        interval['amplitude'] = float(interval['amplitude'])
        interval['start'] = 225

        interval['miny'] += i
        interval['maxy'] += i
        interval['center'] += i
        interval['start'] += i

        pattern_min_center.append([interval['miny'] + 30, interval['center'] + 30])

        print("Interval predicted", interval)

        intervals.append((interval, M, window, i))

intervals = sorted(intervals, key=lambda x: (x[0]['miny'], x[0]['center'] - x[0]['miny']))

resdata = [x[0] for x in intervals]

intervals_json = {
    'start': [],
    'miny': [],
    'maxy': [],
    'center': [],
    'trend': [],
    'amplitude': [],
    'minmaxamplitude': [],
    'last_point': [],
    'isgood': [],
    'state' : [],
    'mina' : [],
    'maxa' : []

}


for x in resdata:
    for key, val in x.items():
        intervals_json[key].append(val)

resdata = pd.DataFrame(intervals_json)

print("Saving result...")

resdata.to_csv('./results/' + FILE, index=None)

print("Done!")


# Drawing

plt.figure()
plt.plot(np.arange(len(price_series)), price_series)
for i in range(len(tmp_array)):
    try:
        plt.plot(tmp_array[i][0], tmp_array[i][1], color='orange')
    except:
        pass

for x in pattern_min_center:
    try:
        plt.plot(x, price_series[[min(len(price_series) - 1, x[0]), min(len(price_series) - 1, x[1])]], 'ro-')
    except:
        pass

plt.plot(np.arange(len(tmp)) + window_size - 1, tmp, color='green')
plt.fill_between(np.arange(len(tmp_array)) + window_size - 1, tmp_max, tmp_min, color='g', alpha=0.4)
plt.show()
