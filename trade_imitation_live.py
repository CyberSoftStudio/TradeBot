import scripts.Bot as Bot
import math
import numpy as np

intervals = []

with open('../train_data/ltcusd_m5.txt', 'r') as f:
    lines = list(f)
    price_series = [float(x) for x in lines[0][1:-2].split(',')]
    price_times = [str(x) for x in lines[1][1:-2].split(",")]
    # print(line)
    n = len(price_series)
    # print(price_series)

print(price_times[-2000], price_times[-1])
price_series = np.array(price_series)
window_size = 256

bot = Bot.Bot([])
# {'scale':200, 'window_size':1024, 'mult_const':4, 'assurance': 0.9, 'model_key': 2}
# {'assurance': 0.9, 'key': 2}
bot.change_config({'assurance': 0.9, 'model_key': 2})

limit = len(price_series) - window_size

for i in range(20000, limit):
    print('{}/{}'.format(i, limit))
    bot.set_data(price_series[i:i + window_size])

    interval = bot.predict()

    if len(interval) > 0:
        interval['miny'] += i
        interval['maxy'] += i
        interval['center'] += i

        print("Interval predicted", interval)
        intervals.append(interval)

intervals = sorted(intervals, key=lambda x: (x['miny'], x['center'] - x['miny']))
print("Number of intervals", len(intervals))

trade_count = 0
average_balance = 0

bad_attempts = 0
bad_volume = 0

axe = []

for i in range(len(price_series)):
    axe.append([])

for i in range(len(intervals)):
    x = intervals[i]
    axe[x['miny']].append({
        'id': i,
        'type': 0,
        'trend': x['trend']
    })

    axe[x['center']].append({
        'id': i,
        'type': 1
    })

stop_loss = 10 * 1e-5

first_balance = 100
second_balance = 0

first_fee = 0
second_fee = 0

open_transactions = []

trade_count = 0
bad_count = 0

for i in range(len(axe)):
    if len(axe[i]) == 0:
        continue

    for x in axe[i]:
        if x['type'] == 1:
            if len(open_transactions) == 0 or open_transactions[-1]['id'] != x['id']:
                continue

            first_balance = (second_balance - second_fee) * price_series[i]
            second_balance = 0

            print(open_transactions[-1]['price'], price_series[i], price_series[i] - open_transactions[-1]['price'])

            if open_transactions[-1]['price'] > price_series[i]:
                bad_count += 1

            del open_transactions[-1]

    for x in axe[i]:
        if x['type'] == 0:
            if first_balance == 0 or x['trend'] < -0.5:
                continue
            trade_count += 1
            second_balance = (first_balance - first_fee) * 1/price_series[i]
            first_balance = 0
            open_transactions.append({'id': x['id'], 'price': price_series[i]})

print("Number of transactions", trade_count)
print("Number of bad transactions", bad_count)
print("End balance is", first_balance, second_balance)

# print("Statistic")
# print("Trade count -", trade_count)
# print("Average additional balance -", average_balance/trade_count)
# print("Bad attempts count -", bad_attempts)
# print("Negative changes -", bad_volume)