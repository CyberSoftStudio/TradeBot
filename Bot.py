from Predictor import Predictor
from TradingSystem import TradingSystem
from TestTradeSystem import TestTradingSystem
from datetime import datetime, timedelta
import time
import numpy as np


class Bot:
    def __init__(self, auth_info, test=True, exchange_name = None):
        self.keypoint_queue = []
        self.data = []
        self.predictor = Predictor([])
        self.test = test
        self.predictor.config['extract_alpha'] = 0.5
        if (test == False):
            self.trade_system = TradingSystem(auth_info=auth_info, test=test)
        else:
            self.trade_system = TestTradingSystem(auth_info = auth_info, test=test)
        self.keypoint_id = 0
        self.cripto = 'xbt'
        self.fiat = 'usd'
        self.symbol = 'XBTUSD'
        self.rsymbol = 'USDXBT'

    @staticmethod
    def prepare_data(exchange_data):
        close = [x['close'] for x in exchange_data]
        timestamps = [x['timestamp'] for x in exchange_data]
        return np.array(close), timestamps

    def prepare_buy_order(self, interval, symbol='xbt'):
        self.trade_system.get_orderbook(symbol)

        return 0

    def prepare_sell_order(self, interval, symbol='xbt'):
        self.trade_system.get_orderbook(symbol)

        return 0

    @staticmethod
    def make_keypoints(interval, id):
        keyp1 = {
            'time': interval['miny'],
            'trend': interval['trend'],
            'type': 0,
            'id': id
        }
        keyp2 = {
            'time': interval['center'],
            'trend': interval['trend'],
            'type': 1,
            'id': id
        }

        return keyp1, keyp2

    @staticmethod
    def check_time(order):
        order_timepoint = order['time']
        current_timepoint = datetime.now()

        diff = current_timepoint - order_timepoint if current_timepoint >= order_timepoint else order_timepoint - current_timepoint

        if diff < timedelta(seconds=10):
            return True

        return False

    def test_check_time(self, order):
        order_timepoint = order['time']
        current_timepoint = datetime.utcfromtimestamp(self.trade_system.candles[self.trade_system.ptr]['timestamp'])

        print("Time points", current_timepoint, order_timepoint, "Test time difference", order_timepoint - current_timepoint)

        diff = current_timepoint - order_timepoint if current_timepoint >= order_timepoint else order_timepoint - current_timepoint

        if diff < timedelta(seconds=10):
            return True

        return False

    def prediction_loop(self):
        exchange_data = self.trade_system.get_candles()[0]
        exchange_data.reverse()
        # print(exchange_data)
        closes, times = self.prepare_data(exchange_data)
        # print(closes)
        # print(times)
        self.predictor.set_data(data=closes)
        interval = self.predictor.predict()


        if len(interval) > 0:
            print(datetime.now(), "Found interval", interval, file=open('log.txt', 'a+'))

            time_shift = datetime.utcfromtimestamp(times[255])
            time_delta = timedelta(minutes=5)

            print("Timeshift", time_shift)

            self.keypoint_id += 1

            print("Predicted interval", interval)

            interval['miny'] = time_shift + time_delta * (interval['miny'] - 226)
            interval['center'] = time_shift + time_delta * (interval['center'] - 226)

            keyp1, keyp2 = self.make_keypoints(interval, self.keypoint_id)
            print('WE WILL MAKE NEW ORDER', keyp1, keyp2)
            self.keypoint_queue.append(keyp1)
            self.keypoint_queue.append(keyp2)

    def trading_loop(self):

        if self.test:
            check_time = self.test_check_time
        else:
            check_time = self.check_time

        try:
            print("WE ARE CHECKING ORDER", len(self.keypoint_queue) > 0, check_time(self.keypoint_queue[0]))
        except:
            pass

        if len(self.keypoint_queue) > 0 and check_time(self.keypoint_queue[0]):
            print("WE WANT TO SUGGEST ORDER")

        if not (len(self.keypoint_queue) > 0 and check_time(self.keypoint_queue[0])):
            print("Nothing interesting")
            return None

        point = self.keypoint_queue[0]
        balances = self.trade_system.get_balances()
        candle = self.trade_system.get_candles(count=1)[0]
        if point['type'] == 0:
            quantity = [x['amount'] for x in balances if x['currency']==self.fiat][0]
            order = {
                'price':candle['close'],
                'quantity': quantity,
                'symbol': self.symbol
            }
        else:
            quantity = [x['amount'] for x in balances if x['currency'] == self.cripto][0]
            order = {
                'price': candle['close'],
                'quantity': quantity,
                'symbol': self.rsymbol
            }

        self.trade_system.make_order([order])

        del self.keypoint_queue[0]








