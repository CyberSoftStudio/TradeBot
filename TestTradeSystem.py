import pandas as pd
import json
from datetime import datetime
import matplotlib.pyplot as plt
cnt = 0

class TestTradingSystem:
    def __init__(self, auth_info, test=False):
        with open('./train_data/ltcusd_m5_2.txt', 'r') as f:
            lines = list(f)
            price_series = [float(x) for x in lines[0][1:-2].split(',')]
            plt.figure()
            plt.plot(price_series)
            plt.show()
            price_times = []

            for x in lines[1][1:-2].split(","):
                try:
                    price_times.append(datetime.strptime(str(x), " '%Y.%m.%d %H:%M:%S'").timestamp())
                except:
                    price_times.append(datetime.strptime(str(x), "'%Y.%m.%d %H:%M:%S'").timestamp())

            # print(line)
            n = len(price_series)
            # print(price_series)
            price_series.reverse()
            price_times.reverse()

        candles = []
        for i in range(len(price_series)):
            candles.append({"timestamp": price_times[i], "close":price_series[i]})

        self.candles = candles # json.load(open("./train_data/btcusd_bitmex_candles.json"))['candles']
        self.candles.reverse()
        self.balances = [{'currency':'xbt', 'amount':0}, {'currency':'usd', 'amount':100}]
        self.ptr = 256

    def get_range(self, symbol, startTime, endTime):
        return None

    def make_order(self, orders):
        print(orders)
        order = orders[0]
        symbol = order['symbol']
        if symbol == 'XBTUSD':
            self.balances[0]['amount'] += order['quantity'] / order['price']
            self.balances[1]['amount'] -= order['quantity']
        elif symbol == 'USDXBT':
            self.balances[1]['amount'] += order['quantity'] * order['price']
            self.balances[0]['amount'] -= order['quantity']

    def get_orderbook(self, symbol, count=50):
        return None

    def get_candles(self, count=256):
        tmp = (self.candles[self.ptr - count:self.ptr], True)
        return tmp

    def get_balances(self):
        return self.balances

    def closeDay(self):
        self.ptr += 1