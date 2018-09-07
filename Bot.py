from Predictor import Predictor
from TradingSystem import TradingSystem
from datetime import datetime, timedelta
import numpy as np


class Bot:
    def __init__(self, auth_info, test=False, exchange_name = None):
        self.order_queue = []
        self.data = []
        self.predictor = Predictor([])
        self.trade_system = TradingSystem(auth_info=auth_info, test=test)

    @staticmethod
    def prepare_data(exchange_data):
        close = [x['close'] for x in exchange_data]
        timestamps = [x['timestamp'] for x in exchange_data]
        return np.array(close), timestamps

    @staticmethod
    def prepare_order(interval):
        return 0

    @staticmethod
    def check_time(order):
        return False

    def prediction_loop(self):
        exchange_data = self.trade_system.get_candles()
        data, times = self.prepare_data(exchange_data)
        interval = self.predictor.set_data(data=data)
        if len(interval) > 0:
            print(datetime.now(), "Found interval", interval, file=open('log.txt', 'a+'))

        order = self.prepare_order(interval)

        self.order_queue.append(order)

    def trading_loop(self):
        if self.check_time(self.order_queue[0]):
            balances = self.trade_system.get_balances()
            self.trade_system.make_order([self.order_queue[0]])
            del self.order_queue[0]








