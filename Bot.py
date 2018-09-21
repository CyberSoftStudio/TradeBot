from Predictor import Predictor
from Predictor_test import Predictor as Predictor_test
from TradingSystem import TradingSystem
from TestTradeSystem import TestTradingSystem
from datetime import datetime, timedelta
import time
import numpy as np
import json


class Bot:
    def __init__(self, auth_info, test=True, exchange_name = None):
        self.keypoint_queue = []
        self.open_transactions = {}
        self.data = []
        self.predictor = Predictor([])
        self.test = test
        self.predictor.config['extract_alpha'] = 0.5
        self.predictor.config['assurance'] = 0.95
        if (test == False):
            self.trade_system = TradingSystem(auth_info=auth_info, test=test)
        else:
            self.trade_system = TestTradingSystem(auth_info = auth_info, test=test)
        self.keypoint_id = 0
        self.cripto = 'xbt'
        self.fiat = 'usd'
        self.symbol = 'XBTUSD'
        self.rsymbol = 'USDXBT'

        self.stats = {
            'count':0,
            'average':0,
            'bad_deals':0,
            'amount':0,
            'bad_sum': 0
        }

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
            'amplitude': interval['amplitude'],
            'type': 0,
            'id': id
        }
        keyp2 = {
            'time': interval['center'],
            'trend': interval['trend'],
            'amplitude': interval['amplitude'],
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
        current_timepoint = datetime.utcfromtimestamp(self.trade_system.candles[self.trade_system.ptr]['timestamp']).timestamp()

        print("Time points", current_timepoint, order_timepoint, "Test time difference", order_timepoint - current_timepoint)

        diff = abs(current_timepoint - order_timepoint) if current_timepoint >= order_timepoint else order_timepoint - current_timepoint

        if diff < 10:
            return True

        return False

    def prediction_loop(self):
        exchange_data = self.trade_system.get_candles()[0]
        # exchange_data.reverse()
        # print(exchange_data)
        closes, times = self.prepare_data(exchange_data)
        # print(closes)
        print(times)
        self.predictor.set_data(data=closes)
        interval = self.predictor.predict()


        if len(interval) > 0:
            print(datetime.now(), "Found interval", interval, file=open('log.txt', 'a'))

            time_shift = times[255]
            time_delta = 300

            print("Timeshift", time_shift)

            self.keypoint_id += 1

            print("Predicted interval", interval)

            if(interval['miny'] < 225 and interval['center'] > 226):
                interval['miny'] = 225

            interval['miny'] = time_shift + time_delta * (interval['miny'] - 225)
            interval['center'] = time_shift + time_delta * (interval['center'] - 225)

            keyp1, keyp2 = self.make_keypoints(interval, self.keypoint_id)
            print('WE WILL MAKE NEW ORDER', keyp1, keyp2)
            self.keypoint_queue.append(keyp1)
            self.keypoint_queue.append(keyp2)

    @staticmethod
    def lower_than_current_time(timepoint):
        try:
            ok = timepoint < datetime.utcnow()
        except:
            ok = datetime.utcfromtimestamp(timepoint) < datetime.utcnow()

        return ok

    def lower_than_current_time_test(self, timepoint):
        current_timepoint = datetime.utcfromtimestamp(self.trade_system.candles[self.trade_system.ptr]['timestamp']).timestamp()
        try:
            ok = timepoint < current_timepoint
        except:
            ok = timepoint < current_timepoint

        return ok

    def get_stats_from_balances(self, prev_balance, curr_balance, order):
        prev_usd_amount = prev_balance[0]['amount'] * order['price'] + prev_balance[1]['amount']
        curr_usd_amount = curr_balance[0]['amount'] * order['price'] + curr_balance[1]['amount']

        self.stats['amount'] += prev_usd_amount
        self.stats['average'] += abs(curr_usd_amount - prev_usd_amount)
        self.stats['count'] += 1
        self.stats['bad_deals'] += (curr_usd_amount - prev_usd_amount) < 0
        if (curr_usd_amount - prev_usd_amount) < 0:
            self.stats['bad_sum'] += prev_usd_amount - curr_usd_amount

    def normalize_stats(self):
        self.stats['average'] /= self.stats['count']

    def get_stats(self):
        return self.stats

    def trading_loop(self):

        self.keypoint_queue = sorted(self.keypoint_queue, key=lambda x: x['time'])

        if self.test:
            check_time = self.test_check_time
            lower_time = self.lower_than_current_time_test
        else:
            check_time = self.check_time
            lower_time = self.lower_than_current_time

        try:
            print("WE ARE CHECKING ORDER", len(self.keypoint_queue) > 0, check_time(self.keypoint_queue[0]))
        except:
            pass

        if len(self.keypoint_queue) > 0 and check_time(self.keypoint_queue[0]):
            print("WE WANT TO SUGGEST ORDER")

        if not (
                len(self.keypoint_queue) > 0 and
                check_time(self.keypoint_queue[0]) and
                self.keypoint_queue[0]['trend'] > 0 and
                self.keypoint_queue[0]['amplitude'] > 0.4
        ):

            print("Nothing interesting")

            if len(self.keypoint_queue) > 0:
                print('lower time', lower_time(self.keypoint_queue[0]['time']))
                while len(self.keypoint_queue) > 0 and lower_time(self.keypoint_queue[0]['time']):
                    del self.keypoint_queue[0]

                while len(self.keypoint_queue) > 0:
                    point = self.keypoint_queue[0]
                    if point['type'] == 1 and not (point['id'] in self.open_transactions):
                        del self.keypoint_queue[0]

                    else:
                        break

            return None

        point = self.keypoint_queue[0]
        balances = self.trade_system.get_balances()
        candle = self.trade_system.get_candles(count=1)[0][0]
        if point['type'] == 0:
            quantity = [x['amount'] for x in balances if x['currency']==self.fiat][0]
            order = {
                'price':candle['close'],
                'quantity': quantity,
                'symbol': self.symbol
            }
            self.open_transactions[point['id']] = {
                'open_price': order['price'],
                'close_price': 0,
                'open_timestamp': self.trade_system.candles[self.trade_system.ptr]['timestamp'],
                'close_timestamp': 0
            }
        else:
            quantity = [x['amount'] for x in balances if x['currency'] == self.cripto][0]
            order = {
                'price': candle['close'],
                'quantity': quantity,
                'symbol': self.rsymbol
            }

            try:
                self.open_transactions[point['id']]['close_price'] = order['price']
                self.open_transactions[point['id']]['close_timestamp'] = self.trade_system.candles[self.trade_system.ptr]['timestamp']

                print(json.dumps(self.open_transactions[point['id']]), file=open('transactions.txt', 'a+'))

                del self.open_transactions[point['id']]
            except:
                return None

        prev_balance = self.trade_system.get_balances()
        self.trade_system.make_order([order])
        curr_balance = self.trade_system.get_balances()


        self.get_stats_from_balances(prev_balance, curr_balance, order)

        del self.keypoint_queue[0]








