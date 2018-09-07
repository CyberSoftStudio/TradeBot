# import MonitorFabric
# import TraderFabric
# import Monitor
# import Trader
import bitmex
from Monitor_bitmex import Monitor_bitmex
from Trader_bitmex import Trader_bitmex


# пока что только под bitmex, потом сделаю полиморфно
class TradingSystem:
    def __init__(self, auth_info, test=False):
        self.client = bitmex.bitmex(api_key=auth_info['api_public'], api_secret=auth_info['api_secret'], test=test)
        self.monitor = Monitor_bitmex(self.client)
        self.trader = Trader_bitmex(self.client)

    def get_range(self, symbol, startTime, endTime):
        return self.monitor.get_quote(symbol=symbol, startTime=startTime, endTime=endTime)

    def make_order(self, orders):
        return self.trader.make_order(orders)

    def get_orderbook(self, symbol, count=50):
        return self.monitor.get_orderbook(symbol, count=count)

    def get_candles(self, count=256):
        return self.monitor.get_candles(count=count)