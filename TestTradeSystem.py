import pandas as pd
import json
cnt = 0

class TestTradingSystem:
    def __init__(self, auth_info, test=False):
        self.candles = json.load(open("./train_data/btcusd_bitmex_candles.json"))['candles']
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
            self.balances[0]['amount'] += order['quality'] / order['price']
            self.balances[1]['amount'] -= order['quality']
        elif symbol == 'USDXBT':
            self.balances[1]['amount'] += order['quality'] * order['price']
            self.balances[0]['amount'] -= order['quality']

    def get_orderbook(self, symbol, count=50):
        return None

    def get_candles(self, count=256):
        tmp = (self.candles[self.ptr - count:self.ptr], True)
        self.ptr += 1
        return tmp

    def get_balances(self):
        return self.balances