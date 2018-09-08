from Predictor import Predictor
from TradingSystem import TradingSystem
from datetime import datetime, timedelta
import time
import numpy as np


class Bot:
    def __init__(self, auth_info, test=False, exchange_name = None):
        self.config = {
            'api_public': 'M9C8G0sR_xyAH-P-McPtGtFU',
            'api_secret': 'virblf2ij2unSG8VNuwsq5VTw0axnIVYwodKlgeAO0wGqVBS'
        }
        self.keypoint_queue = []
        self.data = []
        self.predictor = Predictor([])
        self.trade_system = TradingSystem(auth_info=auth_info, test=test)
        self.keypoint_id = 0
        self.symbol = 'ltc'

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

    def prediction_loop(self):
        exchange_data = self.trade_system.get_candles()
        data, times = self.prepare_data(exchange_data)
        self.predictor.set_data(data=data)
        interval = self.predictor.predict()


        if len(interval) > 0:
            print(datetime.now(), "Found interval", interval, file=open('log.txt', 'a+'))

            time_shift = datetime.strptime(times[256], " '%Y.%m.%d %H:%M:%S")
            time_delta = timedelta(minutes=5)

            self.keypoint_id += 1

            interval['miny'] = time_shift + time_delta * (interval['miny'] - 226)
            interval['center'] = time_shift + time_delta * (interval['center'] - 226)

            keyp1, keyp2 = self.make_keypoints(interval, self.keypoint_id)

            self.keypoint_queue.append(keyp1)
            self.keypoint_queue.append(keyp2)

    def trading_loop(self):
        if self.check_time(self.keypoint_queue[0]):
            point = self.keypoint_queue[0]
            balances = self.trade_system.get_balances()
            orderbook = self.trade_system.get_orderbook(symbol=self.symbol)
            if point['type'] == 0:
                avg = lambda x: sum(x) / len(x)
                avg_price = avg((x for x in orderbook if x['side'] == 'Buy'))
                order = {

                }
                self.trade_system.make_order()

            else:
                pass
            del self.keypoint_queue[0]








