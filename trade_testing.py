from Predictor_test import Predictor as Bot
import math
import matplotlib.pyplot as plt
import libs.extremumlib as elib
import numpy as np

intervals = []

with open('./train_data/ltcusd_m5_2.txt', 'r') as f:
    lines = list(f)
    price_series = [float(x) for x in lines[0][1:-2].split(',')]
    # price_times = [str(x) for x in lines[1][1:-2].split(",")]
    # print(line)
    n = len(price_series)
    # print(price_series)

price_series = np.array(price_series)

transactions = [
    {"open_price": 62.026, "close_price": 62.146, "open_timestamp": 1535752800.0, "close_timestamp": 1535754600.0},
    {"open_price": 62.056, "close_price": 62.096, "open_timestamp": 1535753100.0, "close_timestamp": 1535754900.0},
    {"open_price": 62.186, "close_price": 62.026, "open_timestamp": 1535756700.0, "close_timestamp": 1535758800.0},
    {"open_price": 62.216, "close_price": 62.106, "open_timestamp": 1535757300.0, "close_timestamp": 1535759700.0},
    {"open_price": 63.036, "close_price": 63.406, "open_timestamp": 1535763600.0, "close_timestamp": 1535766000.0},
    {"open_price": 63.246, "close_price": 63.926, "open_timestamp": 1535776500.0, "close_timestamp": 1535778600.0},
    {"open_price": 63.596, "close_price": 63.646, "open_timestamp": 1535779800.0, "close_timestamp": 1535781000.0},
    {"open_price": 63.756, "close_price": 63.826, "open_timestamp": 1535789700.0, "close_timestamp": 1535791500.0},
    {"open_price": 63.766, "close_price": 64.386, "open_timestamp": 1535793300.0, "close_timestamp": 1535794200.0},
    {"open_price": 65.836, "close_price": 66.066, "open_timestamp": 1535814300.0, "close_timestamp": 1535816700.0},
    {"open_price": 66.576, "close_price": 66.526, "open_timestamp": 1535823300.0, "close_timestamp": 1535825100.0},
    {"open_price": 66.606, "close_price": 66.446, "open_timestamp": 1535824200.0, "close_timestamp": 1535825400.0},
    {"open_price": 66.436, "close_price": 66.366, "open_timestamp": 1535826000.0, "close_timestamp": 1535827800.0},
    {"open_price": 66.816, "close_price": 66.836, "open_timestamp": 1535833200.0, "close_timestamp": 1535835300.0},
    {"open_price": 66.736, "close_price": 67.226, "open_timestamp": 1535834700.0, "close_timestamp": 1535836800.0},
    {"open_price": 66.816, "close_price": 66.856, "open_timestamp": 1535835900.0, "close_timestamp": 1535838000.0},
    {"open_price": 66.946, "close_price": 66.806, "open_timestamp": 1535836500.0, "close_timestamp": 1535838300.0},
    {"open_price": 66.886, "close_price": 66.616, "open_timestamp": 1535837700.0, "close_timestamp": 1535840700.0},
    {"open_price": 66.756, "close_price": 66.466, "open_timestamp": 1535839200.0, "close_timestamp": 1535841300.0},
    {"open_price": 66.366, "close_price": 66.516, "open_timestamp": 1535843700.0, "close_timestamp": 1535845800.0},
    {"open_price": 66.226, "close_price": 66.476, "open_timestamp": 1535844000.0, "close_timestamp": 1535846100.0},
    {"open_price": 66.446, "close_price": 66.326, "open_timestamp": 1535845200.0, "close_timestamp": 1535847600.0},
    {"open_price": 66.166, "close_price": 66.666, "open_timestamp": 1535872800.0, "close_timestamp": 1535874600.0},
    {"open_price": 64.476, "close_price": 64.486, "open_timestamp": 1535897700.0, "close_timestamp": 1535899800.0},
    {"open_price": 65.316, "close_price": 65.536, "open_timestamp": 1535920500.0, "close_timestamp": 1535922900.0},
    {"open_price": 65.436, "close_price": 65.606, "open_timestamp": 1535921100.0, "close_timestamp": 1535923800.0},
    {"open_price": 65.476, "close_price": 65.596, "open_timestamp": 1535921400.0, "close_timestamp": 1535924100.0},
    {"open_price": 65.596, "close_price": 65.886, "open_timestamp": 1535926800.0, "close_timestamp": 1535928600.0},
    {"open_price": 65.696, "close_price": 65.816, "open_timestamp": 1535927100.0, "close_timestamp": 1535929200.0},
    {"open_price": 65.776, "close_price": 65.916, "open_timestamp": 1535927700.0, "close_timestamp": 1535929500.0},
    {"open_price": 65.786, "close_price": 65.876, "open_timestamp": 1535928300.0, "close_timestamp": 1535930100.0},
    {"open_price": 65.206, "close_price": 65.296, "open_timestamp": 1535943900.0, "close_timestamp": 1535947200.0},
    {"open_price": 64.796, "close_price": 64.506, "open_timestamp": 1535972400.0, "close_timestamp": 1535975100.0},
    {"open_price": 64.696, "close_price": 64.556, "open_timestamp": 1535973300.0, "close_timestamp": 1535975400.0},
    {"open_price": 65.096, "close_price": 64.886, "open_timestamp": 1535987100.0, "close_timestamp": 1535989200.0},
    {"open_price": 64.836, "close_price": 64.866, "open_timestamp": 1535991300.0, "close_timestamp": 1535994000.0},
    {"open_price": 64.716, "close_price": 64.876, "open_timestamp": 1535992200.0, "close_timestamp": 1535994900.0},
    {"open_price": 65.486, "close_price": 65.356, "open_timestamp": 1536017100.0, "close_timestamp": 1536018900.0},
    {"open_price": 65.556, "close_price": 65.636, "open_timestamp": 1536019500.0, "close_timestamp": 1536021600.0},
    {"open_price": 66.326, "close_price": 67.096, "open_timestamp": 1536024000.0, "close_timestamp": 1536025800.0},
    {"open_price": 66.736, "close_price": 67.136, "open_timestamp": 1536024600.0, "close_timestamp": 1536026400.0},
    {"open_price": 66.726, "close_price": 67.316, "open_timestamp": 1536024900.0, "close_timestamp": 1536026700.0},
    {"open_price": 66.096, "close_price": 66.436, "open_timestamp": 1536036600.0, "close_timestamp": 1536038400.0},
    {"open_price": 69.086, "close_price": 68.646, "open_timestamp": 1536063000.0, "close_timestamp": 1536063900.0},
    {"open_price": 68.856, "close_price": 68.396, "open_timestamp": 1536062400.0, "close_timestamp": 1536064200.0},
    {"open_price": 68.676, "close_price": 68.656, "open_timestamp": 1536078600.0, "close_timestamp": 1536080400.0},
    {"open_price": 68.756, "close_price": 68.726, "open_timestamp": 1536078900.0, "close_timestamp": 1536080700.0},
    {"open_price": 69.286, "close_price": 68.376, "open_timestamp": 1536086100.0, "close_timestamp": 1536087900.0},
    {"open_price": 68.196, "close_price": 67.826, "open_timestamp": 1536088500.0, "close_timestamp": 1536090600.0},
    {"open_price": 68.076, "close_price": 67.766, "open_timestamp": 1536112500.0, "close_timestamp": 1536114600.0},
    {"open_price": 67.886, "close_price": 63.686, "open_timestamp": 1536140400.0, "close_timestamp": 1536142200.0},
    {"open_price": 67.796, "close_price": 63.896, "open_timestamp": 1536140700.0, "close_timestamp": 1536142500.0},
    {"open_price": 67.056, "close_price": 63.786, "open_timestamp": 1536141000.0, "close_timestamp": 1536143100.0},
    {"open_price": 62.246, "close_price": 62.006, "open_timestamp": 1536147000.0, "close_timestamp": 1536149400.0}
]

init_timestamp = 1535662800.0

for trans in transactions:
    trans['open_timestamp'] = (trans['open_timestamp'] - init_timestamp) / 300
    trans['close_timestamp'] = (trans['close_timestamp'] - init_timestamp) / 300

plt.plot(price_series)

for trans in transactions:
    plt.axvline(x=trans['open_timestamp'], color='red')
    plt.axvline(x=trans['close_timestamp'], color='red')

plt.show()